const state = { token: null, busy: false, documentPage: 1, documentPages: 1, view: "overview" };
const $ = (id) => document.getElementById(id);

function toast(message) {
  const node = $("toast");
  node.textContent = message;
  node.classList.add("show");
  window.setTimeout(() => node.classList.remove("show"), 3200);
}

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (options.method === "POST" && state.token) headers["X-TunnelBookAI-Control"] = state.token;
  const response = await fetch(path, { ...options, headers });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}

function dispositionCount(run, key) { return Number(run.dispositions[key] || 0); }
function resultClass(value) { return String(value || "").toLowerCase().replace("needs_", ""); }
function formatNumber(value) { return new Intl.NumberFormat("tr-TR").format(Number(value || 0)); }
function formatBytes(value) {
  const bytes = Number(value || 0);
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
}
function formatDuration(seconds) {
  if (!Number.isFinite(Number(seconds))) return "—";
  const hours = Number(seconds) / 3600;
  if (hours >= 24) return `${(hours / 24).toFixed(1)} gün`;
  if (hours >= 1) return `${hours.toFixed(1)} saat`;
  return `${Math.round(Number(seconds) / 60)} dk`;
}

function render(payload) {
  state.token = payload.control_token || state.token;
  const { control, run } = payload;
  $("runId").textContent = run.run_id;
  $("runState").textContent = run.state;
  $("progressPercent").textContent = `${run.progress_percent.toFixed(1)}%`;
  $("progressCount").textContent = `${run.processed_documents} / ${run.total_documents} belge`;
  $("progressBar").style.width = `${Math.min(100, run.progress_percent)}%`;
  $("progressBar").parentElement.setAttribute("aria-valuenow", String(run.progress_percent));
  $("statusMessage").textContent = control.message || "—";
  $("currentBatch").textContent = control.current_batch_id || "Henüz başlamadı";
  $("currentDocument").textContent = control.current_document_id || "Beklemede";
  $("batchMetric").textContent = `${run.completed_batches} / ${run.total_batches}`;
  $("stagedMetric").textContent = dispositionCount(run, "STAGED") + dispositionCount(run, "ALREADY_PROCESSED");
  $("reviewMetric").textContent = dispositionCount(run, "NEEDS_REVIEW") + dispositionCount(run, "RECOVERY_REQUIRED");
  $("failedMetric").textContent = dispositionCount(run, "FAILED") + run.failed_batches;

  const active = ["STARTING", "RUNNING", "STOP_REQUESTED"].includes(control.status);
  const resumable = ["PAUSED", "ERROR", "INTERRUPTED"].includes(control.status);
  $("startButton").disabled = state.busy || active || resumable || control.status === "FINISHED";
  $("stopButton").disabled = state.busy || !active || control.status === "STOP_REQUESTED";
  $("resumeButton").disabled = state.busy || !resumable;
  const badge = $("statusBadge");
  badge.textContent = control.status;
  badge.className = `badge ${active ? "running" : resumable ? (control.status === "ERROR" ? "error" : "paused") : control.status === "FINISHED" ? "finished" : "neutral"}`;

  const rows = $("documentRows");
  rows.replaceChildren();
  if (!run.recent_documents.length) {
    const row = document.createElement("tr");
    row.innerHTML = '<td colspan="4" class="empty">Henüz sonuç yok.</td>';
    rows.append(row);
  } else {
    run.recent_documents.forEach((item) => {
      const row = document.createElement("tr");
      row.className = "clickable-row";
      row.addEventListener("click", () => openDocument(item.document_id));
      [item.document_id, item.disposition || "—", item.section || "—", item.chunks ?? 0].forEach((value, index) => {
        const cell = document.createElement("td");
        cell.textContent = String(value);
        if (index === 1) cell.className = `result ${resultClass(value)}`;
        row.append(cell);
      });
      rows.append(row);
    });
  }
}

async function refresh() {
  try {
    const payload = await api("/api/status");
    render(payload);
    document.querySelector(".connection").classList.add("online");
    $("connectionText").textContent = "Yerel bağlantı aktif";
  } catch (_error) {
    document.querySelector(".connection").classList.remove("online");
    $("connectionText").textContent = "Bağlantı kesildi";
  }
}

async function action(path, successMessage) {
  state.busy = true;
  try {
    await api(path, { method: "POST", body: "{}", headers: { "Content-Type": "application/json" } });
    toast(successMessage);
  } catch (error) { toast(error.message); }
  finally { state.busy = false; await refresh(); }
}

async function refreshLogs() {
  try {
    const payload = await api("/api/logs");
    $("logOutput").textContent = payload.lines.length ? payload.lines.join("\n") : "Worker henüz çıktı üretmedi.";
    $("logOutput").scrollTop = $("logOutput").scrollHeight;
  } catch (error) { toast(error.message); }
}

function setModelHealth(kind, mode, detail) {
  const card = $(`${kind}Health`);
  const status = $(`${kind}Status`);
  card.dataset.state = mode;
  $(`${kind}Light`).className = `health-light ${mode}`;
  status.textContent = mode === "online" ? "Çalışıyor" : mode === "offline" ? "Çalışmıyor" : "Kontrol ediliyor";
  card.setAttribute("aria-label", `${kind === "llm" ? "LLM" : "Embedding"}: ${status.textContent}. ${detail}`);
  $(`${kind}Detail`).textContent = detail;
}

async function refreshModels() {
  const button = $("modelButton");
  button.disabled = true;
  setModelHealth("llm", "checking", "Yerel servis sorgulanıyor…");
  setModelHealth("embedding", "checking", "Yerel servis sorgulanıyor…");
  $("modelStatus").textContent = "Model sağlık kontrolü yapılıyor…";
  try {
    const payload = await api("/api/models");
    const llmOnline = payload.llm?.status === "AVAILABLE";
    const embeddingOnline = payload.embedding?.status === "AVAILABLE";
    const embeddingDetail = [payload.embedding?.model, payload.embedding?.vector_dimension ? `${payload.embedding.vector_dimension} boyut` : null].filter(Boolean).join(" · ") || "Yapılandırılmış embedding modeli bulunamadı";
    setModelHealth("llm", llmOnline ? "online" : "offline", payload.llm?.model || "Yapılandırılmış LLM bulunamadı");
    setModelHealth("embedding", embeddingOnline ? "online" : "offline", embeddingDetail);
    $("modelStatus").textContent = llmOnline && embeddingOnline ? "İki model de isteklere yanıt veriyor." : "Bir veya daha fazla model servisi hazır değil.";
  } catch (error) {
    setModelHealth("llm", "offline", "Sağlık kontrolüne ulaşılamadı");
    setModelHealth("embedding", "offline", "Sağlık kontrolüne ulaşılamadı");
    $("modelStatus").textContent = "Model sağlık kontrolü başarısız.";
    toast(error.message);
  } finally { button.disabled = false; }
}

function switchView(name) {
  state.view = name;
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.view === name));
  document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
  $(`${name}View`).classList.add("active");
  if (name === "documents") loadDocuments();
  if (name === "search") loadRetrievalStatus();
  if (name === "statistics") loadStatistics();
  if (name === "improvements") loadImprovements();
  if (name === "review") loadReview();
}

async function loadDocuments() {
  const q = encodeURIComponent($("documentSearch").value.trim());
  const disposition = encodeURIComponent($("documentDisposition").value);
  try {
    const payload = await api(`/api/documents?q=${q}&disposition=${disposition}&page=${state.documentPage}&page_size=50`);
    state.documentPage = payload.page;
    state.documentPages = payload.pages;
    $("documentTotal").textContent = `${formatNumber(payload.total)} belge`;
    $("pageText").textContent = `${payload.page} / ${payload.pages}`;
    $("prevPage").disabled = payload.page <= 1;
    $("nextPage").disabled = payload.page >= payload.pages;
    const tbody = $("allDocumentRows");
    tbody.replaceChildren();
    if (!payload.documents.length) {
      const row = document.createElement("tr"); row.innerHTML = '<td colspan="6" class="empty">Bu filtreye uygun belge yok.</td>'; tbody.append(row); return;
    }
    payload.documents.forEach((item) => {
      const row = document.createElement("tr"); row.className = "clickable-row"; row.addEventListener("click", () => openDocument(item.document_id));
      const nameCell = document.createElement("td");
      const name = document.createElement("strong"); name.textContent = item.source_name || item.document_id;
      const id = document.createElement("small"); id.textContent = item.document_id;
      nameCell.append(name, id); row.append(nameCell);
      [item.format, item.disposition, item.section || "—", item.chunks, item.reason].forEach((value, index) => {
        const cell = document.createElement("td"); cell.textContent = String(value ?? "—");
        if (index === 1) cell.className = `result ${resultClass(value)}`;
        if (index === 4) cell.className = "reason-cell";
        row.append(cell);
      });
      tbody.append(row);
    });
  } catch (error) { toast(error.message); }
}

function summaryItem(label, value, className = "") {
  const item = document.createElement("div");
  const key = document.createElement("span"); key.textContent = label;
  const val = document.createElement("strong"); val.textContent = String(value ?? "—"); val.className = className;
  item.append(key, val); return item;
}

async function openDocument(documentId) {
  try {
    const item = await api(`/api/documents/${encodeURIComponent(documentId)}`);
    $("detailTitle").textContent = item.source_name || item.document_id;
    const summary = $("detailSummary"); summary.replaceChildren();
    summary.append(
      summaryItem("Durum", item.disposition, `result ${resultClass(item.disposition)}`),
      summaryItem("Bölüm", item.section || "—"), summaryItem("Chunk", item.chunks),
      summaryItem("Sayfa", item.pages), summaryItem("Tablo", item.tables), summaryItem("Görsel", item.figures)
    );
    const reason = document.createElement("p"); reason.className = "reason-banner"; reason.textContent = item.reason; summary.append(reason);
    renderChunks(item.chunk_items || []);
    renderAssets(item.assets || []);
    $("detailDialog").showModal();
  } catch (error) { toast(error.message); }
}

function renderChunks(chunks) {
  $("chunkCount").textContent = `${chunks.length} chunk`;
  const list = $("chunkList"); list.replaceChildren();
  if (!chunks.length) { const p = document.createElement("p"); p.className = "empty compact-empty"; p.textContent = "Chunk bulunamadı. Yukarıdaki neden açıklamasını kontrol et."; list.append(p); return; }
  chunks.forEach((chunk) => {
    const details = document.createElement("details"); details.className = "chunk-card";
    const summary = document.createElement("summary");
    const title = document.createElement("strong"); title.textContent = `#${chunk.ordinal ?? "?"} · ${chunk.chunk_type || "CHUNK"}`;
    const meta = document.createElement("span"); meta.textContent = `${chunk.token_count ?? "—"} token · Bölüm ${chunk.section || "—"}`;
    summary.append(title, meta);
    const pre = document.createElement("pre"); pre.textContent = chunk.text || "İçerik boş.";
    details.append(summary, pre); list.append(details);
  });
}

function renderAssets(assets) {
  const list = $("assetList"); list.replaceChildren();
  if (!assets.length) { const p = document.createElement("p"); p.className = "empty compact-empty"; p.textContent = "Önizlenebilir çıktı bulunamadı."; list.append(p); return; }
  assets.forEach((asset) => {
    const button = document.createElement("button"); button.className = `asset-card ${asset.kind}`; button.type = "button";
    if (asset.kind === "image") { const image = document.createElement("img"); image.src = asset.url; image.alt = ""; image.loading = "lazy"; button.append(image); }
    const copy = document.createElement("span"); const name = document.createElement("strong"); name.textContent = asset.name; const size = document.createElement("small"); size.textContent = formatBytes(asset.size); copy.append(name, size); button.append(copy);
    button.addEventListener("click", () => openPreview(asset)); list.append(button);
  });
}

async function openPreview(asset) {
  $("previewTitle").textContent = asset.name;
  const body = $("previewBody"); body.replaceChildren();
  if (asset.kind === "image") {
    const image = document.createElement("img"); image.src = asset.url; image.alt = asset.name; body.append(image);
  } else {
    try { const response = await fetch(asset.url); if (!response.ok) throw new Error(`HTTP ${response.status}`); const pre = document.createElement("pre"); pre.textContent = await response.text(); body.append(pre); }
    catch (error) { toast(error.message); return; }
  }
  $("previewDialog").showModal();
}

function renderBars(target, values) {
  const root = $(target); root.replaceChildren();
  const rows = Object.entries(values || {});
  const maximum = Math.max(1, ...rows.map(([, value]) => Number(value)));
  if (!rows.length) { root.textContent = "Henüz veri yok."; return; }
  rows.forEach(([label, value]) => {
    const row = document.createElement("div"); row.className = "bar-row";
    const copy = document.createElement("div"); const key = document.createElement("span"); key.textContent = label; const count = document.createElement("strong"); count.textContent = formatNumber(value); copy.append(key, count);
    const track = document.createElement("i"); const fill = document.createElement("b"); fill.style.width = `${Math.max(2, Number(value) / maximum * 100)}%`; track.append(fill); row.append(copy, track); root.append(row);
  });
}

async function loadRetrievalStatus() {
  const badge = $("retrievalBadge");
  try {
    const data = await api("/api/retrieval/status");
    badge.textContent = data.ready ? "READY" : "HAZIR DEĞİL";
    badge.className = `badge ${data.ready ? "finished" : "error"}`;
    const manifest = data.manifest || {};
    $("retrievalIdentity").textContent = data.ready
      ? `${formatNumber(manifest.vector_count)} vektör · ${formatNumber(manifest.dimension)} boyut · ${manifest.model_id || "model bilinmiyor"} · ${manifest.index_id || "index bilinmiyor"}`
      : `Index kullanılamıyor: ${data.reason || "bilinmeyen neden"}`;
    $("semanticSearchButton").disabled = !data.ready;
  } catch (error) {
    badge.textContent = "HATA";
    badge.className = "badge error";
    $("retrievalIdentity").textContent = "Retrieval index durumu okunamadı.";
    $("semanticSearchButton").disabled = true;
    toast(error.message);
  }
}

function sourceLocator(item) {
  if (item.page_start != null) {
    return item.page_end != null && item.page_end !== item.page_start
      ? `Sayfa ${item.page_start}–${item.page_end}` : `Sayfa ${item.page_start}`;
  }
  if (item.slide_number != null) return `Slayt ${item.slide_number}`;
  if (item.sheet_name) return `Sayfa/sekme ${item.sheet_name}`;
  return `Canonical satır ${item.canonical_line_number || "—"}`;
}

function renderSemanticResults(data) {
  const root = $("semanticResults"); root.replaceChildren();
  const results = data.results || [];
  $("semanticSearchStatus").textContent = results.length
    ? `${formatNumber(results.length)} canonical kanıt bulundu · ${data.model_id}`
    : "Bu sorgu ve bölüm filtresi için sonuç bulunamadı.";
  if (!results.length) {
    const empty = document.createElement("p"); empty.className = "empty";
    empty.textContent = "Sonuç bulunamadı."; root.append(empty); return;
  }
  results.forEach((item, index) => {
    const card = document.createElement("article"); card.className = "semantic-card";
    const head = document.createElement("div"); head.className = "semantic-card-head";
    const identity = document.createElement("div");
    const title = document.createElement("h3"); title.textContent = `${index + 1}. ${item.document_id}`;
    const chunk = document.createElement("span"); chunk.textContent = item.chunk_id;
    identity.append(title, chunk);
    const score = document.createElement("strong"); score.textContent = `${(Number(item.score) * 100).toFixed(1)}%`;
    score.title = "Cosine benzerlik skoru";
    head.append(identity, score);
    const locator = document.createElement("div"); locator.className = "semantic-locator";
    [
      `Bölüm ${item.section_id || "—"}`,
      sourceLocator(item),
      item.chunk_type || "CHUNK",
      item.canonical_retrieval_path || "canonical konum yok"
    ].forEach((value) => { const tag = document.createElement("span"); tag.textContent = value; locator.append(tag); });
    const snippet = document.createElement("p"); snippet.textContent = item.snippet || "Metin özeti bulunamadı.";
    card.append(head, locator, snippet); root.append(card);
  });
}

async function runSemanticSearch() {
  const button = $("semanticSearchButton");
  const query = $("semanticQuery").value.trim();
  if (!query) return;
  button.disabled = true;
  button.textContent = "Aranıyor…";
  $("semanticSearchStatus").textContent = "Canonical index doğrulanıyor ve sorgu embeddingi hesaplanıyor…";
  try {
    const params = new URLSearchParams({ q: query, top_k: "10" });
    const section = $("semanticSection").value;
    if (section) params.set("section", section);
    renderSemanticResults(await api(`/api/retrieval/search?${params.toString()}`));
  } catch (error) {
    $("semanticSearchStatus").textContent = `Arama başarısız: ${error.message}`;
    toast(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Semantik ara";
  }
}

async function loadStatistics() {
  try {
    const data = await api("/api/statistics");
    const metrics = [
      ["Markdown", data.assets.markdown_documents], ["Tablo", data.assets.tables], ["Görsel", data.assets.figures],
      ["Sayfa", data.assets.pages], ["OCR okunan belge", data.assets.ocr_documents], ["Metin karakteri", data.assets.text_characters]
    ];
    const root = $("assetMetrics"); root.replaceChildren(); metrics.forEach(([label, value]) => root.append(summaryItem(label, formatNumber(value))));
    renderBars("chunkStats", data.chunk_types); renderBars("formatStats", data.formats);
    renderBars("warningStats", Object.fromEntries((data.top_warnings || []).map((row) => [row.code, row.count])));
    renderBars("informationalWarningStats", Object.fromEntries((data.informational_warnings || []).map((row) => [row.code, row.count])));
    $("warningNote").textContent = data.warning_note || "Sayılar etkilenen benzersiz belge sayısını gösterir.";
    const speed = $("speedStats"); speed.replaceChildren();
    speed.append(summaryItem("Ölçülen çalışma", formatDuration(data.observed_seconds)), summaryItem("Belge başına ortalama", data.seconds_per_document ? formatDuration(data.seconds_per_document) : "—"), summaryItem("Kalan tahmini süre", formatDuration(data.estimated_remaining_seconds)), summaryItem("Yarıda kesilen deneme", formatNumber(data.attempts.INTERRUPTED || 0)));
    const note = document.createElement("p"); note.className = "muted"; note.textContent = data.note; speed.append(note);
  } catch (error) { toast(error.message); }
}

async function loadImprovements() {
  try {
    const data = await api("/api/improvements");
    const total = Number(data.total_candidates || 0);
    const processed = Number(data.processed || 0);
    const percent = total ? processed / total * 100 : 100;
    $("improvementPercent").textContent = `${percent.toFixed(1)}%`;
    $("improvementCount").textContent = `${formatNumber(processed)} / ${formatNumber(total)} belge`;
    $("improvementBar").style.width = `${Math.min(100, percent)}%`;
    $("improvementBar").parentElement.setAttribute("aria-valuenow", String(percent));
    $("improvementMessage").textContent = data.message || "—";
    $("improvementCurrent").textContent = data.current_document_id || "Aktif belge yok";
    const active = ["STARTING", "RUNNING"].includes(data.status);
    const badge = $("improvementBadge");
    badge.textContent = data.status || "READY";
    badge.className = `badge ${active ? "running" : data.status === "ERROR" || data.status === "FINISHED_WITH_FAILURES" ? "error" : data.status === "FINISHED" ? "finished" : "neutral"}`;
    $("improvementStartButton").disabled = active || data.status === "FINISHED";
    const metrics = $("improvementMetrics"); metrics.replaceChildren();
    metrics.append(summaryItem("İyileştirildi", formatNumber(data.improved)), summaryItem("Değişmedi", formatNumber(data.unchanged)), summaryItem("Başarısız", formatNumber(data.failed)), summaryItem("Toplam aday", formatNumber(total)));
    const beforeAfter = $("improvementBeforeAfter"); beforeAfter.replaceChildren();
    const codes = new Set([...Object.keys(data.before || {}), ...Object.keys(data.after || {})]);
    if (!codes.size) beforeAfter.textContent = "Henüz kalite sinyali yok.";
    codes.forEach((code) => beforeAfter.append(summaryItem(code, `${formatNumber(data.before?.[code] || 0)} → ${formatNumber(data.after?.[code] || 0)}`)));
    renderBars("improvementDeferred", data.deferred || {});
    const review = data.section_review;
    const reviewPanel = $("sectionReviewPanel");
    reviewPanel.hidden = !review;
    if (review) {
      $("sectionReviewId").textContent = `${review.review_id} · ${review.status}`;
      const reviewSummary = $("sectionReviewSummary"); reviewSummary.replaceChildren();
      reviewSummary.append(
        summaryItem("İncelenen", formatNumber(review.reviewed_documents)),
        summaryItem("Bölümü düzeltilen", formatNumber(review.updated)),
        summaryItem("Karantina", formatNumber(review.quarantined)),
        summaryItem("Staging belge", `${formatNumber(review.before?.documents || 0)} → ${formatNumber(review.after?.documents || 0)}`),
        summaryItem("Staging chunk", `${formatNumber(review.before?.chunks || 0)} → ${formatNumber(review.after?.chunks || 0)}`),
        summaryItem("Aramaya hazır", `${formatNumber(review.before?.retrieval_ready_chunks || 0)} → ${formatNumber(review.after?.retrieval_ready_chunks || 0)}`)
      );
    }
    const recovery = data.targeted_recovery;
    const recoveryPanel = $("targetedRecoveryPanel");
    recoveryPanel.hidden = !recovery;
    if (recovery) {
      $("targetedRecoveryId").textContent = `${recovery.review_id} · ${recovery.status}`;
      const recoverySummary = $("targetedRecoverySummary"); recoverySummary.replaceChildren();
      recoverySummary.append(
        summaryItem("Kurtarılan tam metin", formatNumber(recovery.updated)),
        summaryItem("Yeni chunk", formatNumber((recovery.after?.chunks || 0) - (recovery.before?.chunks || 0))),
        summaryItem("Yeni aramaya hazır", formatNumber((recovery.after?.retrieval_ready_chunks || 0) - (recovery.before?.retrieval_ready_chunks || 0)))
      );
    }
    const section3Research = data.section_3_research;
    const section3ResearchPanel = $("section3ResearchPanel");
    section3ResearchPanel.hidden = !section3Research;
    if (section3Research) {
      $("section3ResearchId").textContent = `${section3Research.review_id} · ${section3Research.status}`;
      const section3ResearchSummary = $("section3ResearchSummary"); section3ResearchSummary.replaceChildren();
      section3ResearchSummary.append(
        summaryItem("İncelenen/eşlenen", formatNumber(section3Research.reviewed_documents)),
        summaryItem("Yeni staging belge", formatNumber((section3Research.after?.documents || 0) - (section3Research.before?.documents || 0))),
        summaryItem("Yeni chunk", formatNumber((section3Research.after?.chunks || 0) - (section3Research.before?.chunks || 0))),
        summaryItem("Yeni aramaya hazır", formatNumber((section3Research.after?.retrieval_ready_chunks || 0) - (section3Research.before?.retrieval_ready_chunks || 0))),
        summaryItem("Bölüm 3 birincil belge", `${formatNumber(section3Research.before?.primary_sections?.["3"] || 0)} → ${formatNumber(section3Research.after?.primary_sections?.["3"] || 0)}`)
      );
    }
    const recent = $("improvementRecent"); recent.replaceChildren();
    if (!(data.recent || []).length) {
      const p = document.createElement("p"); p.className = "empty"; p.textContent = "Henüz işlem yok."; recent.append(p);
    }
    (data.recent || []).forEach((item) => {
      const card = document.createElement("article"); card.className = "review-card resolved";
      const title = document.createElement("strong"); title.textContent = item.document_id;
      const meta = document.createElement("span"); meta.textContent = `${item.action} · ${item.status}`;
      card.append(title, meta); recent.append(card);
    });
  } catch (error) { toast(error.message); }
}

async function updateReviewItem(documentId, status, note) {
  try {
    await api("/api/review", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ document_id: documentId, status, note }) });
    toast(status === "RESOLVED" ? "İncelendi olarak kaydedildi." : "Kuyruğa geri alındı."); await loadReview();
  } catch (error) { toast(error.message); }
}

async function loadReview() {
  try {
    const data = await api("/api/review");
    $("reviewOpen").textContent = `${data.open} açık`;
    $("reviewTabCount").textContent = data.open;
    const root = $("reviewCards"); root.replaceChildren();
    if (!data.documents.length) { const p = document.createElement("p"); p.className = "empty"; p.textContent = "İnceleme bekleyen belge yok."; root.append(p); return; }
    data.documents.forEach((item) => {
      const card = document.createElement("article"); card.className = `review-card ${item.review_status === "RESOLVED" ? "resolved" : ""}`;
      const top = document.createElement("div"); const copy = document.createElement("div"); const title = document.createElement("h3"); title.textContent = item.source_name || item.document_id; const meta = document.createElement("span"); meta.textContent = `${item.format} · ${item.disposition} · ${item.document_id}`; copy.append(title, meta); const badge = document.createElement("strong"); badge.textContent = item.review_status === "RESOLVED" ? "İNCELENDİ" : "AÇIK"; top.append(copy, badge);
      const reason = document.createElement("p"); reason.textContent = item.reason;
      const note = document.createElement("textarea"); note.placeholder = "İnceleme notu veya denenecek kütüphane…"; note.value = item.review_note;
      const actions = document.createElement("div"); const inspect = document.createElement("button"); inspect.className = "button secondary"; inspect.textContent = "Çıktıları incele"; inspect.addEventListener("click", () => openDocument(item.document_id)); const toggle = document.createElement("button"); toggle.className = "button primary"; toggle.textContent = item.review_status === "RESOLVED" ? "Tekrar aç" : "İncelendi"; toggle.addEventListener("click", () => updateReviewItem(item.document_id, item.review_status === "RESOLVED" ? "OPEN" : "RESOLVED", note.value)); actions.append(inspect, toggle);
      card.append(top, reason, note, actions); root.append(card);
    });
  } catch (error) { toast(error.message); }
}

document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
$("documentFilters").addEventListener("submit", (event) => { event.preventDefault(); state.documentPage = 1; loadDocuments(); });
$("semanticSearchForm").addEventListener("submit", (event) => { event.preventDefault(); runSemanticSearch(); });
$("prevPage").addEventListener("click", () => { state.documentPage -= 1; loadDocuments(); });
$("nextPage").addEventListener("click", () => { state.documentPage += 1; loadDocuments(); });
$("closeDetail").addEventListener("click", () => $("detailDialog").close());
$("closePreview").addEventListener("click", () => $("previewDialog").close());
$("startButton").addEventListener("click", () => action("/api/start", "İşlem başlatıldı."));
$("resumeButton").addEventListener("click", () => action("/api/resume", "Checkpoint üzerinden devam ediliyor."));
$("stopButton").addEventListener("click", () => action("/api/stop", "Güvenli durdurma istendi."));
$("logButton").addEventListener("click", refreshLogs);
$("modelButton").addEventListener("click", refreshModels);
$("improvementStartButton").addEventListener("click", async () => {
  await action("/api/improvements/start", "Hedefli iyileştirme başlatıldı.");
  await loadImprovements();
});

refresh(); refreshLogs(); refreshModels(); loadReview();
window.setInterval(refresh, 2000);
window.setInterval(refreshLogs, 8000);
window.setInterval(() => { if (state.view === "improvements") loadImprovements(); }, 2000);

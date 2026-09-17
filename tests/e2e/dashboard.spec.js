const { test, expect } = require("@playwright/test");

const status = {
  control_token: "test-token",
  control: {
    status: "IDLE",
    current_batch_id: null,
    current_document_id: null,
    message: "İşlem başlatılmaya hazır."
  },
  run: {
    run_id: "CPR_TEST",
    state: "READY_TO_INGEST",
    total_batches: 58,
    completed_batches: 1,
    failed_batches: 0,
    total_documents: 885,
    processed_documents: 3,
    progress_percent: 0.34,
    dispositions: { ALREADY_CANONICAL: 1, PENDING: 881, STAGED: 1, UNSUPPORTED: 1 },
    recent_documents: [
      { document_id: "ING_PILOT", disposition: "STAGED", section: "2.4.1", chunks: 22, warnings: [] }
    ]
  }
};

const models = {
  decision: "AVAILABLE",
  llm: { status: "AVAILABLE", model: "qwen/qwen3.8-27b" },
  embedding: {
    status: "AVAILABLE",
    model: "text-embedding-baai-bge-m3-568m",
    vector_dimension: 1024
  }
};

const improvements = {
  status: "READY", total_candidates: 424, processed: 0, improved: 0, unchanged: 0,
  failed: 0, current_document_id: null, message: "Hedefli iyileştirme hazır.",
  before: { CHUNK_UNDER_MIN: 365, CHUNK_OVER_MAX: 48 }, after: {},
  deferred: { FIGURE_IMAGE_UNAVAILABLE: 1 }, recent: [],
  section_review: {
    review_id: "MSR_section_3_4_6_full_text_v1", status: "APPLIED",
    reviewed_documents: 83, updated: 36, quarantined: 18,
    before: { documents: 669, chunks: 31350, retrieval_ready_chunks: 30763 },
    after: { documents: 651, chunks: 30700, retrieval_ready_chunks: 30100 }
  },
  targeted_recovery: {
    review_id: "MSR_jstage_targeted_recovery_v1", status: "APPLIED", updated: 2,
    before: { chunks: 30700, retrieval_ready_chunks: 30100 },
    after: { chunks: 30752, retrieval_ready_chunks: 30152 }
  },
  section_3_research: {
    review_id: "MSR_section_3_papercrawler_deep_research_v1", status: "APPLIED",
    reviewed_documents: 6, updated: 6, quarantined: 0,
    before: { documents: 653, chunks: 30873, retrieval_ready_chunks: 30280, primary_sections: { "3": 2 } },
    after: { documents: 656, chunks: 30926, retrieval_ready_chunks: 30332, primary_sections: { "3": 4 } }
  }
};

const retrievalStatus = {
  ready: true,
  reason: "READY",
  manifest: {
    index_id: "BRI_TEST", model_id: "text-embedding-baai-bge-m3-568m",
    dimension: 1024, vector_count: 30332, shard_count: 474
  }
};

const retrievalSearch = {
  query: "püskürtme beton maliyeti", section: "6", top_k: 10,
  index_id: "BRI_TEST", model_id: "text-embedding-baai-bge-m3-568m",
  results: [{
    document_id: "ING_TUNNEL_COST", chunk_id: "ING_TUNNEL_COST_CH_1",
    chunk_type: "TEXT_CHUNK", section_id: "6", secondary_section_ids: [],
    page_start: 8, page_end: 9, canonical_line_number: 1,
    canonical_retrieval_path: "corpus/canonical/objects/ING_TUNNEL_COST/chunks/embedding_ready.jsonl",
    score: 0.733575, snippet: "Püskürtme beton ve kazı destekleme birim fiyatları."
  }]
};

test.beforeEach(async ({ page }) => {
  await page.route("**/api/status", (route) => route.fulfill({ json: status }));
  await page.route("**/api/logs", (route) => route.fulfill({ json: { lines: ["pilot checkpoint complete"] } }));
  await page.route("**/api/models", (route) => route.fulfill({ json: models }));
  await page.route("**/api/retrieval/status", (route) => route.fulfill({ json: retrievalStatus }));
  await page.route("**/api/retrieval/search?*", (route) => route.fulfill({ json: retrievalSearch }));
  await page.route("**/api/documents?*", (route) => route.fulfill({ json: {
    total: 1, page: 1, pages: 1, page_size: 50,
    documents: [{
      document_id: "ING_PILOT", source_name: "pilot.pdf", format: "PDF",
      disposition: "STAGED", section: "2.4.1", chunks: 1,
      reason: "İşlem tamamlandı.", needs_attention: false
    }]
  }}));
  await page.route("**/api/documents/ING_PILOT", (route) => route.fulfill({ json: {
    document_id: "ING_PILOT", source_name: "pilot.pdf", disposition: "STAGED",
    section: "2.4.1", chunks: 1, pages: 2, tables: 1, figures: 1,
    reason: "İşlem tamamlandı.",
    chunk_items: [{ chunk_id: "CH1", ordinal: 1, chunk_type: "TEXT_CHUNK", section: "2.4.1", token_count: 12, text: "Tunnel pilot chunk" }],
    assets: [{ name: "normalized/document.md", kind: "text", size: 20, url: "/api/preview?document_id=ING_PILOT&path=normalized%2Fdocument.md" }]
  }}));
  await page.route("**/api/preview?*", (route) => route.fulfill({ contentType: "text/markdown", body: "# Pilot markdown" }));
  await page.route("**/api/statistics", (route) => route.fulfill({ json: {
    assets: { markdown_documents: 3, tables: 4, figures: 5, pages: 6, ocr_documents: 2, text_characters: 1200 },
    chunk_types: { TEXT_CHUNK: 8 }, formats: { PDF: 9 }, top_warnings: [],
    attempts: { INTERRUPTED: 1 }, observed_seconds: 3600, seconds_per_document: 120, estimated_remaining_seconds: 7200,
    note: "Ölçülen süre."
  }}));
  await page.route("**/api/improvements", (route) => route.fulfill({ json: improvements }));
  await page.route("**/api/review", (route) => {
    if (route.request().method() === "POST") return route.fulfill({ json: { status: "RESOLVED" } });
    return route.fulfill({ json: { open: 1, total: 1, documents: [{
      document_id: "ING_PILOT", source_name: "pilot.pdf", format: "PDF",
      disposition: "NEEDS_REVIEW", reason: "Manuel inceleme gerekiyor: LOW_SECTION_CONFIDENCE",
      review_status: "OPEN", review_note: ""
    }] } });
  });
});

test("renders operational progress and safe controls", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Kaynak işleme kontrolü" })).toBeVisible();
  await expect(page.getByTestId("status-badge")).toHaveText("IDLE");
  await expect(page.getByText("1 / 58")).toBeVisible();
  await expect(page.getByRole("cell", { name: "ING_PILOT", exact: true })).toBeVisible();
  await expect(page.getByText("pilot checkpoint complete")).toBeVisible();
  await expect(page.getByTestId("start-button")).toBeEnabled();
  await expect(page.getByTestId("stop-button")).toBeDisabled();
  await expect(page.getByTestId("resume-button")).toBeDisabled();
  await expect(page.getByTestId("llm-health")).toHaveAttribute("data-state", "online");
  await expect(page.getByTestId("embedding-health")).toHaveAttribute("data-state", "online");
  await expect(page.getByTestId("llm-health")).toContainText("Çalışıyor");
  await expect(page.getByTestId("embedding-health")).toContainText("1024 boyut");
  if (process.env.TUNNELBOOKAI_SCREENSHOT) {
    await page.screenshot({ path: "/tmp/tunnelbookai-dashboard.png", fullPage: true });
  }
});

test("shows red lights when model services are unavailable", async ({ page }) => {
  await page.unroute("**/api/models");
  await page.route("**/api/models", (route) => route.fulfill({
    json: {
      decision: "MODEL_SERVICE_UNAVAILABLE",
      llm: { status: "MODEL_SERVICE_UNAVAILABLE", model: "qwen/qwen3.8-27b" },
      embedding: { status: "MODEL_SERVICE_UNAVAILABLE", model: "text-embedding-baai-bge-m3-568m" }
    }
  }));
  await page.goto("/");
  await expect(page.getByTestId("llm-health")).toHaveAttribute("data-state", "offline");
  await expect(page.getByTestId("embedding-health")).toHaveAttribute("data-state", "offline");
  await expect(page.getByText("Bir veya daha fazla model servisi hazır değil.")).toBeVisible();
});

test("start action carries the local control token", async ({ page }) => {
  let receivedToken = null;
  await page.route("**/api/start", async (route) => {
    receivedToken = route.request().headers()["x-tunnelbookai-control"];
    await route.fulfill({ json: { control: { status: "STARTING" } } });
  });
  await page.goto("/");
  await page.getByTestId("start-button").click();
  await expect.poll(() => receivedToken).toBe("test-token");
});

test("remains usable on a phone-sized viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(page.getByTestId("start-button")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Worker günlüğü" })).toBeVisible();
});

test("browses documents, chunks and readonly markdown", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Belgeler ve chunklar" }).click();
  const documentTable = page.locator("#allDocumentRows");
  await expect(documentTable.getByText("pilot.pdf", { exact: true })).toBeVisible();
  await documentTable.getByText("pilot.pdf", { exact: true }).click();
  await expect(page.getByText("#1 · TEXT_CHUNK")).toBeVisible();
  await page.getByText("#1 · TEXT_CHUNK").click();
  await expect(page.getByText("Tunnel pilot chunk")).toBeVisible();
  await page.getByText("normalized/document.md").click();
  await expect(page.getByText("# Pilot markdown")).toBeVisible();
});

test("runs semantic search and shows canonical source locators", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Semantik arama" }).click();
  await expect(page.getByTestId("retrieval-badge")).toHaveText("READY");
  await page.getByPlaceholder(/Tünel yapımında/).fill("püskürtme beton maliyeti");
  await page.getByLabel("Bölüm filtresi").selectOption("6");
  await page.getByRole("button", { name: "Semantik ara", exact: true }).click();
  await expect(page.getByRole("heading", { name: "1. ING_TUNNEL_COST" })).toBeVisible();
  await expect(page.getByText("Sayfa 8–9")).toBeVisible();
  await expect(page.getByText("Bölüm 6")).toBeVisible();
  await expect(page.getByText("73.4%")).toBeVisible();
});

test("renders extraction statistics and manual review queue", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "İstatistikler" }).click();
  await expect(page.getByText("OCR okunan belge")).toBeVisible();
  await expect(page.getByText("TEXT_CHUNK")).toBeVisible();
  await page.getByRole("button", { name: /Manuel inceleme/ }).click();
  await expect(page.getByText("LOW_SECTION_CONFIDENCE")).toBeVisible();
  await expect(page.getByRole("button", { name: "İncelendi" })).toBeVisible();
});

test("shows targeted improvement candidates and starts with the control token", async ({ page }) => {
  let receivedToken = null;
  await page.route("**/api/improvements/start", async (route) => {
    receivedToken = route.request().headers()["x-tunnelbookai-control"];
    await route.fulfill({ json: { control: { status: "STARTING" } } });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "İyileştirme", exact: true }).click();
  await expect(page.getByText("CHUNK_UNDER_MIN")).toBeVisible();
  await expect(page.getByText("365 → 0")).toBeVisible();
  await expect(page.getByText("3, 4 ve 6. bölüm kararları")).toBeVisible();
  await expect(page.getByText("83", { exact: true })).toBeVisible();
  await expect(page.getByText("669 → 651")).toBeVisible();
  await expect(page.getByText("Resmi tam metinlerle değiştirilenler")).toBeVisible();
  await expect(
    page.locator("#targetedRecoverySummary > div").filter({ hasText: "Yeni chunk" })
      .getByText("52", { exact: true })
  ).toBeVisible();
  await expect(page.getByText("Bölüm 3 kaynak güçlendirmesi")).toBeVisible();
  await expect(
    page.locator("#section3ResearchSummary > div").filter({ hasText: "Bölüm 3 birincil belge" })
      .getByText("2 → 4", { exact: true })
  ).toBeVisible();
  await page.getByRole("button", { name: "İyileştirmeyi başlat" }).click();
  await expect.poll(() => receivedToken).toBe("test-token");
});

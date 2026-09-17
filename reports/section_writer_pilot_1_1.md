# Yerel Qwen bölüm yazarı pilotu — 1.1

- Bölüm: **1.1 Tünelin Tanımı**
- Durum: **DRAFTED_UNAUDITED**
- Model: `qwen/qwen3.8-27b`
- Draft kimliği: `DRF_25a2b5c31856ff4a3e6d0a7edcf332df23794659e674bd0e978a84102ddbbcca`
- Yazılabilir soru: **42 / 50**
- Bilerek yanıtlanmayan `UNSUPPORTED` soru: **8 / 50**
- Kapsanan yazılabilir soru: **42 / 42**
- Paragraf: **35**
- Cümle: **105**
- Yaklaşık sözcük: **1.794**
- Kullanılan kayıtlı claim: **51**
- Qwen checkpoint partisi: **6 / 6**

## Bütünlük sonucu

- 105 cümlenin tamamı en az bir kayıtlı claim ve en az bir uygun soru kimliğine bağlıdır.
- Kayıt dışı claim, bilinmeyen soru ve `UNSUPPORTED` soru referansı sayısı **0**.
- Taslak ve sentence-map SHA-256 değerleri manifestle eşleşmektedir.
- Draft manifesti ile sentence-map toplam 2/2 JSON şema doğrulamasından geçti.
- İlgili writer/preparation/prewriting/retrieval/foundation testleri 27/27 geçti.

## Manuel gözlem ve sınır

Bu çıktı kanıt kontrollü ilk ham taslaktır; yayın metni değildir. Bölüm, 50 soruluk bankanın
geniş kapsamını altı ayrı Qwen partisinde ele aldığı için bazı tanımlar tekrarlanmakta ve
bakım, risk, sürdürülebilirlik gibi 1.1 başlığı için ikincil konulara genişlemektedir. Her
cümlede claim bağlantısı bulunması, claimin cümleyi gerçekten bütünüyle desteklediğini tek
başına kanıtlamaz. Sıradaki zorunlu kapılar cümle-claim kanıt auditi, soru kapsam auditi ve
editoryal daraltma/birleştirmedir.

## Artifactler

- Taslak: `book/production/drafts/DRF_25a2b5c31856ff4a3e6d0a7edcf332df23794659e674bd0e978a84102ddbbcca/section.md`
- Sentence map: `book/production/drafts/DRF_25a2b5c31856ff4a3e6d0a7edcf332df23794659e674bd0e978a84102ddbbcca/sentence_map.json`
- Manifest: `book/production/drafts/DRF_25a2b5c31856ff4a3e6d0a7edcf332df23794659e674bd0e978a84102ddbbcca/manifest.json`

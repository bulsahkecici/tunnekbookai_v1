# Sıradaki Pilot Bölüm Seçimi

## Karar

Sıradaki pilot bölüm **1.4 — En İyi Tünel Mühendislik Uygulamaları** olarak seçildi.

Seçim auditi:
`NPS_bc29d114d042439be93d2427752264127766e2fcaf1cf799dc621e7f5f7d3abf`

## Yöntem

Aktif section-preparation manifestindeki `READY_WITH_LIMITATIONS` bölümler tarandı.
Zaten frozen olan 1.1 aday kümesinden çıkarıldı. Kalan 16 bölüm sırasıyla şu ölçütlerle
sıralandı:

1. `UNSUPPORTED` sayısı düşük olan,
2. eşitlikte `SUPPORTED` sayısı yüksek olan,
3. eşitlikte yazılabilir claim toplamı (`SUPPORTED + PARTIAL`) yüksek olan,
4. eşitlikte toplam claim sayısı yüksek olan,
5. son eşitlikte bölüm kimliği küçük olan.

Bu politika, ilk taslakta evidence dışı iddia üretme riskini azaltırken doğrudan destekli
malzemeyi öne çıkarır.

## İlk beş aday

| Sıra | Bölüm | Başlık | Supported | Partial | Unsupported | Yazılabilir | Claim |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | 1.4 | En İyi Tünel Mühendislik Uygulamaları | 20 | 22 | 8 | 42 | 84 |
| 2 | 2.4 | Tünellerin Projelendirilmesi | 12 | 30 | 8 | 42 | 71 |
| 3 | 2.2 | Tünel Yapım Yöntemleri | 10 | 31 | 9 | 41 | 85 |
| 4 | 2.4.1.3 | Kullanım Aşaması Çalışmaları | 10 | 29 | 11 | 39 | 74 |
| 5 | 2.4.1.2 | İnşaat Esnasındaki Çalışmalar | 17 | 21 | 12 | 38 | 101 |

1.4 ile 2.4 aynı en düşük `UNSUPPORTED` sayısına (8) ve aynı yazılabilir toplamına
(42) sahiptir. 1.4, daha fazla doğrudan `SUPPORTED` claim (20'ye karşı 12) ve daha geniş
claim havuzu (84'e karşı 71) sunduğu için öne çıktı.

## Sınırlar ve devam adımı

- 22 `PARTIAL` claim yalnızca kanıtlanan alt kapsamıyla kullanılabilir.
- 8 `UNSUPPORTED` claim taslağa alınmamalıdır.
- Bu seçim yeni corpus verisi eklenirse yeniden hesaplanmalıdır.
- Bu çalışma bölüm metni, evidence auditi veya freeze üretmedi.

Önerilen sonraki işlem:

```bash
book write --section 1.4 --batch-size 8
```

Ardından 1.1 pilotundaki aynı sıra uygulanmalıdır: post-writing evidence audit, gerekirse
en fazla iki revizyon, question coverage, editorial audit ve freeze.

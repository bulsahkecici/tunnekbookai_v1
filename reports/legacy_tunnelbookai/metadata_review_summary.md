# Metadata İnsan İnceleme Kuyruğu

- Kuyruk satırı: **196**
- Bu çalıştırmada uygulanan onaylı karar: **0**

## Kullanım

1. `data/metadata/metadata_review_queue.csv` dosyasında öneri ve kanıt alanlarını inceleyin.
2. Gerekirse `proposed_*` alanlarını düzeltin; `reviewer`, `review_notes` ve `reviewed_at` alanlarını doldurun.
3. Kabul edilen satırda `review_status` değerini `approved` yapın.
4. `06_metadata_review.py` yeniden çalıştırıldığında yalnızca onaylı kararlar Markdown ve metadata CSV'ye uygulanır.

Otomatik öneriler insan onayı olmadan authoritative metadata olarak uygulanmaz.

## Durumlar

- pending_human_review: 196

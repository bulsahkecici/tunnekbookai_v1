# TunnelBookAI Retrieval Improvement Manual Review

Control: DENSE_V1 · Recommended: BILINGUAL_HYBRID_RRF

## Failure Transition Detail

| query | baseline cause | BM25_V1 | DENSE_NEIGHBOR_1 | HYBRID_RRF_30 | HYBRID_RRF_60 | HYBRID_RRF_100 | BILINGUAL_DENSE_RRF | BILINGUAL_HYBRID_RRF | RERANK_20 | RERANK_50 |
|---|---|---|---|---|---|---|---|---|---|---|
| Q001 What is the New Austrian Tunnelling Meth | gold_annotation_scope | no | no | no | no | no | no | no | no | no |
| Q011 What is overbreak in tunnel excavation? | gold_annotation_scope | yes | no | yes | no | no | no | no | yes | yes |
| Q018 Tünel aydınlatma tasarımı nasıl yapılır? | chunk_boundary | no | no | no | no | no | no | no | no | no |
| Q036 Tünel kazısında sökme ve nakliye işleri | chunk_boundary | yes | no | no | no | no | no | no | no | no |
| Q041 Squeezing ground behaviour in deep tunne | chunk_boundary | no | no | yes | yes | yes | no | yes | no | no |
| Q042 Şişen zeminlerde tünel davranışı | embedding_semantics | yes | no | yes | yes | yes | no | yes | yes | yes |
| Q048 Jeolojik etüt raporunda hangi bilgiler b | chunk_boundary | no | no | no | no | no | no | no | no | no |
| Q052 Tünel işletme maliyetleri nelerdir? | table_numeric | no | no | no | no | no | no | no | no | no |
| Q054 Tünel havalandırma sistemlerinin işletil | table_numeric | yes | no | no | no | no | no | no | no | no |
| Q056 Tünel trafik yönetimi ve izleme | chunk_boundary | no | yes | no | no | no | no | no | yes | no |
| Q060 Tünel elektromekanik tesisat bakımı | chunk_boundary | no | no | no | no | no | no | no | no | no |
| Q064 Acil kaçış yolları ve kaçış tünelleri | embedding_semantics | yes | no | yes | yes | yes | no | yes | yes | yes |
| Q071 Tünel güvenliği yönetmeliğinde belirtile | chunk_boundary | no | yes | no | no | no | no | no | no | no |
| Q075 KGM tünel projelerinde uyulacak esaslar | chunk_boundary | yes | no | yes | yes | yes | no | yes | no | yes |
| Q076 AASHTO design specification references | chunk_boundary | no | no | no | no | no | no | no | no | no |
| Q078 Minimum gabari ve serbest yükseklik şart | table_numeric | no | no | no | no | no | no | no | no | no |
| Q079 Acceptance criteria and quality control  | chunk_boundary | yes | no | yes | yes | yes | no | yes | yes | yes |
| Q081 Tunnel lighting energy cost per kWh | table_numeric | yes | no | no | no | no | no | no | yes | yes |
| Q087 Ventilation air flow rate requirements | table_numeric | no | no | no | no | no | no | no | no | no |
| Q089 Concrete compressive strength class requ | chunk_boundary | yes | no | yes | yes | yes | no | yes | yes | yes |
| Q091 Türkiye'deki karayolu tünellerinin isiml | table_numeric | no | no | no | no | no | no | no | no | no |
| Q098 Bolu Dağı Tüneli | table_numeric | no | no | no | no | no | no | no | no | no |
| Q109 tünel havalandırma sistemi tasarımı | cross_lingual | no | no | no | no | no | yes | yes | yes | no |
| Q110 kaya kütlesi sınıflandırma sistemleri | cross_lingual | no | no | no | no | no | no | no | no | no |
| Q111 tunnel maintenance and operation costs | cross_lingual | no | no | no | no | no | no | no | no | no |
| Q112 shotcrete application requirements | cross_lingual | no | no | no | no | no | yes | yes | yes | no |
| Q113 rock bolt pull-out test | cross_lingual | no | no | no | no | no | yes | yes | no | no |

## Wins vs Dense v1 (recommended variant)

- `Q002` NATM yönteminin temel ilkesi nedir? (definition, tr)
- `Q003` What is shotcrete used for in tunnels? (definition, en)
- `Q005` What does the Q-system classify? (definition, en)
- `Q006` RMR kaya kütle sınıflandırma sistemi nedir? (definition, tr)
- `Q007` What is GSI in rock engineering? (definition, en)
- `Q008` Tünel aynası ne demektir? (definition, tr)
- `Q010` Aç-kapa tünel yöntemi nedir? (definition, tr)
- `Q020` Tünel drenaj sistemi tasarımı (design, tr)
- `Q024` Tünelde su yalıtımı nasıl yapılır? (design, tr)
- `Q025` TBM tunnel excavation process (construction, en)
- `Q028` Delme patlatma yöntemi ile kazı (construction, tr)
- `Q038` Tünel güzergahında jeoteknik araştırmalar (geotechnical, tr)
- `Q041` Squeezing ground behaviour in deep tunnels (geotechnical, en)
- `Q042` Şişen zeminlerde tünel davranışı (geotechnical, tr)
- `Q043` Groundwater and permeability in tunnelling (geotechnical, en)
- `Q047` Face stability analysis in soft ground (geotechnical, en)
- `Q050` Tünel bakım ve onarım işleri (operations, tr)
- `Q055` SCADA and tunnel control systems (operations, en)
- `Q061` Tunnel fire safety requirements (safety, en)
- `Q062` Tünelde yangın güvenliği önlemleri (safety, tr)

## Regressions vs Dense v1 (recommended variant)

- `Q004` Püskürtme beton nedir ve ne için kullanılır? (definition, tr)
- `Q012` Konverjans ölçümü nedir? (definition, tr)
- `Q013` How are rock bolts designed and dimensioned? (design, en)
- `Q016` Tünel kaplama tasarımı esasları (design, tr)
- `Q026` TBM ile tünel kazısı nasıl yapılır? (construction, tr)
- `Q027` Drill and blast excavation method (construction, en)
- `Q034` Süren uygulaması ve ön destek (construction, tr)
- `Q049` Tunnel inspection and maintenance procedures (operations, en)
- `Q058` Tünel içi kaplama temizliği ve yıkama (operations, tr)
- `Q059` Drainage system maintenance in tunnels (operations, en)
- `Q065` Smoke control with jet fans (safety, en)
- `Q068` Karayolu tünellerinde trafik güvenliği (safety, tr)
- `Q069` Dangerous goods transport through tunnels (safety, en)
- `Q072` MADDE hükümlerine göre tünel işletmecisinin sorumlulukları (regulation, tr)
- `Q073` Karayolları Teknik Şartnamesi püskürtme beton gereksinimleri (regulation, tr)
- `Q074` Technical specification requirements for tunnel concrete (regulation, en)
- `Q084` Püskürtme beton dozaj ve kalınlık değerleri (numeric, tr)
- `Q085` Rock bolt length and spacing values (numeric, en)
- `Q090` Deformasyon ölçüm sonuçları ve limit değerler (numeric, tr)
- `Q099` What equipment is needed for tunnel operation and maintenance? (source_specific, en)
# TunnelBookAI Dense Retrieval Manual Review

Human-readable audit of the frozen dense baseline. Scores are cosine similarity.

## Top 20 Successes

### `Q004` — Püskürtme beton nedir ve ne için kullanılır?

- language: **tr** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **47**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000072-C0018` — #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanarak hava b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7523 | `DOC000072-C0018` | ✔ |  | 47 Püskürtme Beton Kaplamalar |
| 2 | 0.7129 | `DOC000196-C0022` |  |  | 1.1 Genel Özellikleri |
| 3 | 0.7126 | `DOC000214-C0001` |  |  | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme El |
| 4 | 0.7120 | `DOC000087-C0278` |  |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |
| 5 | 0.7102 | `DOC000236-C0279` |  |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |

### `Q009` — What is an immersed tube tunnel?

- language: **en** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **26**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0075` —  the principal types of tunnel construction and include (1) immersed tube tunnels, (2) cut-and-cover tunnels, (3) bored or mined tunnels, and (4) air-

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6669 | `DOC000003-C0076` | ✔ |  | 4.3.1 Immersed Tube Tunnels |
| 2 | 0.5850 | `DOC000015-C0020` | ✔ |  | Immersed Tube 1.4.1.5 |
| 3 | 0.5848 | `DOC000047-C0253` | ✔ |  | 11.1.2 Types of Immersed Tunnel |
| 4 | 0.5830 | `DOC000047-C0252` |  |  | 11.1 INTRODUCTION |
| 5 | 0.5783 | `DOC000047-C0256` |  |  | 11.2.1 General |

### `Q012` — Konverjans ölçümü nedir?

- language: **tr** · type: **definition** · difficulty: **hard** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0325` — ## 15.2.2.11 Convergence Gages Convergence Gages may be used for monitoring closure of the ground across either open excavations or m

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5675 | `DOC000047-C0325` | ✔ |  | 15.2.2.11 Convergence Gages |
| 2 | 0.5563 | `DOC000037-C0126` |  |  | 4 SONUÇLAR VE ÖNERİLER |
| 3 | 0.5397 | `DOC000236-C0316` |  |  | 401.04 Kalite Kontrol Deneyleri |
| 4 | 0.5387 | `DOC000196-C0059` |  |  | 5 ALETSEL GÖZLEM |
| 5 | 0.5305 | `DOC000236-C0365` |  |  | Tablo-407-13 Sıkışma ve Yüzey Kalınlık Özellikleri |

### `Q013` — How are rock bolts designed and dimensioned?

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0131` — ## 6.5.2.2 Rock Bolts Rock bolts (Figure 6-18) have a friction or grout anchor in the rock and are tensioned as soon as that anchor

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6733 | `DOC000047-C0131` | ✔ |  | 6.5.2.2 Rock Bolts |
| 2 | 0.6178 | `DOC000047-C0214` |  |  | 9.5.2 Rock Reinforcement |
| 3 | 0.6122 | `DOC000047-C0182` |  |  | 8.2.3 Blocky Rock |
| 4 | 0.6038 | `DOC000047-C0136` |  |  | 6.6.1 Empirical Method |
| 5 | 0.6035 | `DOC000037-C0034` |  |  | 3.2 Ground Reinforcement |

### `Q014` — Kaya bulonu boyu nasıl hesaplanır?

- language: **tr** · type: **design** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0243` — ## 350.04.07.02.01 SN-Bulonları ve PG-Bulonları 1. Aksi onaylanmadıkça bulonların minimum çapı ST 42 için 28 mm, ST 52 için 25 mm olacaktır. 2

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6591 | `DOC000290-C0004` | ✔ |  | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; |
| 2 | 0.6069 | `DOC000124-C0027` |  |  |  |
| 3 | 0.5943 | `DOC000290-C0003` | ✔ |  | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; |
| 4 | 0.5891 | `DOC000294-C0019` |  |  | ÖLÇÜM VERİLERİNİN DEĞERLENDİRİLMESİ |
| 5 | 0.5768 | `DOC000236-C0244` | ✔ |  | 350.04.07.02.01 SN-Bulonları ve PG-Bulonlari |

### `Q015` — Tunnel lining design requirements

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **33**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0083` — ock mass • May provide only temporary support until a final lining is placed • To protect against spalling and fallout of rock wedges between reinforc

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6728 | `DOC000047-C0251` | ✔ |  | 10.8 SELECTING A LINING SYSTEM |
| 2 | 0.6592 | `DOC000047-C0230` |  |  | 10.1 INTRODUCTION |
| 3 | 0.6585 | `DOC000047-C0231` | ✔ |  | 10.2.1 Lining Stiffness and Deformation |
| 4 | 0.6583 | `DOC000047-C0290` | ✔ |  | 13.3.3 Tunnel Design, Construction, and Condition |
| 5 | 0.6491 | `DOC000024-C0002` |  |  | 5. Tunnel Design Criteria |

### `Q017` — How is a tunnel ventilation system designed?

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **32**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0027` — ssenger station due to power loss, which cripples lighting, ventilation, and safety systems. Disrupted sewer, steam, and water lines allowing material

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7222 | `DOC000047-C0049` | ✔ |  | 2.4.5 Ventilation Requirements |
| 2 | 0.6930 | `DOC000037-C0026` | ✔ |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |
| 3 | 0.6889 | `DOC000003-C0075` |  |  | 4.2.1 Typical Road Tunnels |
| 4 | 0.6862 | `DOC000015-C0024` | ✔ |  | Basic Types of Ventilation Systems 1.4.9.1 |
| 5 | 0.6843 | `DOC000197-C0023` | ✔ |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |

### `Q019` — Segment lining for TBM tunnels

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **40**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0083` — els, the ground between ribs is stabilized by lagging or by segmental plates | | | Precast Concrete Segment Lining | • Usually associated with soft gr

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7185 | `DOC000047-C0133` | ✔ |  | 6.5.7 Precast Segment Lining |
| 2 | 0.7064 | `DOC000047-C0245` |  |  | 10.5.1 Description |
| 3 | 0.6576 | `DOC000047-C0249` | ✔ |  | 10.6 STEEL PLATE LINING |
| 4 | 0.6531 | `DOC000037-C0063` | ✔ |  | 4.1 The Lining |
| 5 | 0.6518 | `DOC000047-C0191` |  |  | 8.3.5 Steel Rib Support System |

### `Q021` — Support classes selection for weak rock

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0203` — ## 9.4 GROUND CLASSIFICATION AND SEM EXCAVATION AND SUPPORT CLASSES ## 9.4.1 Rock Mass Classification Systems A series of qualitative and quantitative

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6205 | `DOC000308-C0009` | ✔ |  | Elements of Commonly Used Excavation and Support Classes (ES |
| 2 | 0.6192 | `DOC000074-C0006` |  |  |  |
| 3 | 0.6009 | `DOC000047-C0135` |  |  | 6.6.1 Empirical Method |
| 4 | 0.5927 | `DOC000047-C0206` |  |  | 9.4.5 Tunnel Excavation, Support, and Pre-Support Measures |
| 5 | 0.5917 | `DOC000047-C0205` |  |  | 9.4.5 Tunnel Excavation, Support, and Pre-Support Measures |

### `Q022` — Portal tasarımı ve şev stabilitesi

- language: **tr** · type: **design** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **7**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000070-C0005` — #### 5 Kop Tüneli Portal ve Diğer İmalatlar <!-- image --> Portal, tünel ağızlarında inşa edilen sanat yapılarıdır. Tünel kazısının başlat

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6798 | `DOC000289-C0001` | ✔ |  | TÜNEL PORTAL TASARIMI 18-11 2019, Ankara M. Sercan KÜÇÜKASLA |
| 2 | 0.5974 | `DOC000290-C0003` | ✔ |  | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; |
| 3 | 0.5796 | `DOC000290-C0004` | ✔ |  | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; |
| 4 | 0.5672 | `DOC000259-C0021` |  |  | Slayt 33 |
| 5 | 0.5672 | `DOC000295-C0021` |  |  | Slayt 33 |

### `Q023` — Waterproofing membrane systems in tunnels

- language: **en** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0201` — ## 9.3.4 Waterproofing The SEM uses flexible, continuous membranes for tunnel waterproofing. Most frequently PVC membranes are us

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7218 | `DOC000047-C0271` | ✔ |  | 11.5.1 External Waterproofing of Tunnels |
| 2 | 0.7185 | `DOC000047-C0039` |  |  | Allowable Infiltration |
| 3 | 0.6894 | `DOC000047-C0201` | ✔ |  | 9.3.4 Waterproofing |
| 4 | 0.6680 | `DOC000015-C0036` |  |  | Interior Composite Tunnel Liners (NCHRP, 2010; FHWA 2005) 3. |
| 5 | 0.6422 | `DOC000015-C0035` |  |  | Catchment Troughs and Pipes 3.6.1 |

### `Q029` — Shotcrete application technique and thickness

- language: **en** · type: **construction** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0212` — ## 9.5.1.1 Effect of Shotcrete When concrete is sprayed on a rough ground surface, it fills small openings, cracks and fissures and as initia

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6844 | `DOC000047-C0250` | ✔ |  | 10.7 SHOTCRETE LINING |
| 2 | 0.6538 | `DOC000047-C0212` | ✔ |  | 9.5.1.1 Effect of Shotcrete |
| 3 | 0.6431 | `DOC000047-C0351` | ✔ |  | 16.4.5 Shotcrete Repairs |
| 4 | 0.6416 | `DOC000007-C0012` |  |  | Table of Contents |
| 5 | 0.6308 | `DOC000047-C0358` |  |  | GLOSSARY |

### `Q030` — Püskürtme betonun uygulanma tekniği

- language: **tr** · type: **construction** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **38**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0098` — da kırılmalar yaşanmıştır. Kesici kafada kullanılan suköpük püskürtme sistemi killerin sivanması nedeniyle sık sık tıkanmış ve çalışmalarda büyük zama

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7586 | `DOC000087-C0278` | ✔ |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |
| 2 | 0.7545 | `DOC000236-C0279` | ✔ |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |
| 3 | 0.7386 | `DOC000072-C0018` | ✔ |  | 47 Püskürtme Beton Kaplamalar |
| 4 | 0.7310 | `DOC000196-C0022` |  |  | 1.1 Genel Özellikleri |
| 5 | 0.7253 | `DOC000074-C0010` |  |  |  |

### `Q031` — Grouting and ground improvement ahead of the face

- language: **en** · type: **construction** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0033` — -TBM tunneling without applying improvement methods. ## 3.1 Grouting Grouting involves the process of injecting a material into the ground with the fo

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6436 | `DOC000047-C0222` | ✔ |  | 9.5.4.2 Ground Improvement |
| 2 | 0.6307 | `DOC000037-C0033` | ✔ |  | 3 GROUND IMPROVEMENT |
| 3 | 0.6077 | `DOC000047-C0144` |  |  | 6.6.4 Pre-Support and Other Ground Improvement Methods |
| 4 | 0.5874 | `DOC000047-C0010` |  |  | TABLE OF CONTENTS |
| 5 | 0.5821 | `DOC000047-C0208` |  |  | 9.4.5 Tunnel Excavation, Support, and Pre-Support Measures |

### `Q032` — Enjeksiyon ile zemin iyileştirme

- language: **tr** · type: **construction** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **25**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000072-C0012` — si gerekmektedir. Stabiliteyi sağlamak ve suyu önlemek için enjeksiyon, zemini dondurma, denetimli drenajla zemin suyu seviyesinin düşürülmesi ve bası

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7125 | `DOC000288-C0003` | ✔ |  | Zemin İyileştirme Yöntemleri |
| 2 | 0.6579 | `DOC000288-C0004` | ✔ |  | Permeasyon Enjeksiyonu |
| 3 | 0.6565 | `DOC000288-C0005` | ✔ |  | Çatlatma Enjeksiyonu |
| 4 | 0.6229 | `DOC000288-C0006` | ✔ |  | Kompaksiyon Enjeksiyonu |
| 5 | 0.6116 | `DOC000124-C0028` |  |  |  |

### `Q033` — Forepoling and umbrella arch support

- language: **en** · type: **construction** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **6**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0219` — ground Facilities (COSUF). This committee will be under the umbrella of the ITA, in close cooperation with the PIARC. ## 7.4 Effects of Fire on the Tu

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5695 | `DOC000047-C0144` | ✔ |  | 6.6.4 Pre-Support and Other Ground Improvement Methods |
| 2 | 0.5672 | `DOC000047-C0221` |  |  | 9.5.4.1 Pre-support Measures |
| 3 | 0.5523 | `DOC000120-C0003` |  |  | EXAMPLE FOR EVALUATION OF SUPPORT NUMBER |
| 4 | 0.5463 | `DOC000047-C0222` |  |  | 9.5.4.2 Ground Improvement |
| 5 | 0.5450 | `DOC000047-C0129` | ✔ |  | 6.5.1 Excavation Support Options |

### `Q034` — Süren uygulaması ve ön destek

- language: **tr** · type: **construction** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000070-C0004` — 9/443 çelik hasır, Q32 PG Bulon (6m), 1,5 Enjeksiyonlu Boru Süren, 30 cm Püskürtme Beton (C20/25) Kop tünelinde yukarıda verilen sınıflandırma birimle

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6787 | `DOC000217-C0001` | ✔ |  | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme El |
| 2 | 0.5991 | `DOC000047-C0144` |  |  | 6.6.4 Pre-Support and Other Ground Improvement Methods |
| 3 | 0.5869 | `DOC000047-C0220` |  |  | 9.5.4.1 Pre-support Measures |
| 4 | 0.5839 | `DOC000244-C0008` |  |  | Karayolları Genel Müdürlüğü . Bölge Müdürlüğü T.C. ULAŞTIRMA |
| 5 | 0.5831 | `DOC000308-C0011` |  |  | Elements of Commonly Used Soft Ground Excavation and Support |

### `Q035` — Cut and cover tunnel construction stages

- language: **en** · type: **construction** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0078` — ## 4.3.2 Cut-and-Cover Tunnels Shallow-depth tunnels in land are frequently designed as structures to be constructed using the cu

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6905 | `DOC000003-C0078` | ✔ |  | 4.3.2 Cut-and-Cover Tunnels |
| 2 | 0.6644 | `DOC000047-C0092` |  |  | 5.1 INTRODUCTION |
| 3 | 0.6536 | `DOC000015-C0018` | ✔ |  | Construction Methods 1.4.1 |
| 4 | 0.6392 | `DOC000047-C0094` |  |  | 5.3.1 General |
| 5 | 0.6360 | `DOC000021-C0004` | ✔ |  | Cut-and-cover |

### `Q037` — Geotechnical investigation for tunnel route selection

- language: **en** · type: **geotechnical** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0035` — ## 1.2.4 Geotechnical Investigations As discussed in Chapter 3, geotechnical investigations are critical for proper planning of a

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7046 | `DOC000047-C0035` | ✔ |  | 1.2.4 Geotechnical Investigations |
| 2 | 0.6706 | `DOC000047-C0051` | ✔ |  | 3.1.1 Phasing of Geotechnical Investigations |
| 3 | 0.6528 | `DOC000047-C0058` |  |  | 3.5.1 General |
| 4 | 0.6522 | `DOC000122-C0005` |  |  | 1.1 Basic Procedure |
| 5 | 0.6441 | `DOC000127-C0002` |  |  | Tünel Güzergah ı Seçim Çal ı ş malar ı ; |

### `Q039` — Rock mass classification systems comparison

- language: **en** · type: **geotechnical** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **11**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0085` —  of MRMR in mining and SMR in slope stability analysis from RMR system and development of QTaM and RME in TBM performance analysis from Q and RMR syst

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6496 | `DOC000037-C0085` | ✔ |  | 2 APPLICATION OF ROCK MASS CLASSIFICATION SYSTEMS IN TBM PER |
| 2 | 0.6370 | `DOC000307-C0007` | ✔ |  | DEVELOPMENT OF ROCK MECHANICS AND ROCK MASS CLASSIFICATION S |
| 3 | 0.6340 | `DOC000124-C0017` |  |  |  |
| 4 | 0.6262 | `DOC000037-C0088` | ✔ |  | 4.2 Use of Rock Mass Fabric Index |
| 5 | 0.6201 | `DOC000047-C0120` | ✔ |  | 6.3.5 Rock Mass Rating (RMR) System |

## Borderline Queries

Gold found, but only low in the ranking (MRR@10 <= 0.25).

### `Q002` — NATM yönteminin temel ilkesi nedir?

- language: **tr** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **1** · MRR@10 **0.167** · doc_recall@10 **1**
- expected evidence: `DOC000103-C0001` — ### NATM TÜNEL YAPIMI 1. **T ÜNEL KAZISI VE DESTEKLEME** - 1.1. **KAZI YÖNTEMİ VE AŞAMALARI** Tünellerde kazı destekleme işl

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6512 | `DOC000308-C0007` |  |  | 4. Sequential Excavation Method NATM |
| 2 | 0.6370 | `DOC000124-C0020` |  |  |  |
| 3 | 0.6230 | `DOC000302-C0142` |  |  | Slayt 151 |
| 4 | 0.6136 | `DOC000047-C0198` |  |  | 9.2 BACKGROUND AND CONCEPTS |
| 5 | 0.6123 | `DOC000076-C0005` |  |  |  |

### `Q006` — RMR kaya kütle sınıflandırma sistemi nedir?

- language: **tr** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **7**
- recall@10 **1** · MRR@10 **0.200** · doc_recall@10 **1**
- expected evidence: `DOC000072-C0030` — #### 61 RMR Zemin Sınıflandırma Ölçütüne Göre Bu RMR ölçütü zeminin kalitesini belirlemeye yarayan, bu sayede tüneller, büyük ya

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7616 | `DOC000124-C0017` |  |  |  |
| 2 | 0.6561 | `DOC000071-C0009` |  |  |  |
| 3 | 0.6553 | `DOC000074-C0005` |  |  |  |
| 4 | 0.6487 | `DOC000302-C0132` |  |  | Slayt 141 |
| 5 | 0.6482 | `DOC000309-C0004` | ✔ |  | Kaya Sınıflama Sistemleri |

### `Q008` — Tünel aynası ne demektir?

- language: **tr** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **33**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0112` — lmıştır. Şöyle ki; ezilme zonuna girilirken veya çıkılırken aynadaki iri boyutlu kaya blokları kendi kendini tutamamaktadır. Kesici kafa üzerinde bulu

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5957 | `DOC000105-C0009` |  |  | 8 SONUÇLAR |
| 2 | 0.5888 | `DOC000262-C0006` |  |  | JEOFİZİK GÖZLEMLER: |
| 3 | 0.5846 | `DOC000066-C0001` |  |  | Tünel Kontrol Mühendisi Geliştirme Kursu YENİ AVUSTURYA TÜNE |
| 4 | 0.5796 | `DOC000105-C0004` | ✔ |  | 4 FRANSIZ YÖNTEMİ |
| 5 | 0.5744 | `DOC000069-C0001` |  |  |  |

### `Q010` — Aç-kapa tünel yöntemi nedir?

- language: **tr** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000049-C0012` — li | Kocakaya Tüneli | Şehzadeler Tüneli | İskilip Tüneli | Aç-Kapa Tüneli | Ahmet Muhip Dranas Tüneli | Havza Tüneli | | BÖLGE NO | BÖLGE NO | 2 | 2 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6367 | `DOC000290-C0007` |  |  | Kaya şevlerinin duraylılığı hesaplamaları genel olarak; |
| 2 | 0.6050 | `DOC000076-C0004` |  |  |  |
| 3 | 0.6001 | `DOC000098-C0011` |  |  |  |
| 4 | 0.5999 | `DOC000072-C0012` | ✔ |  | 22 Yumuşak Zeminlerde Tünel İnşası |
| 5 | 0.5880 | `DOC000069-C0002` |  |  |  |

### `Q016` — Tünel kaplama tasarımı esasları

- language: **tr** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **40**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0129` — ise 3454 m'dir. Tünel kazı çapı 3450 mm'dir. Tünelin ikinci kaplamasının tamamlanmasinın ardından elde edilecek nihai çap 2600 mm'dir. Tünel güzergâhı

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6884 | `DOC000096-C0003` |  |  | 2 Uygulama Esasları |
| 2 | 0.6553 | `DOC000072-C0003` |  |  | ÖZET |
| 3 | 0.6520 | `DOC000072-C0002` |  |  | İÇİNDEKİLER |
| 4 | 0.6460 | `DOC000165-C0002` | ✔ |  | TASARIM YAKLAŞIMI |
| 5 | 0.6444 | `DOC000096-C0002` |  |  | 2 Uygulama Esasları |

### `Q020` — Tünel drenaj sistemi tasarımı

- language: **tr** · type: **design** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **26**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000045-C0004` — ra tünel genişliğine bağlıdır. | | | Yanıcı ve Toksik Madde Drenajı | 6 |  |  |  |  |  | Tehlikeli madde taşınmasına izin verilen tünellerde zoru

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6327 | `DOC000087-C0237` |  |  | 350.03.02.09.02 Malzeme ve Yapım |
| 2 | 0.6276 | `DOC000236-C0238` |  |  | 350.03.02.09.02 Malzeme ve Yapim |
| 3 | 0.6240 | `DOC000166-C0008` |  |  | 5. Sonuç ve Öneriler |
| 4 | 0.6084 | `DOC000166-C0006` | ✔ |  | 2.3. Tünellerde drenaj sistemleri ve sorunlar |
| 5 | 0.5958 | `DOC000162-C0002` |  |  | 3.2.2.Yeraltı yapilarinda |

### `Q024` — Tünelde su yalıtımı nasıl yapılır?

- language: **tr** · type: **design** · difficulty: **hard** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **132**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000049-C0020` — li (2) ve Satıh Durumu (3) | Atnalı BSK | | Kaplama Cinsi / Su Yalıtımı (Var / Yok) | Beton / Yok | | Acil Çıkışlar (4) (Var/Yok) | Yok | | Acil Servi

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7342 | `DOC000076-C0003` |  |  |  |
| 2 | 0.7005 | `DOC000236-C0254` |  |  | 350.06.01.03.01 Yüzey Hazirlanması |
| 3 | 0.6897 | `DOC000087-C0253` |  |  | 350.06.01.02.03 Aksesuar |
| 4 | 0.6797 | `DOC000218-C0001` | ✔ |  | Tünel Kontrol Mühendisi Geliştirme Kursu YALITIM VE DRENAJ N |
| 5 | 0.6797 | `DOC000067-C0001` | ✔ |  | Tünel Kontrol Mühendisi Geliştirme Kursu YALITIM VE DRENAJ N |

### `Q025` — TBM tunnel excavation process

- language: **en** · type: **construction** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **23**
- recall@10 **1** · MRR@10 **0.125** · doc_recall@10 **1**
- expected evidence: `DOC000011-C0008` — ## The TBM Competitiveness formula 32 The TBM Competitiveness formula captures the ratio between the length and diameter of the

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7022 | `DOC000011-C0011` |  |  | 2.2.2. Mechanized Tunnelling |
| 2 | 0.6724 | `DOC000011-C0010` |  |  | 2.2.2. Mechanized Tunnelling |
| 3 | 0.6675 | `DOC000011-C0007` |  |  | Tunnel Construction methods |
| 4 | 0.6599 | `DOC000011-C0016` |  |  | Tunnelling Method |
| 5 | 0.6534 | `DOC000015-C0019` |  |  | Bored Tunnels 1.4.1.3 |

### `Q028` — Delme patlatma yöntemi ile kazı

- language: **tr** · type: **construction** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **14**
- recall@10 **1** · MRR@10 **0.143** · doc_recall@10 **1**
- expected evidence: `DOC000070-C0004` — skavatör ile Kazı, Delici Ekskavatör ile Kazı, Düzgün-Kesme Patlatma Tekniği ile Yapılan Kazı ve TBM (Tunel Boring Machine ) dir. Uygulamada kazı dest

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6371 | `DOC000287-C0071` |  |  | Slayt 74 |
| 2 | 0.6314 | `DOC000072-C0011` |  |  | 19 Kayaç Zeminlerde Tünel İnşası |
| 3 | 0.6230 | `DOC000236-C0038` |  |  | 204.05.03 Delme |
| 4 | 0.6217 | `DOC000198-C0059` |  |  | 1 GİRİŞ |
| 5 | 0.6124 | `DOC000207-C0031` |  |  | 2 GENEL ÇALIŞMA SİSTEMİ |

### `Q038` — Tünel güzergahında jeoteknik araştırmalar

- language: **tr** · type: **geotechnical** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **1** · MRR@10 **0.200** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0122` — ## 3.2 EPB-TBM'in Kazı Materyali ile ilgili Jeoteknik Ölçme ve Değerlendirmeler Bu bölümde, kazı performansını belirleyen ve denetleyen önemli bir bağ

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7314 | `DOC000302-C0050` |  |  | Slayt 54 |
| 2 | 0.6807 | `DOC000127-C0002` |  |  | Tünel Güzergah ı Seçim Çal ı ş malar ı ; |
| 3 | 0.6579 | `DOC000076-C0006` |  |  |  |
| 4 | 0.6533 | `DOC000302-C0036` |  |  | Slayt 40 |
| 5 | 0.6493 | `DOC000302-C0001` | ✔ |  | TÜNELLERDE GÜZERGAH SEÇİMİ VE jeoteknik araştırmalar son |

### `Q043` — Groundwater and permeability in tunnelling

- language: **en** · type: **geotechnical** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **43**
- recall@10 **1** · MRR@10 **0.250** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0075` — ypically depends on the depth, cross section, and soil/rock/groundwater conditions along the alignment. Other constraints include geographical and env

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6781 | `DOC000047-C0039` |  |  | Allowable Infiltration |
| 2 | 0.6761 | `DOC000047-C0109` |  |  | 5.7.1 Construction Dewatering |
| 3 | 0.6601 | `DOC000047-C0149` |  |  | 6.8.3.1 Factors on the Lining Loads due to Water Flow |
| 4 | 0.6592 | `DOC000047-C0077` | ✔ |  | 3.5.6 Groundwater Investigation |
| 5 | 0.6554 | `DOC000047-C0347` |  |  | 16.3.1 General |

### `Q047` — Face stability analysis in soft ground

- language: **en** · type: **geotechnical** · difficulty: **medium** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **1**
- recall@10 **1** · MRR@10 **0.111** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0144` — orted so that ground control is never compromised. ## 6.6.6 Face Stability In general, face stability is not as great a concern in rock tunnels as in 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6497 | `DOC000047-C0163` |  |  | 7.3.3 Choosing between Earth Pressure Balance Machines and S |
| 2 | 0.6190 | `DOC000047-C0170` |  |  | 7.5.3 Settlement Calculations |
| 3 | 0.6180 | `DOC000047-C0010` |  |  | TABLE OF CONTENTS |
| 4 | 0.6101 | `DOC000047-C0206` |  |  | 9.4.5 Tunnel Excavation, Support, and Pre-Support Measures |
| 5 | 0.6060 | `DOC000047-C0022` |  |  | LIST OF FIGURES |

### `Q063` — Emergency escape routes and cross passages

- language: **en** · type: **safety** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **1** · MRR@10 **0.200** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0375` — , and More Effective Visual, Audible, and Tactile Signs for Escape Routes The scan team noted that the signs Europeans use to indicate emergency escap

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6911 | `DOC000047-C0041` |  |  | 1.3.6.1 Emergency Egress |
| 2 | 0.6368 | `DOC000005-C0003` |  |  | 1.2.2 Constructional measures for road safety in tunnels |
| 3 | 0.6193 | `DOC000172-C0027` |  |  | Slayt 27 |
| 4 | 0.5933 | `DOC000168-C0003` |  |  | Distance between lay-bys |
| 5 | 0.5929 | `DOC000047-C0375` | ✔ |  | 1. Develop Universal, Consistent, and More Effective Visual, |

### `Q069` — Dangerous goods transport through tunnels

- language: **en** · type: **safety** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **25**
- recall@10 **1** · MRR@10 **0.143** · doc_recall@10 **1**
- expected evidence: `DOC000002-C0010` — vehicle -  Prohibition of passage of the vehicles carrying hazardous materials TMO will give warnings to and remove vehicles which violate these rule

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6750 | `DOC000168-C0005` |  |  | ADR Agreement 2007/2009 |
| 2 | 0.6737 | `DOC000173-C0019` |  |  | Slayt 19 |
| 3 | 0.6703 | `DOC000173-C0007` |  |  | Slayt 7 |
| 4 | 0.6699 | `DOC000021-C0017` |  |  | Mining |
| 5 | 0.6685 | `DOC000173-C0002` |  |  | Slayt 2 |

### `Q073` — Karayolları Teknik Şartnamesi püskürtme beton gereksinimleri

- language: **tr** · type: **regulation** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **0.167** · doc_recall@10 **1**
- expected evidence: `DOC000072-C0018` — #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanarak hava b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6937 | `DOC000236-C0277` |  |  | 351.07.04 Çevresel Şartlarla İlgili Gereksinimler |
| 2 | 0.6804 | `DOC000087-C0282` |  |  | 351.08.15 Operatörlerin Yeterliliği |
| 3 | 0.6784 | `DOC000236-C0283` |  |  | 351.08.15 Operatörlerin Yeterliliği |
| 4 | 0.6702 | `DOC000236-C0285` |  |  | 351.10.01 Basınç Dayanım Sınıfları |
| 5 | 0.6688 | `DOC000293-C0012` |  |  | Püskürtme Beton |

### `Q074` — Technical specification requirements for tunnel concrete

- language: **en** · type: **regulation** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **3**
- recall@10 **1** · MRR@10 **0.143** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0202` — hese construction aspects have to be addressed in detail in specifications and working procedures and they have to be rigidly enforced. ## 9.3.5.3 Sho

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6362 | `DOC000047-C0099` |  |  | 5.4.3.1 Cast-in-Place Concrete |
| 2 | 0.6289 | `DOC000047-C0038` |  |  | 1.3.3 Tunnel Cross-Section |
| 3 | 0.6198 | `DOC000047-C0271` |  |  | 11.5.1 External Waterproofing of Tunnels |
| 4 | 0.6168 | `DOC000047-C0230` |  |  | 10.1 INTRODUCTION |
| 5 | 0.6157 | `DOC000001-C0010` |  |  | 3.2. Lighting systems design results |

### `Q083` — Tünel uzunluklarına göre sınıflandırma tablosu

- language: **tr** · type: **numeric** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **25**
- recall@10 **1** · MRR@10 **0.125** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0052` — | 5 rpm | | Disk Sayıs1 | 52 | | Disk Boyutu (inç) | 17 | | Uzunluk (m) | 152 | <!-- image --> ## 4 TBM GENEL PERFORMANSI 7 Temmuz 2013 tarihine Suruç

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6653 | `DOC000075-C0126` |  |  |  |
| 2 | 0.6352 | `DOC000124-C0008` |  |  |  |
| 3 | 0.6182 | `DOC000072-C0002` |  |  | İÇİNDEKİLER |
| 4 | 0.6049 | `DOC000075-C0004` |  |  |  |
| 5 | 0.6038 | `DOC000072-C0008` |  |  | 7 Enkesitlerine Göre Sınıflandırma |

### `Q086` — Kaya sınıflarına göre destek elemanları çizelgesi

- language: **tr** · type: **numeric** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **0.200** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0226` — ## Tablo- 350-2 Kaya Sınıfları ve Özellikleri | KAYA SINIFI | TANIMI | ÖZELLİKLERİ | |---------------|----------------------------------

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6677 | `DOC000074-C0006` |  |  |  |
| 2 | 0.6670 | `DOC000087-C0227` |  |  | Tablo- 350-2 Kaya Sınıfları ve Özellikleri |
| 3 | 0.6640 | `DOC000087-C0225` |  |  | 350.02.02 Uygulama ve Yöntemler |
| 4 | 0.6595 | `DOC000236-C0227` |  |  | 350.02.03.02 Sınıflandırma Sistemi |
| 5 | 0.6541 | `DOC000236-C0226` | ✔ |  | 350.02 Kaya Sınıflandırma |

### `Q114` — geotechnical investigation report contents

- language: **en** · type: **geotechnical** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **1** · MRR@10 **0.111** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0454` — mler, rakım değerleri vb., - b. Jeoloji: Proje güzergâhının jeolojik özellikleri, güzergâhın jeolojik niteliğine ilişkin genel veriler, - c. Drenaj: P

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6398 | `DOC000047-C0085` |  |  | 4.2 GEOTECHNICAL DATA REPORT |
| 2 | 0.6249 | `DOC000122-C0010` |  |  | 1.7 Geotechnical report |
| 3 | 0.5972 | `DOC000047-C0086` |  |  | 4.3 GEOTECHNICAL DESIGN MEMORANDUM |
| 4 | 0.5959 | `DOC000047-C0008` |  |  | TABLE OF CONTENTS |
| 5 | 0.5836 | `DOC000047-C0051` |  |  | 3.1.1 Phasing of Geotechnical Investigations |

## Hard Failures (no gold in top-10)

All 27 failing queries, with the classified cause in `dense_v1_failures.csv`.

### `Q001` — What is the New Austrian Tunnelling Method?

- language: **en** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000308-C0007` — ## 4. Sequential Excavation Method NATM The Sequential Excavation Method (SEM), also commonly referred to as the New Austrian Tunneling Method (NATM),

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6218 | `DOC000124-C0005` |  |  |  |
| 2 | 0.6151 | `DOC000066-C0004` |  |  | Trans-Sibirya Demiryolu Tünel çalışmalarına ait fotoğraflar, |
| 3 | 0.6086 | `DOC000105-C0003` |  |  | 3 YENİ AVUSTURYA TÜNEL AÇMA YÖNTEMİNİN (NATM) GELİŞTİRİLMESİ |
| 4 | 0.6076 | `DOC000168-C0014` |  |  | Definition of the system |
| 5 | 0.6046 | `DOC000110-C0001` |  |  | TUNNELLING PRACTICE in mid NINETEEN HUNDREDS |

### `Q011` — What is overbreak in tunnel excavation?

- language: **en** · type: **definition** · difficulty: **hard** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000122-C0007` — nalyses for the determination of discontinuity con- trolled overbreak and sliding of wedges Methods: Key Block Theory [18], analyses using stereograph

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5960 | `DOC000021-C0001` |  |  | WIKIPEDIA |
| 2 | 0.5733 | `DOC000011-C0009` |  |  | 2.2.1. Conventional Tunnelling (Drill &amp; Blast and Sequen |
| 3 | 0.5724 | `DOC000025-C0003` |  |  | 1. Cut and Cover Tunnelling : |
| 4 | 0.5701 | `DOC000047-C0058` |  |  | 3.5.1 General |
| 5 | 0.5602 | `DOC000037-C0039` |  |  | 4 ENCOUNTERING PROBLEMS |

### `Q018` — Tünel aydınlatma tasarımı nasıl yapılır?

- language: **tr** · type: **design** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **7**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0454` — tüler vb.), yapısal peyzaj elemanları, donatılar, dış mekan aydınlatma, sulama, drenaj vb. altyapı sistemlerinin üstyapıya yansıyan yapı elemanları ve

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7011 | `DOC000075-C0059` |  |  |  |
| 2 | 0.6530 | `DOC000075-C0014` |  |  |  |
| 3 | 0.6514 | `DOC000044-C0002` |  |  | 1.1. Lighting literature review |
| 4 | 0.6495 | `DOC000045-C0005` |  |  | TÜNEL GÜVENLİĞİ PROJE KRİTERLERİ (1) |
| 5 | 0.6315 | `DOC000130-C0004` |  |  | Karayolu Tünellerinde Standart Güvenlik Sistemleri ve Ekipma |

### `Q036` — Tünel kazısında sökme ve nakliye işleri

- language: **tr** · type: **construction** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **18**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0103` — ## Kazılabilirlik İndeksi Kullanılarak Tünel Açma Makinası (TBM) Performans Parametrelerinin Belirlenmesi Analysis of the T

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6347 | `DOC000087-C0236` |  |  | 350.03.02.05 Aşırı Sökülme |
| 2 | 0.6277 | `DOC000236-C0237` |  |  | 350.03.02.05 Aşırı Sökülme |
| 3 | 0.6091 | `DOC000069-C0002` |  |  |  |
| 4 | 0.6046 | `DOC000261-C0004` |  |  | TÜNEL PORTAL ÇIKIŞI İYİLEŞTİRME ÇALIŞMASI |
| 5 | 0.5970 | `DOC000068-C0020` |  |  | LOKOMOTİF |

### `Q041` — Squeezing ground behaviour in deep tunnels

- language: **en** · type: **geotechnical** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0046` — ## 2 ESTIMATION OF SQUEEZING LEVELS Aydan et al., (1993) proposed a method for predicting the level of squeezing during tunneling through s

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6752 | `DOC000037-C0031` |  |  | J. Rostami |
| 2 | 0.6520 | `DOC000037-C0044` |  |  | 7 CONCLUSIONS |
| 3 | 0.6491 | `DOC000116-C0001` |  |  | INTRODUCTION |
| 4 | 0.6441 | `DOC000047-C0012` |  |  | TABLE OF CONTENTS |
| 5 | 0.6406 | `DOC000047-C0186` |  |  | 8.2.7 Mixed Face Tunneling |

### `Q042` — Şişen zeminlerde tünel davranışı

- language: **tr** · type: **geotechnical** · difficulty: **medium** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **11**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000074-C0006` — onu,prefabrik kaplama | | 8 | Sıkıştıran (Çok derinde) | Az şişen killer (kaolen minerali) | (2.10-4.50) (B+H) | Dairesel kalıcı destek ve püskürtme b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6695 | `DOC000047-C0155` |  |  | SOFT GROUND TUNNELING |
| 2 | 0.6576 | `DOC000302-C0031` |  |  | Slayt 35 |
| 3 | 0.6566 | `DOC000072-C0005` |  |  | ÇİZELGELER DİZİNİ |
| 4 | 0.6507 | `DOC000072-C0015` |  |  | 31 Tünel İnşaatlarında Karşılaşılabilen Bazı Sorunlar |
| 5 | 0.6486 | `DOC000072-C0004` |  |  | ŞEKİLLER DİZİNİ |

### `Q048` — Jeolojik etüt raporunda hangi bilgiler bulunur?

- language: **tr** · type: **geotechnical** · difficulty: **hard** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0454` — mler, rakım değerleri vb., - b. Jeoloji: Proje güzergâhının jeolojik özellikleri, güzergâhın jeolojik niteliğine ilişkin genel veriler, - c. Drenaj: P

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5821 | `DOC000302-C0006` |  |  | Slayt 6 |
| 2 | 0.5605 | `DOC000302-C0040` |  |  | Slayt 44 |
| 3 | 0.5491 | `DOC000037-C0060` |  |  | 2.2 The Geology and the Geotechnics |
| 4 | 0.5486 | `DOC000047-C0054` |  |  | 3.3.1 Site Reconnaissance and Preliminary Surveys |
| 5 | 0.5458 | `DOC000037-C0108` |  |  | 6 KAYNAKLAR |

### `Q052` — Tünel işletme maliyetleri nelerdir?

- language: **tr** · type: **operations** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000045-C0002` — ## İŞLETME Tünel güvenliğinde bu maddelere ek olarak; tüneli işleten idare yetkili makamlarla (polis, itfaiye, ambulans) ge

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7045 | `DOC000075-C0121` |  |  |  |
| 2 | 0.6544 | `DOC000100-C0004` |  |  | Vaka Çalışması |
| 3 | 0.6466 | `DOC000075-C0024` |  |  |  |
| 4 | 0.6440 | `DOC000012-C0001` |  |  |  |
| 5 | 0.6405 | `DOC000002-C0007` |  |  | (3) Tunnel Management Office Operator |

### `Q054` — Tünel havalandırma sistemlerinin işletilmesi

- language: **tr** · type: **operations** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000130-C0004` —  | 11 ## TÜNEL S İ STEMLER İ -  ENERJ İ -  AYDINLATMA -  HAVALANDIRMA -  YANGIN ALGILAMA VE SÖNDÜRME -  HABERLE Ş ME -  TRAF İ K KONTROL <!-- im

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6712 | `DOC000096-C0004` |  |  | 3 Korunma Hücreleri |
| 2 | 0.6351 | `DOC000075-C0117` |  |  |  |
| 3 | 0.6164 | `DOC000075-C0014` |  |  |  |
| 4 | 0.6153 | `DOC000075-C0101` |  |  |  |
| 5 | 0.6143 | `DOC000036-C0030` |  |  | ÜÇÜNCÜ BÖLÜM Tünel İşletmesi ile İlgili Görevler Tünel işlet |

### `Q056` — Tünel trafik yönetimi ve izleme

- language: **tr** · type: **operations** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000048-C0011` — ## 1.2.13.Trafik Mühendisi Görev Ve Yetkileri: a)Tünel Bak ı m İş letme Ş efli ğ i s ı n ı rlar ı içerisinde yatay ve dü ş ey i ş 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6832 | `DOC000167-C0010` |  | ⚑ | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |
| 1 | 0.6618 | `DOC000036-C0030` |  |  | ÜÇÜNCÜ BÖLÜM Tünel İşletmesi ile İlgili Görevler Tünel işlet |
| 2 | 0.6429 | `DOC000129-C0002` |  |  | Alarm Durumu |
| 3 | 0.6417 | `DOC000036-C0031` |  |  | Risk analizi |
| 4 | 0.6311 | `DOC000036-C0035` |  |  | Alternatif güzergahlar ve gabariler |

### `Q060` — Tünel elektromekanik tesisat bakımı

- language: **tr** · type: **operations** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000048-C0013` — ellerde Yap ı lan Bak ı m Hizmetleri; - Yap ı sal Bak ı m - Elektrik, Elektronik Ve Elektromekanik Sistemlerin Bak ı m ı olmak üzere iki grupta toplan

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6562 | `DOC000075-C0109` |  |  |  |
| 2 | 0.6442 | `DOC000075-C0108` |  |  |  |
| 3 | 0.6433 | `DOC000075-C0101` |  |  |  |
| 4 | 0.6374 | `DOC000075-C0116` |  |  |  |
| 5 | 0.6328 | `DOC000075-C0102` |  |  |  |

### `Q064` — Acil kaçış yolları ve kaçış tünelleri

- language: **tr** · type: **safety** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000045-C0001` — e şerit sayısı, tünel geometrisi, aydınlatma, havalandırma, kaçış yolları ve acil çıkışlar, acil servisler için erişim, acil istasyonlar, acil güç kay

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6608 | `DOC000172-C0027` |  |  | Slayt 27 |
| 2 | 0.6510 | `DOC000047-C0041` |  |  | 1.3.6.1 Emergency Egress |
| 3 | 0.6286 | `DOC000075-C0015` |  |  |  |
| 4 | 0.6206 | `DOC000129-C0002` |  |  | Alarm Durumu |
| 5 | 0.6191 | `DOC000036-C0036` |  |  | Tehlikeli maddeler |

### `Q071` — Tünel güvenliği yönetmeliğinde belirtilen asgari gereklilikler

- language: **tr** · type: **regulation** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000036-C0002` — MADDE 1- (1) Grizu gazı ve/veya yanıcı gazlar veya tozlar nedeniyle muhtemel patlayıcı ortama sahip yeraltı kömür ocakla

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6886 | `DOC000045-C0004` |  |  | TÜNEL GÜVENLİĞİ PROJE KRİTERLERİ (1) |
| 2 | 0.6764 | `DOC000167-C0013` |  |  | 5. SONUÇLAR |
| 3 | 0.6742 | `DOC000075-C0014` |  |  |  |
| 4 | 0.6688 | `DOC000036-C0035` |  |  | Alternatif güzergahlar ve gabariler |
| 5 | 0.6670 | `DOC000130-C0002` |  |  | TÜNEL GÜVENL İĞİ PROJE KR İ TERLER İ |

### `Q075` — KGM tünel projelerinde uyulacak esaslar

- language: **tr** · type: **regulation** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000045-C0001` — = original_page_start + chunk_local_page - 1 --> ## TÜRKİYE KARAYOLLARI TÜNELLERİNİN TARİHÇESİ VE TÜNEL GÜVENLİK KRİTERLERİ 1 ## Ahmet İrfan ÜNAL 1 YT

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6334 | `DOC000075-C0170` |  |  |  |
| 2 | 0.6285 | `DOC000075-C0175` |  |  |  |
| 3 | 0.6259 | `DOC000075-C0171` |  |  |  |
| 4 | 0.6214 | `DOC000075-C0178` |  |  |  |
| 5 | 0.6212 | `DOC000075-C0173` |  |  |  |

### `Q076` — AASHTO design specification references

- language: **en** · type: **regulation** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000015-C0038` — ## 3.8 Other Types of Structural Repairs (FHWA, 2009) and (AASHTO, 2010) The following links take the reader to repair information contained in other 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6180 | `DOC000047-C0365` |  |  | REFERENCES |
| 2 | 0.5785 | `DOC000015-C0104` |  |  | 4.13 Glossary of Selected Items |
| 3 | 0.5725 | `DOC000047-C0236` |  |  | 10.3.2 Load Combinations |
| 4 | 0.5677 | `DOC000003-C0227` |  |  | List of Abbreviations |
| 5 | 0.5645 | `DOC000003-C0226` |  |  | List of Abbreviations |

### `Q078` — Minimum gabari ve serbest yükseklik şartları

- language: **tr** · type: **regulation** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000036-C0035` — nayı ile gerçekleştirilebilir. ## Alternatif güzergahlar ve gabariler

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5633 | `DOC000236-C0483` |  |  | 521.03.03 Yapım Şartları |
| 2 | 0.5626 | `DOC000045-C0004` |  |  | TÜNEL GÜVENLİĞİ PROJE KRİTERLERİ (1) |
| 3 | 0.5577 | `DOC000087-C0338` |  |  | 405.03.01 Agrega |
| 4 | 0.5569 | `DOC000075-C0013` |  |  |  |
| 5 | 0.5562 | `DOC000063-C0008` |  |  | ÜÇÜNCÜ BÖLÜM |

### `Q079` — Acceptance criteria and quality control tests

- language: **en** · type: **regulation** · difficulty: **hard** · cross-lingual: **False**
- annotation: `body_presence_anchor` · gold chunks: **22**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000007-C0015` — | 6.7 | Checking the tunnelling machine for suitability and acceptance based on a risk analysis | Checking the tunnelling machine for suitability and 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6055 | `DOC000087-C0364` |  |  | 407.12 Kalite Kontrol Deneyleri |
| 2 | 0.6046 | `DOC000236-C0367` |  |  | 407.12 Kalite Kontrol Deneyleri |
| 3 | 0.6045 | `DOC000170-C0073` |  |  | GLOSSARY |
| 4 | 0.6033 | `DOC000087-C0296` |  |  | Ayrıca: |
| 5 | 0.5975 | `DOC000087-C0337` |  |  | Tablo-404-3 Kalite Kontrol Deneyleri |

### `Q081` — Tunnel lighting energy cost per kWh

- language: **en** · type: **numeric** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000002-C0006` — icity Cost | Electricity Cost | | |  Jet fan @ 1,000,000 1 kwh x 20 | 20.0 Million NPR | | |  Lighting and others | 5.0 Million NPR | | | Sub-total 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6781 | `DOC000001-C0012` |  |  | 3.3. Lighting systems costs |
| 2 | 0.6664 | `DOC000001-C0011` |  |  | 3.3. Lighting systems costs |
| 3 | 0.6574 | `DOC000001-C0010` |  |  | 3.2. Lighting systems design results |
| 4 | 0.6493 | `DOC000044-C0002` |  |  | 1.1. Lighting literature review |
| 5 | 0.6485 | `DOC000001-C0009` |  |  | 3.1. Materials and methods |

### `Q087` — Ventilation air flow rate requirements

- language: **en** · type: **numeric** · difficulty: **hard** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000195-C0003` — ## Projeye Dair T eknik Bilgiler: İhale Bedeli: 61.267.757,18 Tl İşveren Kurum: DSİ 21.Bölge Müdürlüğü Kontrolörlük: DSİ 21.Bölge Mü

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6281 | `DOC000075-C0186` |  |  |  |
| 2 | 0.6141 | `DOC000197-C0023` |  |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |
| 3 | 0.5948 | `DOC000075-C0091` |  |  |  |
| 4 | 0.5938 | `DOC000037-C0026` |  |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |
| 5 | 0.5937 | `DOC000075-C0190` |  |  |  |

### `Q089` — Concrete compressive strength class requirements

- language: **en** · type: **numeric** · difficulty: **hard** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0238` —  of the concrete φ = 0.55 for plain concrete f c ' = 28 day compressive strength of the concrete S = The section modulus of the lining section based o

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6358 | `DOC000236-C0285` |  |  | 351.10.01 Basınç Dayanım Sınıfları |
| 2 | 0.6256 | `DOC000087-C0284` |  |  | Tablo-351-5 Püskürtme Beton İçin Basınç Dayanım Sınıfları ve |
| 3 | 0.6211 | `DOC000087-C0108` |  |  | Tablo-308-17 Beton Sınıfları ve Basınç Dayanımları |
| 4 | 0.6158 | `DOC000087-C0110` |  |  | Tablo-308-19 Taze Beton Kıvam Sınıfları |
| 5 | 0.5990 | `DOC000236-C0104` |  |  | 308.04 Beton Sınıfları |

### `Q091` — Türkiye'deki karayolu tünellerinin isimleri ve uzunlukları

- language: **tr** · type: **named_entity** · difficulty: **hard** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000071-C0055` — | **Tünel Adı: KHM** **Kilometre: 5+45f&gt;°°** | **Formasyon:** **İftAtMft Fİ*).** | **Kaya sınıflaması (CSIR-RMR):** **Ç6 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6711 | `DOC000049-C0149` |  |  | 2015 YILINDA TAMAMLANMASI PLANLANAN TÜNELLER |
| 2 | 0.6551 | `DOC000167-C0004` |  |  | 4. TÜRKİYE'DE TÜNEL GÜVENLİĞİ |
| 3 | 0.6494 | `DOC000098-C0007` |  |  |  |
| 4 | 0.6466 | `DOC000075-C0019` |  |  |  |
| 5 | 0.6388 | `DOC000073-C0001` |  |  |  |

### `Q098` — Bolu Dağı Tüneli

- language: **tr** · type: **named_entity** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000038-C0001` — local_page - 1 --> ## An Ex-Post Cost - Benefit Analysis of Bolu Mountain Tunnel Project 1 Gaye KOCABAŞ 1 , Barış Serkan KOPURLU 2 ## ABSTRACT This pa

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5457 | `DOC000126-C0001` |  |  | TURK E TUNELCILIK SEMINERI2O13 |
| 2 | 0.5378 | `DOC000211-C0017` |  |  | Sayfa 17 |
| 3 | 0.5219 | `DOC000304-C0049` |  |  | Slayt 53 |
| 4 | 0.5219 | `DOC000283-C0049` |  |  | Slayt 53 |
| 5 | 0.5126 | `DOC000167-C0007` |  |  | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |

### `Q109` — tünel havalandırma sistemi tasarımı

- language: **tr** · type: **design** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **27**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000003-C0027` — ssenger station due to power loss, which cripples lighting, ventilation, and safety systems. Disrupted sewer, steam, and water lines allowing material

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6572 | `DOC000096-C0004` |  |  | 3 Korunma Hücreleri |
| 2 | 0.6236 | `DOC000075-C0065` |  |  |  |
| 3 | 0.6202 | `DOC000166-C0008` |  |  | 5. Sonuç ve Öneriler |
| 4 | 0.6179 | `DOC000199-C0004` |  |  | YÜKSEK PERFORMANS DÜŞÜK ENERJİ MALİYETİ |
| 5 | 0.6129 | `DOC000037-C0011` |  |  | içiNDEKİLER/ R / CONTENTS |

### `Q110` — kaya kütlesi sınıflandırma sistemleri

- language: **tr** · type: **geotechnical** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000047-C0065` — ## 3.5.3.2 Rock Identification and Classification In rock, rock mass characteristics and discontinuiti es typically have a much greater influence on g

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7039 | `DOC000072-C0059` |  |  | Ek-2’in devamı |
| 2 | 0.6714 | `DOC000236-C0226` |  |  | 350.02 Kaya Sınıflandırma |
| 3 | 0.6618 | `DOC000124-C0009` |  |  |  |
| 4 | 0.6436 | `DOC000071-C0009` |  |  |  |
| 5 | 0.6398 | `DOC000124-C0017` |  |  |  |

### `Q111` — tunnel maintenance and operation costs

- language: **en** · type: **operations** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000036-C0030` — ontrol Merkezi olan tünel veya grup tünellerde, Tesisler ve Bakım Başmühendisliğine bağlı Tünel Bakım İşletme Şefliğince, - b) Kontrol Merkezi olmayan

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7072 | `DOC000041-R1-C0001` |  |  | Estimate of annual operating costs Highway Tunnel |
| 2 | 0.6971 | `DOC000019-C0005` |  |  | 2.2 Estimating Operational and Regular Maintenance Costs |
| 3 | 0.6964 | `DOC000012-C0001` |  |  |  |
| 4 | 0.6911 | `DOC000002-C0007` |  |  | (3) Tunnel Management Office Operator |
| 5 | 0.6867 | `DOC000004-C0001` |  |  | 7. COST OF MAINTENANCE |

### `Q112` — shotcrete application requirements

- language: **en** · type: **construction** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **23**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000072-C0018` — #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanarak hava b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6293 | `DOC000047-C0250` |  |  | 10.7 SHOTCRETE LINING |
| 2 | 0.5690 | `DOC000227-C0004` |  |  |  |
| 3 | 0.5685 | `DOC000047-C0351` |  |  | 16.4.5 Shotcrete Repairs |
| 4 | 0.5461 | `DOC000047-C0213` |  |  | 9.5.1.1 Effect of Shotcrete |
| 5 | 0.5408 | `DOC000007-C0012` |  |  | Table of Contents |

### `Q113` — rock bolt pull-out test

- language: **en** · type: **regulation** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **7**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000087-C0243` — ## 350.04.07.02.01 SN-Bulonları ve PG-Bulonları 1. Aksi onaylanmadıkça bulonların minimum çapı ST 42 için 28 mm, ST 52 için 25 mm olacaktır. 2

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6213 | `DOC000047-C0218` |  |  | 9.5.2.2 Practical Aspects |
| 2 | 0.6044 | `DOC000047-C0131` |  |  | 6.5.2.2 Rock Bolts |
| 3 | 0.5569 | `DOC000037-C0034` |  |  | 3.2 Ground Reinforcement |
| 4 | 0.5562 | `DOC000047-C0214` |  |  | 9.5.2 Rock Reinforcement |
| 5 | 0.5514 | `DOC000122-C0022` |  |  | 5 REFERENCES |

## Low-Content Interference

Queries where flagged low-content chunks occupy the most top-5 slots.

### `Q102` — Tünel kontrol mühendisi geliştirme kursu içeriği

- language: **tr** · type: **source_specific** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **8**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000066-C0001` — <!-- image --> <!-- image --> # Tünel Kontrol Mühendisi Geliştirme Kursu YENİ AVUSTURYA TÜNEL AÇMA YÖNTEMİ (NATM) 24~28 Şubat 2020, Ankara Suhan Mutlu

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6279 | `DOC000221-C0001` | ✔ |  | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destek Sistem |
| 2 | 0.6184 | `DOC000302-C0038` |  |  | Slayt 42 |
| 3 | 0.6101 | `DOC000302-C0043` |  |  | Slayt 47 |
| 4 | 0.6090 | `DOC000302-C0099` |  | ⚑ | Slayt 103 |
| 5 | 0.6082 | `DOC000302-C0098` |  | ⚑ | Slayt 102 |

### `Q056` — Tünel trafik yönetimi ve izleme

- language: **tr** · type: **operations** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **16**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000048-C0011` — ## 1.2.13.Trafik Mühendisi Görev Ve Yetkileri: a)Tünel Bak ı m İş letme Ş efli ğ i s ı n ı rlar ı içerisinde yatay ve dü ş ey i ş 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6832 | `DOC000167-C0010` |  | ⚑ | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |
| 1 | 0.6618 | `DOC000036-C0030` |  |  | ÜÇÜNCÜ BÖLÜM Tünel İşletmesi ile İlgili Görevler Tünel işlet |
| 2 | 0.6429 | `DOC000129-C0002` |  |  | Alarm Durumu |
| 3 | 0.6417 | `DOC000036-C0031` |  |  | Risk analizi |
| 4 | 0.6311 | `DOC000036-C0035` |  |  | Alternatif güzergahlar ve gabariler |

### `Q062` — Tünelde yangın güvenliği önlemleri

- language: **tr** · type: **safety** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **0.333** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0467` — lir. Kesilen otlar uygulama sahasından uzaklaştırılacaktır. Yangınlara karşı koruma amacıyla, yol dış kenarından en az 2,5 m mesafedeki tüm kuru otlar

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7313 | `DOC000036-C0035` |  |  | Alternatif güzergahlar ve gabariler |
| 2 | 0.7262 | `DOC000167-C0010` |  | ⚑ | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |
| 2 | 0.6961 | `DOC000167-C0012` | ✔ |  | 4.3. İncelenen Tünellerde Tespit Edilen Güvenlik Sorunları v |
| 3 | 0.6940 | `DOC000036-C0036` |  |  | Tehlikeli maddeler |
| 4 | 0.6873 | `DOC000166-C0002` | ✔ |  | 2.1. Demiryolu tünellerinde güvenlik |

### `Q067` — Traffic safety in road tunnels

- language: **en** · type: **safety** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **0.500** · doc_recall@10 **1**
- expected evidence: `DOC000002-C0013` — ## (1) Traffic accident, Vehicle breakdown Upon receiving a report of (or confirming via CCTV) traffic accident (vehicle breakd

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7068 | `DOC000167-C0010` |  | ⚑ | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |
| 1 | 0.6714 | `DOC000005-C0003` | ✔ |  | 1.2.2 Constructional measures for road safety in tunnels |
| 2 | 0.6650 | `DOC000003-C0094` |  |  | 4.5.1 Key Safety Functions |
| 3 | 0.6591 | `DOC000047-C0032` |  |  | 1.1.2 Classes of Roads and Vehicle Sizes |
| 4 | 0.6573 | `DOC000167-C0001` |  |  | Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği * |

### `Q068` — Karayolu tünellerinde trafik güvenliği

- language: **tr** · type: **safety** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **1** · MRR@10 **0.500** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0468` — ## 516.02.11 Trafik Güvenliği Açısından Tehlike Oluşturan Ağaç ve Çalıların Kaldırılması Yol kenarında yer alan kökleri gevşemiş, göv

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.8684 | `DOC000167-C0010` |  | ⚑ | 4.2. Türkiye'de Karayolu Tünellerinde Meydana Gelen Trafik K |
| 1 | 0.7007 | `DOC000167-C0001` | ✔ |  | Türkiye'deki Karayolu Tünellerinde Trafik Güvenliği * |
| 2 | 0.6919 | `DOC000045-C0003` |  |  | 7. SONUÇ VE ÖNERİLER |
| 3 | 0.6895 | `DOC000042-C0002` |  |  | 1. Giriş |
| 4 | 0.6892 | `DOC000130-C0004` |  |  | Karayolu Tünellerinde Standart Güvenlik Sistemleri ve Ekipma |

### `Q001` — What is the New Austrian Tunnelling Method?

- language: **en** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000308-C0007` — ## 4. Sequential Excavation Method NATM The Sequential Excavation Method (SEM), also commonly referred to as the New Austrian Tunneling Method (NATM),

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6218 | `DOC000124-C0005` |  |  |  |
| 2 | 0.6151 | `DOC000066-C0004` |  |  | Trans-Sibirya Demiryolu Tünel çalışmalarına ait fotoğraflar, |
| 3 | 0.6086 | `DOC000105-C0003` |  |  | 3 YENİ AVUSTURYA TÜNEL AÇMA YÖNTEMİNİN (NATM) GELİŞTİRİLMESİ |
| 4 | 0.6076 | `DOC000168-C0014` |  |  | Definition of the system |
| 5 | 0.6046 | `DOC000110-C0001` |  |  | TUNNELLING PRACTICE in mid NINETEEN HUNDREDS |

### `Q002` — NATM yönteminin temel ilkesi nedir?

- language: **tr** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **4**
- recall@10 **1** · MRR@10 **0.167** · doc_recall@10 **1**
- expected evidence: `DOC000103-C0001` — ### NATM TÜNEL YAPIMI 1. **T ÜNEL KAZISI VE DESTEKLEME** - 1.1. **KAZI YÖNTEMİ VE AŞAMALARI** Tünellerde kazı destekleme işl

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6512 | `DOC000308-C0007` |  |  | 4. Sequential Excavation Method NATM |
| 2 | 0.6370 | `DOC000124-C0020` |  |  |  |
| 3 | 0.6230 | `DOC000302-C0142` |  |  | Slayt 151 |
| 4 | 0.6136 | `DOC000047-C0198` |  |  | 9.2 BACKGROUND AND CONCEPTS |
| 5 | 0.6123 | `DOC000076-C0005` |  |  |  |

### `Q003` — What is shotcrete used for in tunnels?

- language: **en** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **50**
- recall@10 **1** · MRR@10 **0.333** · doc_recall@10 **1**
- expected evidence: `DOC000003-C0076` — y have various liner systems, including rock reinforcement, shotcrete, steel ribs and lattice girder, precast concrete segment, cast-in-place concrete

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6410 | `DOC000018-C0003` |  |  | Support |
| 2 | 0.6297 | `DOC000047-C0349` |  |  | 16.4 STRUCTURAL REPAIR - CONCRETE |
| 3 | 0.6270 | `DOC000015-C0022` | ✔ |  | Unlined Tunnels in Rock with Reinforcement As Needed 1.4.3.1 |
| 4 | 0.6168 | `DOC000047-C0250` | ✔ |  | 10.7 SHOTCRETE LINING |
| 5 | 0.6145 | `DOC000047-C0212` | ✔ |  | 9.5.1.1 Effect of Shotcrete |

### `Q004` — Püskürtme beton nedir ve ne için kullanılır?

- language: **tr** · type: **definition** · difficulty: **easy** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **47**
- recall@10 **1** · MRR@10 **1.000** · doc_recall@10 **1**
- expected evidence: `DOC000072-C0018` — #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanarak hava b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7523 | `DOC000072-C0018` | ✔ |  | 47 Püskürtme Beton Kaplamalar |
| 2 | 0.7129 | `DOC000196-C0022` |  |  | 1.1 Genel Özellikleri |
| 3 | 0.7126 | `DOC000214-C0001` |  |  | Tünel Kontrol Mühendisi Geliştirme Kursu Tünel Destekleme El |
| 4 | 0.7120 | `DOC000087-C0278` |  |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |
| 5 | 0.7102 | `DOC000236-C0279` |  |  | 351.08.07 Püskürtmenin Uygulanma Tekniği |

### `Q005` — What does the Q-system classify?

- language: **en** · type: **definition** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **9**
- recall@10 **1** · MRR@10 **0.500** · doc_recall@10 **1**
- expected evidence: `DOC000037-C0085` —  granitic rock and found a satisfactory correlation between Q system and TBM field penetration index (FPI). related to joint orientation). They conclu

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.5589 | `DOC000072-C0032` |  |  | 2.2.1.2. Q Zemin Sınıflandırma Ölçütüne Göre |
| 2 | 0.5406 | `DOC000047-C0116` | ✔ |  | 6.3.4 Q System |
| 3 | 0.5147 | `DOC000074-C0003` |  |  |  |
| 4 | 0.5082 | `DOC000007-C0003` |  |  | Table of Contents |
| 5 | 0.5040 | `DOC000302-C0131` |  |  | Slayt 140 |

## Cross-Lingual

Question in one language, gold restricted to the other.

### `Q109` — tünel havalandırma sistemi tasarımı

- language: **tr** · type: **design** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **27**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000003-C0027` — ssenger station due to power loss, which cripples lighting, ventilation, and safety systems. Disrupted sewer, steam, and water lines allowing material

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6572 | `DOC000096-C0004` |  |  | 3 Korunma Hücreleri |
| 2 | 0.6236 | `DOC000075-C0065` |  |  |  |
| 3 | 0.6202 | `DOC000166-C0008` |  |  | 5. Sonuç ve Öneriler |
| 4 | 0.6179 | `DOC000199-C0004` |  |  | YÜKSEK PERFORMANS DÜŞÜK ENERJİ MALİYETİ |
| 5 | 0.6129 | `DOC000037-C0011` |  |  | içiNDEKİLER/ R / CONTENTS |

### `Q110` — kaya kütlesi sınıflandırma sistemleri

- language: **tr** · type: **geotechnical** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000047-C0065` — ## 3.5.3.2 Rock Identification and Classification In rock, rock mass characteristics and discontinuiti es typically have a much greater influence on g

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7039 | `DOC000072-C0059` |  |  | Ek-2’in devamı |
| 2 | 0.6714 | `DOC000236-C0226` |  |  | 350.02 Kaya Sınıflandırma |
| 3 | 0.6618 | `DOC000124-C0009` |  |  |  |
| 4 | 0.6436 | `DOC000071-C0009` |  |  |  |
| 5 | 0.6398 | `DOC000124-C0017` |  |  |  |

### `Q111` — tunnel maintenance and operation costs

- language: **en** · type: **operations** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000036-C0030` — ontrol Merkezi olan tünel veya grup tünellerde, Tesisler ve Bakım Başmühendisliğine bağlı Tünel Bakım İşletme Şefliğince, - b) Kontrol Merkezi olmayan

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.7072 | `DOC000041-R1-C0001` |  |  | Estimate of annual operating costs Highway Tunnel |
| 2 | 0.6971 | `DOC000019-C0005` |  |  | 2.2 Estimating Operational and Regular Maintenance Costs |
| 3 | 0.6964 | `DOC000012-C0001` |  |  |  |
| 4 | 0.6911 | `DOC000002-C0007` |  |  | (3) Tunnel Management Office Operator |
| 5 | 0.6867 | `DOC000004-C0001` |  |  | 7. COST OF MAINTENANCE |

### `Q112` — shotcrete application requirements

- language: **en** · type: **construction** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **23**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000072-C0018` — #### 47 Püskürtme Beton Kaplamalar Püskürtme beton, onarım yada yapım amacıyla önceden kuru yada ıslak yolla hazırlanarak hava b

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6293 | `DOC000047-C0250` |  |  | 10.7 SHOTCRETE LINING |
| 2 | 0.5690 | `DOC000227-C0004` |  |  |  |
| 3 | 0.5685 | `DOC000047-C0351` |  |  | 16.4.5 Shotcrete Repairs |
| 4 | 0.5461 | `DOC000047-C0213` |  |  | 9.5.1.1 Effect of Shotcrete |
| 5 | 0.5408 | `DOC000007-C0012` |  |  | Table of Contents |

### `Q113` — rock bolt pull-out test

- language: **en** · type: **regulation** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **7**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000087-C0243` — ## 350.04.07.02.01 SN-Bulonları ve PG-Bulonları 1. Aksi onaylanmadıkça bulonların minimum çapı ST 42 için 28 mm, ST 52 için 25 mm olacaktır. 2

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6213 | `DOC000047-C0218` |  |  | 9.5.2.2 Practical Aspects |
| 2 | 0.6044 | `DOC000047-C0131` |  |  | 6.5.2.2 Rock Bolts |
| 3 | 0.5569 | `DOC000037-C0034` |  |  | 3.2 Ground Reinforcement |
| 4 | 0.5562 | `DOC000047-C0214` |  |  | 9.5.2 Rock Reinforcement |
| 5 | 0.5514 | `DOC000122-C0022` |  |  | 5 REFERENCES |

### `Q114` — geotechnical investigation report contents

- language: **en** · type: **geotechnical** · difficulty: **hard** · cross-lingual: **True**
- annotation: `heading_anchor_language_restricted` · gold chunks: **5**
- recall@10 **1** · MRR@10 **0.111** · doc_recall@10 **1**
- expected evidence: `DOC000087-C0454` — mler, rakım değerleri vb., - b. Jeoloji: Proje güzergâhının jeolojik özellikleri, güzergâhın jeolojik niteliğine ilişkin genel veriler, - c. Drenaj: P

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6398 | `DOC000047-C0085` |  |  | 4.2 GEOTECHNICAL DATA REPORT |
| 2 | 0.6249 | `DOC000122-C0010` |  |  | 1.7 Geotechnical report |
| 3 | 0.5972 | `DOC000047-C0086` |  |  | 4.3 GEOTECHNICAL DESIGN MEMORANDUM |
| 4 | 0.5959 | `DOC000047-C0008` |  |  | TABLE OF CONTENTS |
| 5 | 0.5836 | `DOC000047-C0051` |  |  | 3.1.1 Phasing of Geotechnical Investigations |

## Numeric / Table Failures

### `Q081` — Tunnel lighting energy cost per kWh

- language: **en** · type: **numeric** · difficulty: **medium** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000002-C0006` — icity Cost | Electricity Cost | | |  Jet fan @ 1,000,000 1 kwh x 20 | 20.0 Million NPR | | |  Lighting and others | 5.0 Million NPR | | | Sub-total 

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6781 | `DOC000001-C0012` |  |  | 3.3. Lighting systems costs |
| 2 | 0.6664 | `DOC000001-C0011` |  |  | 3.3. Lighting systems costs |
| 3 | 0.6574 | `DOC000001-C0010` |  |  | 3.2. Lighting systems design results |
| 4 | 0.6493 | `DOC000044-C0002` |  |  | 1.1. Lighting literature review |
| 5 | 0.6485 | `DOC000001-C0009` |  |  | 3.1. Materials and methods |

### `Q087` — Ventilation air flow rate requirements

- language: **en** · type: **numeric** · difficulty: **hard** · cross-lingual: **False**
- annotation: `heading_anchor` · gold chunks: **2**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **0**
- expected evidence: `DOC000195-C0003` — ## Projeye Dair T eknik Bilgiler: İhale Bedeli: 61.267.757,18 Tl İşveren Kurum: DSİ 21.Bölge Müdürlüğü Kontrolörlük: DSİ 21.Bölge Mü

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6281 | `DOC000075-C0186` |  |  |  |
| 2 | 0.6141 | `DOC000197-C0023` |  |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |
| 3 | 0.5948 | `DOC000075-C0091` |  |  |  |
| 4 | 0.5938 | `DOC000037-C0026` |  |  | 6.2 Ventilation (in the Tunnel and Inside the Belt Channel) |
| 5 | 0.5937 | `DOC000075-C0190` |  |  |  |

### `Q089` — Concrete compressive strength class requirements

- language: **en** · type: **numeric** · difficulty: **hard** · cross-lingual: **False**
- annotation: `body_density_anchor` · gold chunks: **1**
- recall@10 **0** · MRR@10 **0.000** · doc_recall@10 **1**
- expected evidence: `DOC000047-C0238` —  of the concrete φ = 0.55 for plain concrete f c ' = 28 day compressive strength of the concrete S = The section modulus of the lining section based o

| # | score | chunk | gold? | low? | preview |
|---|---|---|---|---|---|
| 1 | 0.6358 | `DOC000236-C0285` |  |  | 351.10.01 Basınç Dayanım Sınıfları |
| 2 | 0.6256 | `DOC000087-C0284` |  |  | Tablo-351-5 Püskürtme Beton İçin Basınç Dayanım Sınıfları ve |
| 3 | 0.6211 | `DOC000087-C0108` |  |  | Tablo-308-17 Beton Sınıfları ve Basınç Dayanımları |
| 4 | 0.6158 | `DOC000087-C0110` |  |  | Tablo-308-19 Taze Beton Kıvam Sınıfları |
| 5 | 0.5990 | `DOC000236-C0104` |  |  | 308.04 Beton Sınıfları |

<!-- image -->

Logo

ISSN: 2564-6605

Ömer Halisdemir Üniversitesi Mühendislik Bilimleri Dergisi, Cilt 6, Sayı 2, (2017), 642-652 Omer Halisdemir University Journal of Engineering Sciences, Volume 6, Issue 2, (2017 ), 642-652

<!-- image -->

Icon

## YÜKSEK HIZLI DEMİRYOLU TÜNELLERİNDE GÜVENLİK TÜNELİ MODELLEMELERİ: ANKARA-İSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

Evren POŞLUK (ORCID: 0000-0001-9520-5268) 1 Mustafa KORKANÇ (ORCID: 0000-0001-7382-8077) 2 *

1

TCDD 2. Demiryolu Yapım Grup Müdürlüğü, Bozüyük, Bilecik, Türkiye 2 Jeoloji Mühendisliği Bölümü, Mühendislik Fakültesi, Niğde Ömer Halisdemir Üniversitesi, Niğde, Türkiye

Geliş / Received:

17.10.2016

Düzeltmelerin gelişi / Received in revised form:

18.05.2017

Kabul  / Accepted:

31.05.2017

## ÖZ

Bu  çalışmada Ankara-İstanbul yüksek  hızlı demiryolu  projesinde yer alan 26 numaralı tünel (Proje Km:216+260-222+360) irdelenmiştir. 13,77 m. çapındaki tünel açma makinesi (TBM) ile imalatı devam eden 26 numaralı tünel ve devamı (toplam uzunluğu 7096 m) altyapı güvenlik önlemleri açısından değerlendirilmiştir. Tünellerde  güvenliğin  sağlanabilmesi  amacıyla  paralel  tünel,  yaklaşım  ve  emniyet  şaft  tünelleri  ile  ray  altı güvenlik  tüneli  alternatifleri  modellenmiştir.  Bu  modeller  maliyet,  imalat  süreleri  ve  uygulama  kolaylığı açısından irdelenmiştir. Tünel güzergahı boyunca yerel kaya koşullarının oldukça zor ve karmaşık olduğu da göz önüne  alınarak  bu  tünel  için  en  az  maliyet  ve  en  kısa  imalat  süresi  olarak  ray  altı  emniyet  tüneli  olduğu belirlenmiştir. Bu modelin, daha önce uygulanmamış olması sebebi ile işletme sırasında uygulanabilirliği Phase 2 V.  8.0  programı  ile  irdelenmiş,  işletmecilik  faaliyetleri  sırasında  oluşabilecek  eksenel  gerilmeler  göz  önüne alınarak ray altı ekipmanlarının daha rijit hale getirilmesi koşulu ile uygulanabilir olduğu sonucuna varılmıştır.

Anahtar Kelimeler: Yüksek hızlı demiryolu tüneli, ray altı tünel, tünel güvenlik modellemeleri, sayısal analiz

## TUNNEL SAFETY MODELLINGS IN HIGH SPEED RAILWAY TUNNELS: CASE OF ANKARA-ISTANBUL HIGH SPEED TRAIN PROJECT TUNNEL NO. 26

## ABSTRACT

In this study, tunnel 26 (Project Km:216+260-222+360) of the Ankara-Istanbul high-speed railway project was studied in detail. The tunnel 26 and its continuation (total length: 7096 m), which are excavating with a 13,77 meter-diameter  tunnel  boring  machine  (TBM),  was  evaluated  in  point  of  infrastructure  safety  measures.  To ensure  safety  in  the  tunnels,  parallel  tunnel,  approach  and  safety  shaft  tunnels,  sub-rail  safety  tunnels  were modelled. These models were evaluated on the basis of cost, manufacturing time and ease of application. By considering the complex local rock conditions, it was confirmed that the sub-rail safety tunnel is the best tunnel with regard to  minimum cost and minimum manufacturing time. Because this model has not been performed before, the applicability was performed by using Phase 2 V. 8.0., and by considering the axial stresses that can be observed  during  the  operation,  the  sub-rail  equipments  are  applicable  under  the  condition  that  they  are  more rigid.

Keywords : High speed railway tunnel, sub-rail tunnel, tunnel safety modelling, numerical analysis

* Corresponding author / Sorumlu yazar. Tel.: +90 388 225 2259; e-mail / e-posta: mkorkanc@ohu.edu.tr

YÜKSEK  HIZLI  DEMİRYOLU  TÜNELLERİNDE  GÜVENLİK  TÜNELİ  MODELLEMELERİ:  ANKARAİSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

## 1. GİRİŞ

Demiryolu güzergâh çalışmaları sırasında kısıtlı kurp ve eğim toleransları nedeni ile sıkça tünel çözümlerine başvurulmaktadır  [1].  Bununla  birlikte  işletme  sırasında  tünellerde  yeterli  güvenlik  önlemlerinin  alınmaması kötü sonuçlar doğurmaktadır. Örneğin 1842'de Fransa'da bulunan Mendon demiryolu tünelinde meydana gelen kazada 150 kişinin öldüğü rapor edilmiştir [2]. 1995 yılında ise Azerbaycan'ın başkenti Bakü'de yaşanan kazada 289 kişi yaşamını yitirmiştir. Yüksek hızlı demir yollarında ise en ciddi tünel kazalarından biri 11 Eylül 2008'de İngiltere  ile  Fransa  arasında  bulunan  Manş  Tünelinde  gerçekleşmiştir.  Olayın  nedeni  bir  vagondaki  kimyasal madde (toksik fenol) yüklü kamyonda patlama olmasıdır. Bu kazada 12 kişi hayatını kaybetmiştir [3].

Yapılan  araştırmalar  ulaşım  tünelleri  içerisinde  en  az  kazaya  rağmen  en  fazla  can  kaybının  demiryolu tünellerinde  olduğunu  ortaya  koymaktadır.  Bunun  nedeni  tek  seferde  en  fazla  yolcunun  demiryolu  ile taşınmasıdır.  Bu  veriler  de  göstermektedir  ki  demiryolu  tünellerinde  güvenlik  önlemlerinin  alınması  ulaşım güvenliği açısından son derece önemlidir.

Demiryolu işletmeciliğinde tünel içerisinde olası riskler uzun durma, hattan çıkma (deray), çarpışma ve yangın olarak  sıralanabilir.  Bu  durumlarda  gerek  yolcunun  kendi  kendini  tahliye  etmesi  gerekse  de  olaya  müdahale edilebilmesi amacı  ile ana tünelden bağımsız ek tünel yapılarak tahliyenin sağlanması gerekmektedir. Diamantidis ve ark. [4], uzun demiryolu tünellerinde risk analizine yönelik yaptıkları çalışmalarında ilk olarak, dünyadaki tünel projelerini kısaca gözden geçirmişler, alınan risk analiz  yöntemlerini tartışılmışlardır. Her bir riski  ele  alarak  ölçülebilir  hedef  güvenlik  seviyeleri  önermişlerdir.  Ayrıca  risk  azaltılmasına  yönelik  güvenlik sistemlerini de özetlemişlerdir. Ayrıca Eskesen ve ark. [5], Uluslararası Tünel Derneğinin (ITA) 2 nolu çalışma grubu tarafından tünel ve metro projelerinin risklerinin belirlenmesi ve risk yönetimi için rehberlik edecek genel kuralları  içeren  bir  el  kitabı  hazırlanmışlar.  Bu  kılavuzda,  günümüz  tünel  uygulamalarının  başlangıcından işletmeye  alınmasına  kadar  tüm  proje  uygulaması  süresince  risk  yönetimi  aşamaları  anlatılmıştır.  Hızlı  tren demiryolları yatırımlarının dünyada hızla gelişmesi, Avrupa'da birçok ülkede hızlı trenin kullanılması ve yeni projelerin hazırlanması, standardizasyon ihtiyacını da beraberinde getirmiştir.

Bu çalışma kapsamında dünyada birçok ülkede geliştirilen ve kullanılan demiryolu tünel güvenlik standartları incelenmiştir. Proje ve imalat sırasında düşünülmesi gereken tünel alt yapı güvenlik önlemlerine ait dünyadan örnekler  ile  Ankara-İstanbul  hızlı  tren  projesi  kapsamında  yer  alan  26  numaralı  tünel  ve  bu  tünel  için uygulanabilecek  alt  yapı  güvenlik  önlemleri  ayrıntılı  olarak  incelenmiştir.  Yapılan  çalışmada  dünyada  yaygın kullanıma sahip paralel tünel, yaklaşım tünelleri ve emniyet bacaları (şaftları) ile bu çalışma ile geliştirilen ray altı tünel uygulamaları, maliyet uygulama kolaylığı ve imalat süreleri açısından kıyaslanmış, uygulanabilirlikleri karşılaştırılmıştır.

## 2. MATERYAL VE METOT

## 2.1. Tünel Güzergâhı ve Bölgenin Jeolojik Özellikleri

Örtü kalınlığının 30-236 m arasında değiştiği 26 numaralı tünel, Ankara-İstanbul hızlı tren projesinde Bilecik ilinin  10  km  güney  doğusunda,  Ahmetpınar  köyünün  200  m  doğusundan  bulunmaktadır.  Tünel  güzergahının batısında  Bozüyük-Mekece  karayolu  ve bölge  morfolojisini oluşturan  Karasu  Deresi bulunmaktadır (Şekil 1). Çalışma alanında farklı araştırmacılar tarafından farklı zamanlarda yapılan çalışmalarla güzergah jeolojisi ortaya konulmaya  çalışılmıştır.  Bu  çalışmalardan  Tüysüz  ve  Genç  [6]'e  göre,  inceleme  alanının  tabanında  karmaşık nitelikli  metapelit,  metabazit,  serpantinit  birimi  (Söğüt  Metamorfitleri)  bulunmakta,  bunları  intrüzif  ilişki  ile felsik intrüzifler kesmektedir (Şekil 2). Ayrıca araştırmacılar yörede Miyosen karasal çökelleri, yamaç molozu ve alüvyonlar ile heyelan malzemesinin de yer aldığını belirtmişlerdir (Şekil 3).

Tünel  güzergahı boyunca  karşılaşılan temel birim Şentürk ve  Karaköse [7] tarafından Söğüt Metamorfitleri, Yılmaz [8] tarafından da Söğüt metabaziti olarak adlandırılmıştır. Bu kayalar çoğunlukla metapellit ve ofiyolitik (serpantinit, serpantinleşmiş peridotit, piroksenit, ve diyabaz-mikrogabro) kayalardır.

Metapelitler (Şekil 2a) tünel güzergahında oldukça geniş bir alan kaplamaktadır. Yaygın olarak gri fillatlar ve bunlarla ardalanmalı olan grimsi-boz renkli metakumtaşları ve metasilttaşlarından oluşmaktadır (Şekil 2b). Gri fillatlar sık aralıklı yapraklanmalıdır.  Yapraklanma  yüzeyleri  parlaktır.  Tane  boyunun  nispeten  irileştiği kesimlerde  benekli  şist  görünümü  kazanmışlardır.  Kırık  ve  makaslama  zonlarında  kolaylıkla  ezildiğinden yumuşak  ve  dağılgan  bir  yapı  sunmaktadır.  Metabazitler,  yeşil  ve  tonlarındaki  renkleri  ile  mostrada  kolayca tanınırlar. Yer yer masif, çoğunlukla iyi yapraklanmalıdırlar. Bazı kesimlerde ise açık ve koyu yeşil renklerde bantlı yapılar sunmaktadır. Tünel güzergahı boyunca metapelitler Ahmetpınar köyünün 1,5 km G-GD kesiminde rastlanmaktadır.

## E. POŞLUK, M. KORKANÇ

Şekil 1. 26 numaralı tünelin yer bulduru haritası

<!-- image -->

Topographical map

Şekil 2. Söğüt  metamorfitleri ve onları  kesen  felsik intrüzyonlar (a-  metapelitlerin tünel  girişinde  görünümü,  b-fillat  ve  metasilttaşı,  c-serpantinit  içerisindeki  kuvars bantları [6], d-felsik intrüzyonlar [6])

<!-- image -->

Photograph

Ofiyolitik kayalar inceleme alanı içinde 2 büyük tektonik dilim halinde mostra vermektedir. Ayrıca az sayıda küçük dilimlere de rastlanmıştır. Serpantinitler genellikle yeşil ve tonlarında, siyahımsı renkli olup, çoğunlukla YÜKSEK  HIZLI  DEMİRYOLU  TÜNELLERİNDE  GÜVENLİK  TÜNELİ  MODELLEMELERİ:  ANKARAİSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

ezik ve makaslanmalıdır (Şekil 2c). Birim, her ne kadar tartışmalı da olsa genellikle Triyas yaşlı olarak kabul edilmektedir [7, 9].

Felsik  intrüzyonlar,  aşırı  ayrışmalı,  silisleşmiş,  felsik  bileşimli  (granitik)  dayk,  sil,  damar  ve  stoklardan oluşmaktadır.  Mostrada  beyaz,  kirli  beyaz,  sarımsı  ve  yer  yer  kahverengi  renklerde  gözlenirler.  Dayk  ve  sil kalınlıkları birkaç cm ile 3-5 metre arasında değişim göstermektedir (Şekil 2d).

Neojen çökel kayaları inceleme alanı içinde Ahmetpınarı köyü D-GD'sunda Çiftçeşme ve Tekçeşme Tepeleri arasındaki  zirvelerde  mostra  vermektedir.  Tünel  güzergahının  güneyinde  (tünelin  çıkış  kısmında)  ise  K-G yönünde akan Karasu çayı vadisi boyunca oluşmuş alüvyonlar bulunmaktadır. Söz konusu alüvyonlar, bölgedeki tüm  kaya  birimlerinin  çakıl,  kum,  kil  boyutlarındaki  tutturulmamış  malzemelerinden  oluşmaktadır.  Ayrıca Ahmetpınar  köyü  batısında  oldukça  geniş  bir  alanı  kapsayan  alanda  toplanmış  her  boy  malzemeden  oluşan heyelan malzemesi de gözlenmektedir. Tünel kazısı sırasında bu birimlerle karşılaşılması beklenmemektedir.

## 2.2. Mühendislik Jeolojisi Çalışmaları

26 numaralı tünel güzergahı, jeolojik açıdan için oldukça kompleks  yapılar barındırmaktadır. Tünel güzergahının  giriş  kısımlarında  (Ahmetpınar  köyü  batısında)  heyelan,  devamında  fay  zonları,  zayıf-çok  zayıf kayalar ile sağlam kayaya kadar değişen nitelikte birimlerin geçilmesi muhtemeldir. Ayrıca tünel güzergahının, Karasu Deresi yatağına paralel ve alt kotundan geçmesi ile bölgenin yağış ortalamasının yüksek alması yeraltı suyu  risklerini  de  arttırmaktadır.  Tünel  güzergahının  araştırılması  amacı  ile  farklı  tarihlerde  36  adet  karotlu sondaj çalışması yapılmış, bu sondajlardan ve yüzey araştırmalarından yararlanılarak tünel profili oluşturulmaya çalışılmıştır (Şekil 3).

Şekil 3. İncelenen 26 numaralı tünelin boy kesiti [6]

<!-- image -->

Geographical map

Sondaj çalışmalarından elde edilen karot numuneleri üzerinde, ISRM [10] belirtilen yöntemler esas alınarak laboratuvar  deneyleri  gerçekleştirilmiştir.  Bu  deneyler  ile  kayaçların  birim  hacim  ağırlık,  tek  eksenli  basınç direnci, poisson oranı ve elastisite modülü değerleri belirlenmiştir (Tablo 1).

Kayaçların  birim  hacim  ağırlık  değeri  bileşim  ve  dokularıyla  yakından  ilişkilidir.  Pratikte  birim  hacim ağırlıkları yüksek olan kayaçlar genellikle düşük poroziteli, düşük su emmeli ve yüksek özgül ağırlık değerlerine sahiptir [11]. İncelenen kayaçlardan elde edilen ortalama birim hacim ağırlıklar, NBG  [12]'e göre sınıflandırıldığında 'orta' birim hacim ağırlığa sahip kayaçlar olarak tanımlanmıştır.

Kayaçların  mekanik  özelliklerinin  belirlenmesi  dayanım  ve  deformobilite  açısından  oldukça  önemlidir. Yapılan  bu  çalışmada  elde  edilen  verilere  göre,  metapelitlerden  ortalama  12,52-34,56  MPa,  ofiyolitlerden ortalama 22,21 MPa ve felsik intrizüf kayaçlardan ise 27 MPa olan basınç dayanımı değerleri elde edilmiş olup, incelenen kayaçlar, Deere ve Miller [13]'a göre 'çok düşük-düşük' dayanımlı kayaç sınıfına girmektedir. Söz konusu  bu  kayaçlar,  Deere  ve  Miller  [13]'e  elastisite  modülüne  göre  sınıflandığında  'çok  düşük'  elastisite modülüne sahip kayaçlar olarak sınıflanmıştır. Kayaçlardan mühendislik açıdan düşük dayanım değerleri elde edilmesinde bölgenin jeolojik özellikleri ile ayrışmanın en etkin parametreler oldukları düşünülmüştür.

Tablo 1. Yapılan sondajlardan elde edilen karotlara ait deney sonuçları [14, 15, 16]

| Litoloji                                       | Özellik                                |   Örnek sayısı | Ortalama   | En büyük değer   | En küçük değer   |
|------------------------------------------------|----------------------------------------|----------------|------------|------------------|------------------|
| Söğüt Metamorfitleri Metapellit (zayıf kaya)   | Birim hacim ağırlık (γ n , kN/m 3 )    |             27 | 23,36      | 25,04            | 21,61            |
| Söğüt Metamorfitleri Metapellit (zayıf kaya)   | Tek eksenli basınç dayanımı (σ c, MPa) |             23 | 12,52      | 32               | 4,92             |
| Söğüt Metamorfitleri Metapellit (zayıf kaya)   | Elastisite modülü (E, GPa)             |             17 | 1,52       | 3,33             | 1,22             |
| Söğüt Metamorfitleri Metapellit (zayıf kaya)   | Poisson oranı (υ)                      |             17 | 0,27       | 0,31             | 0,17             |
| Söğüt Metamorfitleri Metapellit, (sağlam kaya) | Birim hacim ağırlık (γ n , kN/m 3 )    |             35 | 25,47      | 28,1             | 23,2             |
| Söğüt Metamorfitleri Metapellit, (sağlam kaya) | Tek eksenli basınç dayanımı (σ c, MPa) |             29 | 34,56      | 54,53            | 22,71            |
| Söğüt Metamorfitleri Metapellit, (sağlam kaya) | Elastisite modülü (E, GPa)             |             27 | 4,03       | 10,87            | 2,85             |
| Söğüt Metamorfitleri Metapellit, (sağlam kaya) | Poisson oranı (υ)                      |             27 | 0,26       | 0,32             | 0,21             |
| Söğüt Metamorfitleri (Ofiyolit)                | Birim hacim ağırlık (γ n , kN/m 3 )    |             18 | 24,85      | 27,85            | 22,35            |
| Söğüt Metamorfitleri (Ofiyolit)                | Tek eksenli basınç dayanımı (σ c, MPa) |             14 | 22,21      | 33,85            | 17,36            |
| Söğüt Metamorfitleri (Ofiyolit)                | Elastisite modülü (E, GPa)             |             14 | 5,76       | 11,12            | 2,68             |
| Söğüt Metamorfitleri (Ofiyolit)                | Poisson oranı (υ)                      |             14 | 0,25       | 0,33             | 0,23             |
| Felsik İntrizüf                                | Birim hacim ağırlık (γ n , kN/m 3 )    |             31 | 24,36      | 25,04            | 21,61            |
| Felsik İntrizüf                                | Tek eksenli basınç dayanımı (σ c, MPa) |             30 | 27         | 51               | 12,3             |
| Felsik İntrizüf                                | Elastisite modülü (E, GPa)             |             20 | 5,4        | 10,5             | 3,05             |
| Felsik İntrizüf                                | Poisson oranı (υ)                      |             20 | 0,22       | 0,27             | 0,18             |

## 2.3. Tünel Tip Kesiti ve Özellikleri

Çalışmanın yapıldığı 26 numaralı tünelin imalatında mekanize kazı yöntemi kullanılmaktadır. Bu amaçla 13,77 m  çapında  tam  dairesel  Tünel  Açma  Makinesi  (TBM)  kullanılmaktadır  (Şekil  4).  Sert  kaya  TBM'i  olarak nitelenen makine tek kalkanlı olup, miks (sert-yumuşak) kafa dizaynına sahiptir. Tünelde kazıyı takiben 45 cm kalınlığa 2 m. genişliğe sahip 8 adet prekast döşenerek bir kazı adımı tamamlanmaktadır. Tünel iç çapı 12,50 m. olup, ray üst kotundan itibaren 8,00 m. yüksekliğe sahiptir.

Şekil 4. Kullanılmakta olan tünel açma makinesi ve tünel tip kesiti

<!-- image -->

Photograph

<!-- image -->

Engineering drawing

## 2.4. 26 Numaralı Tünel için Altyapı Güvenlik Önerileri

Yüksek  hızlı  demiryolu  (250-350  km/saat)  işletmeciliğinde  tünel  güvenliğinin  proje  dizayn  aşamasında tasarlanması  gerekmektedir.  Her  tünel  için  risk  analizi  yapılarak  uzunluk,  coğrafik  ve  iklim  koşulları,  erişim kolaylığı (karayoluna erişim mesafesi) gibi veriler değerlendirilerek güvenlik modelleri geliştirilmelidir.

YÜKSEK  HIZLI  DEMİRYOLU  TÜNELLERİNDE  GÜVENLİK  TÜNELİ  MODELLEMELERİ:  ANKARAİSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

Halen  işletmecilik  faaliyetlerinin  yürütüldüğü  Ankara-İstanbul  yüksek  hızlı  tren  koridorunda  bulunan  26 numaralı  tünel,  güzergah  özellikleri,  tünel  çapı  ve  tünel  uzunluğu  açısından  ülkemizdeki  en  önemli  ulaşım tünellerinden biridir. 6100 m. uzunluğundaki tünelin devamında yer alan aç-kapa yapısı ile birlikte tünel, 7096 m. olacaktır. Bu nedenle söz konusu tüneller alt yapı güvenlik önlemleri açısından birlikte değerlendirilmiştir. Bu amaçla 26 numaralı tünel için maliyet, süre ve uygulama kolaylıkları da göz önünde bulundurularak üç farklı güvenlik modeli geliştirilmiştir. Geliştirilen modellerden ray altı kaçış modelinin uygulanabilirliğinin değerlendirilmesi amacı ile Pahase V.8 yazılımı kullanılarak analiz yapılmıştır.

## 2.4.1. Paralel Tünel

Paralel tünel, ana tünele paralel olarak yapılan ve en fazla 1000 m'de bir ana tünelle bağlantısı olan tünellerdir. Bu tür uygulamalar, tünel altyapı güvenliği açısından Diamantidis ve ark. [4] tarafından %80 riskli tünel olarak değerlendirilmektedir (Şekil 5).

Şekil 5. Çift hat tren tünellerinde risk oranı [4]

26  numaralı  tünel  için  önerilen  paralel  tünellerde  acil  durum  müdahaleleri  sırasında  araç  kullanımı  da düşünülerek tünel genişliği 2,25 metre, yüksekliği de 2,25 m. olarak değerlendirmeye alınmıştır. Paralel tüneller ana  tünel girişinden  2014  metre,  çıkışından  ise  3043  metre  ilerletilmiştir.  Bunun nedeni, tünelin giriş bölgesindeki yerel kaya koşullarının çıkış bölgesine oranla daha zayıf olmasından kaynaklanmıştır. 26 numaralı tünel için önerilen paralel tünel modeli ve tünel kesiti, Şekil 6'de sunulmuştur.

Şekil 6. Paralel tünel modelinin uygulama şeması.

<!-- image -->

Engineering drawing

Önerilen paralel tünel uygulaması 5057 metre imalat içermektedir. Bu imalatın ise 755 gün civarında süreceği hesaplanmıştır.  Tünel  imalatı  sırasında  karşılaşılabilecek  olumsuzluklar  (kazı  destek  sınıfındaki  değişiklikler, aşırı  sökülmeler,  deformasyonlar  vb.)  hesaba  katılmadan  yapılan  hesaplamalarda  maliyetinin  8,7  milyon  € olacağı öngörülmektedir. Önerilen paralel tünel modelinde tahliye noktalarında 500 m 2 emniyet alanı bulunmakta ve bu hali ile ek kamulaştırma ve düzenleme maliyeti de içermektedir.

## 2.4.2. Yaklaşım Tüneli ve Güvenlik Bacası

Yüksek  hızlı  tren  tünellerinde  alt  yapı  emniyet  önlemleri  olarak  başvurulan  bir  diğer  yöntem  de  yaklaşım tünelleri  ve  kaçış  bacalarıdır.  26  numaralı  tünel  için  geliştirilen  bu  modelde  7  adet  yaklaşım  tüneli  ve  6  adet güvenlik noktası önerilmiştir (Şekil 7). Ayrıca acil durum müdahaleleri sırasında araç kullanımı da düşünülerek yaklaşım tünellerinin genişliği 2,25 m. yüksekliği de 2,25 m. olarak değerlendirmeye alınmıştır.

Şekil 7. Yaklaşım tüneli modelinin uygulama şeması

<!-- image -->

Engineering drawing

Bu tünellerin toplam uzunluğu 2296 metredir. Bölgedeki tünel açma tecrübelerine dayanarak tünellerinde aynı anda  çalışıldığı  varsayımı  ile  imalatların  kaplama  betonu  ile  birlikte  en  az  360  gün  içerisinde  tamamlanacağı öngörülmüştür. Yaklaşım tüneli ve kaçış bacası uygulamaları için ek kamulaştırma maliyetleri söz konusudur. Tünellerin emniyet alanları ve ek kamulaştırma bedelleri ile birlikte maliyetinin 5,1 milyon € civarında olacağı hesaplanmıştır.

## 2.4.3. Ray Altı Güvenlik Tüneli

Bu  çalışma  ile  geliştirilen  bu  model,  rayların  altında,  tüneli  boydan  boya  kat  edecek  şekilde  bir  tünelin oluşturulması esasına dayanmaktadır (Şekil 8a). Modelde ana tünelden kaçış tüneline kadar her bin metrede bir bağlantı sağlanması öngörülmektedir (Şekil 8b).

Şekil 8. Önerilen ray altı emniyet tünel kesitleri (a-ray altı emniyet tüneli, b-ana tünelray altı emniyet tüneli bağlantı kesiti)

<!-- image -->

Engineering drawing

Ray altı kaçış tünelinde önceden hazırlanan yapılar birleştirilerek ray altı tünelin imalatının tamamlanabileceği düşünülmektedir.  Bu  yöntemin  uygulanması  sonucunda  tünelin  tamamlanmasını  ancak  130  gün  öteleyeceği öngörülmektedir.  Ek  kamulaştırma  bedeli  de  bulunmayan  ray  altı  güvenlik  tünelinin  ek  olarak  1,3  milyon  € maliyet ile tamamlanabileceği hesaplanmıştır.

YÜKSEK  HIZLI  DEMİRYOLU  TÜNELLERİNDE  GÜVENLİK  TÜNELİ  MODELLEMELERİ:  ANKARAİSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

## 3. BULGULAR VE TARTIŞMA

Üzerinde ayrıntılı olarak çalışılan toplam 7097 m. uzunluğundaki tünel için geliştirilen 3 farklı tünel altyapı emniyet  modeli,  uzunluk,  tamamlanma  süresi  ve  maliyet  durumlarına  göre  değerlendirilmiş  olup,  bu  durum Tablo 2'de özetlenmiştir.

Tablo 2. 26 numaralı tünel için alt yapı güvenlik modellerinin karşılaştırması

| Güvenlik Modeli                    |   Uzunluk (m) |   Tamamlanma Süresi (gün) | Maliyet (milyon €)   |
|------------------------------------|---------------|---------------------------|----------------------|
| Paralel tünel                      |          5057 |                       755 | 8,7                  |
| Yaklaşım tüneli ve güvenlik bacası |          2296 |                       360 | 5,1                  |
| Ray altı tüneli                    |          6100 |                       130 | 1,3                  |

26 numaralı tünel için alt yapı güvenlik önlemleri kapsamında ayrıntılı olarak değerlendirilen modellerden ray altı tünel uygulamasının en kısa sürede ve en az maliyetle uygulanabileceği tablodan da anlaşılmaktadır. Ancak her ne kadar bu model uluslararası standartları [17, 18] sağlasa da daha önce uygulanmamış olması, gerek imalat gerekse  yoğun  işletmecilik  faaliyetlerini  de  düşünüldüğünde  sorunsuz  uygulanabilirliği  tartışma  konusudur. Modelin uygulanabilirliğinin araştırılması amacı ile 2 boyutlu sonlu elemanlar yöntemi analiz yapan Rocscience Phase 2 V. 8.0 [19] programından yararlanılmıştır (Şekil 9).

Analizler sırasında (ana tünel kazısı ve sonrasında farklı stabilite problemlerinin oluşacağı öngörüldüğünden) ana tünel stabil olarak kabul edilmiştir. Bu amaçla ana tünelin Söğüt Metamorfitlerinde (metapellit) sağlam kaya koşullarında  açıldığı  varsayılarak  girdi  parametreleri  seçilmiştir.  Buna  göre,  yapılan  değerlendirmede  kaya kütlesinin GSI [20] değeri 28 ila 38 aralığında yer almaktadır ve ortalama 32 olarak tespit edilmiştir. Bunun yanı sıra,  kaya  malzemesi sabiti (mi) 10 olarak alınmıştır. Grafitşistlerde kazı  yöntemi olarak tünel açma  makinesi uygulanacağı  için  örselenme  faktörü  (D)  sıfır  kabul  edilmiştir.  Nümerik  analizlerde  kullanılacak  parametreler RocLab v1.032 [21] programından yararlanılarak analizin yapılacağı bölgede bulunan 100 metrelik örtü yükü baz alınarak belirlenmiştir. Hoek ve Diederichs [22] tarafından önerilen deformasyon modülü (Em) kullanılmıştır. Ayrıca Hoek ve ark. [23] tarafından önerilen yenilme kriterinden de yararlanılmıştır. Analizlerde kullanılan kaya parametreleri Tablo 3'te özetlenmiştir.

Buna ek olarak 26 nolu tünel güzergâhı,  Afet İşleri Genel Müdürlüğü 'Türkiye Deprem Bölgeleri Haritası' değerlendirmelerine göre 2. derece deprem bölgesinde yer almaktadır ve bölgede beklenen ivme değeri ise 0,300,40  g  arasındadır.  Bu  nedenle,  analiz  modellerine  yatay  yer  ivmesi  0,40  g  olacak  şekilde  ek  sismik  yük eklenerek deprem etkisi de dikkate alınmıştır.

Tablo 3. Sayısal analizde kullanılan kaya malzemesi özellikleri

| Kaya Özellikleri                       | Değerler   |
|----------------------------------------|------------|
| Kohezyon, C (MPa)                      | 0,350      |
| Tek eksenli basınç dayanımı, σ c (MPa) | 34,56      |
| Elastisite modülü, E (MPa)             | 4030       |
| Deformasyon modülü, E m (MPa)          | 373,71     |
| İçsel sürtünme açısı, ɸ (°)            | 40,74      |
| Birim hacim ağırlık, γ n (kN/m 3 )     | 25,47      |
| Kaya malzemesi sabiti, m i             | 10         |
| Kaya kütle sabiti, m b                 | 0,882      |
| Kaya kütle sabiti, s                   | 0,0005     |
| Kaya kütle sabiti, a                   | 0,520      |
| Örselenme faktörü, D                   | 0          |
| Jeolojik dayanım indeksi, GSI          | 32         |
| Poisson oranı, ʋ                       | 0,26       |

Ayrıca  analizlerde  kullanılan  iç  kaplama  ve  güvenlik  tüneli  elemanlarına  ait  parametreler  de  Tablo  4'te özetlenmiştir.

Modelleme aşamasında 5 temel adım göz önünde bulundurulmuştur. Bunlar:

1. Aşama: yerinde gerilmelerin yerleştirilmesi,
2. Aşama: güvenlik tünelinin ve dolgunun imalatı

## E. POŞLUK, M. KORKANÇ

3. Aşama: grobeton ve ray elemanlarının yerleştirilmesi
4. Aşama: yayılı yükün yerleştirilmesi (trenlerin yerleştirilmesi)
5. Aşama: 0,4 g yatay deprem yer ivmesinin yerleştirilmesidir.

Tablo 4. Phase analizi için kullanılan parametreler

| Malzeme Cinsi            |   Elastisite Modülü (MPa) | Poisson Oranı   |   Basınç Dayanımı (MPa) | Çekme Dayanımı (MPa)   | Literatür                                   |
|--------------------------|---------------------------|-----------------|-------------------------|------------------------|---------------------------------------------|
| Güvenlik tüneli (C25/30) |                     30000 | 0,2             |                      25 | 1,8                    | [24]                                        |
| İç kaplama (C30/37)      |                     32000 | 0,2             |                      30 | 1,9                    | [24]                                        |
| Grobeton (C16/20)        |                     27000 | 0,2             |                      16 | 1,4                    | [24]                                        |
| Dolgu malzemesi          |                     26150 | 0,2             |                      14 | 1,3                    | Bu çalışmada kabul edilen dolgu özellikleri |

Yapılan analizlerde toplam yer değiştirme değerleri ve eksenel gerilmeler Şekil 9.'de gösterilmiştir. Analizler değerlendirildiğinde depremli durumda güvenlik tünelinde maksimum yer değiştirmenin 0,4 - 0,6 mm. civarında olduğu görülmektedir. Bu  da güvenlik tünelinin uygulama  sırasında sorunsuz olarak kullanabileceğini göstermektedir. Ancak sayısal analiz çıktılarında özellikle eksenel gerilmelere bakıldığında (Şekil 9e) güvenlik tünelinde  gerilmelerin  arttığı  görülmektedir.  Özellikle  iki  trenin  aynı  anda  geçtiği  koşullarda  rotasyonel gerilmelerin  lineer  gerilmelere  göre  daha  fazla  arttığı  görülmektedir.  Bu  da  uygulama  sırasında  ek  tedbirlerin alınması gerektiğini, özellikle ray altı elemanlarının daha rijit bir hale getirilmesi gerektiğini düşündürmektedir. Bununla  birlikte  gerek  maliyet,  gerek  uygulama  süresi  gerekse  de  uygulama  kolaylığı  açısından  önerilen  ve uygulanabilir olduğu düşünülen ray altı kaçış modelinin benzer projelerde ana tünel imalatına başlamadan önce düşünülmesi  gerekmektedir.  Çünkü  uygulama  sırasında  benzer  emniyet  tedbirlerinin  tasarlanması  ana  tünel tasarımın omurgasını değiştirmekte ve projelere ek yükler getirmektedir.

Şekil  9. Phase  analiz  sonuçları  (a-  güvenlik  tüneli  ve  dolgu  imalatı  sonrası toplam  yer  değiştirme,  b-  Grobeton  ve  ray  elemanlarının  yerleştirilmesi sonrası toplam yer değiştirme, c- Yayılı yük (22,5 ton/dingil) sonrası toplam yer  değiştirme,  d-  0,4  g.  deprem  ivmesi  sonrası  toplam  yer  değiştirme,  egüvenlik tüneli ve civarı eksenel gerilmeler)

<!-- image -->

Engineering drawing

YÜKSEK  HIZLI  DEMİRYOLU  TÜNELLERİNDE  GÜVENLİK  TÜNELİ  MODELLEMELERİ:  ANKARAİSTANBUL HIZLI TREN PROJESİ 26 NUMARALI TÜNEL ÖRNEĞİ

## 4. SONUÇLAR

7097 m. uzunluğundaki 26 numaralı tünelde 3 farklı tünel altyapı emniyet modeli, uzunluk, tamamlanma süresi ve  maliyet  durumları  göz  önüne  alınarak  yapılan  değerlendirmelerde,  ray  altı  ekipmanların  rijit  seçilmesi kaydıyla uygulanması en ekonomik, hızlı ve uygulanabilir altyapı tünel güvenlik önerisinin ray altı kaçış tüneli olduğu sonucuna varılmıştır.

## TEŞEKKÜR

Bu çalışma, 26 numaralı tünelin altyapı güvenlik sorununa çözüm getirebilmesi amacıyla yapılmıştır. Yazarlar çalışmaları sırasında desteklerinden dolayı TCDD  yetkililerine, çalışma alanın jeolojisi konusundaki önerilerinden dolayı da Prof. Dr. Okan Tüysüz ile Arş. Gör. Elif Apaydın POŞLUK'a teşekkürlerini sunarlar. Ayrıca çalışmanın son haline gelmesinde katkı, görüş ve önerilerinden dolayı yayını inceleyen hakemlere sonsuz teşekkürlerini sunarlar.

## KAYNAKLAR

- [1] POŞLUK,  E.,  ERTİN,  A.,  KORKANÇ  M.,  PİLATİN,  R.Y.,  ARICA,  E.,  'Ankara-İstanbul  Hızlı  Tren Projesi  2.  Etap  26  Nolu  Tünelin  TBM  Kazı  Performansının  QTBM  Metodu  ile  Tahmini',  KAYAMEK 2011- X. Bölgesel Kaya Mekaniği Sempozyumu, 8-9 Aralık 2011, s:20-30, Ankara, Türkiye, 2011.
- [2] KRAUSMANN, E., MUSHTAG, F., 'Analysis of Tunnel-Accident Data and Recommendations for Data Collection and Accident Investigation', EU SafeT Project D4.5 Report, Turin, 7-20, 2005.
- [3] AMUNDSEN, F.H., MELVEAR, P., RONES, P., 'Studies on Norwegian Road Tunnels, an Analysis of Traffic Accident and Car Fires in Road Tunnels', Norwegian Public Roads Administration TTS 15 Report, Oslo, 14-16, 1997.
- [4] DIAMANTIDIS,  D.,  ZUCCARELLI,  F.,  WESTHAUSER,  A.,  'Safety  Of  Long  Railway  Tunnels', Reliability Engineering and System Safety, 135-145, 2000.
- [5] ESKESEN,  S.D.,  TENGBORG,  P.,  KAMPMANN,  J.,  VEICHERTS,  T.H.,  'Guidelines  for  Tunnelling Risk Management:  International Tunnelling Association', Working  Group  No.  2,  Tunnelling  and Underground Space Technology 19 217-237 (ITA/AITES Accredited Material)., 2004.
- [6] TÜYSÜZ, O., GENÇ, Ş. C., 'TCDD Ankara-İstanbul Hızlı Tren Projesi Vezirhan-İnönü Etabı T26 Tünel Güzergahının Jeolojisi Raporu', Avrasya Yer Bilimleri Ensditüsü, İTÜ, İstanbul, 2012.
- [7] ŞENTÜRK,  K.,  KARAKÖSE,  C.,  'Orta  Sakarya  Bölgesinde  Liyas  Öncesi  Ofiyolitlerinin  ve  Mavi Şistlerinin Oluşumu ve Yerleşmesi', Türkiye Jeoloji Kur. Bült., 24-1,1-11, 1981.
- [8] YILMAZ,  Y.,  'Söğüt-Bilecik  Bölgesinde  Polimetamorfizma  ve  Bunların  Jeoteknik  Anlamı',  Türkiye Jeoloji Kur. Bül, 22-1, 85-100, 1979.
- [9] MONOD, O., OKAY, A.I., 'Late Triassic Paleo-Tethyan subduction: Evidence from Triassic blueschists in NW Turkey',  Tenth  Meeting  of  the  European  Union  of  Geosciences  (EUG  10),  28.3.1999-  1.4.1999, Strasbourg. Journal Conference Abstracts, 4, p. 315, 1999.
- [10] INTERNATIONAL  SOCIETY  FOR  ROCK  MECHANICS  (ISRM),  'The  Complete  ISRM  Suggested Methods for Rock Characterization. Testing and Monitoring: 1974-2006', Suggeste Methods prepared by the Commission on Testing Methods, ISRM, R. Ulusay and .A. Hudson (eds.), Kozan Ofset, Ankara, 628 p, 2007.
- [11] ERGUVANLI, K., Mühendislik Jeolojisi, İTÜ Gümüşsuyu Matbaası, İstanbul, Türkiye, 1975.
- [12] NORWEGIAN GROUP FOR ROCK MECHANICS (NBG) Engineering Geology and Rock Engineering. Handbook No. 2, 1985.
- [13] DEERE,  D.U.,  MILLER,  R.P.,  'Engineering  Classification  And  Index  Properties  For  Intact  Rock', Technical Report No. AFWL-TR-65-116, Air Force Weapons Lab., Kirtland Air force Base, 308 pp, 1966.
- [14] YÜKSEL  PROJE  ULUSLARARASI  A.Ş.,  'Ankara-İstanbul  Hızlı  Tren  Projesi  (Köseköy-İnönü)  Proje Raporu', 2004.
- [15] JEMAS,  'Ankara-İstanbul  Hızlı  Tren  Projesi  (II.  Etap)  Vezirhan-İnönü  (II.  Kısım)  Tünel  -  26  Sondaj Raporu', 2010.
- [16] AKADEMİ, 'Ankara-İstanbul Hızlı Tren Projesi (2.Etap) Vezirhan-İnönü (Kesim 2); İşleri Kapsamında DT-26 Tüneline Sondaj Yapılması İşi Sondaj Raporu', 2013.
- [17] UIC Code 779-9, 'Safety in Railway Tunnels', 2003.

## E. POŞLUK, M. KORKANÇ

- [18] TSI,  2008/163/EC  'Concerning  the  Technical  Specification  of  Interoperability  Relating  to  Safety  in Railway Tunnels in the Trans-European Conventional and High-Speed Rail System', 2008.
- [19] ROCSCIENCE, 'Phase2  V  8.0  Finite  Element  Analysis  for  Excavations  and  Slopes',  Rocscience  Inc., Toronto, Ontario, Canada, 2010.
- [20] MARINOS, P., HOEK, E., 'GSI: A Geologically Friendly Tool for Rock Mass Strength Estimation', Proceedings  of  the  GeoEng2000  at  the  international  conference  on  geotechnical  and  geological engineering, Melbourne, Australia, 2000.
- [21] ROCSCIENCE, Roclab v1.032 Rock Mass Strength Analysis Using the Generalized HoekBrown Failure Criterion, Rocscience Inc., Toronto, Ontario, Canada, 2011.
- [22] HOEK, E., DIEDERICHS, M.S., 'Empirical Estimation of Rock Mass Modulus', International Journal of Rock Mechanics and Mining Science, 43, 203-215, 2006.
- [23] HOEK,  E.,  CARRANZA-TORRES,  C.,  CORKUM,  B.,  'Hoek-Brown  Failure  Criterion  2002  Edition', Proceedings of the NARMS-TAC 2002, Mining Innovation and Technology, Toronto, Canada, 267-273, 2002.
- [24] TÜRK  STANDARTLARI  ENSTİTÜSÜ,  'TS  500-Betonarme  Yapıların  Tasarım  ve  Yapım  Kuralları', 2000.
<!-- image -->

Icon

Isı Bilimi ve Tekniği Dergisi, 40, 2, 319-334, 2020 J. of Thermal Science and Technology ©2020 TIBTD Printed in Turkey ISSN 1300-3615 https://doi.org/10.47480/isibted.817057

## UZUN BİR KARAYOLU TÜNELİNDE ACİL DURUM SİMÜLASYONU

## Nureddin DİNLER* ve Özkan KAÇAN**

*Gazi Üniversitesi Mühendislik Fakültesi Makina Mühendisliği Bölümü 06570 Maltepe, Ankara, ndinler@gazi.edu.tr, ORCID: 0000-0002-2872-9050 **Karayolları Genel Müdürlüğü, 06100 Çankaya, Ankara, okacan@kgm.gov.tr, ORCID: 0000-0002-3120-5995

(Geliş Tarihi: 22.05.2020, Kabul Tarihi: 30.09.2020)

Özet: Karayolu taşımacılığında coğrafi olarak aşılması güç olan bölgelerde tüneller hem kat edilecek yolu kısaltmakta hem de yakıt tasarrufu sağlamaktadır. Bir taşıtın tünel içerisinde yanması oluşabilecek en kötü senaryodur. Dünyada insanların hayatlarını kaybetmesi ile sonuçlanan büyük tünel yangınları olmuştur. Ülkemizde de Ovit, Kop ve Zigana tüneli gibi uzun karayolu tünelleri inşa edilmektedir. Bu çalışmada, uzun bir karayolu tüneli (14500 m) içerisindeki taşıt  yangını  (30  MW) için acil durum  modellemesi yapılmıştır. Acil durum için kritik nokta belirlenerek, 1000 m uzunluğunda  bölge  1/100  ölçeğinde  incelenmiştir.  Çalışmada  Ansys  Fluent  kullanılmıştır.  Türbülanslı  akış  şartları dikkate  alınmıştır.  Yangının  olduğu  bölgedeki  sıcaklık  dağılımı,  karbonmonoksit  (CO)  emisyon  dağılımı  ve  hız dağılımları  incelenmiştir.  Elde  edilen  sonuçlar  grafikler  halinde  verilmiş  ve  yorumlanmıştır.  Sıcaklık  değerleri incelendiğinde yangın bölgesinde ortalama sıcaklık değerlerinin ilk 30 m'de ortalama 400 K'in üzerinde belirlenmiştir CO emisyon değerlerinin ise atış şaftına kadar 400 ppm seviyelerinin altına düşmediği, özellikle ilk 50 m'de ortalama 1000 ppm'in üzerinde olduğu belirlenmiştir.

## Anahtar Kelimeler:

Karayolu tüneli, acil durum, havalandırma.

## EMERGENCY SIMULATION IN A LONG HIGHWAY TUNNEL

Abstract: In regions that are difficult to overcome geographically in road transport, tunnels both shorten the road to be covered and save fuel. It is the worst scenario that a vehicle can burn in a tunnel. There have been major tunnel fires in the world that have resulted in people's lives. In our country, long highway tunnels such as the Ovit, Kop and Zigana tunnels are being built. In this study, emergency modeling was carried out for vehicle fire (30 MW) in a long road tunnel (14.5 km). The critical point for the emergency was determined and the 1000 m long region was examined on a scale of 1/100. Ansys Fluent was used in the study. Turbulent flow conditions are taken into account. Temperature distribution,  carbon  monoxide (CO) emission distribution  and  velocity distributions in the region  where the  fire is located were examined. Results are given in graphs and interpreted. When the temperature values are examined, the average temperature values in the fire zone were obtained above 400 K in the first 30 m. It was obtained that the CO values did not fall below 400 ppm until the firing shaft, especially in the first 50 m, above 1000 ppm on average. Keywords: Road tunnel, emergency condition, ventilation.

## SEMBOLLER T Sıcaklık [K]

|     |                                           | T 0   | Ortam başlangıç sıcaklığı [  C]         |
|-----|-------------------------------------------|-------|------------------------------------------|
| A   | Tünel kesit alanı [m 2 ]                  | T f   | Yangın sıcaklığı [  C]                  |
| C p | Karışımın öz ısısı [kJ/kg  C]            | t     | Zaman [s]                                |
| D h | Tünel hidrolik çapı [m]                   | V     | Tünel içi hava hızı [m/s]                |
| D * | Yangın karakteristik çapı [m]             | V c   | Kritik hız [m/s]                         |
| Fr  | Froude sayısı [=V/ √𝑔𝐿]                   |      | Genel değişken                           |
| g   | Yer çekimi ivmesi [m/s 2 ]                | µ     | Dinamik viskozite değeri [kg/ms]         |
| H   | Tünel yüksekliği [m]                      | Ɛ     | Türbülans yutulma oranı                  |
| K 1 | Froude sayısına bağlı katsayı [F r -1/3 ] | Γ     | Genel difüzyon katsayısı                 |
| k   | Türbülans kinetik enerjisi                | δ     | Bir özelliğin iki değeri arası fark      |
| L   | Karakteristik uzunluk [m]                 | θ     | Eğim                                     |
| m * | Kütlesel debi [kg/s]                      | ρ     | Hava yoğunluğu [kg/m 3 ]                 |
| P   | Tünel kesitinin çevre uzunluğu [m]        | ρ 0   | Ortam başlangıç hava yoğunluğu [kg/m 3 ] |
| p   | Basınç [Pa]                               | EPC   | Avrupa Parlamentosu ve Konseyi           |
| Q   | Yangın yükü [MW]                          | HAD   | Hesaplamalı Akışkanlar Dinamiği          |
| Q c | Taşınıma bağlı ısı salınımı [kW]          | KGM   | Karayolları Genel Müdürlüğü              |
| Q * | Boyutsuz ısı salınım oranı                | PIARC | Dünya Yol Birliği                        |

## GİRİŞ

Ulaştırmanın güç olduğu coğrafi engellerin aşılmasında karayolu tünelleri ulaşımı kolaylaştırmaktadır. Bu tüneller, ulaşımı kolaylaştırırken bölgeler arası ilişkileri geliştirmede izole gözüken bölgelerin ekonomik gelişiminde  de  bir  katalizör  olarak  kullanılmaktadır. Günümüzde, insanlığa birçok katkı sağlayan bu tünellerin yukarıda belirtilen iyi yönlerinin dışında tünel içerisindeki olası bir kaza ve kaza sonrasında oluşabilecek sıkıntılar oldukça ciddi boyutlara ulaşabilmektedir. Bu kazaların açık karayolundaki benzer  kazalara  göre  sıklığı  az  olmakla  birlikte  sahip oldukları etki oldukça yüksek olabilmekte ve bu nedenle medyanın ve halkın ilgisini daha çok çekmektedir.

Dünya  çapında  yaşanmış  olan  ve  yaşanan  en  ciddi karayolu tüneli kazası olarak anılan 1999 yılında meydana gelen Mont Blanc (Fransa) Tüneli felaketidir. 11,6 km uzunluğundaki tünelde bir kamyonda başlayan yangın, 23 tır ve 10 arabaya yayılarak 39 kişinin hayatını kaybetmesine  sebep  olmuştur.  Tünel  uzun  yıllar  önce tasarlandığından, tünel güvenlik ekipmanlarının ve acil durum senaryolarının yetersizliğinden kaynaklı tespitler uzun süre dile getirilmiştir. Aynı yıl gerçekleşen bir diğer kaza olan Tauern Tüneli felaketinde ise, bakım nedeniyle tünel trafiği tek şeritten sağlanırken, bir kamyon bekleme kuyruğuna  hızla  çarpmış,  zincirleme  kazalar  meydana gelmiş, yangın saç spreyi de içeren çeşitli malları taşıyan başka bir  kamyonun  da  alev  almasıyla yayılmıştır. Yangını  söndürmek  yaklaşık  16  saat  sürmüştür.  2  yıl sonra gerçekleşen (2001) Gotthard Tüneli kazasında ise, kontrolü  kaybedilen  bir  kamyon  karşı  şeride  geçmiş, tehlikeli madde taşıyan bir başka kamyona çarpmış ve 7 ağır yük  taşıtına yayılan  bir  tünel  yangınına  sebep olmuştur. Yangın sonucunda 11 kişi hayatını kaybetmiştir  (PIARC,  2017).  Tüm  bu  kazaların  ortak özellikleri; tünellerin uzun (&gt; 6 km) ve tek tüp  halinde olmasıdır. Söz konusu kazalar doğrudan etkilerinin yanı sıra,  uzun  süre  tünellerin  kapalı  kalmaları  sebebiyle, alternatif  güzergâhlarda  trafik  sıkışıklığına  yol  açmış, buna bağlı kaza oranları yükselmiştir. Sadece Gotthard Tünelinin  kapanması  nedeniyle  İtalya  ekonomisi  2,5 milyar Euro zarara uğramıştır. Tüm Avrupa ekonomisine zararın 15 milyar Euro'yu bulduğu tahmin edilmektedir (EU Report, 2003). Yaşanan üzücü tünel yangınları, bu konuya olan ilgiyi daha da arttırmıştır.

Karayolu tünel yangını; yangının dinamik süreci (türbülans, yanma, radyasyon, vb.) ve tünelin geometrik düzeni  (tünel  geometrisi,  araç  geometrisi  ve  bunların düzeni gibi) arasındaki karşılıklı etkileşimler  nedeniyle çok karmaşık bir olgudur. Meydana gelen tünel yangınlarının nedenleri; aracın kendiliğinden tutuşmasına (yük, yakıt ve araç dâhil), araç çarpışmasına ve aşırı yüklü çarpışmalara (örneğin, ön arka çarpışma ve yan duvarla çarpışma) göre sınıflandırılabilir. Bu nedenlere bağlı yangınlar, tünel duvarının yanında, sağ / sol şeritte ya da yolun ortasında rastgele ateş dağılımını mümkün kılmaktadır. Yangının gelişimi, duman dağılımı ve tünel kaplamasındaki hasar, tüneldeki yangının yerine büyük  ölçüde  bağımlıdır.  Bu  sebeplere  bağlı  olarak karayolu tüneli  yangınlarında,  duman  hareketi  ve  tünel yangın  güvenliği  yönetiminin  anlaşılmasına  açık  bir ihtiyaç doğmuştur (Wang vd., 2017).

Karayolu  tünellerinde,  belirli  bir  yönde  duman  akışını sağlamak için havalandırma sistemleri kullanılmaktadır. Hava hızı çok düşük olduğunda, yangın dumanı iki yönlü olarak  yayılır.  Hava  hızı  yüksek  olduğunda  ise  atım yönünde  yangın  dumanı  hızla  yayılır  ve  tünelin  içini doldurur.  Her  iki  durumda,  yangın  kaynağına  yaklaşan itfaiyeciler için tehlikeli olabilir.

Boyuna havalandırma yapılan tünellerde, havalandırma hızının  kritik  hızdan  çok  yüksek  olduğu  durumlarda hava  akımının  alt  kısmında  katmanlaşma  sorunu  baş gösterebilmektedir. Bu sebeple geri akışın engellenmesini  sağlayacak  en  düşük  hızı  belirlemek amacıyla sınırlandırma hızı kavramı geliştirilmiştir (Wu ve Bakar, 2000). Li vd. (2010), gerçekleştirdiği model deneylerde sınırlandırma hızı tanımlanmıştır. Tünellerin çoğu,  duman  hareketini  önemli  ölçüde  etkileyebilecek bir eğime sahiptir. Atkinson ve Wu (1996), tünel eğimi ile  kritik  hız  arasındaki  etkileşimi  incelemek  için  düz zemin ile  %10'a kadar eğimli tünel modellerinde deneysel çalışmalar yürütmüşlerdir. Bu çalışmalar sonunda, düz bir tünelle eğimli bir tünel arasındaki kritik hızlar  arasında  ilişki  kurmuşlardır.  Hyun  vd.  (2009), yaptığı benzer bir çalışmada eğim ve kritik hız arasındaki ilişki önerilmiştir. Chow vd. (2015) ise aynı ilişkiyi farklı katsayı ile tanımlamışlardır. Bu çalışmaların  yanında,  tünel  içerisinde  taşıt  blokajının yangın üzerine etkisi ile ilgili incelemeler de yapılmıştır. Oka ve Atkinson (1995), blokaj etkisinin ısı yayma oranı üzerine  yaptığı  etkiyi  incelemişlerdir.  Bu  çalışmada, yangının tünel genişliğinin büyük kısmını işgal ettiği ve tavana doğru yükselerek arttığı, kritik hızların da azaldığı gözlemlenmiştir. Benzer şekilde yapılan diğer araştırmalarda  da  yangının  gerisinde  konumlandırılan araçların blokaj oranının artmasıyla kritik hızın azaldığı gösterilmiştir  (Li  vd.,  2010; Lee  and  Tsai,  2012;  Alva vd. 2017).  Hu vd. (2007) deneysel çalışmasında tünel içindeki duman  sıcaklığının değişimi incelenmiştir. Deneylerde  yangın  boyutu,  tünel  kat  yüksekliği,  tünel kesit geometrisi ve havalandırma hızı etkisi incelenmiştir. Duman hareket yönünde olan havalandırma  hızının  etkisi  ve  tünel  içindeki  bariyer etkisinin duman sıcaklığı ve hareketi üzerindeki etkileri de  çalışmada  araştırılmıştır.  Deneysel  sonuçlar,  tünel içinde taşıt hareketi olmadığı sürece yangın boyutundaki artışın  tünel  tavanındaki  duman  sıcaklığını  artırdığını göstermektedir.

Tünel yangınlarıyla ilgili bir diğer araştırma konusu da tünellerin  kesit  değişimlerinin  yangın  üzerine  etkisidir. Bu  çalışmaların  en  önemlilerinden  birisi  Kurioka  vd. (2003), tünel içerisinde çıkan bir yangının yakın bölgesindeki olayları analiz etmek için yaptıkları deneylerdir. Yaptıkları çalışmada 1/10, 1/2 ve tam ölçekli olmak üzere ve tam ölçekli modelde dikdörtgen ve at nalı kesitli olmak üzere modeller kullanmışlardır. Deneylerde kare kesitli yangın  kaynağı  kullanmışlardır.  En/boy oranı, açığa çıkan ısı miktarı ve uzunlamasına havalandırma hızı değiştirilmiştir. Alevin eğilmesi, görünür alev yüksekliği, duman tabakasının maksimum sıcaklığı ve konumu için ampirik formüller 1/10 ölçekli model tünel kullanılarak elde edilmiştir. Yangın kaynağının  yakınındaki  alanda  yangın  olayını  tahmin etmek için buldukları ampirik bağıntıların uygulanabilir olduğunu belirtmişlerdir. Lee ve Ryou (2005), benzer bir çalışmada aynı hidrolik çapa sahip tünel için en/boy oranı arttıkça kritik hızın arttığını tespit etmişlerdir. Vauquelin ve Wu (2006), ölçekli modeller üzerine yapılan deneysel çalışmalarında  tünel  genişliğinin  kritik  hız  üzerindeki etkisini  araştırmışlar  ve  tünel  kesitinin  en/boy  oranının düşük olduğu durumlarda, tünelin genişliği arttıkça kritik hızın arttığını tespit etmişlerdir.

Bu  çalışmaların  dışında,  Kashef  vd.  (2009),  iki  bölge (düz  ve  kavisli)  tarafından  oluşturulan  uzun  bir  yol tünelinde  30  MW'lık  bir  etkinlikte  duman  yayılmasını kontrol etmek  için farklı acil  durum  havalandırma stratejilerinin etkinliğini değerlendirmiştir. Sonuçlar, düz bölgedeki senaryolar durumunda geri tepmenin önlendiğini  veya  sınırlandırıldığını  göstermiştir.  Tam tersine,  kavisli  bölgede  yer  aldığında,  temiz  hava  ile yanma ürünleri arasında iyi bir karıştırma gerçekleştiği görülmüştür. Bu karıştırma prosesi, düz zonda gerilemeye  neden  olmuş  ve  düz  bölgede  geriye  doğru uzanarak,  geri  tepme  derecesini  arttırmıştır.  Çalışma sonucunda kavisli bölgedeki duman geri tepmesini en aza indirmek  için,  kavisli  bölge  boyunca  tavan  jet  fanları kurmak önemi vurgulanmıştır. Benzer şekilde, Caliendo vd. (2012), kavisli tünellerde yangın etkisini incelemiş, tünelin tam ortasında meydana gelen bir otobüs yangınını simüle ederek, 3 m/s kritik  havalandırma  hızı için  geri tepmenin önlendiğini göstermiştir. Karaaslan vd. (2011), at nalı kesitli bir tünelin ölçek modeli üzerinde yaptıkları tünel  yangını  çalışmasında  duman  hareketini  incelemiş ve dumanın kontrolü için fan çalışma sırasının, fan itiş gücünün  ve  havalandırmaya  başlama  zamanının  tünel yangınları üzerindeki önemini vurgulamışlardır.

Literatür  çalışmalarında,  giriş  bölümünde  bahsedildiği üzere karayolu tünel yangınlarıyla ilgili; kritik hız kavramı, geri katmanlaşma, maksimum duman sıcaklığı, tünel içerisindeki araçların blokaj etkileri, tünel kesitinin etkileri  (en,  boy,  hidrolik  çap,  kavis  vb.),  yanan  araç türünün  etkileri,  atmosferik  koşulların  etkisi  ve  son zamanlarda da yangın önleme sistemlerinin etkinliği (su sisi ve sulu yangın önleme sistemleri vb.) üzerine bir çok çalışma yapılmıştır.  Bu çalışmada 14500 metrelik uzun bir  karayolu  tünelindeki  tünel  iç  kesiminde  acil  durum olarak 30 MW gücünde yangın modellemesi yapılmıştır. İncelenen 1000 metrelik kesiminde, 1/100 ölçek model kullanılarak,  tünel  geometrisi,  araçlar,  tahliye  noktaları ve jet fanlar modellenmiştir.

## PROBLEMİN TANIMI

Karayolu tünellerinde gerçek boyutta bir yangın düzeneği kurularak tünel içerisindeki yangına bağlı türbülans, sıcaklık değişimi, hava hızı değişimi, duman emisyonları, görüş mesafesi gibi parametreleri incelemek en  doğru  verileri  sağlayabilir.  Ancak,  bu  düzeneklerin kurulumları hem süre hem maliyet yönünden olanaksızdır. Günümüzde HAD (Hesaplamalı Akışkanlar Dinamiği) yazılımları sayesinde tam ölçekli ya da küçük ölçekli çalışmalara göre çok daha düşük maliyette, diğer yöntemlerle erişilmesi çok zor olan birçok ayrıntılı veri elde edilerek daha etkin değerlendirme yapılabilmektedir (Caliendo vd., 2012).

Bu çalışmada, ölçek  model  yaklaşımı ve  Ansys Fluent yazılımı ile süreklilik, momentum, enerji ve tür denklemleri çözülerek türbülans, yanma, yüzdürme gibi karmaşık  süreçler  tanımlanmış,  yangın  sonucu  oluşan dumanın  gaz sıcaklığı, hava akış hızı, zehirli gaz konsantrasyonları,  tünelde  görüş  mesafesi,  insanların tahliye  işlemleri  gibi  süreçlerle  ilgili  değerlendirmeler yapılmış  ve  analitik  olarak  tek  boyutlu  denklemler  ile başlangıç hesapları yapılmıştır.

14500 m uzunluğunda çift tüp bulunan tünel, Karayolları Genel  Müdürlüğü  (KGM)  Teknik  Şartnamesine  göre devlet  ve  il  yolları  standardına  uygun  olarak  2  şeritli yapılmaktadır (KGM, 1997). Tünelin havalandırma sistemi, trafikle aynı yönde çalışacak şekilde tasarlanmıştır. Tünelin bulunduğu konum ve uzunluğu ile 'EPC'nin  2004/54/EC  sayılı  direktifi'  ve  'Karayolları Teknik  Şartnamesi'  göz  önünde  bulundurularak  klasik boyuna  havalandırma  sisteminin  seçilmesi  bu  tünel  için uygun görülmemiştir (EPC, 2004; KGM, 1997).

Yapısal maliyetleri (gabarinin büyümesi ve kanal maliyetleri) ve işletme zorlukları dolayısıyla yarı enine ve  enine  havalandırma  sistemlerinin  yerine,  çok  uzun tünellerde  kullanılan  ve  diğer  sistemlere  göre  maliyeti daha uygun olan bölünmüş boyuna havalandırma sistemi tercih  edilmiştir  ve  havalandırma  sistemine  ait  şematik gösterimi Şekil 1'de verilmiştir.

Şekil 1. Havalandırma sistemi şematik gösterimi.

<!-- image -->

Bar chart

Tünelde  havalandırma  amaçlı  3  adet  ana  şaft  yapısı bulunmaktadır. Eksenel fanların bulunduğu her ana şaft yapısı içerisinde birbirinden 50 m mesafe aralıklı sırasıyla 1 kirli hava kanalı ve 1 temiz hava kanalı şaftı bulunmaktadır (Şekil 2). Bu temiz ve kirli hava şaftları her iki tüpe de bağlanmaktadır. Bu sistemde jet fanlar ve eksenel fanlar beraber kullanılmaktadır.

Şekil 2 . Şaftların şematik gösterimi.

<!-- image -->

Engineering drawing

## Tünelin Yapısal Özellikleri

Tünele ait fiziksel özellikler Tablo 1'de verilmiştir. Tünelde eğim yer yer değişmekle beraber, büyük kısımlar çatı  eğimli  +0,85  ila  -3,30  ve  +3,30  ila  -0,85  şeklinde değişmektedir. Hesaplamalarda eğime göre bölümler ayrı ayrı yapılmış olup bu bölümler Şekil 3'te gösterilmiştir.

Tablo 1. Tünele ait fiziksel özellikler.

| Hesaplarda Kullanılan Parametreler   | Doğu Tüpü Değerleri   |
|--------------------------------------|-----------------------|
| Tünel uzunluğu                       | 14 500 m              |
| Tünel boyuna eğimi                   | Çatı eğim             |
| Tünel kesit alanı                    | 67 m 2                |
| Tünel yüksekliği                     | 7,3 m                 |
| Tünel çevresi                        | 31,16 m               |
| Tünel hidrolik çapı                  | 8,6 m                 |
| Şerit sayısı                         | 2                     |
| Giriş portalı rakımı                 | 1014 m                |
| Çıkış portalı rakımı                 | 1210 m                |

Şekil 3. Hesap yapılan bölümlerin şematik gösterimi.

<!-- image -->

Engineering drawing

Tünele ait havalandırma hesapları için 2045 yılı tahmini trafik  dağılımı  referans  alınmıştır.  Tünelin  yapılacağı güzergâhta, KGM'den alınan 2045 yılı trafik tahminine göre hesaplanan saatlik trafik verileri Tablo 2'de verilmiştir. Hesaplamalarda, 2045 yılı trafik dağılımına göre, Tablo 3'te gösterilen,  günlük trafiğin %10 değeri olarak saatlik en yüksek trafik yükü alınmıştır.

Tablo 2. Trafik verileri.

|   Yıllar |   Otomobil |   Hafif Yüklü Ticari Taşıt |   Otobüs |   Kamyon |   Kamyon, Römork, Çekici, Yarı Römork |   Toplam |
|----------|------------|----------------------------|----------|----------|---------------------------------------|----------|
|     2015 |       3187 |                        254 |       65 |      528 |                                   382 |     4416 |
|     2016 |       6754 |                        342 |       87 |      663 |                                  1340 |     9186 |
|     2017 |      12095 |                        455 |      116 |      708 |                                  1816 |    15190 |
|     2018 |      21661 |                        555 |      141 |      715 |                                  2006 |    25078 |

Tablo 3. Hesaplamalara katılan saatlik en yüksek trafik yükü.

| Trafik Verileri              | Trafik Verileri   |
|------------------------------|-------------------|
| Trafik akış (tek/çift yönlü) | Tek yön           |
| Ağır vasıta                  | 286 araç/saat     |
| Orta yüklü ticari araç       | 56 araç/saat      |
| Otomobil                     | 2166 araç/saat    |

## Tünel Geometrisi ve Ölçek Model Kullanımı

Hesaplamalara  göre  kritik  nokta  olarak  bulunan  DT\_3 lokasyonu 11500 m'de (giriş portalından uzaklığı, % 3,3 eğimli kısım) meydana gelebilecek 30 MW'lık bir araç yangını, başlangıç noktası kabul edilmiş ve buna göre bir analiz çalışması yapılmıştır.

Şekil 4. Geometrik model.

<!-- image -->

Engineering drawing

Geometri,  yapının  fiziksel  geometrisini  termodinamik yönden  uygun  yansıtacak  boyutlarda  hazırlanmalıdır. Seçilen  senaryoda,  yangının  1000  metrelik  kesiminde, %3,3  eğimli,  1/100  ölçek  model  kullanılarak,  tünel geometrisi, araçlar, tahliye noktaları ve jet fanlar modellenmiştir (Şekil 4).

14500 metrelik tünelin geometrisinin tam ölçekte modellenmesi  hem  zor  hem  de  analiz  açısından  çok yüksek maliyetler gerektirmektedir. Bu nedenle, bu çalışmada  tüneldeki  yangına  bağlı  fiziksel  ve  kimyasal süreçleri  inceleyebilmek için  ölçek  model  kullanılmıştır. Literatürde  yapılan  çalışmalarda  farklı  ölçek  modeller olmakla beraber bu çalışmada, birçok yangın güvenliğiyle ilgili  bilimsel  çalışmada  kullanılan  Froude  ölçek  modeli tercih  edilmiştir  ve  kullanılan  korelasyonların  örnekleri Tablo 4'te verilmiştir (Lee ve Tsai, 2012; Alpgiray, 2016; Gong vd., 2016; Tang vd., 2017).

Tablo 5'te, tünel geometrik verileri, araçlar ve fanlara ait modelde kullanılan prototip modelin boyutları ve ölçek model karşılıkları verilmiştir.

## Temel  Sınır  Şartlarının  Belirlenmesi  ve  Ağ  Yapısı Seçimi

Yangın  yüküne  bağlı,  oluşacak  gaz  debisi  ve  emisyon dağılımını doğru tahmin edebilmek önemlidir. Bu çalışmada, tünelde tehlikeli madde taşımacılığı yapılmayacağı varsayılmıştır. Tehlikeli madde taşımacılığına bağlı yangınların dışında 30 MW'lık araç yangınlarını 25-50 tonluk ağır yük taşıtları yangınları ve bu  taşıtların  beraber  karıştığı  kazalar  oluşturmaktadır (PIARC,  2017:7).  Tablo  6'da  farklı ülkelerin tünel yangın yükü standartları verilmiştir. Tünelde tüp başına trafik  yükünün,  nispeten  küçük  olduğu  düşünülerek, birden  fazla  ağır  yük  taşıtının  çarpışması  ve  yangınına bağlı riskin düşük olması beklenmektedir. Tüm faktörler değerlendirilerek, havalandırma tasarımında yangın yükü 30 MW olarak alınmıştır.

Tablo 4. Froude ölçek model sisteminde kullanılan korelasyonlara örnekler (Ingason vd. 2015).

| Birim                  | Ölçek                                           |
|------------------------|-------------------------------------------------|
| Isı salınım oranı (kW) | Q M /Q F =(I M /I F ) 5/2                       |
| Hız (m/s)              | V M /V F =(I M /I F ) 1/2                       |
| Zaman (s)              | t M /t F =(I M /I F ) 1/2                       |
| Sıcaklık (K)           | T M /T F =1                                     |
| Gaz konsantrasyonu     | Y M /Y F =1                                     |
| Basınç (Pa)            | P M /P F =( I M /I F )                          |
| Yanma hızı (kg/(m 2 s) | (m' f δH c ) M /(m' f δH c ) F =(I M /I F ) 1/2 |
| Debi (kg/s)            | ρ w,M / ρ w,F =(I M /I F ) 5/2                  |

Tablo 5. Tünelin ve kullanılan ekipmanların 1/100 ölçek model boyutları.

| Tünelin ve Kullanılan Ekipmanların Geometrik Verileri   | Prototip Model   | 1/100 Ölçek Model     |
|---------------------------------------------------------|------------------|-----------------------|
| Hesap Yapılan Uzunluk (m)                               | 1000,00          | 10,00                 |
| Eğim (-)                                                | %3,30            | %3,30                 |
| Tünel Yüksekliği (H T ) (m)                             | 7,22             | 0,0722                |
| Tünel Hidrolik Çapı (D H ) (m)                          | 8,60             | 0,0086                |
| Şerit Sayısı (-)                                        | 2                | 2                     |
| Taze Hava Şaftı Ölçüleri (m 2 )                         | 10  5           | 0,1  0,05            |
| Egzoz Hava Şaftı Ölçüleri (m 2 )                        | 4,5  3          | 0,045  0,03          |
| Otomobil Ölçüleri (boy x en x yükseklik) (m 3 )         | 4,2  1,8  1,4  | 0,042  0,018  0,014 |
| Otobüs Ölçüleri (boy x en x yükseklik) (m 3 )           | 12  2,5  2,9   | 0,12  0,025  0,029  |
| Ağır Yük Taşıtı Ölçüleri (boy x en x yükseklik) (m 3 )  | 13  2,5  3,6   | 0,12  0,025  0,036  |
| Jet Fan Dış Çapı (m)                                    | 1,4              | 0,014                 |
| Jet Fan İç Çapı(m)                                      | 1,25             | 0,0125                |
| Jet Fan Uzunluk (m)                                     | 3,4              | 0,034                 |

Tünel yangınlarıyla ilgili kabul edilen yangın sıcaklık/zaman eğrilerine göre (Şekil 5) yangının yaklaşık 5 dakikada en yüksek sıcaklık değerine ulaşacağı kabul edilmiş ve oluşacak en yüksek sıcaklık, modifiye  edilmiş  hidrokarbon  eğrisi  referans  alınarak hesaplanmıştır.  Modifiye  edilmiş  hidrokarbon  eğrisine (HCM) göre, zamana bağlı sıcaklık farkı Denklem 1 ile hesaplanmaktadır (Taillefer vd., 2013).

<!-- formula-not-decoded -->

Denklem 1'de t, yangının başlangıcından itibaren dakika olarak geçen süreyi, δT oluşan sıcaklık farkını göstermektedir. Başlangıç tünel sıcaklığı 20 o C olduğundan en yüksek sıcaklık değeri 1120 o C (1393 K) olarak hesaplanmıştır.

Yangın  sonrası  oluşacak  duman  miktarını  ve  içeriğini belirlemek  için  'Runehamar  Tünel  Yangın  Testleri' sonuçlarından  faydalanılmıştır.  Bu  testlerde  66  ve  202 MW  aralığında dört farklı ağır yük taşıtı yangını incelenmiştir  (Li  ve  diğerleri,  2012).  Yangın  sonrası oluşacak duman miktarı (m*gaz), tüketilen yakıt miktarı (m*yakıt) ve tüketilen hava miktarının (m*hava) toplamına eşittir.

<!-- formula-not-decoded -->

Tablo 6. Bazı ülkelerin yangın tasarım yükleri (PIARC, 2017).

| Ülke      | Yangın Tasarım Yükü (MW)   | Açıklamalar                                               |
|-----------|----------------------------|-----------------------------------------------------------|
| Avusturya | 30                         | Yüksek risk kategorisinde 50 MW                           |
| Fransa    | 30-200                     | Tehlikeli madde taşımacılığı varsa 200 MW                 |
| Almanya   | 30-100                     | Tünel uzunluğu ve ağır yük taşıt sayısına göre değişiyor. |
| İtalya    | 20-200                     | Tehlikeli madde taşımacılığı varsa 200 MW                 |
| Japonya   | 30                         | Su sisi sistemiyle birlikte, havalandırma amaçlı          |
| Norveç    | 20-100                     | Risk sınıfına göre değişiyor.                             |
| Portekiz  | 10-100                     | Trafik yoğunluğu ve özelliklerine göre değişiyor.         |
| Singapur  | 30-200                     | İzin verilen araç türüne göre değişiyor.                  |
| İsviçre   | 30                         | Duman atım hızı 3,3-4 m/s arasında olacak şekilde         |
| Amerika   | 30-300                     | Tehlikeli madde taşımacılığı varsa 300 MW                 |

Şekil 5. Yangın durumunda karakteristik zaman/sıcaklık eğrileri (Maraveas ve Vrakas, 2014).

<!-- image -->

Line chart

Li vd. (2012) Runehamar T1 testi sonuçlarına göre hesap yapılarak 30 MJ için değeri için yaklaşık olarak 9,824 kg hava,  1,622  kg  yakıt  tüketilmektedir  ve  m*gaz  =  11,45 kg/s bulunmuştur.

Yangın sonrası oluşacak dumanın gaz içeriği, öncelikli olarak  yanan  yakıta  bağlıdır.  Birçok  küçük  ve  büyük yangın testleri  yapılmış  ve  yangın  sonucu  oluşan  CO2, CO, HCN, NO, NH3, HCl, SO2 gibi gazların miktarları saptanıp bir korelasyona ulaşmaya çalışılmıştır (Ingason vd., 2015). Tünel içerisinde meydana gelen yangınlarda, yangın sonucu oluşan CO ve CO2'in tüneldeki miktarının belirlenebilmesi  önemlidir.  CO2  oranı  yanan  üründen bağımsız olarak sadece ısı salınım oranına bağlı olmakla beraber,  CO  oranı  yanan  yakıtın  türü  ve  geometrisiyle doğrudan ilişkilidir. 'Runehamar Tünel Yangın Testleri' raporuna göre oluşan CO2 miktarı (m*CO2), Denklem 3'e göre belirlenebilir (Li vd., 2012).

<!-- formula-not-decoded -->

burada Q, MW birimiyle, m*CO2 ise, kg/s birimiyle ifade edilmektedir.  Denklem  3'e  göre,  m*CO2  =  2,61  kg/s bulunur.

Oluşan CO gazı miktarı ve is miktarı, yakıt türüne bağlı olarak değiştiğinden bunlarla ilgili kabuller yapılmıştır. 'Fire in Tunnels' raporuna göre, tünelde 30 MW 'lık bir otobüs yangınına ait test sonuçlarına göre, her 2 kg CO2 gazına  karşılık,  0,1  kg  CO  gazı,  0,05  kg  is  ortaya çıkmaktadır (FIT, 2005: 60, 70). Bu sonuçları Runehamar test sonuçlarıyla birleştirerek en kötü senaryo düşünüldüğünde; 11,45 kg gaz içeriğinde, 2,61 kg CO2 ortaya çıkacaktır. Gaz içeriğinde yaklaşık %22 oranında CO2, %1 oranında CO ve %0,5 oranında is bulunduğu kabul edilmiş, kalan kısım su buharı olarak tanımlanmıştır.

Jet fanlar, kapasitesi ve iç hacmine bağlı olarak momentum kaynağı olarak değerlendirilmiştir. Her bir jet fanın, jet fan kataloglarından seçilerek 45 kW, 1304 N/m 3 itki gücüne sahip olduğu kabul edilmiştir. Yangın bölgesine  100'er  m  yakınlıktaki  fan  grupları  (1  ve  2 numaralı fan grupları), yangını tetikleme riski ve yoğunluk değişimi nedeniyle verimsiz olacağı için çalıştırılmamıştır. Şafta kadar olan kısımdaki 2 grup (4 adet jet fan) devreye girmiştir.

Olası bir yangın durumunda gerek acil durum araçlarının müdahalesi, gerekse tünel içinde dumandan ve sıcaklıktan arındırılmış bir ortam sağlanabilmesi amacıyla tünel içinde oluşabilecek ters katmanlaşmanın önlenmesi gerekmektedir. Ters katmanlaşma, duman ve sıcak  havanın  istenilen  havalandırma  yönünün  tersine ilerlemesidir. Kritik hız ise ters katmanlaşmanın önüne geçilen minimum havalandırma hızıdır.

Tünel içerisinde yangın esnasında havalandırma sistemi aracılığı ile sağlanan hava hızı, dumanı istenilen yönde yönlendirmek ve bu esnada ters katmanlaşmayı engelleyebilmek için kritik hızdan büyük olmalıdır.

Karayolu tünellerinde duman, trafiğin akış yönüne doğru yönlendirilmelidir. Bu sayede yangın bölgesinde oluşabilecek bir trafik sıkışıklığı durumunda, araçların ve içerisindeki yolcuların dumana ve sıcaklığa maruz kalmamaları sağlanmış olur.

Kritik hız; yangın ısıl yükü, tünel yüksekliği, tünel kesit alanı,  tünel  eğimi,  ortam  sıcaklığı  gibi  parametrelere bağlıdır. Denklem 4 ve Denklem 6'nın birlikte çözülmesiyle kritik hız ve kritik sıcaklık hesaplanabilmektedir (Toprak, 2014).

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Burada;

<!-- formula-not-decoded -->

Yukarıdaki  denklemlerde  Vc kritik  hızı  (m/s),  Tf  kritik sıcaklığı (  C), T0 başlangıç sıcaklığı (  C), Qc  taşınımla ısı yükünü (kW), H tünel yüksekliğini (m), ρ0  ortam hava yoğunluğunu (kg/m 3 ), cp havanın özgül ısısını (kj/kg o C), K1 Froude sayısı faktörünü, θ tünel eğimini, A tünel kesit alanını (m 2 ), g yerçekimi ivmesini(kg.m/s 2 ) göstermektedir. Eğimin %-3,3 olduğu kısımda, 30 MW'lık yangın durumunda kritik hız ve sıcaklık değerleri hesabında kullanılan değerler ve Tablo 7'de ve NFPA  (National  Fire  Protection  Association)'a  göre iterasyon sonuçları Tablo 8'de gösterilmiştir.

Şekil 6. Şaftlar öncesi yangın durumu şematik gösterimi.

<!-- image -->

Line chart

Tablo 7. Eğimin %-3,3 olduğu kısımda kritik hız hesabında kullanılan değerler.

| Yangın Yükü (Q) (MW)                    | 30,00   |
|-----------------------------------------|---------|
| Tünel Yüksekliği (H T ) (m)             | 7,22    |
| Tünel Kesit Alanı (A) (m 2 )            | 67,00   |
| Tünel Eğimi (θ) (%)                     | -3,30   |
| Ortam Hava Yoğunluğu (ρ 0 ) (kg/m 3 )   | 1,20    |
| Ortam Sıcaklığı (T o ) (  C)           | 20,00   |
| Havanın Özgül Isısı (C P ) (kj/kg  C)  | 1,01    |
| Froude Sayısı Faktörü (K 1 ) (Fr -1/3 ) | 0,61    |

Tablo 8. Eğimin %-3,3 olduğu kısımda kritik hız ve sıcaklık değerleri iterasyonları (NFPA 502, 2017: Annex-D).

|   İterasyon | T f (C)   | V c (m/s)   |
|-------------|-----------|-------------|
|           1 | 20,00     | 2,98        |
|           2 | 144,26    | 2,65        |
|           3 | 159,80    | 2,62        |
|           4 | 161,51    | 2,61        |
|           5 | 161,70    | 2,61        |
|           6 | 161,72    | 2,61        |
|           7 | 161,72    | 2,61        |
|           8 | 161,72    | 2,61        |

Eğimin %-3,3 olduğu kısımda 30 MW'lık yangın durumunda kritik hız (Vc) 2,61 m/s, kritik sıcaklık (Tc) 162°C  bulunmuştur.  Yüksek  eğim  nedeniyle,  yangın sonucu  oluşan  baca  etkisi  en  çok  bu  bölümde  etkili olmaktadır.  Tünel  içi  havalandırma  tasarım  hızı,  bu değeri aşacak şekilde 3 m/s olarak seçilmiştir.

Yangının arka kısmındaki (giriş kısmından arkada kalan 11500  metrelik  mesafe)  jet  fanların  çalıştığı  ve  tünel içinde  3  m/s'lik  hava  hızının  sağlandığı  varsayılarak, model çalışmadaki tünel giriş portalı 3 m/s hava hızını sağlayacak şekilde dinamik basınç olarak tanımlanmıştır. Tünel içerisindeki yangının etkisi, yangının tünel içerisindeki pozisyonuna bağlı olarak değişmektedir. Bu çalışmada yangın sonucu oluşan dumanın tahliyesi için dumanın  en  yakın  hava  değişim  istasyonunun  yayılım yönüne yönlendirilmesi (Şekil 6) göz önünde bulundurulmuştur (CETU, 2003: 69).

Şaftın ileri kısmındaki tersinir çalışan jet fanların sayısal olarak  hesaplanan  senaryoya  göre,  tünel  içinde  şafta kadar  1  m/s  hava  hızını  sağladığı  varsayılarak,  model çalışmadaki çıkış portalından tünel içerisine 1 m/s hava hızını sağlayacak şekilde dinamik basınç tanımlanmıştır.

Tünel şaftlarındaki 2×70 m 3 /s debili aksiyal fanlar tam kapasite ile tahliye amaçlı çalıştırılmıştır. Tahliye fanlarına  ait  tünele  bağlanan  menfezler  basınç  olarak tanımlanmıştır.

Duman,  birim  yüzey  alandan  (ağır  yük  taşıtı  ya  da otobüsün  yüzey  alanı  30  m 2 )  geçen  kütle  akısı  olarak tanımlanmıştır. Otobüs boyutu yükseklikleri 2,5 metre ile 3  metre  arasında  değişmektedir.  Yapılan  çalışmada, yangın sonucu oluşan dumanın, otobüsün üst  yüzeyine yakın  bir  bölgeden  dağıldığı  düşünülerek,  yerden  2,5 metre yükseklikte, 12 metre uzunluğunda yüzey (otobüs üst yüzeyi) yangın kaynağı olarak seçilmiştir. Kullanılan sınır şartları Tablo 9'da ve Şekil 7'de geometri üzerinde de gösterilmiştir.

Tablo 9. Kullanılan sınır şartları.

| Kararlı Rejim Sınır Koşulları         | Prototip Model   | 1/100 Ölçek Model   |
|---------------------------------------|------------------|---------------------|
| Isı salınım oranı (kW)                | 30000            | 0,30                |
| Tünel içi hava hızı (m/s)             | 3,00             | 0,30                |
| Kirli hava şaftı hava hızı            | 9,57             | 0,96                |
| Taze hava şaftı hava hızı             | 2,68             | 0,27                |
| Tünel içi sıcaklık (K)                | 293,00           | 293,00              |
| Duman sıcaklığı (K)                   | 1393             | 1393                |
| Debi (kg/s)                           | 11,45            | 0,0001145           |
| Jet Fan itki gücü (N/m 3 )            | 1304             | 342                 |
| Betonarme duvar kaplama kalınlığı (m) | 0,30             | 0,003               |

## Ağ yapısı seçimi

Analizlerden daha kesin ve kısa zamanda çözüm alabilmek için ağ yapısı hücre boyutlarının uygun seçilmesi önemlidir (McGrattan ve Forney, 2004). Duman  karakteristiğini  ölçmek  için  minimum  yangın karakteristik çapı (D*) Denklem 7 ile belirlenir.

Şekil 7. Sınır şartlarının şematik gösterimi.

<!-- image -->

Engineering drawing

Kontrol amaçlı olarak, yangın bölgesine yakın bir noktada, farklı ağ sayılarında hız, sıcaklık ve yoğunluk değerleri karşılaştırılmıştır (Tablo 10).  3 ve 4 numaralı ağ sayılarında, sonuçlara etkilerin çok az olduğu görülmüştür. Tüm hesaplamalarda 10 -6 ile 10 -9 mertebesinde yakınsama sağlanmıştır.

<!-- formula-not-decoded -->

Burada,  Q, kW  biriminden  ısı salınım oranını, ρ0, başlangıç  hava  yoğunluğunu,  cp0  başlangıç  havanın başlangıç özgül ısısını, T0 başlangıç ortam sıcaklığını ve g ise yerçekimi ivmesini ifade eder.

Yüksekliğe  (H)  bağlı,  boyutsuz  ısı  salınım  oranı  (Q*), Denklem 8 ile belirlenir.

<!-- formula-not-decoded -->

Denklem 7 ve Denklem 8 birleştirilerek Denklem 9 elde edilir.

<!-- formula-not-decoded -->

Eğer Denklem 9 doğru sonuç veriyorsa, Denklem 10 ile uygun ağ (grid) hücre boyutu elde edilir (Li ve diğerleri, 2012).

Yangın bölgesi mesh boyutu = 0.075 D* (10)

Ölçek modelde kullanılan sınır değerlerine göre, Denklem 7 ve 8'den boyutsuz yangın çapı ve boyutsuz ısı salınım oranı hesaplanırsa;

<!-- formula-not-decoded -->

Q = 0,3 1,2(1,01)(293)(√9,81)( 0,0722) 5/2 =  0,193 bulunur. Denklem 9 ile kontrol yapıldığında,

D* / H = 0,512,   (Q*) 2/5 = 0,512 bulunur.

Doğru sonuç alındığı için, Denklem 10 ile 0.075  0,037 = 0,0028 m bulunur.

Hücre boyutu, tüneldeki ağ yapımını basitleştirmek için 0,0028 metre yerine 0,002 m olarak, tetrahedral elemanlardan  oluşan  düzensiz  ağ  yapısı  kullanılmıştır. Ağ,  yangın  bölgesinde,  jet  fan  kısımlarında,  şaftların bulunduğu bölgede ve portal giriş çıkışında iyileştirilmiştir. Toplam 2 293 533 ağ hücresi üretilmiştir (Şekil 8).

Şekil 8. Ağ yapısı gösterimi.

<!-- image -->

Engineering drawing

Tablo 10. Farklı ağ sayılarında sonuçların karşılaştırılması.

|   No | Ağ Element Sayısı   | Hız     | %   | Sıcaklık   | %   | Yoğunluk   | %   |
|------|---------------------|---------|-----|------------|-----|------------|-----|
|    1 | 943 057             | 1,80421 | %29 | 329,13     | %-7 | 1,01039    | %8  |
|    2 | 1 120 445           | 1,48539 | %-6 | 311,15     | %-1 | 1,0879     | %1  |
|    3 | 2 141 331           | 1,4197  | %0  | 309,07     | %0  | 1,10271    | %0  |
|    4 | 2 293 533           | 1,4016  | -   | 308,904    | -   | 1,09952    | -   |

## Matematiksel Modelleme

Analizler kararlı rejimde basınç tabanlı olarak yapılmıştır.  Akışa  dair  parametreleri  hesaplayabilmek için  akışkanın  uyması  gereken  kütle  ve  momentumun korunumu gibi temel prensiplerden yola çıkılarak temel akış denklemleri elde edilebilir. Genel değişken  kullanılarak, süreklilik,  momentum,  enerji,  türbülans modeli denklemleri gibi tüm denklemler genel bir formda yazılabilir. Genel bir  değişkeni için üç boyutlu genel taşınım denklemi Denklem 11'de verilmiştir.

<!-- formula-not-decoded -->

Bu  eşitlikte;  ,  genel  bir  değişkeni,  Γ,  genel  difüzyon katsayısını  ve S ,  kaynak  terimini  temsil  etmektedir. Genel  taşınım  denklemi  için,  değişkenler  ve  bunlara karşılık gelen difüzyon katsayıları ile kaynak terimleri de Tablo 11'de verilmiştir.

Türbülans modeli seçiminde, Reynolds-Averaged Navier-Stokes (RANS) denklemleri, modellenen türbülans ölçeğindeki transport denklemlerini akışa dair parametrelerin ortalama değeri olarak ifade etmektedir. Çözüm  yapılırken;  basınç,  sıcaklık,  enerji  ya  da  tür konsantrasyonu gibi skaler büyüklükler için ortalanmış değerler kullanılarak sistem çözümlenebilir hale getirilmektedir.  Bu  çalışmada,  süreklilik  denkleminin sağlanması, hesap yükünün nispeten az olması, türbülans harcanım  oranının  hesaplanması  ve  sonucun  negatif çıkmaması (hızın karesi) gibi konularda oldukça tutarlı olan  realizeable  k/ε  modeli  kullanılmıştır  (Berberoğlu, 2008).  Bu  modelde  k,  türbülans  kinetik  enerjisini,  ε, türbülans yutulma oranınını (turbulence dissipation rate) ifade  eder.  Türbülanslı  viskozite  değeri  µt;  k  ve  ε'nın fonksiyonu olarak ifade edilir.

## SONUÇLAR

Çalışmada, 2045 yılı trafik verileri temel alınarak tespit edilen kritik yangın bölgesinin incelenmesi amaçlanmıştır.  Bu  bölge,  iki  tüp  şeklinde  olan  tünelin Doğu tüpü girişinden 11500 metre uzaklıkta yer almaktadır. 30 MW'lık bir otobüs yangını durumu Ansys Fluent  programı  yardımıyla  incelenmiştir.    Elde  edilen hız,  sıcaklık,  karbon  monoksit  emisyonları  sonuçları sırasıyla bölüm içerisinde verilmiştir.

Analiz sonuçları; yangın bölgesinde oluşabilecek hasarları tespit edebilmek için dikey kesitte, tünel boyunca duman dağılımını görebilmek için yatay kesitte, atış  fanlarının  performanslarını  izleyebilmek  ve  olası tünel  içine  duman  basma  riskini  görebilmek  için  şaft bölgesinde  yatay  kesitte,  yangın  bölgesine  müdahale edecek itfaiye personeli ve ters yönde tünel kullanıcılarının  tahliyesi  için  önemli  olan  yerden  1,7 metre mesafede yatay kesitte incelenmiştir.

Hız dağılımı incelendiğinde, dağılım yangın bölgesinden kirli  hava  şaftına  kadar  3  m/s  değerinin  üzerindedir. Temiz hava şaftından, tünel çıkışına kadar olan kesimde ise  trafiğin  tersi  yönde  yaklaşık  1  m/s'lik  hava  hızı sağlanmaktadır. Atış fanlarına yakın bölgedeki hız vektörleri  Şekil 9'da  verilmiştir.  Jet  fan  gruplarının çalıştığı  150  m'lik  kesimde  yerel  hız  dağılımı  da  Şekil 10'da verilmiştir. Yangın bölgesinden 150 m ve 250 m mesafede çalışan jet fan gruplarının hız konturları incelendiğinde, piyasada bulunabilen jet fanlara ait teknik  özelliklere  göre  33,6  m/s'lik  hava  hızını  doğru şekilde yansıttığı görünmektedir. Jet fan grupları arasındaki 100 m'lik mesafe jet fanların çalışma verimi açısından yeterli görünmektedir.

Şekil  11'de  yerden  1,7  m  mesafede  lokal  hız  dağılımı gösterilmiştir. Yangın bölgesinin arka kısmında, insanların tahliye edileceği bölgede (trafik akış yönünün tersi istikamette), yerden 1,7 m mesafede hız 3 m/s'dir. Trafik yönünde yangın mahaline yakın kısımlarda hız 67  m/s  seviyelerindeyken,  diğer  kısımlarda  4  m/s'yi geçmemektedir.

Tablo 11. Genel taşınım denklemi için, değişkenler ve bunlara karşılık gelen difüzyon katsayıları ve kaynak terimleri (Novozhilov, 2001).

| Denklem                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                              | S                                                                                                                                                                                                                                                                                            |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Süreklilik                                                                                                                                                                                                                                                                                    | 1                                                                                                                                                                                                                                                                                             | 0                                                                                                                                                                                                                                                                                             | 0                                                                                                                                                                                                                                                                                             |
| x-momentum                                                                                                                                                                                                                                                                                    | u                                                                                                                                                                                                                                                                                             |  e                                                                                                                                                                                                                                                                                           |                                     x w z x v y x u x x P e e e                                                                                                                                                                                        |
| y-momentum                                                                                                                                                                                                                                                                                    | u z                                                                                                                                                                                                                                                                                           |  e                                                                                                                                                                                                                                                                                           |                                           y w z y v y y u x y P e e e                                                                                                                                                                            |
| z-momentum                                                                                                                                                                                                                                                                                    | u z                                                                                                                                                                                                                                                                                           |  e                                                                                                                                                                                                                                                                                           |                                       z w z z v y z u x g z P e e e ref      ) (                                                                                                                                                                   |
| Türbülans kinetik enerjisi                                                                                                                                                                                                                                                                    | k                                                                                                                                                                                                                                                                                             | k e                                                                                                                                                                                                                                                                                         |    G P                                                                                                                                                                                                                                                                                    |
| Türbülans kinetik enerji yutulması                                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                              |    e                                                                                                                                                                                                                                                                                       | ) ( 2 1   C CG k                                                                                                                                                                                                                                                                          |
| Enerji                                                                                                                                                                                                                                                                                        | h                                                                                                                                                                                                                                                                                             | h e                                                                                                                                                                                                                                                                                         | R Q                                                                                                                                                                                                                                                                                          |
| Kimyasal reaksiyon h                                                                                                                                                                                                                                                                          | Y F                                                                                                                                                                                                                                                                                           | Y e                                                                                                                                                                                                                                                                                         |        r Y Y k C F R 0 , min                                                                                                                                                                                                                                                         |
|                                                                                        2 2 2 2 2 2 2 x w z u y w z v x v y u z w y v x u e P  z p g G e                       1 |                                                                                        2 2 2 2 2 2 2 x w z u y w z v x v y u z w y v x u e P  z p g G e                       1 |                                                                                        2 2 2 2 2 2 2 x w z u y w z v x v y u z w y v x u e P  z p g G e                       1 |                                                                                        2 2 2 2 2 2 2 x w z u y w z v x v y u z w y v x u e P  z p g G e                       1 |

Şekil 9. Boyuna kesitte atış fanlarına yakın 150 m'lik kısımda yerel hız dağılımı.

<!-- image -->

Line chart

<!-- image -->

Bar chart

<!-- image -->

Engineering drawing

Şekil 10. Boyuna kesitte jet fan gruplarının çalıştığı 150 m'lik kesimde lokal hız dağılımı.

<!-- image -->

Engineering drawing

Şekil 11. Yerden 1,7 m mesafede 400 m'lik mesafede lokal hız dağılımı.

<!-- image -->

Engineering drawing

Şekil 12'de yangının olduğu kısımda 1300 K gibi yüksek sıcaklık değeri görünürken, yangın bölgesinde sıcaklığın 600 K düzeyinde olduğu, havalandırma yönünde yangına en yakın fan grubunun bulunduğu ilk 50 m'lik kısımda 400-500  K  seviyelerine  düştüğü  gözlemlenmektedir. Bunun nedeni de jet fanların çalışması ile havanın tahliye edilmesidir.

Yangın bölgesindeki sıcaklık dağılımı 400 K civarında olduğu  belirlendikten  sonra  sıcaklık  skalası  en  yüksek 600 K olacak şekilde belirlenmiş ve yangına müdahale noktasında  önemli  olan  200  m'lik  bölge  içerisindeki sıcaklık dağılımı Şekil 13'te verilmiştir.Şekil 12 ve Şekil 13  incelendiğinde,  yangın  bölgesinden  geriye  doğru sıcaklık yayılmamıştır. Bu da tünel kullanıcılarının tüneli tahliyesi için güvenli alanın oluştuğunu ve havalandırma için  seçilen  tasarım  hızının  (3  m/s)  yeterli  olduğunu göstermektedir. Sıcaklığa bağlı karışım havası yoğunluk düşüşü  nedeniyle  yangın  mahalline  yakın  noktalarda tünel tavanına yakın kısımlarda iken, yangın olan bölgeye uzaklık arttıkça soğuyan havanın, yoğunluğunun artması nedeniyle sıcaklığın tüm kesitte homojen olarak dağıldığı gözlemlenmektedir.

Eksenel fanların yangın durumunda ne şekilde etkileneceğini tespit edebilmek için Şekil 14'te, zeminden 6 m yükseklikte yerel sıcaklık dağılımı verilmiştir. Yangın bölgesinde sıcaklık değerleri 600 K

seviyelerindeyken, yangın bölgesinden 200 m uzaklıkta tavan sıcaklığı 330 K seviyelerine düşmüştür. Çalıştırılmayan  ilk  jet  fan  grubunda  sıcaklık  değerleri 500  K  seviyelerindedir.  Havalandırma  sisteminin  ana elemanları olan jet fanlar 250  C (523 K)'de 90 dakika süre  ile  çalışacak  şekilde  seçildiği  kabulüyle,  yangın bölgesinden  150  m  ileride  bulunan  ve  aktif  olan  jet fanların zarar görmeyeceği öngörülebilir.

Şekil  15'te,  ortalama  bir  insan  boyunun  1,7  m  olduğu kabul edilerek 400 m'lik kısımda zemin seviyesine yakın sıcaklık  dağılımı  verilmiştir.  Yangın  bölgesinden,  tünel kullanıcılarının tahliyesinin yapılacağı geri bölgede sıcaklık değerlerinin yükselmediği görünmektedir. Havalandırma  yönünde  ilk  150  m'lik  kısımda  sıcaklık değeri  330  K  (63  C)  seviyelerini  geçmektedir.  Bu  da yangına müdahale noktasında gelecek itfaiye personelinin gerekli koruyucu önlemleri almasını gerektirmektedir.

Şekil 14. Zeminden 6 m yükseklikte, 200 m'lik kısımda tavan bölgesi sıcaklık dağılımı.

<!-- image -->

Engineering drawing

Şekil 15. Zeminden 1,7 m yükseklikte, 400 m'lik kısımda sıcaklık dağılımı.

<!-- image -->

Engineering drawing

Şekil  16'da  yangın  bölgesinden,  trafik  yönünde  10  m ileride tünel kesitinin yerel sıcaklık dağılımı verilmiştir. Beklenildiği gibi, karışım havasının sıcaklığı bağlı yoğunluk  düşüşü  nedeniyle  sıcak  hava  yükselmiş  ve tünel tavanında en yüksek değerler ölçülmüştür.

<!-- image -->

Engineering drawing

yüzeylere  sıcaklığın  yayılması  200  C'de  başlar,  kritik sıcaklık ise 300  C'dir. (PIARC, 1991).

Sıcaklık analizi sonuçları incelendiğinde, yangın bölgesinden  trafik  yönünde  ilk  50  metrelik  kısımda ölçülen en yüksek sıcaklıklar 200  C'nin üzerinde seyretmektedir.  Bu  bölümde  beton  malzemelerin  zarar görebileceği  öngörülebilir.  Özellikle  yangın  bölgesi  ve 20  m  ilerisine  kadar  olan  bölümde  sıcaklıklar  belirli bölümlerde 300  C'yi (573 K) aşmaktadır. Bu bölümlerde yapısal dökülmeler ve kalıcı hasarlar beklenebilir. Özellikle  yangının  çıktığı  bölgeye  yakın  olan  20  m'lik mesafede tavan sıcaklık değerleri kritik değerleri aşmaktadır.

Şekil  16. XY  ekseninde  yangın  bölgesinden  10  m  ileride sıcaklık dağılımı.

<!-- image -->

Line chart

Şekil 17'de, 0 m yangın bölgesi olmak üzere, -40 m tünel kullanıcılarının  tahliye  güzergâhında,  360  m'de  trafik yönünde  kirli  hava  atış  şaftına  kadar  olan  mesafede ölçülen  en  yüksek  sıcaklıklar  ve  ortalama  sıcaklıklar grafik olarak gösterilmiştir.

Tünel  içindeki beton yapının hasarı; beton yapının dağılması ve ısıl olarak mukavemetinin azalmasına bağlı olarak  değerlendirilmektedir.  Isıl  bozulma,  tünel  astar veya  döşeme  kalınlığının  yarısını  aşarsa  yapının  ciddi şekilde  hasar  gördüğü  kabul  edilir.  Tünellerde  beton Yangın mahalinden trafik yönünde ilk 100 m'lik kısımda tünelin tavan kısmına yakın bulunan bölgede, 100°C ile 350°C arasında sıcaklık değerlerinin değiştiği ve yangına dayanıklı malzemelerin kullanılmaması durumunda, aydınlatma  armatürlerinde,  aydınlatma,  haberleşme  ve veri  iletim  kablolarında,  kablo  kanallarında,  ve  destek elemanlarında  kalıcı  hasarlar  olabileceği  öngörülebilir (PIARC, 1991).

Şekil  17. Yangın  bölgesinden  40  m  geride  ve  360  m  ileride (trafik yönüne) sıcaklık değişimi.

Acil durumlardaki önemli noktalardan birisi de karbonmonoksit  emisyonu  konsantrasyonlarıdır.  Şekil 18'de yangın bölgesinden geriye doğru dumanın yayılmadığı  görünmektedir.  Yangın  bölgesinden  şafta kadar  olan  bölümde  karışım  havasında  bulunan  CO seviyesi  10000  ppm'den  400  ppm  seviyelerine  kadar azalmıştır.

Şekil 19. Boyuna kesitte, zeminden 1,7 m mesafede CO ve duman dağılımı.

<!-- image -->

Engineering drawing

Şekil 19'da şaftların  sonrasındaki duman dağılımını da görebilmek için 400 m'lik kısımda CO dağılımı gösterilmiştir. Sıcaklık düşmesi nedeniyle yangın mahallinden  şafta  doğru  karışım  havasının  yoğunluğu yükselmekte  ve  duman  tünel  kesitine  dengeli  biçimde dağılmaktadır. Yangının olduğu bölgenin hemen sonrasındaki çalışmayan ilk jet fan grubu havalandırmaya karşı blokaj etkisi yaptığından dolayı ilk jet fan grubunun altında ufak bir kısımda dumanın çöktüğü görünmektedir.

Şekil 20'de 0 m yangın bölgesi olmak üzere, -40 m tünel kullanıcılarının  tahliye  güzergâhında,  360  m'de  trafik yönünde kirli hava atış şaftına kadar olan mesafede ölçülen en yüksek ve ortalama CO  değerleri grafik olarak gösterilmiştir.

Şekil 21'de yangın bölgesinin 10 m ilerisinden, kirli hava atış  şaftına  kadar  CO  miktarı  değişimi  detaylı  olarak grafikte  gösterilmiştir.  Ortalama  CO  değerlerinin  atış şaftına  kadar  400  ppm  seviyelerinin  altına  düşmediği, özellikle  ilk  50  m'de  ortalama  1000  ppm'in  üzerinde olduğu görülmektedir. Yangın mahallinden trafik yönüne göre geride kalan kısımda CO oranının kabul edilebilir seviyelerde olduğu (Şekil 20), bu da yangının gerisinde bekleyen tünel kullanıcılarının dumandan etkilenmeden tahliyesinin gerçekleşebileceğini göstermektedir.

CO  analizi  sonuçları  incelendiğinde,  yangın  bölgesine yakın  50  m'lik  mesafede  sıcaklık  kaynaklı  yoğunluk farkı nedeniyle CO'in tünelin tavan kısmında yoğunlaştığı, 60 m'de çalıştırılmayan jet fanın engellemesinden  dolayı  ortalama  değerlerin  nispeten yükseldiği,  70  m'den  sonra  ise  dumanın  soğuyarak çökmeye başlamasıyla beraber en üst ve ortalama değer arasındaki farkın kapandığı görünmektedir. İlk 30 m'de yangın durumunda tünel kullanıcıları için kabul edilebilir güvenlik kriterlerine göre 1200 ppm seviyesinin (Caliendo vd., 2013) üzerinde olduğu görülmektedir. Bu da  yangın  söndürme  ekiplerinin  oksijen  maskesi  vb. koruyucu  önlemler  alarak  yangına  müdahale  etmesini gerektirmektedir.

Şekil 20. Yangın bölgesinden 40 m geride ve 360 m ileride (trafik yönüne) CO değişimi.

<!-- image -->

Line chart

Şekil 21. Yangın bölgesinden kirli hava şaftına kadar CO değişimi.

<!-- image -->

Line chart

## DEĞERLENDİRME VE ÖNERİLER

Literatür çalışmalarından faydalanılarak seçilen tasarım yangın  yüküne  göre  kritik  hız  ve  sıcaklık  değerleri hesaplanmış analitik olarak yapılan hesaplar sonucunda yangın sonucu oluşan kritik nokta olarak tünelde eğimin en  yüksek  olduğu  DT\_3  lokasyonu  bulunmuştur.  Bu bölgede eğimin negatif olması sebebiyle, yangın sonucu oluşan  baca  etkisinin  yüksek  olması  bu  sonucu  ortaya çıkarmıştır. Ansys Fluent yazılımında geometri hazırlanırken, mesh yapısı hazırlanırken ve uygun model seçilirken (k- türbülans modeli) literatür çalışmalarından faydalanılmış ve sonuçların analitik hesaplamalarla uygunluk gösterdiği görülmüştür.

Yangın bölgesinden 150 m ve 250 m mesafede çalışan jet fan  gruplarının  hız  konturları  incelendiğinde,  fanların çalışma  hızı  33,6  m/s  olarak  elde  edilmiştir.  Jet  fan grupları  arasındaki  100  m  mesafe  jet  fanların  çalışma verimi açısından yeterli görünmektedir. Yangın bölgesinin  arka  kısmında,  insanların  tahliye  edileceği bölgede (trafik akış yönünün tersi istikamette) hava hızı 3 m/s olmaktadır. Ayrıca, trafik yönünde yangın mahaline yakın kısımlarda hız 6-7 m/s seviyelerindeyken, diğer kısımlarda 4 m/s'yi geçmemektedir.

Eksenel fanların yangın durumunda ne şekilde etkileneceğini tespit edebilmek  için  zeminden  6  m yükseklikte  yerel  sıcaklık  dağılımı  verilmiştir.  Yangın bölgesinde  sıcaklık  değerleri  600  K  seviyelerindeyken, yangın bölgesinden 200 m uzaklıkta tavan sıcaklığı 330 K  seviyelerine  düşmüştür.  Yangın  bölgesinden,  tünel kullanıcılarının tahliyesinin yapılacağı geri bölgede sıcaklık değerlerinin yükselmediği görünmektedir. Havalandırma  yönünde  ilk  150  m'lik  kısımda  sıcaklık değeri 330 K (63  C) seviyelerini geçmektedir. Ortalama sıcaklık  değerlerinin  ilk  30  m'de  ortalama  400  K'in üzerinde  olduğu  ve  yangına  müdahale  ekipleri  ve  o bölgedeki tünel kullanıcıları için riskli olduğu görünmektedir.  Bununla  birlikte,  0  m  yangın  bölgesi olmak üzere, -40 m tünel kullanıcılarının tahliye güzergâhında,  360  m'de  trafik  yönünde  kirli  hava  atış şaftına  kadar  olan  mesafede  hesaplanan  ortalama  CO değerlerinin atış şaftına kadar 400 ppm seviyelerinin altına düşmediği,  özellikle  ilk  50  m'de  ortalama  1000  ppm'in üzerinde olduğu belirlenmiştir. Yangın mahallinden trafik yönüne  göre  geride  kalan  kısımda  CO  oranının  kabul edilebilir seviyelerde olduğu, sadece trafik yönünde ilk 50 m'de referans değerin aşıldığı belirlenmiştir.

Çalışmada tünel içerisinden tehlikeli madde yüklü araçların geçmediği (özellikle tankerle akaryakıt taşımacılığı) varsayımı yapılmıştır. Bundan sonra yapılacak  çalışmalarda  çok  uzun  gerçek  bir  karayolu tünelinde  tehlikeli  madde  geçişi  olan  durumlar  hesaba katılarak,  değişik  araç  yangınları  üzerine  (30,  50,  100, 200 MW'lık yangın durumları) çalışma yapılması faydalı olacaktır.

## KAYNAKLAR

Alpgiray B., 2016, Enine Havalandırma Sistemine Sahip Bir Tünelde Yangın Kaynaklı Duman  Tahliyesinin Sayısal Yöntemle İncelenmesi , Yüksek Lisans Tezi, Gazi Üniversitesi Fen Bilimleri Enstitüsü, Ankara.

Alva W.U., Jomaas G., Anne S. and Dederichs A., 2017, The  Influence  of  Vehicular  Obstacles  on  Longitudinal Ventilation Control in Tunnel Fires, Fire Safety Journal , 87, 25-36.

Atkinson  G.T.  and  Wu,  Y.,  1996,  Smoke  Control  in Sloping Tunnels, Fire Safety Journal , 27, 335-341.

Berberoğlu  M.İ.,  2008, Yeraltı  Raylı  Taşıma  Sistemi İstasyonu  İçin  Yangın  Modellemesi  ve  Simülasyonu , Yüksek  Lisans  Tezi,  Gazi  Üniversitesi  Fen  Bilimleri Enstitüsü, Ankara.

Caliendo, C., Ciambelli, P., De Guglielmo, M.L., Meo, M.G.  and  Russo,  P.,  2012,  Numerical  simulation  of different HGV fire scenarios in curved bi-directional road tunnels and safety evaluation, Tunnelling and Underground Space Technology , 31, 33-50.

Caliendo, C., Ciambelli, P., De Guglielmo, M.L., Meo, M.G. ve Russo, P., 2013, 'Simulation of fire scenarious due to different vehicle types with and without trafficin a bi-directional road tunnel', Tunnelling and Underground Space Technology, 37, 22-36.

Chow W.K., Gao Y., Zhao J.H., Dang J.F., Chow C.L. and Miao L., 2015, Smoke movement in tilted tunnel fires with longitudinal ventilation, Fire Safety Journal , 75, 14-22.

CETU. (Novembre, 2003). Dossier Pilote Des Tunnels Equipments  -Ventilation ,  Bron: Centre  D'etudes  Des Tunnels, 45-69.

EPC (European Parliament and of the Council), 2004, On Minimum Safety Requirements for Tunnels in the TransEuropean Road Network, Official Journal of the European Union , Brussel, 29 April 2004, L201, 56-76.

EU  Report,  2003,  EU  (European  Union)  Directorate General  for  Energy  and  Transport, Safety  in  European Road Tunnels , EU Report 1.4.73, Brussel, 1-7.

FIT  (European  Thematic  Network  Fire  in  Tunnels), 2005, Design Fire Scenarious , Technical Report Part 1, A. Haack, STUVA, 60-70.

Gong, L., Jiang, L., Li, S., Shen, N., Zhang, Y. and Sun, J. 2016, 'Theoretical and experimental study on longitudinal  smoke  temperature  distribution  in  tunnel fires',  International  Journal  of  Thermal  Sciences  102, 319-328.

Hu L.H., Huo R., Wang H.B., Li Y.Z. and Yang R.X., 2007,  Experimental  Studies  On  Fire-Induced  Buoyant Smoke Temperature Distribution Along Tunnel Ceiling, Building and Environment , 42, 11, 3095-3915.

Hyun K.G., Ryul K.S., Sun R.H., 2009, An Experimental Study on the Effect of Slope on the Critical Velocity in Tunnel Fires, Journal of Fire Sciences , 28, 27-47.

Ingason, H., Li, Y.Z. ve Lönnermark, A., 2015, Springer Science+Business Media New  York, 'Tunnel Fire Dynamics', 372-384, 473-504.

Karaaslan S., Hepkaya E., Yucel N., 2011, Ölçeklendirilmiş Bir Kısa Tünelde Boyuna Havalandırma Sisteminin CFD Simülasyonu', Isı Bilimi ve Tekniği Dergisi , 33, 1, 63-77.

Kashef A., Saber H.H. and Gao L., 2009, Optimization of Emergency Ventilation Strategies in a Curved Section of  a  Road  Tunnel, National  Republican Congressional Committee (NRCC) , 51289, 11.

KGM  (Karayolları Genel Müdürlüğü Araştırma ve Geliştirme  Dairesi  Başkanlığı),  1997, Karayolu  Tüneli Uygulama Projesi Teknik Şartnamesi ,  KGM Matbaası, Ankara, 1-18.

Kurioka H., Oka Y., Satoh H. and Sugawa O. 2003. Fire Properties  in  Near  Filed  of  Square  Fire  Source  with Longitudinal Ventilation in Tunnels, Fire Safety Journal , 38, 319-340.

Lee S.R. and Ryou H.S., 2005, An Experimental Study of the Effect of the Aspect Ratio on the Critical Velocity in Longitudinal Ventilation Tunnel Fires, Journal of Fire Sciences, 23, 119-138.

Lee  Y.P.  and  Tsai  K.C.,  2012,  Effect  of  Vehicular Blockage  on  Critical  Ventilation  Velocity  and  Tunnel Fire Behavior in Longitudinally Ventilated Tunnels, Fire Safety Journal , 53, 35-42.

Li Y.Z., Lei B. and Ingason H., 2010, Study of Critical Velocity  and  Backlayering  Length  in  Longitudinally Ventilated  Tunnel  Fires, Fire  Safety  Journal ,  45,  361370.

Li, Y.Z., Lei, B., Ingason, H. (2012) Scale modeling and numerical simulation of smoke control for rescue stations in  long  railway  tunnels. Journal  of  Fire  Protection Engineering 22 (2):101-131.

Maraveas, C. and Vrakas, A.S., 2014, Design of Concrete Tunnel Linings for Fire Safety, Structural Engineering International , 3, 1-11.

McGrattan,  K.  and  Forney,  G.,  2004,  Fire  Dynamics Simulator (Version 4), User's Guide. National Institute of Standards and Technology, Gaithersburg, Maryland, USA.

NFPA,  2017, NFPA 502: Standard  for  Road  Tunnels, Bridges,  and  Other  Limited  Access  Highways,  2017 Edition ,  NFPA  (National  Fire  Protection  Association), Massachusetts, USA.

Novozhilov  V.,  2001, Computational  Fluid  Dynamics Modeling of Compartment Fires, Progress in Energy and Comustion Science , 27, 611-666.

Oka Y. and Atkinson G.T., 1995, Control of Smoke Flow in Tunnel Fires, Fire Safety Journal , 25, 305-322.

PIARC  (Permanent  International  Association  of  Road Congress),  1991, 'Fire in Road Tunnels. Protection for Civil  Engineering  Structures,  Electrical  Circuits  and Equipment , PIARC Committee on Road Tunnels, Paris, 175, 55-68.

PIARC  (Permanent  International  Association  of  Road Congress),  2017, Road  Tunnels:  (2017R02EN)  Design Fire Characteristics for Road Tunnels , PIARC Technical Committee 3.3 on Road Tunnels Operations, Paris, 3-64.

Taillefer,  N.,  Carlotti,  P.,  Lemerle,  C.  and  Avenel,  R., 2013, Ten Years of Increased Hydrocarbon Temperature Curves in French Tunnels, Fire Technology , 49(2), 531549.

Tang  F.,  Li  L.,  Chen  W.,  Tao  C.  and  Zhan  Z.,  2017, Studies on Ceiling Maximum Thermal Smoke Temperature  and  Longitudinal  Decay  in  a  Tunnel  Fire with Different Transverse Gas Burner Locations, Applied Thermal Engineering , 110, 1674-1681.

Toprak, A.S., 2014, CFD Application of a metro tunnel fire safety and emergency ventilation systems ,  Master's Thesis, Marmara University Department of Mechanical Engineering, İstanbul.

Vauquelin  O.  and  Wu  Y.,  2006,  Influence  of  Tunnel Width  on  Longitudinal  Smoke  Control, Fire  Safety Journal , 41, 420-426.

Wang  X.Y.,  Spearpoint  M.J.  and  Fleischmann  C.M., 2017, Investigation of the Effect of Tunnel Ventilation on Crib Fires Through Small-Scale Experiments, Fire Safety Journal , 88, 45-55.

Wu Y. and Bakar M.Z.A., 2000, Control of Smoke Flow in Tunnel Fires Using Longitudinal Ventilation System - A Study of the Critical Velocity', Fire Safety Journal , 35, 363-390.
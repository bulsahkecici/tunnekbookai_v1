<!-- image -->

Logo

Original Research / Orijinal Araştırma www.mining.org.tr

## Zayıf zeminlerde açılan büyük çaplı çift tüp tünellerin birbirine olan etkisinin 3 boyutlu sayısal analizlerle incelenmesi, Bolu Tüneli örneği

An analysis of interaction between large diameter double tube tunnels excavated in weak soils through 3D numerical analysis; An example of Bolu Tunnel

Ebu Bekir Aygar a,*

a Fugro Sial Yerbilimleri Müşavirlik ve Mühendislik Ltd. Şti., Ankara, TÜRKİYE

Geliş-Received: 7 Ocak - January 2022 * Kabul-Accepted: 9 Mayıs - May 2022

ÖZ

Bolu Tüneli Ankara İstanbul Otoyolu üzerinde yer almaktadır. Bolu Tüneli proje çalışmalarına 1993 yılında başlanmış olup 2007 yılında trafiğe açılmıştır. 3 şeritli çift tünel olarak projelendirilmiştir. Tünel uzunlukları sağ tünel 2788 m sol tünel 2954 m'dir. Bolu Tüneli inşası sırasında 2 kez sel ve depreme maruz kalmış ve Elmalık kesiminde Düzce Depreminde göçük yaşanmıştır. Göçük sonrasında güzergah değiştirilmiştir. Bolu Tüneli Kuzey Anadolu Fay Hattı ile Düzce Fayı arasındaki tektonik bloktan geçmektedir. Tünelin İstanbul tarafı (Asarsuyu) metakristalin temel kayaları içerisinde yer almakta iken Ankara tarafı (Elmalık) sedimanter kayaçlar içerisinde bulunmaktadır. Tünelde kazı aşamasında kritik sorunların meydana geldiği Elmalık girişinde Elmalık fayı bulunmakta olup, tünelin bu bölümlerinde 1,2 m'ye varan deformasyonlar oluşmuştur. Düzce Depreminde ise Elmalık sol tünel tamamen kapanarak göçük oluşmuştur. Bolu Tünellerinde yaşanan sorunlar ve destek sistemleri tünelcilik açısından çok değerli bilgiler içermektedir. Bu çalışmada, destek sistemleri Flac3d programı ile 3 boyutlu olarak incelenmiş, iki tünelin birbirine olan etkisi, üst yarı, alt yarı ve invert kazılarında meydana gelen değişimler ortaya konmuştur.

Keywords: Bolu Tüneli, Göçük, Flac3d, Düzce Depremi, Tünel etkileşimi

## ABSTRACT

Bolu Tunnel is located on the Ankara İstanbul Highway which started in 1993 and was made available to traffic in 2007. It was built as 3-lane double tunnel. The tunnel lengths of the right and left tunnel are 2788 m and 2954 m respectively. During the construction, it was undergone 2 earthquakes and flooding, and the Elmalık section collapsed after the Düzce Earthquake. After collapse, the route diverted. The tunnel passes through the tectonic block between the North Anatolian Fault and Düzce Fault. The Istanbul side (Asarsuyu) is located within the metacrystalline basement, the Ankara side (Elmalık) is located within the sedimentary rocks. The biggest problems during the excavation of the tunnel located Elmalık fault where deformations up to 1.2 m and collapsed in the earthquake. The problems and support systems in the tunnels contain very valuable information for tunneling. In this study, the supports are examined in 3D with the Flac3d program, the effect of the two tunnels on each other, the deformation changes in the top heading, bench and invert excavations are studied.

Keywords: Bolu Tunnel, Collapse, Flac3d, Düzce earthquake, Tunnel interactions

## Giriş

Zayıf zeminlerde açılan tünellerin destek sistemlerinin belirlenmesi için yapılan çalışmalar günümüzde giderek artmaktadır (Barla 2002, 2016, Hoek 2001, Aygar ve Gökçeoğlu 2020, 2021 a, b, c ve d, Aygar 2000, 2007, 2020, 2021a, 2021b). Zayıf zeminlerde açılan tünellerde yaşanan sorunlara bakıldığı zaman sıkışma ve şişme problemleri ile karşılaşıldığı görülmektedir. Buna ek olarak, tünel ayna ve tavan desteklenmesi sırasında karşılaşılan sorunlar da tünel duraylılığını etkilemektedir. Sıkışma için tünel örtü yüksekliği ve kaya kütlesinin tek eksenli basınç dayanımı temel faktörler olarak karşımıza çıkmaktadır (Jethwa vd. 1984, Sakurai 1983, Singh vd. 1992, Goel vd. 1995, Hoek ve Marinos 2000).

*

Corresponding author: eaygar@gmail.com · https://orcid.org/0000-0002-5738-4602

Zayıf zeminler için destek sistemlerinin tasarımında iki ana yaklaşım üzerinde durulmaktadır: aktif ve pasif destek sistemi tasarımı. Bunlardan ilki olan aktif destek sistemi tasarımında deformasyona izin  verilmeden rijit bir tahkimat uygulanırken pasif yaklaşımda ise deformasyona müsaade edilerek esnek bir tahkimat uygulanmaktadır. Schubert (1996) yaptığı çalışmada iksalar üzerinde deformasyon  boşluğu  önermiştir.  Hoek  (2007,  2012)  ise  meydana gelen deformasyonlar için TH tipi kayan iksalar önermiş ayrıca tünel ayna ve tavan duraylılığının önemi üzerinde durmuştur. Ayrıca zayıf zemin içinde çift tüp olarak açılan geniş çaplı tünellerde ise iki  tünelin birbirine olan etkisi önem kazanmaktadır. Tünellerin kazıları sırasında iki tüp  aynası  arasında  belirli  bir  mesafe bırakılması  önerilir.  Buna  ek  olarak  iki  tünel  arasındaki  topuk mesafesi ise en az tünel çapının 1,5 katı olacak şekilde bırakılması  önerilir  (KGM,  2013).  Tünel  kazısı  sırasında  ise  Yeni  Avusturya Tünelcilik Yöntemi (NATM) (Rabcewicz, 1964 a, b and 1965; Rabcewicz and Golser, 1973) prensiplerine göre tünel üst yarı, alt yarı ve invert şekilde bölümlendirilmektedir. Zira tünel kazısının tek aşamada yapılması mümkün olamamaktadır. Bu durumda ise üst yarı, alt yarı ve invert kazıları arasındaki mesafe çok önem kazanmaktadır. Sağlam kayalarda bu mesafe 100 ila 200 m'ye kadar çıkarken zayıf kayalarda bu değer 20-25 m'ye kadar düşmektedir. Son dönemlerde ise İtalyan yöntemi olarak karşımıza çıkan 'kaya ve zeminlerde deformasyon kontrollü analiz' (ADECO-RS) yöntemi  tam  kesit  kazı  prensibine  göre  destek  sistemi  yapılmaktadır Lunardi 2000a, 2000b, 2008. 2014, 2016, Barla 2002). ADECO-RS yönteminde tünel ayna ve tavan duraylılığı çok önemlidir. Bunun için tünel aynasında uzun fiber bulonlar çakılarak ayna tamamen duraylı hale getirilmektedir. Bu aşamadan sonra tam kesit tünel kazı işlemi yapılmaktadır.

Bu  çalışma  kapsamında,  zayıf  zeminlerde  açılan  tünellerde kazı kademeleri ile tünellerin birbirine olan etkisinin incelenmesi amacıyla Bolu Tünellerindeki uygulamalar dikkate alınmıştır. Bunun için 3 boyutlu analiz imkanı sunan Flac3d (Itasca, 2002) programı  kullanılarak  tünel  kazı  kademeleri  ile  iki  tünelin  birbirine olan etkisi incelenmiştir. Bilindiği üzere Bolu Tüneli yapımı 13 yıl süren, kazı çapı 18 m'ye varan geniş çaplı çift tüpten oluşan bir tüneldir. Kazı işlemi üst yarı, alt yarı ve invert şeklinde olup tüneller arasında 55 m ile 60 m arasında değişen mesafe bırakılmıştır. Kazı işlemi sırasında tünellerde ciddi deformasyonlar ile karşılaşılmış ve  tünel  destek  sistemlerinde  stabilite  ve  göçük  problemleri  ile karşılaşılmıştır. Bu sebeple Bolu Tünellerinde yapılan uygulamalar zayıf kaya kütlelerinde açılan tüneller için çok önemli veriler içermektedir.

## 1. Bolu Tüneli

Bolu  Tüneli  Ankara-İstanbul  Otoyolu  içerisinde  yeralmakta olup, 3 şeritli çift tünelden oluşmaktadır. İstanbul tarafında (Asarsuyu girişi) kazı işlemleri 1993 yılında, Ankara tarafında (Elmalık girişi) ise 1994 yılında kazı işlemlerine başlanmıştır. Tünel kazı işlemleri 2006 yılında tamamlanarak 2007 yılında trafiğe açılmıştır (Şekil 1). Kazı işlemleri toplam 13 yıl sürmüştür. Tüneller arasında 50 ila 60 m arasında değişen topuk bırakılmıştır. Tünel örtü yüksekliği genelde 100 ila 150 m arasında değişmekte olup, en yüksek örtü yüksekliği ise 250 m'dir. Tünel kazı çapı destek sınıflarına bağlı olarak 13 m ile 18,2 m arasında değişmektedir. Kazı alanı ise 133 m 2 ile  260  m 2 arasındadır.  Tünellerin  tamamlanmış halinde yatay açıklık olarak 14,0 m ve yükseklik ise 8,60 m'dir (Şekil 2).

Bolu  Tünelleri  Yeni  Avusturya  Tünelcilik  (NATM)  Yöntemine  göre  projelendirilmiştir.  Projelendirme  aşamasında  sıkışan kayadan çok sağlam kaya sınıfına kadar destek sistemleri belirlenerek kazı işlemlerine başlanmıştır. Tünel kazısı sırasında ise beklenmeyen jeolojik koşullara göre deformasyonlarda ciddi artışlar gözlenmiştir. Bu artışlar yer yer Elmalık girişinde yeralan filiş serileri ile kısa fay zonlarında töleransın 4 ile 5 katına kadar çıkmıştır.  Karşılaşılan  yeni  jeolojik  koşullara  göre  tünel  destek sistemleri  sürekli  olarak  revize  edilmiştir.  Destek  sistemlerinde yapılan bu değişiklikler ilk dönemlerde NATM  prensipleri içerisinde  kalarak  devam  etmiş  ancak  başarı  sağlanamamıştır. 1998 yılı itibari ile de NATM prensiplerinin dışına çıkılarak esnek bir dış kemer ilkesinden vazgeçilmiştir. Yapılan bu revizyonlarda kaplama kalınlığının tamamen artırılması yönüne doğru gidilmiştir. Bu amaçla kısa fay zonlarında dış kaplama ile iç kaplama arasında ara kaplama eklenmiş (Seçenek 3), uzun fay zonlarında ise alt yarı pilot  tünel  yöntemi  (Seçenek  4)  kullanılmıştır.  12  Kasım  1999 Düzce depreminde meydana gelen göçük sonrasında ise bu yöntemlerin uygulanmasına devam edilmiştir. Düzce depreminde Elmalık  girişinde  yaşanan  göçük  incelendiğinde  deformasyonların devam ettiği ve sönümlenemediği bölgede oluşutuğu gözlenmiştir. Bu bölgede iç kaplaması yapılan ilk 400 m lik kesimde ise herhangi bir hasar meydana gelmemiştir (Şekil 1).

<!-- image -->

Geographical map

<!-- image -->

Geographical map

Şekil 1. Bolu Tüneli yer bulduru haritası

<!-- image -->

Engineering drawing

Şekil 2. Bolu Tüneli en kesiti

<!-- image -->

Engineering drawing

## 2.  Jeolojik-Jeoteknik Koşullar

Bolu Tüneli güzergah boyunca tektonizmaya uğramış birimler içerisinde açılmıştır. Tüneli etkileyen ana fay sistemleri 1. Derece aktif fay sitemleridir. Bolu Tüneli boyunca yeralan birimler iki gruba ayrılabilir. İlk grup İstanbul girişinde (Asarsuyu) Metakristalin kayalardan oluşmakta olup genelde metasediman seriler içerisinde açılmıştır. Bu bölüm Bakacak fay zonunun tüneli kestiği yaklaşık km:62+800 e kadar olan bölgeyi kapsamaktadır. Bu noktadan sonra ise  Ankara girişinde  (Elmalık)  yeralan  filiş  serisini  kapsamaktadır. Bu bölgede düşük açılı faylar ile kesilmiş olup bu iki grup arasında yaklaşık 200 m uzunluğundaki Bakacak fayı bulunmaktadır.  Elmalık girişinde tüneli olumsuz etkileyen altaki metakristalin tabaka üzerinde yeralan üstteki sedimanter serisi içerisindeki düşük açılı faylardır. Tünel kazısı ise genelde bu bölümde yapılmış olup beklenmeyen aşırı deformasyonlara neden olmuştur. Elmalık tarafında karşılaşılan filiş serileri tektonizmaya uğramış kiltaşı, silttaşı  ve  kireçtaşı  birimlerinden  oluşmaktadır.  Bu  kesim  genel olarak kaygan yüzeyli ve yüksek plastik özelliklere sahip fay kili malzemesi  içermektedir.  Tüneli  olumsuz  etkileyen  Bakacak  fayı için ise Lettis vd (2000) tarafından yapılan çalışmada fayın uzunluğunun 10 ile 15 km arasında değiştiği belirtilmiş ve tüneli 200 m'lik  bir  kesimde  kestiği  belirtilmiştir.  Fayın  yönelimi  yaklaşık olarak doğu-batı yönünde olup tüneli km:62+800 ile 63+000 arasında dik olarak kesmektedir. Bu fay zonu kırmızı renkli yüksek plastik özellikli olup büyük oranda kaygan yüzeylere sahiptir.

Bolu tüneli 4 ana bölüme ayrılabilir. Bunlar metakristalin tabaka (Yedigöller formasyon), metasediman serileri (İkizoluk formasyonu), Filiş serisi (Fındıcak Formasyonu) ve killi fay zonları olarak  ayrılabilir  (Dalgıç,  2002).  Bolu  Tüneli'nde  sayısal  analiz çalışmaları için metakristalin tabaka ile filiş serileri içinde geçilen bölümler incelenmiştir.  Bu bölümlerin örtü yükseklikleri filiş serisinde 50 m, metakristalin tabaka için ise 100 m'dir. Şekil 3'te Bolu Tüneli'ne ait jeolojik profil verilmektedir.

Şekil 3. Bolu Tüneli jeolojik profili (Geoconsult,1998)

<!-- image -->

Bar chart

## 2.1. Filiş serisinin jeolojik ve jeoteknik özellikleri

Filiş serisi içinde geçilen bölüm tünelin Elmalık girişine yakın kısmında olup km:63+910 ile 64+120 arasında yer almaktadır. Tünelin bu bölümü, temelde düşük plastik özellik gösteren filiş serisinde kazısı yapılmış kiltaşı, kumtaşı ve marnlı kireçtaşını içeMrmektedir. Marnlı kireçtaşı ve bireşik kalkerli kumtaşı az dereceden orta dereceye kadar bozunmuş, zayıftan orta dereceye kadar değişen dayanıma sahiptir. Kiltaşı tabakaları ise yüksek oranda bozunmuş ve oldukça zayıf özelliklere sahiptir ve bloklu malzeme ile ince matriksler halindedir. Matriks, toplam kütlenin %20 ila 40'ını oluşturmaktadır. İnce matriksler killi kumlu silt yapılarından oluşmaktadır.  Şekil  4'de  bu  bölüme  ait  jeolojik  kesit  sunulmaktadır. Çizelge 1'de kaya kütle parametreleri verilmektedir (Geoconsult, 2002).

Şekil 4. Filiş serisi içinde geçilen bölümün jeolojik kesiti

<!-- image -->

Engineering drawing

Çizelge 1. Filiş serisine ait zemin parametreleri (Geoconsult, 2002)

| İçsel sürtünme açısı   | Kohez- yon   | Young modülü   | Hacimsel modül   | Makaslama modülü   | Birim hacim ağırlık   |
|------------------------|--------------|----------------|------------------|--------------------|-----------------------|
| 20°                    | 50 kPa       | 493 MPa        | 411 MPa          | 190 MPa            | 22 kN/m 3             |

## 2.2. Metakristalin tabakanın jeolojik ve jeoteknik özellikleri

Metakristalin  tabaka  içinde  geçilen  bölüm  km:  62+890  ile 63+080 arasında yer almaktadır. Kaya kütlesi amfibolitler ile beyaz renkli sağlam kuvars içinde makaslama bölümlerine sahiptir. Bu  bölüm  kahverengi  yeşil  ve  gri  renkli  orta  dereceden  yüksek dereceye kadar bozunmuş olup oldukça zayıf özelliklere sahiptir. Şekil 5'te metakristalin tabakaya ait jeolojik kesit sunulmaktadır. Sayısal modellemelerde kullanılan bölüme ait zemin parametreleri Çizelge 2'de verilmektedir (Geoconsult, 2002).

Çizelge  2. Metakristalin  tabakaya  ait  zemin  parametreleri  (Geoconsult, 2002)

| İçsel sürtünme açısı   | Kohezyon   | Deformasyon modülü   | Hacimsel modül   | Makaslama modülü   | Birim hacim ağırlığı   |
|------------------------|------------|----------------------|------------------|--------------------|------------------------|
| 25°                    | 50 kPa     | 1000 MPa             | 833 MPa          | 384 MPa            | 22 kN/ m 3             |

Şekil 5. Metakristalin tabaka içinde geçilen bölümün jeolojik kesiti

<!-- image -->

Engineering drawing

## 3. Sayısal Analizler

Sayısal  analiz  çalışmalarında  FLAC 3D programı  kullanılmıştır. Flac3D programı sonlu farklar metodu ile çalışan bir sayısal analiz programıdır (Itasca, 2002). 3 boyutlu olarak zemin, kaya ve diğer yapı elemanlarını modelleyebilmektedir. Tünel analizlerinde kullanılacak  olan  yapısal  elemanlar  modele  tanımlanabilmektedir. Modelde kazı işlemi üst yarı, alt yarı ve invert şeklinde modellenebilmekte ve destek elemanları da modele tanımlanabilmektedir.  Sayısal  analizler  için  Bolu  Tüneli'nde  CM35  ve  CM45  destek sınıfları  seçilmiş  olup  (Şekil  6),  bu  kesimler  sırasıyla  metakristalin  tabaka  ile  filiş  serisi  içerisinde  yer  almaktadır.  Püskürtme beton  kalınlıkları  sırası  ile  35  cm  ve  45  cm  olup  9  m  ile  12  m uzunluklarında  kendinden  delgili  bulonlar  kullanılmıştır.  Tavan kesiminde ise süren olarak IBO tipi bulonlar kullanılmıştır.

Şekil 6. CM 35 ve CM 45 destek sistemi detayları (Aygar, 2020)

<!-- image -->

Engineering drawing

alındığında modelde sınır koşulları uygun olmaktadır.

3.1.  FLAC 3D programı  ile  statik  analizler  için  yapılan  modelleme çalışmaları

Statik çözümlemeler için FLAC 3D programı ile oluşturulan modellerde tünel kazı ve destek sistemleri modellenmiştir. Modelleme  sonuçları  değerlendirilerek  tünelde  meydana  gelen  yenilme durumu ve yerdeğiştirmeler incelenmiştir.

Statik durumda meydana gelen değişimler ve elde edilen sonuçlar tünel kazısı ve destek sistemlerinin değerlendirilmesi açısından  önemlidir.  Zira  oluşturulan  modeller  Bolu  Tünelleri'nde uygulanan kazı ve destek sistemi ile örtüşmektedir. Bundan dolayı statik  durumda meydana gelen değişimlerin incelenmesi destek ve kazı sisteminin doğruluğu açısından önem kazanmaktadır.

Bolu tünelleri için normal arazi koşullarına uygun olacak şekilde modeller oluşturulmuştur. Modelin tünel başlangıç noktaları 0 olarak kabul edilmiştir. Modelde sol tünel başlangıç noktası 0,0,0 sağ tünelde ise 0,55,0 olarak alınmıştır.  Kazı işlemleri 0'dan itibaren Y ekseni boyunca yapılmıştır.

Modelleme sırasında yerçekimi ivmesi kullanılarak başlangıç gerilmeleri  oluşturulmuştur.  Oluşturulan  model  invertte  x,  y,  z yönlerinde  sabitlenirken,  sol  ve  sağ  yüzeyleri  x  yönlerinde,  modelin ön ve arka yüzeyleri y yönünde sabitlenmiş ve tavan ise sabitlenmemiştir (Şekil 7). Modellemelerde sınır koşulları ile açıklık etkileşimini önlemek için, en büyük açıklığın yükseklik veya genişliğinden en az 4 ila 5 misli mesafede olması gerekmektedir. Bundan dolayı modelin sol tarafında 80 m, sağ tarafında ise 135 m, invert bölümünde ise 80 m mesafe bırakılarak modellemesi yapılmıştır. Model derinliği, y ekseni diğer bir ifadeyle tünel ekseni yönünde 100 m olarak alınmıştır.  Tünel  çapının  16  m  olduğu  göz  önüne alındığında modelde sınır koşulları uygun olmaktadır. Şekil 7. Oluşturulan modelde sınır koşulları Modelde arazi koşullarına uygun olarak sağ ve sol tünel arasında eksenden eksene 55 m mesafe bırakılmıştır. Tünel kazısı üç aşamada yapılmaktadır. Bu aşamalar üst yarı, alt yarı ve invert kazısı şeklindedir. Modellemede tünel kazısı uygulama aşamasında olduğu gibi üç aşamada yapılmıştır (Şekil 8). Şekil 7. Oluşturulan modelde sınır ko Modelde  arazi  koşullarına  uygun  olarak  sağ  ve  sol  tünel  arasında  eksenden  eksene  55  m  mesaf bırakılmıştır.  Tünel  kazısı  üç  aşamada  yapılmaktadır.  Bu  aşamalar  üst  yarı,  alt  yarı  ve  invert  kazı şeklindedir.  Modellemede  tünel  kazısı  uygulama  aşamasında  olduğu  gibi  üç  aşamada  yapılmışt (Şekil 8).

<!-- image -->

Engineering drawing

ulları

ş

<!-- image -->

Photograph

turulan modelde tüneller arasında bırakılan mesafe

Şekil 8. FLAC 3D  programı ile oluş Şekil 8. FLAC 3D  programı ile oluşturulan modelde tüneller arasında bırakılan mesafe

Tünellerde üst yarı, alt yarı ve invert kemeri kısımları arasında gerçek uygulamaya paralel olarak tün ekseni  yönünde  60  metre  mesafe  bırakılarak  yapılmıştır.  Şekil  9'da  modelleme  aşaması  sırasınd Tünellerde üst yarı, alt yarı ve invert kemeri kısımları arasında gerçek uygulamaya paralel olarak tünel ekseni yönünde 60 metre mesafe bırakılarak yapılmıştır. Şekil 9'da modelleme aşaması sırasında uygulanan kazı ve destek sistemi şematik olarak verilmektedir.    Modelleme başlangıcında bu mesafeyi oluşturmak için sol tünelde ilk 40 m'lik kısımda üst yarı ve alt yarı bölümlerinde kazı ve desteklerin yapıldığı varsayılarak modelin bu bölümü boşaltılmış  ve  destek  elemanları  yerleştirilmiştir.  Aynı  şekilde  sol  tünel üst yarı bölümünde 40 ile 60 m'lerde de kazı ve destek işleminin yapıldığı  ayrıca  invert  bölümünde  de  ilk  36  m'lik  bölümün  kazı ve invert betonun tamamlandığı varsayılmıştır. Ayrıca sol tünelde ilk 24 m'lik bölümde iç kaplamanın yapıldığı düşünülerek modele uygulanmıştır. Böylelikle sol ve sağ tüneller arasında tünel ekseni yönünde istenilen 60 m'lik mesafe sağlanmıştır. İnşaat aşamasında üst yarı ile alt yarı arasında 20-30 m mesafe bırakılmaktadır. Invert ile alt yarı arasındaki mesafe ise en fazla 4 m olmaktadır. Kazı işlemleri, her bir kademede üst yarıda 1 m, alt yarı da 2 m ve invertte 4 m olarak yapılmaktadır. Modelde kazı işlemleri tünelde yapılana uygun olarak sol tünelde üst yarıda 60. m den başlayarak 1'er m' lik kazılarla 60 ile 66. m'ye kadar 6 aşamada, alt yarıda ise 40 ile 46 m' ye kadar 2 şer m' lik kazılarla 3 aşamada, invert bölümünde ise 36 ile 44 m'ye kadar 4 er m'lik kazılarla 2 aşamada yapılmıştır. Ayrıca sol tünelde 0 ila 24 m'ler arasında iç kaplama betonu yapılmıştır (Şekil 9). Sol tünelde kazı ve tahkimat işlemleri bitirildikten sonra sağ tünelde kazı işlemlerine başlanmıştır. Üst yarıda ilk 8 m' lik bölümün kazısı 1 er m'lik kazılarla 8 aşamada, alt yarıda aynı şekilde ilk 8 m'lik bölümün kazısı 2'şer m'lik kazılarla 4 aşamada ve invert bölümünde ise ilk 8 m'lik bölümün kazısı 4'er m'lik kazılarla 2 aşamada bitirilmiştir (Şekil 10). Şekil 10 sağ tünelde kazı durumunun tamamlanmış halini göstermektedir.

kil  9).  Sol  tünelde  kazı  ve  tahkimat  işlemleri  bitirildikten  sonra  sağ  tünelde  kazı

şlanmıştır.  Üst  yarıda  ilk  8  m'  lik  bölümün  kazısı  1  er  m'lik  kazılarla  8  aşamada,  alt

azı durumunun tamamlanmış halini göstermektedir.

mün kazısı 4'er m'lik kazılarla 2 aşamada bitirilmiştir (Şekil 10). Şekil 10 sağ tünelde

<!-- image -->

Engineering drawing

ekil 9. Sol tünelde yapılan modelleme a

Ş Şekil 9. Sol tünelde yapılan modelleme aşamaları

ekil 9. Sol tünelde yapılan modelleme a

Ş

ş

amaları

<!-- image -->

Bar chart

amaları

Şekil 10. Sağ tünelde modelleme a Şekil 10. Sağ tünelde modelleme aşamaları

ş

rde  iç  kaplamanın  yapılmadığı  durumu  ayrıntılı  bir  şekilde  inceleyebilmek  için  sağ

tatik  analizlerde  iç  kaplamanın  yapılmadığı  durumu  ayrıntılı  bir  şekilde  inceleyebilmek  için  sağ ünelde iç kaplama betonu yapılmamıştır. Şekil 11'de sol tünel için modelde oluşturulan iç kaplama etonu  gösterilmektedir.  Model  üzerinde  meydana  gelen  değişimleri  görebilmek  ve  zamana  bağlı larak yerdeğiştirmeler ile gerilmeleri izleyebilmek amacıyla referans noktaları seçilmiştir. Sol tünel üst arı  kazısı  sırasında  meydana  gelen  değişimler  için  62  m,  sol  tünel  alt  yarıda  meydana  gelen eğişimleri görebilmek amacıyla 42 m, sağ tünelde üst yarı tavan kısmında meydana gelen değişimleri örebilmek  amacıyla  2  m  seçilmiştir.  Belirlenen  bu  noktalarda  modelleme  aşamalarına  bağlı  olarak erdeğiştirme  grafikleri  çizdirilmiştir.  Şekil  12'de  model  üzerinde  belirlenen  noktaların  konumları erilmiştir. a) Sol tünel üzerinde belirlenen noktalar   b) Sa a) Sol tünel üzerinde belirlenen noktalar Şekil 11. Modelde oluşturulan iç kaplama betonunun kesiti görünüşü lama betonu yapılmamıştır. Şekil 11'de sol tünel için modelde oluşturulan iç kaplama ilmektedir.  Model  üzerinde  meydana  gelen  değişimleri  görebilmek  ve  zamana  bağlı ştirmeler ile gerilmeleri izleyebilmek amacıyla referans noktaları seçilmiştir. Sol tünel üst asında  meydana  gelen  değişimler  için  62  m,  sol  tünel  alt  yarıda  meydana  gelen ebilmek amacıyla 42 m, sağ tünelde üst yarı tavan kısmında meydana gelen değişimleri acıyla  2  m  seçilmiştir.  Belirlenen  bu  noktalarda  modelleme  aşamalarına  bağlı  olarak grafikleri  çizdirilmiştir.  Şekil  12'de  model  üzerinde  belirlenen  noktaların  konumları Statik analizlerde iç kaplamanın yapılmadığı durumu ayrıntılı  bir  şekilde  inceleyebilmek  için  sağ  tünelde  iç  kaplama  betonu yapılmamıştır.  Şekil  11'de  sol  tünel  için  modelde  oluşturulan  iç kaplama betonu gösterilmektedir. Model üzerinde meydana gelen değişimleri görebilmek ve zamana bağlı olarak yerdeğiştirmeler ile gerilmeleri izleyebilmek amacıyla referans noktaları seçilmiştir.  Sol  tünel  üst  yarı  kazısı  sırasında  meydana  gelen  değişimler için 62 m, sol tünel alt yarıda meydana gelen değişimleri görebilmek amacıyla 42 m, sağ tünelde üst yarı tavan kısmında meydana gelen değişimleri görebilmek amacıyla 2 m seçilmiştir. Belirlenen bu  noktalarda  modelleme  aşamalarına  bağlı  olarak  yerdeğiştirme grafikleri çizdirilmiştir. Şekil 12'de model üzerinde belirlenen noktaların konumları verilmiştir.

Ş

ekil 10. Sa

ğ

tünelde modelleme a

<!-- image -->

Engineering drawing

ş

amaları

Ş

ekil 11. Modelde olu

ş

turulan iç kaplama

<!-- image -->

Line chart

tirme ve gerilmeler

Ş

Ayrıca tünelde meydana gelen yenilme durumları incelen

verilirken aşağıdaki kısaltmalar kullanılmaktadır (Itasca,

makaslama yeni

makaslama gerilmesine bağlı olarak yenilmen

dolayı yenilmenin durduğunu göstermektedir.

çekme yenil

Çekme  gerilmesine  bağlı

olarak  yenilm

<!-- image -->

Line chart

nedeniyle durduğunu göstermektedir.

a) Sol tünel üzerinde belirlenen noktalar   b) Sa

il 11. Modelde olu

Şekil 11. Modelde oluşturulan iç kaplama betonunun kesiti görünüşü

ş

N:

ğ

tünel üzerinde belirlenen noktalar b) Sağ tünel üzerinde belirlenen noktalar

Herhangi bir yenilmenin olmadığını göstermektedir. ğiş tirme ve gerilmelerin incelenebilmesi belirlenen noktalar Şekil 12. Model üzerinde yerdeğiştirme ve gerilmelerin incelenebilmesi belirlenen noktalar şü

ekil 12. Model üzerinde yerde

turulan iç kaplama betonunun kesiti görünü

Filiş  serisinde  açılan  tünel  için  sağ  tüneldeki  kazı  işle

Ş

lde meydana gelen yenilme durumları incelenmiştir. Flac3d programında yenilme Ayrıca tünelde meydana gelen yenilme durumları incelenmiştir.  Flac3d  programında  yenilme  durumları  verilirken  aşağıdaki kısaltmalar kullanılmaktadır (Itasca, 2002);

Shear-n: makaslama gerilmesine bağlı olarak yenilmenin olduğunu ve hala devam ettiğini göstermektedir.

Shear-p: makaslama gerilmesine bağlı olarak yenilmenin olduğunu ancak kuvvetlerin azalmasından dolayı yenilmenin durduğunu göstermektedir.

Tension-n: çekme gerilmesine bağlı olarak yenilmenin olduğunu ve hala devam ettiğini göstermektedir.

Tension-p: Çekme gerilmesine bağlı olarak yenilmenin olduğunu ancak kuvvetlerin azalması nedeniyle durduğunu göstermektedir.

N: Herhangi bir yenilmenin olmadığını göstermektedir.

Filiş serisinde açılan tünel için sağ tüneldeki kazı işlemi sırasında, ilk  etapta  üst  yarıda  ilk  10  m'lik  bölümün  kazısı  yapılmış daha sonra alt yarı ve invert kazılarına başlanmıştır. Metakristalin bölümde ise, üst yarıda 2 m kazı, daha sonra alt yarıda 2 m kazı işlemi ile beraber tünel kazısı bir bütün olarak devam etmiştir. Böyle 2 farklı sistemin seçilmesindeki temel etken ring kapanma mesafesinin tüneller üzerinde etkisini görebilmektir.

## 3.1.1. Filiş Serisi İçin Yapılan Statik Çözümler

Tünellerde en son aşamada meydana gelen yenilme durumları ile  yerdeğiştirme  değişimleri  incelenmiştir.    Oluşturulan  modellerde  statik  koşullarda  meydana  gelen  yenilme  durumları  Şekil 13'te verilmektedir.

Sol  tünelde  meydana  gelen  yenilme  durumuna  bakıldığında, üst yarıda makaslama kuvvetlerine bağlı olarak yenilmelerin oluştuğu ancak kuvvetlerin azalması ile durduğu gözlenmektedir. Alt yarı bölümünde ise, makaslama ve çekme kuvvetlerinin etkisiyle  yenilmelerin  meydana  geldiği,  ancak  kuvvetlerin  azalması ile sonlandığı görülmektedir. Sağ tünelde meydana gelen yenilme durumlarında ise, aynı şekilde alt yarı bölümünde makaslama ve çekme kuvvetlerine bağlı olarak yenilmelerin meydana geldiği ve kuvvetlerin azalması ile durduğu gözlenirken, üst yarıda ise etkin olarak  makaslama  kuvvetlerinin  etkisiyle  yenilmelerin  meydana geldiği ancak kuvvetlerin azalması ile yenilmelerin durduğu belirlenmiştir.

Şekil 14 ve Çizelge 3'te tünellerde meydana gelen yerdeğiştirmeler sunulmaktadır. Sol tünelde kazı işlemleri ile beraber üst yarı, alt yarı ve invert bölümlerinde yerdeğiştirmelerin devam ettiği gözlenmiştir. Sol tünelde kazı işlemlerinin durması ve sağ tünelde kazı işlemin başladığı durumda ise, sol tünelde değişimlerin durduğu gözlenmiştir. Bir anlamda tüneller arasında bırakılan mesafenin yeterli olduğu görülmüş ve tünellerin birbirine etkisinin olmadığı anlaşılmaktadır. Tünellerde meydana gelen değişimler sınır değerler içerisinde kalmıştır. Tünellerde yapılan kazı aşamaları  ve  destek  sistemleri  ile  tünel  duraylılığı  sağlanmıştır. Sağ tünelde ilk etapta üst yarıda 10 m'lik bölümün kazısı şeklinde başlamış ve bu aşamadan sonra alt yarı ve invert kazılarına geçilmiştir.  Seçilen  bu  yöntemde  üst  yarıda  kazı  aşamaları  sırasında değişimlerin sol tünele göre daha hızlı bir durumda olduğu görülmektedir. Meydana gelen değişimler kazı aşamalarının bitmesi ile beraber sabitlendiği ve tünel duraylılığını etkilemeyecek düzeyde kaldığı gözlenmiştir.

<!-- image -->

Engineering drawing

a) Sol tünel b) Sağ tünel b) Sağ tünel

a) Sol tünel

Şekil 13. Statik analiz sonucunda sol ve sağ tünelde meydana gelen yenilme durumu (kesit görünü Şekil 13. Statik analiz sonucunda sol ve sağ tünelde meydana gelen yenilme durumu (kesit görünüşü)

ş

ü)

Sol tünelde meydana gelen yenilme durumuna bakıldığında, üst yarıda makaslama kuvvetlerine bağlı

olarak yenilmelerin oluştuğu ancak  kuvvetlerin Çizelge 3. Tünellerde meydana gelen yerdeğiştirme ve gerilmeler

azalması

ile durduğu  gözlenmektedir.

Alt yarı

bölümünde  ise,  makaslama  ve  çekme  kuvvetlerinin  etkisiyle  yenilmelerin  meydana  geldiği,  ancak

| kuvvetlerin azalması ile sonlandığı aynı şekilde alt yarı Belirlenen noktalar                | görülmektedir. Sağ tünelde bölümünde makaslama ve çekme x yönü (mm)   | meydana gelen yenilme kuvvetlerine bağlı y yönü (mm)   | durumlarında olarak yenilmelerin z yönü (mm)   |
|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------------------------------------------|------------------------------------------------|
| meydana geldiği ve kuvvetlerin makaslama kuvvetlerinin etkisiyle Sol tünel 62 m tünel tavanı | azalması ile durduğu yenilmelerin meydana 1,84                        | gözlenirken, üst yarıda geldiği ancak kuvvetlerin 12,2 | etkin olarak azalması ile -89                  |
| yenilmelerin durduğu belirlenmiştir. Sol tünel 42 m alt yarı                                 | -8,63                                                                 | -1,97                                                  | -18,5                                          |
| 14 ve Çizelge 3'te tünellerde Sağ tünel 2 m tünel tavanı                                     | meydana gelen 8,94                                                    | yerdeğiştirmeler sunulmaktadır. -7,01                  | Sol tünelde kazı -156                          |

işlemleri ile beraber üst yarı, alt yarı

ve invert bölümlerinde yerdeğiştirmelerin devam  ettiği

gözlenmiştir. Sol tünelde kazı işlemlerinin durması ve sağ tünelde kazı işlemin başladığı durumda ise,

sol  tünelde  değişimlerin  durduğu  gözlenmiştir.  Bir  anlamda  tüneller  arasında  bırakılan  mesafenin

yeterli olduğu görülmüş ve tünellerin birbirine etkisinin olmadığı anlaşılmaktadır. Tünellerde meydana dü

Şekil 14. Sol tünel üst yarı 62. m'de, alt yarı 42.m'de ve sağ tünel 2.m'de  tünel kazı aşamalarına bağlı olarak meydana gelen Şekil 14. Sol tünel üst yarı 62. m'de, alt yarı 42.m'de ve sağ tünel 2.m'de  tünel kazı aşamalarına bağlı olarak meydana gelen düşey yerdeğiştirmeler

<!-- image -->

Line chart

ş

ey yerde

ğ

i

ş

tirmeler

| tünel ile sağ tünel Tünellerde Belirlenen noktalar                       | arasında bırakılan meydana gelen x yönü (mm)   | topuk değişimler y yönü (mm)   | ve z yönü (mm)   |
|--------------------------------------------------------------------------|------------------------------------------------|--------------------------------|------------------|
| kazı aşamaları ve tabakalarda sağ tünel için Sol tünel 62 m tünel tavanı | destek yapılan farklı 1,22                     | sistemleri ile modelleme 15,3  | tünel 10,3       |
| 10 m devam ederek Sol tünel 42 m alt yarı                                | daha sonra alt 8,00                            | yarı ve 26,9                   | invert 19,4      |
| Sağ tünel 2 m tünel tavanı                                               | 3,38                                           | 44,7                           | 67,8             |

3.1.2. Metakristalin Tabaka İçin Yapılan Statik Analiz Çözümler Metakristalin tabakada analizler sonucunda meydana gelen yenilme durumları Şekil 15' te sunulmaktadır.  Sol  tüneldeki  yenilme  durumları  incelendiğinde  alt  yarı  bölümünde  makaslama  ve çekme gerilmelerine bağlı olarak yenilmelerin oluştuğu ve kuvvetlerin azalmasıyla durduğu gözlenmiştir.  Üst  yarı  bölümünde  ise  etkin  olarak  makaslama  kuvvetlerin  etkisiyle  yenilmelerin meydana  geldiği  ve  zamanla  gerilmelerin  azalmasıyla  durduğu  gözlenmiştir.  Sağ  tüneldeki  yenilme durumlarında  ise  alt  yarı  bölümünde  makaslama  kuvvetlerin  etkisiyle  yenilmelerin  oluştuğu  ve gerilmelerin azalmasıyla durduğu gözlenirken invert bölümüne  yakın kısımlarında  makaslama kuvvetlerin  etkisiyle  yenilmelerin  devam  ettiği  görülmektedir.  Üst  yarı  bölümünde  ise  etkin  olarak makaslama kuvvetlerinin  etkisiyle  yenilmelerin  meydana  geldiği  ve  zamanla  kuvvetlerin  azalmasıyla durduğu  gözlenmiştir.  Şekil  16'da  ve  Çizelge  4'de  tünellerde  meydana  gelen  yerdeğiştirmeler  ve gerilmeler  sunulmaktadır.  Meydana  gelen  yerdeğiştirmelerden  de  görülebileceği  gibi,  filiş  serisine benzer  şekilde  sol  tünelde  kazı  işleminin  bitmesi  ile  beraber  sağ  tünel  kazısına  başlandığı  dönem sırasında yerdeğiştirmelerde bir değişim gözlenmemiş ve sabit olarak devam etmiştir. Bir anlamda sağ tünel kazısının sol tünele bir etkisinin olmadığını, sol tünel ile sağ tünel arasında bırakılan topuk ve ayna aralarındaki mesafelerin yeterli olduğunu göstermektedir. Tünellerde meydana gelen değişimler sınır  değerler  içerisinde  kalmıştır.  Tünellerde  yapılan  kazı  aşamaları  ve  destek  sistemleri  ile  tünel duraylılığı sağlanmıştır. Ayrıca filiş ve metakristalin tabakalarda sağ tünel için yapılan farklı modelleme aşamaları incelendiğinde, üst yarıda kazı işleminin 10 m devam ederek daha sonra alt yarı ve invert 3.1.2. Metakristalin Tabaka İçin Yapılan Statik Analiz Çözümler Metakristalin  tabakada  analizler  sonucunda  meydana  gelen yenilme  durumları  Şekil  15'  te  sunulmaktadır.  Sol  tüneldeki  yenilme  durumları  incelendiğinde  alt  yarı  bölümünde  makaslama ve  çekme  gerilmelerine  bağlı  olarak  yenilmelerin  oluştuğu  ve kuvvetlerin azalmasıyla durduğu gözlenmiştir. Üst yarı bölümünde ise etkin olarak makaslama kuvvetlerin etkisiyle yenilmelerin meydana  geldiği  ve  zamanla  gerilmelerin  azalmasıyla  durduğu gözlenmiştir. Sağ tüneldeki yenilme durumlarında ise alt yarı bölümünde makaslama kuvvetlerin etkisiyle yenilmelerin oluştuğu ve gerilmelerin azalmasıyla durduğu gözlenirken invert bölümüne yakın kısımlarında makaslama kuvvetlerin etkisiyle yenilmelerin devam ettiği görülmektedir. Üst yarı bölümünde ise etkin olarak makaslama kuvvetlerinin etkisiyle yenilmelerin meydana geldiği ve  zamanla  kuvvetlerin  azalmasıyla  durduğu  gözlenmiştir.  Şekil 16'da ve Çizelge 4'de tünellerde meydana gelen yerdeğiştirmeler ve gerilmeler sunulmaktadır. Meydana gelen yerdeğiştirmelerden de görülebileceği gibi, filiş serisine benzer şekilde sol tünelde kazı işleminin bitmesi ile beraber sağ tünel kazısına başlandığı dönem sırasında  yerdeğiştirmelerde  bir  değişim  gözlenmemiş  ve  sabit olarak devam etmiştir. Bir anlamda sağ tünel kazısının sol tünele bir etkisinin olmadığını, sol tünel ile sağ tünel arasında bırakılan topuk ve ayna aralarındaki mesafelerin yeterli olduğunu göstermektedir.  Tünellerde  meydana  gelen  değişimler  sınır  değerler içerisinde kalmıştır. Tünellerde yapılan kazı aşamaları ve destek sistemleri ile tünel duraylılığı sağlanmıştır. Ayrıca filiş ve metakristalin tabakalarda sağ tünel için yapılan farklı modelleme aşamaları incelendiğinde, üst yarıda kazı işleminin 10 m devam ederek daha sonra alt yarı ve invert kazılarının yapıldığı durumda tüneldeki yerdeğiştirmelerin daha hızlı olduğu gözlenmiştir. Metakristalin tabaka da ise; üst yarı, alt yarı ve invert kazılarının ardışık olarak yapılarak tünelin bir bütün olarak (tünel halkasının tamamlanması) destek görevini yapmasından dolayı yerdeğiştirmelerin daha yavaş düzeyde olduğu gözlenmiştir. Bu sonuç bize tünelin üst yarı, alt yarı ve invert kazılarının en kısa sürede bitirilmesi ve tünelin bir bütün olarak destek görevinin yapması tünel duraylılığı açısından önemini göstermektedir. Çizelge 4. Tünellerde meydana gelen yerdeğiştirmeler sürede  bitirilmesi  ve  tünelin  bir  bütün  olarak  destek  görevinin  yapması  tünel  duraylılığı  açısından önemini göstermektedir.

<!-- image -->

Engineering drawing

tünelde meydana gelen yenilme durumu

z yönü (mm)

10,3

19,4

67,8

Şekil 15. Statik analiz sonucunda sol ve sağ Şekil 15. Statik analiz sonucunda sol ve sağ tünelde meydana gelen yenilme durumu

<!-- image -->

Line chart

Şekil 16. Sol tünel üst yarı 62 m'de, alt yarı 42 m'de ve sağ tünel 2 m'de  tünel kazı aşamalarına bağlı olarak meydana gelen düşey yerde ğiştirmeler Şekil 16. Sol tünel üst yarı 62 m'de, alt yarı 42 m'de ve sağ tünel 2 m'de  tünel kazı aşamalarına bağlı olarak meydana gelen düşey yerdeğiştirmeler

4. Sonuçlar

## 4. Sonuçlar

Analizlerde yerdeğiştirmeler sınır değerler içerisinde kalmaktadır. Tünel kazısının ardışık olarak yapılması tünel stabilitesi açısından önemlidir. Üst yarı, alt yarı ve invert mesafeleri mümkün olduğunca erken tamamlanmalı ve tünel destek sistemleri bir bütün olarak çalışmalıdır.

İki tünel arasında bırakılan topuk mesafesi ile üst yarı aynaları arasındaki bırakılan mesafeler yeterli geldiği görülmüştür.

Zayıf zeminlerde açılan iki tünelin birbirine olan etkisinin en aza indirilmesi en önemli faktörlerden birisidir.

Her bir kaya sınıfı için bu mesafeler zemine göre revize edilmelidir. Aksi takdirde tünellerin birbirine olan etkisi tünel destek sistemlerinin stabilitesi üzerinde olumsuz etki yapacaktır.

Zayıf zeminlerde açılan tünellerde iç kaplama betonu tünelde deformasyonların sönümlenmesinden hemen sonra yapılmalıdır. Aksi takdirde oluşacak olan şişme ve sıkışma basınçları uzun dönemde dış kaplamanın stabilitesini olumsuz etkileyecektir.

Zayıf zeminlerde yapılacak olan iç kaplama uzun dönemde oluşabilecek olan şişme ve sıkışma basınçlarınıda karşılacak düzeyde olmalıdır. Bu bölgelerde iç  kaplama  donatılı olarak yapılmalıdır.

## Kaynaklar

- Aygar, E. B. 2000. Yeni Avusturya tünelcilik yöntemine eleştirel bir yaklaşım. [master tezi]. [Ankara]:Hacettepe University
- Aygar,  E.B.  2007.  Bolu  Tüneli  duraylılığının  satik  ve  dinamik  analiz yöntemleriyle  incelenmesi.  [doktara  tezi].  [Ankara]:  Hacettepe University.
- Aygar, E.B. 2020. Evaluation of new austrian tunnelling method applied to bolu tunnel's weak rocks. Journal of Rock Mechanics and Geotechnical Engineering 12 (2020) 541-556.
- Aygar, E.B. 2021a. An evaluation on causes behind the bolu tunnel collapse following the 12 November 2 1999 düzce earthquake: seismic action or inadequate tunnel support capacity, in Reviewer.
- Aygar,  E.B.  2021b.  An  assessment  on  problems  encountered  during tunneling in graphitic schists,  in Reviewer.
- Aygar,  E.B.,  Gokceoglu,  C.  2020.  Problems  encountered  during  a  railway tunnel excavation in squeezing and swelling materials and possible engineering measures: a Case study from turkey. Sustainability. 12, 1166, https://doi.org/10.3390/su12031166.
- Aygar,  E.B.  Gokceoglu  C.  2021a.  Evaluation  of  collapsed  zone  in  t24 tunnel (ankara-istanbul high speed railway project, turkey). Euroengeo. 3rd European Regional Conference of IAEG.
- Aygar,  E.B.,  Gokceoglu,  C.  2021b.  A  special  support  design  for  a  large-span tunnel crossing an activefault (t9 tunnel, ankara-sivas high-speed railway project, turkey). Environmental Earth Sciences, 80 (1), 37, https://doi.org/10.1007/s12665-020-09328-1.
- Aygar, E.B., Gokceoglu, C. 2021c. Analytical solutions and 3d numerical analyses of a shallow tunnel excavated in weak ground: a case from turkey. International Journal of Geo-Engineering. 12 (1), 9, DOI: 10.1186/s40703-021-00142-7.
- Aygar,  E.B.,  Gokceoglu,  C.  2021d.  Evaluation  of  collapse  mechanism and portal interaction of a high-speed railway tunnel (t29 Tunnel, turkey). Eurock 2021.Torino.
- Barla, G. 2002. Tunnelling mechanics tunnelling under squeezing rock conditions tunnelling mechanics - advances in geotechnical engi-
- neering and tunnelling (pp.169-268) chapter: 3 publisher: P.O.Box 1675 Editors: D. Kolymbas.
- Barla, G. 2016. Full-face excavation of large tunnels in difficult conditions.  Journal  of  Rock  Mechanics  and  Geotechnical  Engineering, (2016) 294-303.
- Dalgıç, S. 2002. Tunneling in squeezing rock, the bolu tunnel, anatolian motorway. turkey. Engineering Geology.
- Geoconsult ZT GmbH. 1998. Bolu tunnel geological longitudinal profile along left tube as built conditions, asarsuyu portal to elmalık portal.
- Geoconsult ZT GmbH. 2002. Anatolian motorway stretch-2 bolu tunnel by-pass rock support class distribuiton.
- Goel,  R.K.,  Jethwa,  J.L.,  Paithakan,  A.G.  1995.  Tunnelling  through  the young Himalayas - a case history of the Maneri-Uttarkashi power tunnel. Engrg. Geol., 39, pp. 31-44.
- Hoek, E. 2001. Big tunnels in bad rock, The 36th Karl Terzaghi lecture. Journal of Geotechnical and Geo-environmental Engineering, A.S. C.E., 127(9), 726-740.
- Hoek, E. 2007. Practical Rock Engineering, p 341, https://www.rocscience.com/assets/resources/learning/  hoek/Practical-Rock-Engineering-Full-Text.pdf.
- Hoek, E. 2012. Rock Support Interaction analysis for tunnels in weak rcok masses,  https://www.rocscience.com/documents/pdfs/rocnews/winter2012/Rock-Support-Interaction-Analysis-for-Tunnels-Hoek.pdf.
- Hoek, E., Marinos, P. 2000. Predicting tunnel squeezing. Tunnels and Tunnelling International. Part 1 - November 2000, Part 2.

Itasca, 2002. Flac3d User Manual Getting Started.

- Jethwa, J. L. 1981. Evaluation of rock pressures in tunnels through squeezing ground in lower himalayas. PhD thesis.Department of Civil Engineering. University of Roorkee,India, 272.
- KGM (General Directorate of Highways). 2013. Technical specifications of general directorate of highways.
- Lettis,  W.  &amp;  Asssociates Inc.,  A.Barka, 2000. Geologic Characterisation of Fault Rupture Hazard, Gümüşova-Gerede Motorway project report.

Lunardi, P. 2000a. The underground as a resource and reserve for new spaces; adec-rs as an effective tool to be able to realize them (part 1). Proceedings of the Bindi R, Cassani G World Tunnel Congress 2014 - Tunnels for a better Life. Foz do Iguaçu, Brazil.

- Lunardi, P. 2000b. The underground as a resource and reserve for new spaces; adeco-rs as an effective tool to be able to realize them (part 2). Proceedings of the Bindi R, Cassani G World Tunnel Congress 2014 - Tunnels for a better Life. Foz do Iguaçu, Brazil.
- Lunardi, P. 2008. Design and construction of tunnels, analysis of controlled deformation in rocks and soils (adeco-rs). 587 p.
- Lunardi, P. 2014. The design and construction of tunnels using the approach based on the analysis of controlled deformation in rocks and soils. T&amp;T Interneational ADECO-RS Approach, www.rocksoil.com.
- Lunardi,  P.  2016.  Evolution  of  design  and  construction  approaches in the field of tunnelling: the results of applying ADECO-RS when constructing large underground works in urban areas. Procedia Engineering, 165, 484 - 496.
- Rabcewicz, L. 1964a.The new austrian tunnelling method, part one. Water Power. 453-7.

- Rabcewicz, L. 1964b. The new austrian tunnelling method, part two. Water Power 1964b; 511-5.
- Rabcewicz L. 1965. The new austrian tunnelling method, part three. Water Power 1965; 19-24.
- Rabcewicz,  L,  Golser  J.  1973.  Principles  of  dimensioning  the  supporting system for the 'new austrian tunnelling method'. Water Power, Marc, 88-93.
- Sakurai,  S.  1983.  Displacement  measurements  associated  with  the

design of underground openings. Proc. Int. Symp. Field Measurements in Geomechanics, Zurich 2, 1163-1178.

- Schubert, W. 1996. Dealing with squeezing conditions in Alpine tunnels.' Rock Mech. Rock Engng. 29(3), 145-153.
- Singh, B., J, L., Jethwa, A. R., Dube, B., Singh. 1992. Correlation between observed support pressure and rock massquality.' Tunnelling and Underground Space Technology. 7(1).
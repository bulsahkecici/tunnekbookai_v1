## Kazı Derinliğinin Püskürtme Beton Dayanımı Üzerindeki Etkisi: Sayısal Bir Yaklaşım

Effect of Excavation Depth on Shotcrete Strength: A Numerical Approach

## Mustafa KANIK* a , Zülfü GÜROCAK b

Fırat Üniversitesi Mühendislik Fakültesi, Jeoloji Mühendisliği Bölümü, 23119, Elazığ

- Geliş tarihi / Received : 17.08.2017
- Düzeltilerek geliş tarihi / Received in revised form : 27.10.2017

· Kabul tarihi / Accepted

: 30.10.2017

## Öz

Uygun  ve  güvenilir  destek  sistemlerinin  seçimi,  tünelcilikte  maliyet  ve  güvenliği  etkileyen  en  önemli  faktörlerden birisidir.  Farklı  araştırmacılar  tarafından  önerilmiş  olan  görgül  kaya  sınıflama  yöntemleri  destek  tipinin  seçiminde büyük kolaylık sağlamaktadır. Bu konuda kullanılan diğer bir yöntem  sayısal analizlerdir. Görgül olarak elde edilen destek tipinin sayısal olarak da analiz edilmesi sonucunda daha güvenilir ve ekonomik destek tipi belirlenebilmektedir. Bu  çalışmada,  farklı  kaya  sınıfları  için  RMR89  tarafından  önerilen  püskürtme  betonun  dayanımı  ile  kazı  derinliği arasındaki ilişkileri incelemek amacıyla Sonlu Elemanlar Yöntemi (FEM) kullanılarak sayısal modellemeler yapılmıştır. Modellemelerde, Zayıf, Orta ve İyi kaliteli kaya sınıfındaki kaya kütleleri ve farklı kazı derinlikleri dikkate alınmıştır. Kazı derinliğinin artması bağlı olarak, destek sisteminin yenilmeden çalışabilmesi için püskürtme beton dayanımının ne kadar olması gerektiği araştırılmıştır. Yapılan analizlere göre püskürtme beton dayanımının 30 MPa alınması durumda, İyi  kaliteli  Kaya  sınıfında  450  m,  Orta  kaliteli  Kaya  sınıfında  310  m,  Zayıf  kaliteli  Kaya  sınıfında  ise  200  m  kazı derinliğinde  püskürtme  betonda  yenilmeler  meydana  gelmektedir.  Bu  derinliklerden  sonra  destek  sisteminin  duraylı kalabilmesi  için  püskürtme  beton  dayanımının  artırılması  gerekmektedir.  Püskürtme  beton  dayanımı  40  MPa'ya çıkarıldığında, İyi kaliteli Kaya sınıfında 530 m, Orta kaliteli Kaya sınıfında 420 m ve Zayıf kaliteli Kaya sınıfında ise 260 m kazı derinliğine kadar destek elemanlarında yenilme meydana gelmemektedir. İyi kaliteli kaya sınıfında 20 MPa dayanımlı püskürtme beton için yapılan analizlerde, 410 m örtü kalınlığına kadar destek sisteminde yenilme meydana gelmemektedir.  Bu  çalışmadan  elde  edilen  sonuçlar,  kazı  derinliğinin  artması  sonucunda,  destek  sistemlerinin yenilmemesi  için  püskürtme  beton  dayanımın  artırılması  veya  bir  alt  kaya  sınıfı  için  önerilen  destek  sistemlerinin seçilmesi gerektiğini göstermektedir.

Anahtar kelimeler:

Kazı derinliği, Püskürtme beton dayanımı, RMR sınıflama sistemi, FEM analizi

## Abstract

Choosing appropriate and reliable support systems is one of the most important factors affecting cost and security in tunneling. The empirical rock classification methods proposed by different researchers provide great convenience in selecting  the  support  type.  Another  method  used  in  this  regard  is  numerical  analysis.  With  the  aid  of  the  numerical analyses, analyzing the support system empirically obtained helps to determine more reliable and economic support types.  In  this  study,  numerical  models  were  developed  using  Finite  Elements  Method  (FEM)  to  investigate  the relationship  between  the  strength  of  shotcrete  and  the  excavation  depth  for  the  different  rock  classes  proposed  by RMR89. Different  excavation  depths  for  Weak,  Fair  and  Good  rock  masses  are  taken  into  account  in  the  modeling. Depending on the increase in depth of excavation, it has been researched how much the strength of the shotcrete must be so that the support system can continue to support without being yielded. According to the evaluated models, when the shotcrete strength is assumed as 30 MPa, the elements of shotcrete was started to yielded at 200 m depth for the weak  rock  mass,  310  m  depth  for  the  fair  rock  mass  and  450  m  depth  for  the  good  rock  mass.  After  reaching  the mentioned depths, it is necessary to increase the strength of the shotcrete in order to keep the support system stable. Once the shotcrete strength is increased to 40 MPa, there was not failure in the support elements up to the excavation depth of 530 m in the good rock mass, 420 m for fair rock mass and 260 m for the weak rock mass. The support system was determined stable up to 410 m overburden in the evaluated analyses for 20 MPa strengthen shotcrete. In this study, it is revealed that, the increase in depth of excavation indicates that the strength of the shotcrete must be increased to avoid instabilities of the support systems or that the support systems recommended for a lower rock class should be selected.

Keywords : Excavation depth, Numerical modeling, RMR classification system, Shotcrete strength

* a  Zülfü GÜROCAK; zgurocak@gmail.com; Tel: (0532) 355 36 47; orcid.org/0000-0002-1049-8346

b orcid.org/0000-0002-1019-5249

## 1. Giriş

Tünelcilikte maliyet üzerindeki en önemli parametrelerden  birisi,  tünelde  kullanılacak  olan destek  sistemlerinin  çeşididir.  Bu  parametre  kazı sırasında geçilecek birimlerin jeolojik ve jeoteknik özellikleri ile doğrudan ilişkilidir. Tünel güzergâhındaki  birimlerin  jeolojik  ve  jeoteknik özelliklerinin belirlenebilmesi ise tünel güzergâhı boyunca sondaj ve yüzey çalışmalar ile mümkündür. Tünelcilikte ön  destek  sistemlerinin saptanması amacıyla farklı araştırmacılar tarafından birçok kaya  kütle sınıflama sistemi önerilmiştir (Terzaghi, 1946; Lauffer, 1958; Deere, 1964; Wickhamvd., 1972; Bieniawski, 1989; Barton vd., 1974; Palmström, 1995). Önerilen bu sistemler zaman zaman revize edilerek günümüzdeki halini almıştır.

Terzaghi (1946) tarafından önerilen sınıflama sistemi 35  yıldan fazla bir süre etkili olarak kullanılmıştır.  Lauffer  (1958)  ise,  Stini  (1950) tarafından yapılan bir çalışmadan esinlenerek, destek sisteminin çeşidi ve miktarını tünel genişliği ve desteksiz durma süresine bağlı olarak belirlemeye çalışmıştır. Deere (1964) sondaj karotlarından belirlenebilen Kaya Kalite Göstergesi  (RQD)  parametresini  kullanarak  bir sınıflama önermiştir. Wickham vd. (1972) tarafından Amerika Birleşik Devletleri'nde geliştirilen kaya yapısı değerlendirmesi  (RSR) kavramı, sınıflandırma parametrelerinin nispi önemini  ölçmek  için  yapılan  ilk  sınıflandırma sistemdir.  Bieniawski  (1989)  tarafından  önerilen Kaya  Kütle  Puanlama  (RMR)  ve  Barton  vd. (1974)  tarafından  önerilen  Kaya  Kütle  Kalitesi (Q) sistemleri birbirlerinden bağımsız olarak geliştirilmişlerdir.

Bu sınıflama sistemlerinin ikisi de kaya bulonu ve püskürtme  beton  gibi  modern  tünel  güçlendirme yöntemlerinin seçimini sağlayacak niceliksel veriler sağlamaktadırlar. Kaya Kütle İndeksi (RMi)  sınıflama sistemi Palmström  tarafından 1995 yılında, Jeolojik Dayanım İndeksi (GSI) ise ilk  defa  Hoek  vd.  (1995)  tarafından  önerilmiştir. Q,  RMR,  RMi  ve  GSI  sistemleri  zaman  içinde revize edilerek günümüzdeki şeklini almışlardır.

Ayrıca, destek tipinin kazı sırasında belirlenmesinde Yeni Avusturya Tünel  Açma Yöntemi (NATM) sistemi de yaygın olarak kullanılmaktadır.  Bu  metotta  diğer  sistemler  gibi kesin önerilmiş destek elemanları yerine kullanılması  gereken  destek  elemanlarının  türü belirtilmiş olup, destek elemanı sistematiği uygulayıcılar tarafından belirlenmektedir.

## 2. Tünelcilikte Destek  Sistemlerinin  Görgül Olarak Belirlenmesi

Tünelcilikte ön destek sistemlerinin belirlenmesinde temeli puanlama metoduna dayanan RMR, Q ve RMi sistemleri yaygın olarak kullanılmaktadır.  Bu  sınıflamalarda  puanlamalar genel olarak kaya malzemesinin mekanik özellikleri, süreksizliklerin özellikleri ve su durumuna göre yapılmakta ve elde edilen sonuca göre  ön  destek  sistemi  belirlenmektedir.    Yaygın olarak kullanılan bu sistemlerinin avantajları yanında dezavantajları da vardır.

Bu görgül sınıflama sistemlerinin avantajları maddeler halinde sıralanacak olursa:

-  Kaya kütleleri sınıflandırılırken, girilen veriler sistematik olarak tanımlandığından saha araştırmalarının kalitesi daha da artmaktadır.
-  Bu sınıflamalarda nicel bir değerlendirme yapıldığından kişisel değerlendirmelere kıyasla daha güvenilir sonuçlar elde edilmektedir.
-  Sınıflandırma, her kaya kütlesinin kilit parametreleri için bir kontrol listesi oluşturmaktadır. Diğer bir deyişle, kaya kütlesinin tanımlanması sürecini yönlendirmektedir.
-  Sınıflandırma,  tasarım  amaçlı  nicel  bilgilerle sonuçlanmakta  ve  bir  proje  üzerinde  daha  iyi mühendislik  kararı  ve  etkili  iletişim  imkânı sağlamaktadır (Bieniawski, 1993).
-  Nicel bir sınıflandırma, belirli bir projede sağlıklı mühendislik yargısı için  uygun  ve etkili  iletişim  sağlamaya  yardımcı  olmaktadır (Hoek, 2007).
-  Kaya kütlesinin kalitesi ve mekanik özellikleri arasındaki ilişkiler kaya kütlesinin deformasyon, dayanım veya şişme özelliklerini belirlemek ve tahmin etmek için de kullanılabilmektedir.

Dezavantajları bakımından ele alındığında;

-  Tek bir sınıflama sisteminden elde edilen sonuçların  diğer  sistemler  ile  karşılaştırmadan kullanılması, analitik ve gözlemsel tasarım metotlarını göz ardı etmekte ve projedeki olası duraylılık problemlerini önleyememektir.
-  Kaya  kütlesi  sınıflama  sistemlerinin,  üzerinde geliştirildikleri veri  tabanından  kaynaklanan sınırlamaların tam olarak anlaşılmadan kullanılması durumunda güvenilir sonuçlar elde edilememektedir (Bieniawski, 1993).
-  Elde edilen sonuçlarının yanlış değerlendirilmesi  veya  kullanılması  gerçekçi

- olmayan  destek  seçiminin  yapılmasına  neden olabilmektedir.
-  Sınıflandırma sistemlerinin yardımıyla belirlenen destek sisteminin gerçekçiliğinin, uygulamaya geçilmeden önce test edilememesi zorluklara  veya  duraylılık  problemlerine  yol açabilmektedir.
-  Kaya kütle sınıflama sistemleri tarafından önerilen destek elemanlarına (püskürtme beton, kaya bulonu, vb) ait teknik özelliklerin (püskürtme beton dayanımı, kaya bulonu çapı ve dayanımı) tanımlanmamış olması nedeniyle tasarım sırasında güçlüklerle karşılaşılabilmektedir.

Ön destek tasarımın uygulama aşamasındaki güvenirliliği, son yıllarda sıklıkla kullanılan sayısal analizler yardımıyla test edilmektedir.  Bu konuda  yapılan  çalışmalarda  (Geniş  vd.,  2007; Gürocak  vd.,  2007;  Gürocak,  2011;  Kaya  vd., 2011;  Kaya  ve  Bulut,  2013,  Kanık  vd.,  2015; Yalçın vd., 2016, Kaya ve Sayın, 2017) RMR, Q ve RMi gibi görgül sınıflamalar ve sayısal analizler birlikte kullanılmış ve destek tasarımında ampirik ve sayısal yöntemlerin bütünleştirilmesinin önemi ortaya konulmaya çalışılmıştır.  Görgül  olarak  belirlenen  ön  destek sistemlerinin güvenirliliğinin sayısal yöntemler ile analiz edilmesi, daha gerçekçi destek sistemlerinin belirlenebilmesine imkân tanımaktadır.

Bu çalışmanın amacı, görgül sistemler tarafından önerilen  püskürtme  beton  dayanımının  derinlikle olan  ilişkisini  ortaya  koymaktır.  Nitekim  görgül sistemler destek sistemi olarak püskürtme betonu önermekte ancak uygulanacak püskürtme betonun dayanımı hakkında herhangi bir öneride bulunmamaktadır. Bu nedenle, uygulama sırasında genellikle 30 MPa  dayanıma sahip püskürtme beton kullanılmaktadır. Ancak, duraylılığı sağlamak amacıyla artan kazı derinliği ile birlikte püskürtme beton dayanımının da artırılması gerekliliği düşünüldüğünde, kazı derinliği ile püskürtme beton dayanımı arasındaki ilişkinin önemli olduğunu söylemek mümkündür.

Günümüze kadar püskürtme beton tasarımı konusunda farklı araştırmacılar tarafından yapılmış  bir  çok  çalışma  bulunmaktadır  (Wood vd., 1993; Kirsten, 1992; Beauprè vd., 2005; Badr ve  Brooks,  2008;  Patel  vd.,  2012;  Barros  vd., 2014;  NIOSH,  2014;  Zhang,  2014;  Mohajerani vd., 2015; Badr, 2016). Bu çalışmalar genel olarak püskürtme betonun tasarımı ve dayanımının artırılması  konusundadır.  Artan  kazı  derinliği  ile püskürtme  betonun  dayanımının  ne  kadar  olması

gerektiği konusunda yapılmış herhangi bir çalışma bulunmamaktadır.

Bu  çalışmada,  kazı  derinliğinin  püskürtme  beton dayanımı  üzerindeki  etkisini  incelemek  amacıyla sayısal analizlerden yararlanılmış ve bu etki ortaya  çıkarılmaya  çalışılmıştır.  Bu  amaçla,  en yaygın olarak kullanılan görgül yöntemlerden birisi  olan  RMR89  sistemine  ait  kaya  sınıfları dikkate alınmıştır.

Görgül bir kaya kütle sınıflama sistemi olan RMR Sınıflama Sistemi, ilk kez 1972-1973 yılları arasında yapılan çalışmalar sonucunda Bieniawski (1973)  tarafından  geliştirilmiştir.  Sınıflamaya  ait parametreler  ve  bu  parametrelere  ait  puanların belirlenmesi konusunda yine Bieniawski tarafından 1989 yılında yapılan öneriler ile modifiye  edilen  RMR  sınıflaması  (RMR89),  son olarak  2014  yılında  yapılan  değişiklikler  (Celada vd.,  2014)  ile  son  halini  almıştır.  Yaygın  olarak kullanılması ve kabul edilmiş olması sebebiyle bu çalışmada RMR sisteminin 1989 versiyonu tercih edilmiştir.

RMR14'ün  önerilmesinden  önce  uzunca  bir  süre kullanılan RMR89 sistemi aşağıdaki girdi parametrelerini kullanmaktadır;

-  Kayacın  tek eksenli basınç dayanımı  veya nokta yükü dayanım indeksi,
-  Kaya kalitesi göstergesi (% RQD)
-  Süreksizlik ara uzaklığı
-  Süreksizliklerin  durumu  (devamlılık,  açıklık, pürüzlülük, dolgu ve bozunma)
-  Yeraltı suyu durumu

RMR73 versiyonunda dayanım, RQD ve süreksizlik ara uzaklığı için yapılan değerlendirmeler  aralıkların  sınır  değerlerini  de kapsamaktaydı ve bu durum uygulamada hatalara sebep olmaktaydı. Bu üç parametrenin daha hassas  puanlanabilmesi  için  Bieniawski  (1989), ISRM (1981) tarafından önerilen tanımlama ölçütlerini esas alınarak çeşitli abaklar geliştirilmiştir.

RMR89'a göre kaya  kütlesinin  temel  RMR  puanı belirlendikten sonra süreksizlik düzeltmeleri yapılıp nihai RMR puanı elde edilmektedir. Daha sonra düzeltilmiş RMR puanı ile kaya sınıfı ve ön destek önerileri Tablo 1'den belirlenmektedir.

## 3. Sayısal Modellemeler

Bu  çalışmada, analiz modelleri oluşturulurken Sonlu Elemanlar Yönteminden (FEM) yararlanılmıştır.

Tablo 1. RMR89 sistemine göre kaya kütle sınıfları için önerilen birincil destekler (Bieniawski, 1989).

| BİRİNCİL DESTEK   | BİRİNCİL DESTEK                                                                                                                                             | BİRİNCİL DESTEK                                                                                  | BİRİNCİL DESTEK                                                                             | BİRİNCİL DESTEK                                                                             |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Kaya Kütle Sınıfı | Kazı                                                                                                                                                        | Kaya sapmaları * (10 m genişlikteki tünel için uzunluk)                                          | Püskürtme beton                                                                             | Çelik destek                                                                                |
| I                 | Tam kesit, 3 m ilerleme. Bir miktar kaya saplaması haricinde genellikle destek gerektirmez.                                                                 | Tam kesit, 3 m ilerleme. Bir miktar kaya saplaması haricinde genellikle destek gerektirmez.      | Tam kesit, 3 m ilerleme. Bir miktar kaya saplaması haricinde genellikle destek gerektirmez. | Tam kesit, 3 m ilerleme. Bir miktar kaya saplaması haricinde genellikle destek gerektirmez. |
| II                | Tam kesit, 1.0-1.5 m ilerleme, tam kazı destek. Aynaya 20 m mesafede                                                                                        | Kemerin her 2-3 m' sinde yer yer saplama, tel kafeslerle 2-2.5 m aralıklı.                       | Gerektiğinde tavan kemerinde 50 mm.                                                         | Gerekmez                                                                                    |
| III               | Tavan kemeri ve tabandan ilerleme. Tavandan 1.5-3 m ilerleme. Tam kazı destek. Aynaya 10 m mesafeye kadar gerekli.                                          | 3-4 m uzunlukta sistematik saplamalar, kemerde tel kafesli duvarlar ve kemerde 1.5-2 m aralıklı. | Tavan kemerinde 50- 100 mm ve yan duvarlarda 30 mm.                                         | Gerekmez                                                                                    |
| IV                | Tavan kemeri ve tabandan ilerleme. Tavandan 1.0-1.5 m ilerleme. Kazıya uygun şekilde aynaya 10 m mesafeye kadar, gerekli destek.                            | Tel kafesli duvarlarda ve kemerde 1-1.5 m aralıklı, 4-5 m uzunlukta sistematik saplama.          | Tavan kemerinde 100- 150 mm ve yan duvarlarda 100 mm.                                       | Gereken yerde 1.5 m aralıklı yer yer hafif traversler.                                      |
| V                 | Tavan ve tabanda birlikte ilerleme. Tavandan 0.5-1 m ilerleme, kazıyla birlikte destek yerleştirilmeli. Patlamadan hemen sonra püskürtme beton uygulanmalı. | Tel kafesli duvarlarda ve kemerde 1-1.5 m aralıklı, 5 m uzunlukta sistematik saplama.            | Tavan kemerinde 150- 200 mm, yan duvarlarda 150 mm, aynada 50 mm.                           | Çelik iksalı, 0.75 m aralıklı orta-ağır traversler.                                         |

Bu yöntemin temeli, karmaşık bir problemi basit ve küçük parçalara bölerek çözme esasına dayanmaktadır.  Böylece,  kesin  sonuçtan  ziyade yaklaşık  bir  sonuç  elde  edilebilmekte  ve  elde edilen  yaklaşık  sonucun  üzerinde  çalışarak  kesin bir sonuç elde etmek mümkün olmaktadır. Rocscience  (2011)  tarafından  geliştirilmiş  olan Phase 2 v8.0 (Plastic Hybrid Analysis of Stress for Estimation of Support) bilgisayar programı kullanılarak geliştirilen modellemelerde 6 düğümlü  üçgen  sonlu  elemanlar  kullanılmış  ve tünelin 5 katı genişliğinde bir kaya ortamı oluşturulmuştur. Modellemeler, 10 m genişliğinde,  7  metre  yüksekliğinde,  tek  tüp,  at nalı  kesitindeki  zayıf,  orta  ve  iyi  kaliteli  kaya sınıfındaki  kaya  kütleleri  için  RMR89  sisteminin önerdiği ön destek sistemleri için farklı derinliklerde yapılmıştır (Şekil 1).

Buradaki amaç, kazıdan sonra uygulanan püskürtme betonun yenilmeden işlevini sürdürebilmesi  için  değişen  derinliklerde  hangi dayanıma sahip olması gerektiğinin belirlenebilmesidir. Analizlerde, maksimum toplam yer değiştirme (Ut) ve plastik zon kalınlığındaki  (Tpl)  değişimler  dikkate  alınmış  ve 10 m  örtü kalınlığından başlayıp farklı kaya sınıfları  için  550  m  derinliğe  kadar  yapılmıştır. Her bir derinlikte zayıf ve orta kaliteli kayalar için beton dayanımının hem 30 MPa hem de 40 MPa olduğu,  iyi  kaya  için  ise  beton  dayanımının  20 MPa, 30 MPa ve 40 MPa olduğu durumlara göre sayısal  analizler  yapılmıştır.  Sayısal  analizlerde, derinlik  arttıkça  zayıf  ve  orta  kayada  püskürtme beton dayanımının yetersiz kalma olasılığının yüksek olmasından dolayı duraysızlık durumunda beton  dayanımı  40  MPa'  ya  yükseltilerek  yeni analizler yapılmıştır. 30 MPa'lık püskürtme beton dayanımının iyi kaya için belli bir derinliğe kadar gereğinden yüksek olabilmesi olasılığından dolayı 20  MPa  dayanımlı  püskürtme  beton  kullanılarak analizler yapılmıştır.  30  MPa  dayanıma  sahip püskürtme betonun referans değer olarak alınmasının sebebi ise, bu değerin yapılan çalışmalar (Celada vd., 2014) ve teknik şartnamelerde  (KGM,  1997)  istenen  püskürtme beton dayanımı olarak kabul edilmesidir.

## 3.1.  Farklı  Kaya  Sınıfları  ve  Derinlikler  için Yapılan Sayısal Modellemeler

Modellemeler yapılırken, kaya türü olarak magmatik  kaya  ve  RMR89  sistemine  göre  zayıf (IV),  orta  (III)  ve  iyi  (II)  kaya  sınıfına  ait  kaya kütleleri  seçilmiştir.  Sadece  Zayıf,  Orta  ve  İyi kaliteli kaya sınıflarının seçilmesinin sebebi, Çok İyi  kaliteli  kaya  kütlelerinde  püskürtme  betonun destekten  ziyade  emniyet  için  kullanılması,  Çok Zayıf kaliteli  kaya kütlelerinde ise çelik iksa desteğinin ön planda olması ve püskürtme betonun ikinci planda kaldığının düşünülmesidir.

Sayısal analizlerde girdi parametresi olarak kullanılacak  veriler  ise  fay  ve  kıvrım  içermeyen (fay  ve  kıvrımlanma  olan  bölgelerdeki  değişken gerilme  dağılımlarını  göz  ardı  etmek  amacıyla), bloklu ve çok bloklu kayaların Hoek-Brown sabitleri,  GSI  değerleri,  Poisson  oranları,  kaya malzemesinin  ve  kaya kütlesinin  deformasyon modülleri  Hoek  vd.  (1995)  tarafından  verilen  ve RocLab  (Rocscience,  2006)  programı  yardımıyla hesaplanan değerler kullanılarak belirlenmiştir. Birim hacim ağırlıklar (  ) her bir kaya kütlesi için 26  kN/m 3 ,    tek  eksenli  sıkışma  dayanımı  değeri (  c )  ise  her  bir  kaya  sınıfı  için  ortalama  değerler olarak kabul edilmiştir.

Şekil 1. Zayıf, Orta ve İyi kalitedeki kaya kütleleri için oluşturulan modeller.

<!-- image -->

Engineering drawing

GSI,  mb,  s,  a  için  artık  değerler  Cai  vd.  (2007) tarafından önerilen eşitlikler ile belirlenmiştir.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Tüm kaya  kütle  özellikleri  ve  sayısal  analizlerde kullanılan girdi parametreleri ve bu parametrelere ait değerler Tablo 2'de verilmiştir. Ayrıca, kullanılan  destek  elemanlarının  teknik  özellikleri de Tablo 3' de sunulmuştur.

Tünel  kazı  kotundaki  düşey  (σv)  ve  yatay  (σh), gerilmeler, her derinlik için ayrı olarak hesaplanmıştır. Düşey gerilme (σv) değerleri, Fenner (1938) tarafından önerilen eşitlik kullanılarak hesaplanmıştır.

<!-- formula-not-decoded -->

Bu eşitlikte;

γ: Birim hacim ağırlık (kN/m 3 ),

H: Örtü kalınlığı (m) dır.

Yatay gerilme (σh) ise çok değişken ve belirlenmesi zor olan bir parametredir. Yatay gerilmeyi belirleyebilmek için Sheorey vd. (2001) tarafından önerilen eşitlikten yararlanılmıştır.

<!-- formula-not-decoded -->

Bu eşitlikte;

 :  Doğrusal  termal  genleşme  katsayısı  (8  x  10 6 / o C),

G: Jeotermal gradyan (0.024 o C/m),

ѵ : Poisson oranı,

H: Örtü Kalınlığı (m)

Em: Kaya kütlesinin deformasyon modülü (GPa).

İlk  aşamada,  sayısal  analizler  Zayıf,  Orta  ve  İyi kaliteli kaya sınıfları için desteksiz duruma

-

göreyapılmıştır.  Daha  sonra  RMR89 tarafından önerilen  ve  Tablo  1'de  verilen  destek  sistemleri seçilmiş ve  her  10  m'de  bir  sayısal  analizler yapılmıştır.  Ancak,  sayısal  analizlerde,  belli  bir derinlikten  sonra  birbirlerine  yakın  değerler  elde edildiğinden dolayı 10 m örtü kalınlığından başlayıp sırasıyla 50 m ve katlarına karşılık gelen derinlikler için yapılmıştır.

Tablo 2. Sayısal analizlerde kullanılan girdi parametreleri

|            | Zayıf Kaya   | Orta Kaya   | İyi Kaya   |
|------------|--------------|-------------|------------|
|  v , MPa  | 0.26-13.78   | 0.26-11.7   | 0.26-11.7  |
|  h , MPa  | 0.08-3.89    | 0.1-4.55    | 0.09-3.91  |
|  ci , MPa | 30           | 75          | 150        |
| E i , GPa  | 12000        | 27500       | 55000      |
| ν          | 0.28         | 0.25        | 0.22       |
|  , kN/m 3 | 26           | 26          | 26         |
| E m , GPa  | 7000         | 14000       | 32000      |
| GSI        | 43           | 55          | 70         |
| m i        | 18           | 20          | 25         |
| m b        | 2.351        | 4.009       | 8.563      |
| m br       | 1.199        | 1.439       | 1.8701     |
| s          | 0.0018       | 0.0067      | 0.0357     |
| s r        | 0.00022      | 0.00028     | 0.00031    |
| a          | 0.509        | 0.504       | 0.501      |
| a r        | 0.533        | 0.529       | 0.527      |

Yapılan sayısal analizlerin sonuçlarına göre, püskürtme beton dayanımı 30 MPa olarak alındığında Zayıf kaliteli kaya  sınıfı için  200 m'den sonra püskürtme betonda yenilmeler ortaya çıkmaktadır (Şekil 2, Tablo 4). Orta kaliteli kaya sınıfı için ise 30 MPa  dayanımlı püskürtme betonlu destek sistemi 310 m derinlikte, İyi kaya sınıfında ise 450 m derinlikte yenilmeye başlamıştır(Şekil 2, Tablo 5 ve 6).

Zayıf kaliteli kaya sınıfında püskürtme beton dayanımının 40 MPa olarak alınması durumunda, püskürtme betondaki yenilmeler 260 m'den itibaren başlamaktadır. Orta kaliteli kaya sınıfında püskürtme betondaki yenilmeler 420 m'den sonra, iyi  kaliteli  kaya  sınıfında  ise  530  m'den  sonra başlamaktadır (Şekil 3, Tablo 4, 5 ve 6).

Püskürtme  betonda meydana  gelen  yenilmeler kırmızı renk ile gösterilmiş olan bölgelerde meydana  gelmektedir.  Yenilen  bölgelerde  çelik hasırların  güvenlik  katsayılarının  destek  kapasite diyagramlarında 1 in üstünde olması, yenilmelerin püskürtme beton dayanımının yetersizliğinden kaynaklandığını  göstermektedir  (Şekil  2  ve  3). Destek kapasite diyagramlarında daire içine alınmış  olan  destek  elemanları,  tünel  kesitinde daire içine alınmış  yenilen  püskürtme  betonla birlikte hareket eden çelik hasırı temsil etmektedir.

Ayrıca İyi kaliteli kaya sınıfında sığ derinliklerde 30 MPa püskürtme beton dayanımının fazla olabileceği düşünülerek 20 MPa dayanımlı püskürtme beton için de sayısal analizler yapılmış ve sonuç olarak püskürtme betondaki yenilmelerin 410 m'den sonra başladığı görülmüştür (Şekil 4). Tablo  7'de  verilen  değerlere  bakıldığında,  gerek plastik zon kalınlıkları gerekse toplam yer değiştirme  değerlerinde  yenilme  olan  derinliğe kadar bir farklılık olmadığı görülmektedir. Dolayısıyla,  İyi  kaliteli  kaya  sınıfı  için  yaklaşık 410 metre derinliğe kadar 20 MPa'lık püskürtme beton dayanımı yeterli olmaktadır.

Tablo 3. Sayısal analizlerde kullanılan destek elemanlarının karakteristik özellikleri

| Özellikler                               | Püskürtme beton   | Kaya bulonu   | Çelik hasır       |
|------------------------------------------|-------------------|---------------|-------------------|
| Elastisite modülü, (GPa)                 | 30                | 200           | 200               |
| Poisson oranı,                           | 0.2               | -             | 0.35              |
| Tek eksenli basınç dayanımı, (MPa)       | 30                | -             | 500               |
| Artık tek eksenli basınç dayanımı, (MPa) | 3.0               | -             | -                 |
| Çekme dayanımı, (MPa)                    | -                 | -             | 500               |
| Artık dayanımı, (MPa)                    | -                 | -             | -                 |
| Çekme kapasitesi (MN)                    | -                 | 0.2           | -                 |
| Artık Çekme kapasitesi (MN)              | -                 | 0.02          | -                 |
| Tür                                      | -                 | Ø20 mm SN     | Ø6.5 / 150x150 mm |

Şekil 2. 30 MPa'lık püskürtme betonda çelik hasır destek kapasitesi grafikleri ve plastik zon  yayılımı  (1-1.2-1.4  güvenlik  katsayıları  ile  belirlenmiş  çelik  hasırın  güvenlik zarflardır.)

<!-- image -->

Engineering drawing

Tablo 4. Zayıf kaliteli kaya kütlesi için sayısal analizlerden elde edilen Tpl ve Ut değerleri

| ZAYIF KAYA   | Desteksiz   | Desteksiz   | Desteksiz   | Desteksiz   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   |
|--------------|-------------|-------------|-------------|-------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| ZAYIF KAYA   | Tavan       | Tavan       | Duvar       | Duvar       | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   |
| Derinlik (m) | T pl (m)    | U t (m)     | T pl (m)    | U t (m)     | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 |
| 10           | 1.92        | 0.00078     | 1.565       | 0.000975    | 0                                       | 0.0007                                  | 1.375                                   | 0.000975                                | 0                                       | 0.00063                                 | 1.34                                    | 0.000975                                |
| 50           | 2.31        | 0.00135     | 1.81        | 0.00165     | 0                                       | 0.0012                                  | 1.71                                    | 0.0015                                  | 0                                       | 0.00105                                 | 2.37                                    | 0.0015                                  |
| 100          | 3.48        | 0.0035      | 3.36        | 0.00375     | 1.51                                    | 0.0024                                  | 2.67                                    | 0.0036                                  | 1.41                                    | 0.002                                   | 2.61                                    | 0.0036                                  |
| 150          | 6.05        | 0.0068      | 3.84        | 0.0068      | 2.99                                    | 0.004                                   | 2.82                                    | 0.0064                                  | 2.28                                    | 0.0032                                  | 2.61                                    | 0.0064                                  |
| 200          | 6.22        | 0.0105      | 3.43        | 0.0105      | 3.08                                    | 0.0054                                  | 2.54                                    | 0.0081                                  | 2.85                                    | 0.0045                                  | 2.54                                    | 0.0081                                  |
| 250          | 7.78        | 0.0135      | 3.61        | 0.0135      | 5.73                                    | 0.009                                   | 2.58                                    | 0.0105                                  | 2.99                                    | 0.006                                   | 2.37                                    | 0.009                                   |
| 300          | 7.81        | 0.016       | 3.65        | 0.016       | 6.85                                    | 0.012                                   | 2.61                                    | 0.014                                   | 4.75                                    | 0.01                                    | 2.59                                    | 0.012                                   |
| 350          | 7.85        | 0.02        | 4.1         | 0.02        | 7.05                                    | 0.014                                   | 2.68                                    | 0.016                                   | 6.92                                    | 0.015                                   | 2.64                                    | 0.0175                                  |
| 400          | 8.67        | 0.024       | 4.58        | 0.024       | 8.67                                    | 0.021                                   | 2.78                                    | 0.021                                   | 8.51                                    | 0.018                                   | 2.64                                    | 0.021                                   |
| 450          | 9.64        | 0.03        | 3.78        | 0.027       | 9.64                                    | 0.0245                                  | 2.78                                    | 0.0245                                  | 8.76                                    | 0.021                                   | 2.64                                    | 0.024                                   |

Tablo 5 . Orta kaliteli kaya kütlesi için sayısal analizlerden elde edilen Tpl ve Ut değerleri

| ORTA KAYA    | Desteksiz   | Desteksiz   | Desteksiz   | Desteksiz   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   |
|--------------|-------------|-------------|-------------|-------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| ORTA KAYA    | Tavan       | Tavan       | Duvar       | Duvar       | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   |
| Derinlik (m) | T pl (m)    | U t (m)     | T pl (m)    | U t (m)     | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 |
| 10           | 0           | 0.00044     | 0.76        | 0.00056     | 0                                       | 0.0004                                  | 0.39                                    | 0.00056                                 | 0                                       | 0.0004                                  | 0.36                                    | 0.00056                                 |
| 50           | 0           | 0.000585    | 1.26        | 0.000675    | 0                                       | 0.00054                                 | 0.82                                    | 0.000675                                | 0                                       | 0.000495                                | 0.75                                    | 0.000675                                |
| 100          | 1.39        | 0.00124     | 1.37        | 0.00143     | 0                                       | 0.00108                                 | 2.15                                    | 0.00135                                 | 0                                       | 0.00099                                 | 2.15                                    | 0.00135                                 |
| 150          | 3.47        | 0.00275     | 2.59        | 0.003       | 0                                       | 0.0018                                  | 2.21                                    | 0.0022                                  | 0                                       | 0.0016                                  | 2.21                                    | 0.0022                                  |
| 200          | 2.71        | 0.003       | 2.15        | 0.0035      | 0.98                                    | 0.00225                                 | 2.28                                    | 0.00325                                 | 0.97                                    | 0.00225                                 | 2.28                                    | 0.00325                                 |
| 250          | 4.23        | 0.0049      | 2.49        | 0.00525     | 1.24                                    | 0.003                                   | 2.47                                    | 0.0042                                  | 0.98                                    | 0.0027                                  | 2.33                                    | 0.0039                                  |
| 300          | 4.29        | 0.00585     | 2.98        | 0.0063      | 2.71                                    | 0.004                                   | 2.49                                    | 0.0056                                  | 2.59                                    | 0.0036                                  | 2.41                                    | 0.0056                                  |
| 350          | 5.56        | 0.0078      | 3.03        | 0.0078      | 2.96                                    | 0.005                                   | 2.55                                    | 0.007                                   | 2.79                                    | 0.0045                                  | 2.47                                    | 0.007                                   |
| 400          | 5.79        | 0.00845     | 3.04        | 0.0091      | 3.41                                    | 0.006                                   | 2.81                                    | 0.0084                                  | 2.82                                    | 0.00495                                 | 2.53                                    | 0.0077                                  |
| 450          | 5.13        | 0.0091      | 3.11        | 0.0098      | 3.16                                    | 0.0077                                  | 2.98                                    | 0.0098                                  | 2.89                                    | 0.0064                                  | 2.72                                    | 0.0096                                  |

Tablo 6. İyi kaliteli kaya kütlesi için sayısal analizlerden elde edilen Tpl ve Ut değerleri

| İYİ KAYA     | Desteksiz   | Desteksiz   | Desteksiz   | Desteksiz   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 30 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   | 40 MPa dayanımlı püskürtme beton için   |
|--------------|-------------|-------------|-------------|-------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|-----------------------------------------|
| İYİ KAYA     | Tavan       | Tavan       | Duvar       | Duvar       | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   | Tavan                                   | Tavan                                   | Duvar                                   | Duvar                                   |
| Derinlik (m) | T pl (m)    | U t (m)     | T pl (m)    | U t (m)     | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 | T pl (m)                                | U t (m)                                 |
| 10           | 0           | 0.00025     | 0           | 0.0003      | 0                                       | 0.00022                                 | 0                                       | 0.0003                                  | 0                                       | 0.0002                                  | 0                                       | 0.0003                                  |
| 50           | 0           | 0.00025     | 0           | 0.0003      | 0                                       | 0.00024                                 | 0                                       | 0.0003                                  | 0                                       | 0.00022                                 | 0                                       | 0.0003                                  |
| 100          | 0           | 0.000495    | 0           | 0.000585    | 0                                       | 0.00045                                 | 0                                       | 0.00059                                 | 0                                       | 0.00045                                 | 0                                       | 0.00059                                 |
| 150          | 0           | 0.00078     | 1.05        | 0.00091     | 0                                       | 0.000715                                | 1.05                                    | 0.00091                                 | 0                                       | 0.00065                                 | 1.05                                    | 0.00091                                 |
| 200          | 0           | 0.00102     | 1.05        | 0.00119     | 0                                       | 0.000935                                | 1.05                                    | 0.00119                                 | 0                                       | 0.000935                                | 1.05                                    | 0.00119                                 |
| 250          | 0           | 0.0012      | 1.16        | 0.0015      | 0                                       | 0.0012                                  | 1.16                                    | 0.0015                                  | 0                                       | 0.00105                                 | 1.16                                    | 0.0015                                  |
| 300          | 0           | 0.0015      | 1.2         | 0.0018      | 0                                       | 0.00135                                 | 1.2                                     | 0.0018                                  | 0                                       | 0.00135                                 | 1.2                                     | 0.0018                                  |
| 350          | 0           | 0.00165     | 2.3         | 0.0021      | 0                                       | 0.00165                                 | 2.3                                     | 0.0021                                  | 0                                       | 0.0015                                  | 2.3                                     | 0.0021                                  |
| 400          | 1.39        | 0.00275     | 2.36        | 0.0033      | 0                                       | 0.002                                   | 2.36                                    | 0.0024                                  | 0                                       | 0.0018                                  | 2.3                                     | 0.0024                                  |
| 450          | 2.18        | 0.003       | 2.36        | 0.004       | 1.42                                    | 0.0033                                  | 2.36                                    | 0.0044                                  | 0                                       | 0.0024                                  | 2.3                                     | 0.0039                                  |
| 530          |             |             |             |             |                                         |                                         |                                         |                                         | 1.4                                     | 0.003                                   | 2.8                                     | 0.0039                                  |

## 4. Sonuçlar

Püskürtme  beton  dayanımın  derinlikle  ilişkisini belirlemek amacıyla yapılan bu çalışmada, Zayıf, Orta  ve  İyi  kaliteli  kaya  kütleleri  seçilmiştir.  Bu kaya sınıflarında sınıflarında  püskürtme  beton  en etkili  destek  elemanı  olmanıdır  RMR89  için  çok zayıf  kaliteli  kayalarda  çelik  iksa  desteğinin  ön planda olması ve çok sağlam kaliteli kayalarda ise püskürtme betonun desteklemekten ziyade emniyet için uygulanmasından dolayı bu iki sınıf göz ardı edilmiştir.

İyi  kaliteli  kaya  kütleleri  için  yapılan  analizlerde 30  MPa  dayanımlı  püskürtme  beton  480  m  örtü kalınlığına kadar yenilmeden desteklemeye devam etmektedir. Püskürtme beton dayanımı 40 MPa'a çıkartıldığında  530  m  örtü  kalınlığına  kadar  bu destek sistemi duraylı kalabilmektedir. İyi kaliteli kaya sınıfı için ise 530 m örtü kalınlığından sonra bir alt kaya kütle sınıfının destek sistemini kullanmak  yenilmelerin  önüne  geçmektedir.  İyi kaliteli  kaya  için  elde  edilen  diğer  bir  sonuç  ise, püskürtme beton dayanımı 20 MPa  değerine düşürüldüğünde 410 m  örtü kalınlığına kadar destek sisteminde yenilme olmamasıdır.

Orta kaliteli kaya kütle sınıfı için yapılan analizlerde, 30 MPa dayanımlı püskürtme betonda,  310  m  örtü  kalınlığına  kadar  yenilme olmamış, beton dayanımı 40 MPa'a çıkartıldığında  ise  420  m  örtü  kalınlığına  kadar yenilmeden kalabilmiştir.

Şekil 3. 40 MPa'lık püskürtme betonda çelik hasır destek kapasitesi grafikleri ve plastik zon yayılımı (1-1.2-1.4, güvenlik katsayıları ile belirlenmiş çelik hasırın güvenlik zarflardır).

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

Şekil 4. 20 MPa' lık püskürtme betonda Çelik hasır destek kapasitesi grafikleri ve plastik zon yayılımı (1-1.2-1.4, güvenlik katsayıları ile belirlenmiş çelik hasırın güvenlik zarflardır).

Tablo 7. İyi  kaliteli kaya sınıfında 20 MPa dayanımlı püskürtme betonun uygulanması durumunda sayısal analizlerden elde edilen Tpl ve Ut değerleri.

| RMR (Good) 20 MPa   | Tavan    | Tavan    | Duvar    | Duvar    |
|---------------------|----------|----------|----------|----------|
| Derinlik (m)        | T pl (m) | U t (m)  | T pl (m) | U t (m)  |
| 10 m                | 0        | 0.00022  | 0        | 0.00028  |
| 50 m                | 0        | 0.00024  | 0        | 0.0003   |
| 100 m               | 0        | 0.000495 | 0        | 0.000585 |
| 150 m               | 0        | 0.000715 | 1.05     | 0.00091  |
| 200 m               | 0        | 0.000935 | 1.05     | 0.00119  |
| 250 m               | 0        | 0.0012   | 1.16     | 0.0015   |
| 300 m               | 0        | 0.00135  | 1.2      | 0.0018   |
| 350 m               | 0        | 0.00165  | 2.3      | 0.0021   |
| 400 m               | 0        | 0.002    | 2.36     | 0.0024   |
| 410 m               | 1.52     | 0.0033   | 2.5      | 0.0044   |

Analizlerden elde edilen diğer bir sonuç ise 420 m örtü kalınlığından sonra beton dayanımını artırmak yerine kaya sınıfı bir derece daha düşürmek tünelin duraylılığı için yeterli olmaktadır.

Bu  çalışma  kapsamında  yapılan  analizlere  göre, zayıf kaliteli kaya kütlelerine RMR89 destek sistemi 30 MPa'lık püskürtme beton dayanımı ile uygulandığında püskürtme betonda yenilmeler 200  m  örtü  kalınlığında  başlarken,  püskürtme beton dayanımı 40 MPa'a çıkartıldığında püskürtme beton 260 m örtü kalınlığında yenilmeye  başlamıştır.  Ayrıca,  beton  kalınlığını arttırmanın da bir çözüm olabileceği düşünülebilir ancak bu durumda yeni bir destek sistemi önerilmiş olacağından betonun yenildiği derinliklerin  belirlenip  beton  dayanımını  arttırma yolu seçilmiştir.

Bu çalışmadan elde edilen sonuçlar, kazı derinliğinin artması ile birlikte, uygulanan destek sistemlerinin gözden geçirilmesi, destek elemanlarının  dayanımlarının  artırılması  veya  bir alt kaya sınıfına ait desteklerin kullanılması gerektiğini göstermektedir.

## 5. Kaynaklar

Badr, A, 2016. Statistical Analysis of the Variability  in  Shotcrete  Strength,  Global Journal  of  Researches  in  Engineering:  E Civil  And  Structural  Engineering,  Volume 16, Issue 4.

Badr,  A.,  ve  Brooks,  J.J.,  2008.  'Rebound  and Composition of in-Situ Polypropylene Fibre-Reinforced Shotcrete,' 11th 6 Intl Conf  Durability  of  Building  Materials  &amp; Components,  11DBMC,  Istanbul,  Turkey, 11-14 May, Vol. 1, pp. 569-576.

Barton,  N.R., Lien, R.,  and  Lunde,  J.,  1974. Engineering  classification  of  rock  masses for the design of tunnel support,  Rock Mechanics, v. 6, p. 189-239.

Barros, J.A., Lourenço, L.A., Soltanzadeh, F. And Taheri,  M.  (2014)  'Steel-fibre  reinforced concrete for elements failing in bending and in shear,' European Journal of Environmental  and  Civil  Engineering,  31 18(1), pp.33-65.

Beauprè, D., Dufour,J.F., Hutter, J. ve Jolin, M., 2005.  Variability  of  compressive  Strength of  Shotcrete  in  a  Tunnel-Lining  Project, Shotcrete, V. 5, No. 2, pp.22-25.

Bieniawski, Z.T., 1973, Engineering classification of  jointed  rock  masses:  Transaction  of  the South African Institution of Civil Engineers, v. 15, p. 335-344.

Bieniawski,  Z.T.,  1989.  Engineering  Rock  Mass Classifications. Wiley, 251pp, New York.

Bieniawski,  Z.T.,  1993,  Classification  of  rock masses  for  engineering:  The  RMR  system and future trends, In:Hudson,  J.A., ed., Comprehensive Rock Engineering, Volume 3:  Oxford,  Pergamon  Press,  p.  553-573, New York.

- Cai, M., Kaiser, P.K., Tasaka, Y. and Minami, M., 2007.  Determination  of  residual  strength parameters of jointed rock masses using the GSI system, International  Journal of Rock Mechanics  and  Mining  Sciences,  4  (2), 247-265.
- Celada, B., Tardaguila, I., Varona, P., Rodriguez, A.  and  Bieniawski,  Z.T.,  2014.  Innovating tunnel  design  by  an  improved  experiencebased RMR  system. In: World Tunnel Congress,  May  9th  to  15th  2014,  Iguassu Falls, Brazil.
- Deere, D.U., 1964. Technical description of rock cores for engineering purposes, Rock Mech. Rock Eng. 1, 17-22.
- Fenner, R., 1938. Untersuchungen zur Erkenntnis des  Gebirgsdrucks,  Glückauf,  74,  32,  681695.
- Genis, M., Basarir, H., Ozarslan, A., Bilir, E. and Balaban,  E.,  2007.  Engineering  geological appraisal of the rock masses and preliminary support design, Dorukhan Tunnel,  Zonguldak,  Turkey. Engineering Geology, 92, 14-26.
- Gurocak, Z., Solanki, P. and Zaman, M.M., 2007. Empirical and numerical analyses of support requirements for a diversion tunnel at  the  Boztepe  dam  site,  eastern  Turkey. Engineering Geology. 91, 194-208.
- Gurocak,  Z., 2011. Analyses  of stability  and support design for a diversion tunnel at the Kapikaya  dam  site,  Turkey, Bulletin of Engineering Geology and the Environment, 70, 41-52.
- Hoek,  E.,  Kaiser,  P.K.  ve  Bawden,  W.H.,  1995. Support  of  Underground  Excavations  in Hard Rock. Rotterdam, Balkema
- Hoek, E., 2007, Practical rock engineering, RocScience.
- ISRM, (International Society for Rock Mechanics), 1981. ISRM Suggested Methods:  Rock  Characterization,  Testing and  Monitoring,  Pergamon  Press,  London, 211 s.
- Kaya,  A.,  Bulut,  F.,  Alemdag,  S.,  ve  Sayın,  A. (2011).  Analysis  of  support  requirements for  a  tunnel  portal  in  weak  rock:  A  case study  in  Turkey.  Scientific  Research  and Essays, 6(31), 6566-6583.
- Kaya, A. ve Bulut, F. (2013). Stability analyses of tunnels  excavated  in  weak  rock  masses using empirical  and  numerical  methods, Jeoloji  Mühendisliği  Dergisi,  37(2),  103116.
- Kaya, A., and Sayın, A. (2017) Engineering geological appraisal and preliminary support design for the Salarha Tunnel, Northeast Turkey.  Bull  Eng  Geol  Environ, DOI: 10.1007/s10064-017-1177-2
- Kanik, M., Gurocak, Z. and Alemdag, S., 2015. A comparison  of  support  systems  obtained from the RMR89 and RMR14 by numerical analyses: Macka Tunnel project, NE Turkey, Journal of African Earth Sciences,Volume 109, September 2015, 224-238.
- Kirsten, 1992. Comparative efficiency and ultimate strength of meshand fibre reinforced shotcrete as determined from full-scale bending tests, Journal of the South African Institute of Mining and Metallurgy, Nov., 303-322.
- KGM  (Karayolları Genel Müdürlüğü), 2013. NATM  Uygulamalı  Yeraltı Tünel İşleri Teknik Şartnamesi, Karayolları Genel Müdürlüğü, Ankara.
- Lauffer,  H.,  1958,  Gebirgsklassifizierung  für  den Stollenbau:  Geology  Bauwesen,  v.  24,  p. 46-51.
- Mohajerani,  A.,  Rodrigues,  D.,  Ricciuti,C.,  ve Wilson, C., 2015. Early-Age Strength Measurement of Shotcrete, Journal of Materials, Vol 2015, pp 1-10.
- NIOSH,  2014.  Shotcrete  design  and  installation compliance testing: early strength, load capacity, toughness, adhesion strength, and applied quality,' Martin et al. edit, National Institute for Occupational Safety and Health, Publication No. 2015-107, RI 9697.
- Palmström, A., 1995. RMi-a rock mass characterization system for rock engineering  purposes.  Ph.D.  thesis,  Univ. Of Oslo, Norway, 400 pp
- Patel,  P.A.,  Desai,  A.K.,  ve  Desai,  K.A.,  2012. Evaluation  of  engineering properties for polypropylene fiber reinforced concrete, International Journal of Advanced Engineering Technology, 3(1), pp.42-45.

- Rocscience,  2006.  Roclab  bilgisayar  programı, www.rocscience.com
- Rocscience Inc, 2011. Phase 2 v8.0 Finite Element Analysis for Excavations and Slopes, Rocscience Inc., Toronto, Ontario, Canada.
- Sheorey,  P.R.,  Murali,  M.G.,  Sinha,  A.,  2001. Influence of elastic constants on the horizontal in situ stress. Int. J. Rock Mech. Min.Sci. 38 (1), pp 1211-1216.
- Stini,  I.,  "Tunnelbaugeologie,"  Springer-Verlaa, Vienna, 1950, p 336.
- Terzaghi,  K.,  1946,  Rock  defects  and  loads  on tunnel supports, in Proctor, R.V., and White, T.L., eds., Rock tunneling with steel support, Volume 1: Youngstown,Ohio, Commercial Shearing and Stamping Company p. 17-99.
- Wickham, G.E., Tiedemann, H. R. and Skinner, E. H.,  1972,  Support  determination  based  on
- geologic predictions, In: Lane, K.S.a.G., L. A.,  ed.,  North  American  Rapid  Excavation and  Tunneling  Conference:  Chicago,  New York:  Society  of  Mining  Engineers  of  the American Institute of Mining, Metallurgical and Petroleum Engineers, p. 43-64.
- Wood, D.F., Banthia, N. ve Trottier, J-F, 1993. A comparative  study  of  different  steel  fibres in  shotcrete.  In  Shotcrete  for  underground support  VI,  Niagara  Falls,  57-  66.  New York: Am. Soc. Civ. Engrs
- Yalcin,  E.,  Gurocak,  Z.,  Ghabchi,  R.  ve  Zaman, M, 2016. Numerical Analysis for a Realistic Support Design: Case Study of the Komurhan Tunnel in Eastern Turkey, International Journal of Geomechanics, Vol 16(3)
- Zhang, L. 2014, Variability of Compressive Strength  of  Shotcrete  in  a  Tunnel-Lining Project. www.shotcrete.org
Araştırma Makalesi

Research Article

<!-- image -->

Qr code

## PÜSKÜRTME BETONUN YAKLAŞIK MALİYET ANALİZİ İÇİN UYGULAMA GELİŞTİRİLMESİ

## Melda ALKAN ÇAKIROĞLU 1* , Ahmet Ali SÜZEN 2 , İlkenur ŞENTÜRK 3

- 1  Isparta Uygulamalı Bilimler Üniversitesi, Teknoloji Fakültesi, İnşaat Mühendisliği Bölümü, Isparta, Türkiye 2 Isparta Uygulamalı Bilimler Üniversitesi, Uluborlu Meslek Yüksekokulu, Bilgisayar Teknolojileri Bölümü, Isparta, Türkiye.
- 3  Süleyman Demirel Üniversitesi, Fen Bilimleri Enstitüsü, Yapı Eğitimi ABD, Isparta, Türkiye

| Anahtar Kelimeler                                                                   | Öz                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Püskürtme Beton, Maliyet Hesabı, Yaklaşık Maliyet, Yazılım Geliştirme, Microsoft C# | Püskürtme beton depremden hasar görmüş binaların onarım/güçlendirilmesinin yanı sıra metro, baraj, köprü, tünel yapım ve onarımı, şev stabilizasyonları gibi bir çok uygulama alanına sahip olması bakımından karışım tasarımı, uygulanması, makine teçhizat, geri sıçrama vb. faktörlerin maliyete olan etkisinin incelenmesi en önemli olgudur. Püskürtme betonun maliyetine; uygulanma yüzeyi, malzeme kalitesi, geri sekme, işçilik, nakliye vb. gibi birçok faktör etki etmektedir. Bu nedenle maliyeti kesin olarak tayin etmek mümkün değildir. Bu çalışmada püskürtme betonun farklı uygulama ve amaçları için yaklaşık maliyetinin hesaplaması amaçlanmıştır. Püskürtme betonun maliyetini etkileyen parametrelerin maliyete olan etkisini değerlendirebilmek için geliştirilen yazılım, Microsoft Visual Studio platformunda C# programlama dili ile geliştirilmiştir. Yazılımdan analiz edilerek ortaya çıkan veriler, örnek bir çalışma ile karşılaştırılmıştır. Sonuç olarak geliştirilen yazılımında yapılan testlerin, örnekle uyumlu olduğu tespit edilmiştir. |

## DEVELOPING AN APPLICATION FOR APPROXIMATE COST ANALYSIS OF SHOTCRETE

| Keywords                                                                           | Abstract                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Shotcrete, Cost Estimate, Approximate Cost, Application Developing, Microsoft C #. | Shotcrete has many application areas such as repair/reinforcement of buildings damaged by an earthquake as well as metro, dam, bridge, tunnel construction and repair, slope stabilization so it's important to investigate the effects of certain factors, including mixture design, application, machinery and equipment, rebound on cost. The cost of shotcrete is affected by several factors such as the application surface, material quality, rebound, workmanship, transport, etc. Therefore, it is not possible to determine the exact cost. The aim of this study is to calculate the approximate cost of shotcrete for different applications and purposes. The software developed to evaluate the effects of the parameters affecting the cost of shotcrete was developed using C# programming language on Microsoft Visual Studio platform. Data obtained by analyzing on the software were compared with a sample study. As a result, it was determined that the tests performed in the developed software were in agreement with the sample. |

## Alıntı / Cite

Çakıroğlu,  M.  A.,  Süzen,  A.A.,  Şentürk,  İ.,  (2020).  Püskürtme  Betonun  Yaklaşık  Maliyet  Analizi  için  Uygulama Geliştirilmesi, Journal of Engineering Sciences and Design, 8(1), 153-164.

| Yazar Kimliği / Author ID (ORCID Number)                                                                | Makale Süreci / Article Process                                                                                             |                                             |
|---------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| M. Alkan Çakıroğlu, 0000-0002-8919-6278 A.A. Süzen, 0000-0002-5871-1652 İ. Şentürk, 0000-0001-9376-8243 | Başvuru Tarihi / Submission Date Revizyon Tarihi / Revision Date Kabul Tarihi / Accepted Date Yayım Tarihi / Published Date | 08.05.2019 05.08.2019 19.08.2019 20.03.2020 |

## 1. Giriş (Introduction)

Günümüzde insan hayatının ayrılmaz bir parçası haline gelen ve günlük hayatın her alanında etkisini gösteren bilgisayar, hızlı gelişen teknoloji sayesinde bilime daha çok yardımcı olmaktadır. Bilim bilgisayar geliştirirken, aynı

* İlgili yazar / Corresponding author: meldaalkan@isparta.edu.tr, +90-246-214-6808

anda bilgisayar da bilimle senkronize çalışmakta ve bilimsel çalışmaları kolaylaştırmaktadır (Özgür ve İleri, 2002). Günümüzde tüm mühendislik disiplinleri, gerek proje gerekse üretim aşamasında bilgisayar  programlarından yararlanmaktadır (Özgür, 2004). İnşaat sektörü uygulamalarında her geçen gün daha karmaşık ve büyük boyutlu projeler  gündeme  gelmektedir.  İşletmeler  arasında  giderek  artan  rekabet,  bu  karmaşık  projelerin  sadece performansları  açısından değil, süre ve maliyet açısından da değerlendirilmelerini  zorunlu kılmaktadır (Kırankaya,  2007).  İnşaat  sektöründe  uygulama  alanına  sahip  püskürtme  betonun  yaklaşık  maliyet  hesabının üzerinde  dikkatle  durulması  gereken  önemli  bir  olgudur.  Maliyet  faktörü  düşünülmeden  püskürtme  betonun üretim ve uygulamasını planlamak mümkün değildir.

Bu çalışmada püskürtme betonun yaklaşık maliyetini hesaplamak amaçlanmıştır. Bu amaç doğrultusunda, T.C. Çevre  ve  Şehircilik  Bakanlığı  İnşaat  Birim  Fiyat  Analizlerinden  yararlanılarak,  Microsoft  C#  program  dili kullanılarak  bir  bilgisayar  programı  hazırlanmıştır.  Microsoft  C#  dili  nesne  tabanlı  bir  dil  olması  ve  grafiksel kullanıcı  arayüzü  geliştirme  gibi  özelliklere  sahip  olmasından  dolayı  tercih  edilmiştir.  Programda  püskürtme betonun kullanım amacı, betonun yerleşimi, işçilik ve çevre faktörleri ve geri sıçrama miktarının maliyete olan etkileri göz önüne alınmıştır.

Ekonominin önde gelen sektörlerinden biri olan inşaat sektöründe kritik bir faktör olan maliyet ve bu maliyeti etkileyen  faktörlerin  tespiti,  bu  konunun  önemini  arttırmaktadır.  Bu  nedenle  araştırmada  yapı  maliyetinin hesaplanması ve yaklaşık maliyet yöntemleri konuları ile ilgili literatürde yapılan çalışmalar incelenmiştir. Bu çalışmalar  arasından  bazıları;  püskürtme  beton  ve  geri  sıçrama  miktarının  püskürtme  beton  maliyetine  etkisi (Arıoğlu  vd.,  2008),  ahşap  tahkimat  sistemi  ile  püskürtme  beton  ve  çelik  telli  püskürtme  beton  sistemlerinin maliyetlerinin  karşılaştırılması  (Yüksek  vd.,  2004),  püskürtme  beton  operatörleri  için  simülasyon  programı (Börjesson ve Thell 2009), yaş karışım püskürtme betonda çelik lif kullanımının maliyete etkisi (Ayış, 2010), kuru karışım püskürtme beton karışım hesabının bilgisayar ortamında hazırlanması (Çakıroğlu, 2014), maliyet analizi (Altın ve Allahverdi, 2004; Kanıt ve Baykan, 2004; Bostancıoğlu, 2006; Uğur, 2007; Kuruoğlu, vd., 2012; Klakegg ve Lichtenberg, 2016; Bayraktar ve Bayraktar, 2016), yapay zeka ve yapay sinir ağları (Günaydın ve Doğan; 2004; Juszczyk, 2017), PERT-CPM tekniği (Dziadosz, 2013; Karahan ve Ezin, 2014),  yapı bilgi modellemesi (Yaman ve İlhan, 2010; Lee, vd., 2014; Gerçek vd., 2016; Wang, vd., 2016; Abanda vd., 2017; Beşer, 2017), yapay arı koloni algoritması  (Tapao  ve  Cheerarot,  2017;  Dağdeviren  ve  Kaymak,  2018),  onarım/güçlendirme  maliyetleri (Doğramacı vd., 2003; Yanmaz ve Luş, 2005) üzerine yapılmış çalışmalardır. Ancak püskürtme betonun yazılım tabanlı maliyet analizi hakkında yapılmış bir literatür çalışmasına rastlanılamamıştır. Bu nedenle bu çalışmanın yeni çalışma alanlarının belirlenmesine fayda sağlayabileceği söylenebilir.

Püskürtme betonun maliyetinin mümkün olduğunca gerçeğe yakın bir şekilde hesaplanması kullanıcı için önem arz etmektedir. Ancak bu hem zaman alan hem de yanılma olasılığı oldukça yüksek olan bir iştir. Bu çalışmada, farklı  uygulamalar  için  üretimi  yapılacak  püskürtme  betonun  yaklaşık  maliyetini  hesaplamaya  yönelik  bir bilgisayar uygulaması geliştirilmiştir.

## 2. Materyal ve Yöntem (Material and Method)

Hazırlanan programda püskürtme betonun; hammaddeleri, uygulanma şekli, kullanım yerleri, teknik özellikleri, geri  sekmesi  gibi  püskürtme  betonun  maliyet  unsurlarını  ve  teknik  farklılıklarını  hesaba  katan  ve  işleyen  bir uygulama tasarlanmıştır. Çalışmanın gerçekleştirildiği uygulama Microsoft Visual Studio. NET 2017 platformunda C# 6.0 programlama dili kullanılarak geliştirilmiştir.

Uygulama tasarımı bölümünde Kullanımı Amacı (Şekil 1-a), Karışım Türü (Şekil 1-b), Çevresel Koşullar (Şekil 1-c), Beton ve Katkı (Şekil 1-d), Çelik Hasır (Şekil 1-e) isimli 5 menüden oluşmaktadır. Bu beş menüde kendi aralarında alt menülere ayrılmaktadır. Kullanım amacı menüsünde püskürtme betonun uygulanma amacına göre giriş verisi, menü de yer alan seçeneklerden tespit edilmektedir. Karışım türü menüsünden uygulama yapılacak püskürtme betonun karışım türü ekranda yer alan menüden seçim yapılır.

Şekil 1. Uygulamaya ait menülerin tasarımı, (a) Kullanımı Amacı, (b) Karışım Türü, (c) Çevresel Koşullar, (d) Beton Katkı, (e) Çelik Hasır (Design of application menus, (a) purpose of use, (b) type of mixture, (c) environmental conditions, (d) concrete additive, (e) steel mesh)

<!-- image -->

Screenshot from computer

Program  içerisinde  detaylı  bir  kullanım  kılavuzu  yer  almaktadır.  Programın  uluslararası  düzeyde  kullanımın sağlanabilmesi için Türkçe ve İngilizce dil seçenekleri de bulunmaktadır. Programa veri girişi sırasında ara ara çalışmanın durumunu kaydetmek, sonuçları saklamak veya başka bir bilgisayara aktarabilmek için kaydet ikonu, yazıcıdan sonuçların alınabilmesi için de yazıcıdan çıktı alma seçeneği eklenmiştir. Programda ilave olarak her aktif ekranın alt kısmında kullanıcıya yönelik genel bilgilere de yer verilmiştir.

Programda, işçilik ve operatör faktörü, makine ve teçhizat, kullanılan katkı maddeleri, geri sekme, yüzey faktörü gibi  püskürtme  betonun  karışım dizaynı  ve  maliyetini  etkileyen  parametreleri  veri  girişi  olarak  sunmaktadır. Ayrıca  kullanıcıların  isteği  doğrultusunda  gerekli  giriş  alanlarında  hesaplama  yapılmasına  imkân  tanınmıştır. Hesaplanan sonuçların daha sonradan kullanılması için veri girişlerini temsil eden MS Access türünde veri tabanı oluşturulmuştur.

Uygulamayı  kullanacak  kullanıcı  ilk  olarak  kullanım  amacı  menüsünü  (Şekil  2)  seçerek  püskürtme  betonun uygulama alanı ekranında ilk seçimleri yapması gerekmektedir. Hesaplamada kullanılacak zaiyat oranları da bu menü içerisinde kullanıcıya sunulmaktadır. Geri sekme oranlarında literatürdeki kaynaklardan (Aka ve Celep; 1978; Arıoğlu ve Yüksel, 1999; Arıoğlu vd., 2008; Celep, 2017) yararlanılmıştır.

Şekil 2. Açılış ekranı (Splash screen)

<!-- image -->

Screenshot from computer

Bundan  sonraki  süreçte,  uygulamada  kullanım  alanı  seçildikten  sonra  gelen  ekranda  yaklaşık  maliyet  hesabı yapılacak olan püskürtme beton sisteminin kuru veya yaş olarak parametresinin seçilmesi gerekmektedir.  Bu seçimde seçeneklerden sadece birinin aktif hale gelmesi sağlanmıştır. Karışım türünün butonu seçildiği zaman açılan veri giriş sayfasının ekran görüntüsü Şekil 3'de verilmiştir. Ayrıca karışım türü ekranına püskürtme betonun kapasitesi  (m 3 /saat),  işçilik,  operatör  ve  makine-teçhizat  kirası  gibi  maliyeti  etkileyen  parametrelerin  girişi yapılmıştır. Her aktif olan ekranın alt kısmında genel bilgilere yönelik kullanıcıya açıklama notları yazılmıştır.

Şekil 3. Karışım türü, işçilik ve makine ekranı (Mix type, craftsmanship and machine display)

<!-- image -->

Screenshot from computer

Kullanıcının çevresel koşullarda kullanacağı menünün ekran görüntüsü Şekil 4'de verilmiştir. Bu ekran sayesinde hava koşulları,  işçilik  faktörü  ve geri  sekme  ile  ilgili  girdilerin  programa  girişi  sağlanmıştır.  Geri  sekme  oranı, püskürtme betonun uygulama açısı, karışımın özellikleri, uygulama yüzeyinin konumu ve operatörün deneyimine bağlı olarak değişmektedir. Bunun için kullanıcı otomatik geri sekmeyi seçtiği takdirde program seçilen yüzeye uygun  geri  sekme  faktörünü  otomatik  olarak  ekleyecek  şekilde  düzenlenmiştir.  Ayrıca  kullanıcının  bu  oranı manuel  olarak  girmesine  de  olanak  sağlanmıştır.  Manuel  giriş  tercih  edilecekse  sınır  değerler  arasında  giriş yapması gerektiği ile ilgili olarak uyarı yazısı kullanıcının karşısına çıkacak şekilde düzenleme yapılmıştır.

Şekil 4. Çevresel koşullar ekranı (Environmental conditions display)

<!-- image -->

Screenshot from computer

Çevresel  koşulların  etkisi  programa  girildikten  sonra  beton  ve  katkı  oranlarının  belirlendiği  menü  aktif  hale geçmektedir.  Beton  fiyatları  güncel  olarak  değiştiği  için  kullanıcının  betonun  m 3   birim  fiyatını  manuel  olarak programa girmesini sağlayan özellik seçenek olarak eklenmiştir. Kullanıcının betonun uygulanacağı ortama göre seçeceği  katkı  türleri  de  menüde  verilmiştir. Her  katkı  türünün  püskürtme  betonda  kullanılacağı  miktar/oran programın veri tabanında mevcuttur. Burada kullanıcının sadece kullanacağı katkı türünü belirlemesi ve birim fiyatını programa manuel olarak girmesi sağlanmıştır. Hazırlanan programda katkı maddelerinin çimento hacmi ile orantılı olarak kullanılması için bir formülizasyon oluşturulmuş ve arka planda çalışması sağlanmıştır.  Şekil 5'de beton ve katkı veri girişlerinin olduğu ekran görüntüsü verilmiştir.

Şekil 5. Beton ve katkılar ekranı (Concrete and additives display)

<!-- image -->

Screenshot from computer

Kullanıcı  beton  ve  katkı  veri  girişlerini  tamamladıktan  sonra  programda  çelik  hasır  ve  çelik  liflere  ait  veri girişlerinin  yapılacağı  menü  aktif  hale  gelmektedir  (Şekil  6).  Kullanıcının  çelik  hasır/çelik  lif  seçeneklerinden herhangi  birisini  seçmesi  sağlanmıştır.  Bu  seçimin  kullanılacak  püskürtme  betonun  kalınlığı  ve  amacına  göre yapılmasına olanak sağlanmıştır. Programın güncelliği açısından hasır çelik ve çelik lif fiyatları manuel olarak giriş yapılacak  şekilde  düzenlenmiştir.  Diğer  menülerde  olduğu  gibi  ekranın  alt  kısmında  genel  bilgilere  yönelik kullanıcıya notlar yazılmıştır.

Şekil 6. Çelik hasır ve çelik lif ekranı (Steel wire mesh and steel fiber screen)

<!-- image -->

Screenshot from computer

Maliyet analizinin yapılması için gerekli parametrik değerler girildikten sonra hesaplamanın yapılması için gerekli formülüzasyon  işlemi  Şekil  7'de  gösterildiği  gibi  gerçekleştirilmiştir.  Burada  b  yüzey  genişlik,  β  boşluk  oranı katsayısı, Ω geri sekme oranı, 𝚿 hava durumu etkisi, 𝜙 operatör deneyimini temsil etmektedir.

Şekil 7. Formüle göre maliyet analizi hesaplama (Cost analysis by Formula calculation)

<!-- image -->

Screenshot from computer

## 3. Uygulamanın Testi (Application Test)

Geliştirilen uygulamaların sonuçlarını test etmek için Kıyı Enerji Elektrik Üretim A.Ş. firmasının 2012 yılında Erik regülatörü ve HES projesinde kullanılan ve analizi yapılan püskürtme betonun parametreleri vaka çalışmasında kullanılmıştır. Hazırlanan uygulamamanın etkinliği ve güvenirliğini ölçmek için referans olarak seçilen Bekaert firmasından  temin  edilen  2012  yılı  çelik  hasır  ve  çelik  telli  maliyet  kıyaslama  uygulaması  verileri  yazılımda kullanılmak üzere alınmıştır. Projede çelik hasırlı yaş karışım püskürtme beton uygulaması yapılmıştır.

Program 1 m 3  püskürtme beton maliyetini hesaplaması için planlanmıştır. Genişlik 5m, yükseklik 2m ve kalınlık 0,1m  bir  alan  varsayılıp  toplamda  1m 3   alana  yapılacak  püskürtme  beton  fiyatı  hesaplanması  amaçlanmıştır. Kullanıcı  1m 3  alan  için  hesaplanan  fiyatı,  hesaplamak  istediği  alan  ile  çarparak  (birim  fiyat  x  istenilen  alan) istenilen toplam maliyeti bulabilmektedir. Hesaplama işlemi için ilk olarak püskürtme betonun örnek projedeki kullanım amacı seçilmiştir (Şekil 8).

Şekil 8. Programa kullanım amacının girilmesi (Entering the purpose of use in the program)

<!-- image -->

Screenshot from computer

Çalışmada yaş karışım yöntem kullanıldığı için, 'Karışım Türü' ekranından 'Yaş Karışım' butonu seçilmiştir. 1 saatte atımı yapılan püskürtme beton miktarı seçeneklerden seçilmekte, arka planda ise dakikada yapılan atım miktarı hesaplanarak işçi giderleri dakika bazında ne kadar atım yaptığı hesaplanıp ve maliyete eklenmiştir. İşçi sayısı  kişi  başına  ücret  girdisi  yapılmaktadır  fakat  arka  planda  karışım  türüne  ve  kullanılan  işçi  sayısına  göre hesaplama yapılmaktadır. Örnek çalışmada işçi ücreti 10TL (Adam/Saat) ve operatör ücreti 20TL (Adam/Saat) olarak alınmıştır. Mikser ücreti olarak ise 30TL alınmıştır (Şekil 9).

Şekil 9. Karışım türü girişi (Mix type input)

<!-- image -->

Screenshot from computer

Uygulama alanındaki hava koşullarının ideal olduğu varsayılarak devam edilmiştir. Firmadan edinilen bilgiler doğrultusunda işçilik kalitesi iyi ve geri sekmede otomatik seçilmiştir (Şekil 10). Arka planda geri sekme literatür taraması sonucunda oluşturulan; kullanıldığı yüzeye göre % oranında etki tablosuna göre maliyete yansıtılmıştır.

Şekil 10. Çevresel koşullar girişi (Environmental conditions input)

<!-- image -->

Screenshot from computer

Örnek alınan projeye göre betonun m 3  fiyatı 130TL olarak alınmış ve programa aynen yansıtılmıştır. Katkı türü kullanılmadığı için bir veri girişi yapılmamıştır (Şekil 11).

Şekil 11. Beton ve katkı girişi (Concrete and additive input)

<!-- image -->

Screenshot from computer

Firmadan alınan çalışmada çelik lif ve hasır kullanılmıştır. Çelik hasırın m 2  fiyatı olarak 1,55 TL, çelik lifin m 3  fiyatı olarak 3,44 TL olarak veri girişi yapılmıştır (Şekil 12). Veriler m 2  için verilmiştir, program arka planda düzenleme yaparak 1m 3  püskürtme beton için maliyet hesabı çıkarmaktadır.

Şekil 12. Çelik hasır ve çelik lif girişi (Steel wire mesh and steel fiber input)

<!-- image -->

Screenshot from computer

Programa tüm veriler girildikten sonra hesapla butonuna basılarak sonuç ekranına geçiş yapılmıştır. Püskürtme betonun  maliyeti  için  girilen  bilgiler  doğrultusunda,  malzeme  (beton,  çelik)  ve  makine  ve  teçhizat  ücretleri otomatik olarak sonuç ekranında hesaplanmıştır (Şekil 13).

Örnek uygulamada 1m 2 'lik alan için yapılan püskürtme beton maliyetini vermektedir. Hazırlanan programda ise 10m 2 'lik alan için hesaplama yapmaktadır. Toplam + Makine teçhizat giderleri= Toplam Maliyeti formülü ile toplam maliyet  çıkmaktadır.  Makine  teçhizat  giderleri  ayrı  kalem  olarak  hesaplanmaktadır.  Uygulama  sonucuna  göre 195,68+90=285,68 TL olarak toplam maliyet çıkmaktadır. 285,68/10 yapıldığından örnek çalışmada olduğu gibi 1m 2 ' ik alanın maliyet sonucunu vermektedir. Uygulamada maliyet 30,47 TL olarak edilmişken programda yaklaşık maliyet 28,56 TL olarak elde edilmiştir. Firmadan alınan verilerin aktarıldığı programdan elde edilen sonuçlar ile uygulamada yapılan maliyet karşılaştırıldığında benzer olduğu görülmüştür.

Şekil 13. Örnek alınan projenin sonuç ekranı (Result screen of sample project)

<!-- image -->

Screenshot from computer

## 4. Sonuç ve Tartışma (Result and Discussion)

Bu  çalışmada  püskürtme  betonun  geleneksel  betondan  farklılıkları  itibariyle  maliyetini  etkileyen  unsurların tanımlanmasına  ve  bunlara  bağlı  olarak  yaklaşık  maliyetini  mümkün  olduğunca  gerçekçi  bir  yaklaşımla hesaplamak amaçlanmıştır. Ayrıca yazılımın geliştirilme süreci; güncellemelere açık olması, kullanıcının istekleri doğrultusunda yönlenebilmesi ön planda tutulmuştur.

Çalışmada,  püskürtme  beton  uygulaması  yapmak  isteyen  sektör  çalışanları  için,  püskürtme  beton  üretiminde yaklaşık maliyetin hesaplamasına olanak sağlayan bir uygulama yazılımı geliştirilmiştir. Uygulamanın hesaplama bölümünde kullanılan birim fiyatlarda T.C. Çevre ve Şehircilik Bakanlığının belirlediği birim fiyatlar kullanılmıştır. Ayrıca  çalışmada  uygulamanın  etkinlik  düzeyini  ve  güvenilirliğinin  belirlenmesine  yönelik  olarak,  Bekaert firmasından temin edilen 2012 yılında çelik hasır ve çelik telli maliyet kıyaslama uygulaması verileri yazılımda kullanılarak, hesaplanan  değerler  ile  yazılım  çıktıları karşılaştırılmıştır.  Yapılan  karşılaştırma  sonucunda geliştirilen  uygulamanın  doğruluk  sonuçlarında  tutarlı  olduğu  görülmüştür.  Geliştirilen  uygulama  ile  test uygulaması sonucunda elde edilen değerler arasında yaklaşık %5 kadar bir fark olduğu görülmüştür. Betonun tasarım, karışım ve uygulanma safhalarında birçok öngörülemeyen parametre, ortam koşulları ve değişkenden etkilenebileceği düşünülecek olursa maliyeti konusunda net bir sonuca ulaşmak mümkün olmadığından %5'lik farkın kabul edilebilir sınırlar içinde olduğu öngörülmüştür.

Yapılan bu çalışma özellikle inşaat  sektöründe püskürtme beton uygulaması yapacak olan yüklenici açısından yapılması  gereken  yapım  ve  sözleşme  yönetimi  alanındaki  birçok  işleve  cevap  verebilecek  bir  yazılımın geliştirilmesi bakımından güncel bir konudur. Bu amaçla geliştirilen yazılımın, sektörde ilgili ihtiyaç duyulan tüm verilere ve parametrelere etkin ve hızlı bir şekilde ulaşılmasına olanak sağlayacağı beklenmektedir.

Uygulamanın kolaylıkla istenilen algoritmayı geliştirmeye açık olması bakımından, sonrasında kullanımla birlikte ortaya çıkabilecek gereksinimlerde uygulamanın geliştirilerek daha etkin bir hale dönüştürülmesi muhtemeldir. Püskürtme betonun yaklaşık  maliyetini  bilgisayar  ortamında  hesaplama  imkânı  sağlayan  bu  uygulama,  gerek duyulan  ihtiyaçlar  doğrultusunda  yeni  özellikler  eklenmesi  ile  geliştirilebilir  olması  uygulamanın  önemli  bir özelliğidir. Böylece yazılımın farklı çalışmalarda uygulanabilmesine olanak sağlanabilecektir.

## Teşekkür (Acknowledgement)

Bu çalışma Süleyman Demirel Üniversitesi Bilimsel Araştırma Projeleri Koordinasyon Birimi tarafından 1977-YL09 nolu proje kapsamında desteklenmiştir. Ayrıca yazılımın test verilerini sağladığı için Bekaert A.Ş firmasına teşekkür ederiz.

## Conflict of Interest (Çıkar Çatışması)

Yazarlar tarafından herhangi bir çıkar çatışması beyan edilmemiştir. No conflict of interest was declared by the authors.

## Kaynaklar (References)

Abanda, F.H. Kamsu-Foguem, B. Tah, J.H.M., 2017. BIM-New Rules of Measurement Ontology for Construction Cost Estimation, Engineering Science and Technology, an International Journal 20 (2017) 443-459, http://dx.doi.org/10.1016/j.jestch.2017.01.007

Aka, İ., ve Celep, Z., 1978. Püskürtme Beton ve Uygulaması, İstanbul Teknik Üniversitesi, Mühendislik Mimarlık Fakültesi, 19s. Altın, M., ve Allahverdi, N., 2004. Bilgisayar Destekli İnşaat Maliyet Analizleri, Selçuk Teknik Dergisi, 3(1), 1-8.

Arıoğlu,  E.,  ve  Yüksel,  A.,  1999.  Tünel  ve  Yer  altı  Mühendislik  Yapılarında  Çözümlü  Püskürtme  Beton  Problemleri,  Türk Mühendis ve Mimar Odaları Birliği, Maden Mühendisleri Odası İstanbul Şubesi, İstanbul.

Arıoğlu, E., Yüksel, A., Yılmaz A.O., 2008. Püskürtme  Beton Bilgi Föyleri-Çözümlü Problemler, Türk Mühendis ve Mimar Odaları Birliği, Maden Mühendisleri Odası İstanbul Şubesi, Yayın No: 142, ISBN 978-9944-89-565-1, İstanbul.

Ayış, H.İ., 2010. Tünel Açma Sistemlerinde Çelik Lifli Püskürtme Betonun Uygulanabilirliği, Yüksek Lisans Tezi, Yıldız Teknik Üniversitesi, Fen Bilimleri Enstitüsü, Mimarlık Anabilim Dalı Yapı Programı, İstanbul.

Bayraktar,  D.,  ve  Bayraktar,  E.A.,  2016.  Yapım  İşlerinde  Yaklaşık  Maliyetin  Belirlenmesi  Üzerine  Bir  Çalışma,  Beykent Üniversitesi Fen ve Mühendislik Bilimleri Dergisi, 9(2) 2016, 29 - 54.

Beşer,  S.A.,  2017.    Üst  Yapı  İnşaat  İşlerinin  Proje  Üretiminin  ve  Saha  Uygulamalarının  Takip  Edilmesinde  YBM  (Yapı  Bilgi Modellemesi - Building Information Modelling) Programları Kullanılmasının İller Bankası Anonim Şirketine Sağlayacağı Yararların İncelenmesi, Uzmanlık Tezi, İller Bankası Anonim Şirketi.

Bostancıoğlu, E., 2006. Bilgisayar Destekli İnşaat Maliyet Analizleri, Dokuz Eylül Üniversitesi Mühendislik Fakültesi, Fen ve Mühendislik Dergisi, 8(3), 27-49.

Börjesson, P., ve Thell, M., 2009. Shotcrete Simulator For Education of Shotcrete Robot Operators, Master of Science Thesis in Computer  Science,  University  of  Gothenburg,  Department  of  Computer  Science  and  Engineering,  Goteborg,  Sweden. https://gupea.ub.gu.se/handle/2077/22225, Erişim Tarihi: 20/08/2016

Celep, Z., 2017. Deprem Mühendisliğine Giriş ve Depreme Dayanıklı Yapı Tasarımı, Beşinci Baskı, İstanbul.

Çakıroğlu, A.M., 2014. In The Mixing Account of Dry Mix Shotcrete Using DELPHI Programming Language. 4 th  International Advances in Applied Physics and Materials Science Congress &amp; Exhibition, APMAS 2014, 24-27 April 2014, Fethiye/ Muğla. Dağdeviren,  U.,  ve  Kaymak,  B.,  2018.  Yapay  Arı  Koloni  Algoritması  Kullanılarak  Betonarme  İstinat  Duvarlarının  Optimum Maliyet Tasarımını Etkileyen Parametrelerin İncelenmesi, Gazi Üniversitesi Mühendislik ve Mimarlık Fakültesi Dergisi, 33:1 (2018) 239-253, doi 10.17341/gazimmfd.406796

Doğramacı, N., Koçak, A., Ekiz, İ., 2003. Depremde Hasar Gören Yapıların Onarım ve/veya Güçlendirme Maliyetlerinin Toplam Bina Maliyetleri İle Karşılaştırılması, Beşinci Ulusal Deprem Mühendisliği Konferansı, 26-30 Mayıs 2003, İstanbul.

Dziadosz, A., 2013. The Influence of Solutions Adopted at the Stage of Planning the Building Investment on the Accuracy of Cost Estimation, Procedia Engineering 54 (2013) 625-635,

doi: 10.1016/j.proeng.2013.03.057

Gerçek, B., İlal, M.E., Tokdemir , O.B., Günaydın, H.M., 2016. Yapı Bilgi Modellemesi Yardımıyla Metraj ve Maliyet Hesabı, 4. Proje ve Yapım Yönetimi Kongresi, 3 - 5 Kasım 2016, 786-796.

Günaydın, H.M., ve Doğan, S.Z., 2004. A Neural Network Approach for Early Cost Estimation of Structural Systems of Buildings, International Journal of Project Management 22 (2004) 595-602, doi:10.1016/j.ijproman.2004.04.002

Juszczyk,  M.,  2017.  The  Challenges  of  Nonparametric  Cost  Estimation  of  Construction  Works  With  the  Use  of  Artificial Intelligence Tools, Procedia Engineering 196, (2017) 415-422, doi: 10.1016/j.proeng.2017.07.218

Kanıt, R., ve Baykan, U.N., 2004. Bina Yaklaşık Maliyetinin Çoklu Doğrusal Regresyon ile Belirlenmesi, Politeknik Dergisi, 7(4), 359-367.

Karahan,  M.,  ve  Ezin,  Y.,  2014.  PERT-CPM  Tekniğiyle  Bir  İnşaatın  Yapım  Süresi  ve  Maliyetlerinin  Optimizasyonu,  Bartın Üniversitesi İktisadi İdari Bilimler Fakültesi Dergisi, 5(10).

Klakegg, O.J., ve Lichtenberg, S., 2016. Successive Cost Estimation-Successful Budgeting of Major Projects, Procedia - Social and Behavioral Sciences 226 (2016) 176-183. doi: 10.1016/j.sbspro.2016.06.177

Kırankaya,  R.T.,  2007.  Rusya  Federasyonu'nda  İnşaat  İşçiliği  Verimliliğinin  ve  Proje  Karlılığına  Etki  Eden  Faktörlerin İncelenmesi, İstanbul Teknik Üniversitesi, Fen Bilimleri Enstitüsü, İnşaat Mühendisliği Anabilim Dalı, Yapı İşletmesi.

Kuruoğlu,  M.,  Yönez,  E.,  Topkaya,  E.,  Çelik  Y.L.,  2012.    İnşaat  Sektöründe  Kullanılan  Ön  Maliyet  Tahmin  Yöntemlerinin Karşılaştırılması, e-Journal of New World Sciences Academy, 7(1), 263-272.

Lee, S.-K, Kim, K.-R, Yu, J.-H., 2014. BIM and Ontology-Based Approach for Building Cost Estimation, Automation in Construction 41 (2014) 96-105, http://dx.doi.org/10.1016/j.autcon.2013.10.020

Özgür, S.H., ve İleri, R., 2002. Evsel Nitelikli Merkezi Atıksu Arıtma Tesisinin Bilgisayar Destekli Tasarımı, Sakarya Üniversitesi, Fen Bilimleri Enstitüsü Dergisi, 3 (6), 69-76.

Özgür, E., 2004. Bilgisayar Programlama Dilleri, İnşaat Mühendisleri Odası, İzmir Şubesi, 19, (118).

- Tapao, A., ve Cheerarot, R., 2017. Optimal Parameters and Performance of Artificial Bee Colony Algorithm for Minimum Cost Design of Reinforced Concrete Frames, Engineering Structures 151 (2017) 802-820,

http://dx.doi.org/10.1016/j.engstruct.2017.08.059. Uğur, L.  O.  2007.  İnşaat  Firmalarının  Maliyet  ve  Süre  Belirleme  Yöntemleri  Üzerine  Bir  Alan  Çalışması,  4.  İnşaat  Yönetimi Kongresi, 30-31 Ekim 2007, İstanbul, Türkiye. Yaman, H., ve İlhan, B., 2010. İnşaat Sektörü'nde Bina Enformasyonu Modellemesi Kavramına Genel Bir Bakış, 1. Proje ve Yapım Yönetimi Kongresi, 29 Eylül -1 Ekim 2010, ODTÜ Kültür ve Kongre Merkezi, 962-976s., Ankara. Yanmaz, Ö., ve Luş, H., 2005. Yapı Güçlendirme Yöntemlerinin  Yapı Güçlendirme Yöntemlerinin Fayda-Maliyet Analizi, İnşaat Mühendisleri Odası Teknik Dergi, 3497-3522, Yazı 233. Yüksek,  S.,  Demirci,  A.,  ve  Dayı,  Ö.,  2004.  Pulpınar  Krom  İşletmesinde  Püskürtme  Beton  Uygulamaları  ve  Sonuçlarının Geleneksel Ahşap Tahkimatla Karşılaştırılması, KAYAMEK′2004-VII. Bölgesel Kaya Mekaniği Sempozyumu, Sivas, Türkiye.

- Wang, K.-C.,  Wang,  W.-C.,  Wang,  H.-H.,  Hsu,  P.-Y.,  Wu,  W.-H.,  Kung,  C.-J.,  2016.  Applying  Building  Information  Modeling  to Integrate Schedule and Cost for Establishing Construction Progress Curves, Automation in Construction 72 (2016) 397410, http://dx.doi.org/10.1016/j.autcon.2016.10.005

## EKLER (Appendix)

EK 1. Test için Kullanılan Maliyet Çalışması (Cost study used for testing)
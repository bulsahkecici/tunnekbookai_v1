# Kitap Kapsamı ve Soru Bankası v2 — İnceleme Taslağı

Bu dosya iki şeyi birlikte tanımlar: **kitap outline'ının v2 hâli** ve **her aktif bölüm için
yeniden yazılmış soru bankası**. Onaylandığında `book/scope/normalized/` ve
`book/question_bank/normalized/` altındaki v2 dosyaları bu belgeden üretilir.

## Nasıl düzenlenir

- Her başlık `## <bölüm-no> <başlık> {etiket}` biçimindedir. Etiketler:
  - `{chapter}` — üst düzey bölüm; soru içermez.
  - `{keep}` — v1'den korunan başlık.
  - `{new}` — v2'de eklenen başlık.
  - `{inactive: gerekçe}` — kitapta yer almayacak; soru içermez, kimliği geçmiş kayıt için korunur.
  - `{keep, human-analysis}` — korunur, fakat model bu bölümü literatürden yazamaz; insan analiz
    artifact'i (proje verisi) sağlanana kadar `HUMAN_ANALYSIS_ARTIFACT_REQUIRED` kalır.
- Soru satırları `1. ...` biçiminde numaralıdır. Soru silebilir, ekleyebilir, yeniden
  yazabilirsiniz; numaralar normalize sırasında yeniden verilir.
- Başlık metnini değiştirirseniz classification taksonomisi de güncellenir; bölüm **numarasını**
  değiştirmeyin (corpus sınıflandırması ve chunk `section_id` alanları bu numaralara bağlıdır).
- Parantez içindeki `[corpus: birincil/ikincil]` notu, canonical corpus'ta o bölüme sınıflanmış
  belge sayısıdır; yalnızca bilgi amaçlıdır, silinebilir.

## Outline değişikliklerinin özeti

| Değişiklik | Bölümler | Gerekçe |
| --- | --- | --- |
| Pasif | 5.1, 5.2, 5.3, 5.9, 5.9.1, 5.9.2 | Tez yapısı ("Çalışmanın Amacı/Kapsamı/Yöntemi", literatür taraması); kitap içeriği değil |
| Pasif | 6.1, 6.1.1, 6.1.2, 6.1.3, 6.2, 6.2.1, 6.2.2 | 5.x ile aynı tez yapısının tekrarı; 6.2 başlığında tez yazarı adı var |
| İnsan analizi | 7.1, 7.2 | Araştırma bulguları; corpus'tan değil proje verisinden yazılır |
| Yeni | 3.1, 3.2, 3.3 | Bölüm 3'ün hiç alt başlığı yoktu; corpus'ta KGM envanter, seminer ve proje belgeleri var |
| Yeni | 4.3, 4.3.1 | Kaynak taslakta "…" ile boş bırakılan maliyet analizi başlıklarından kalanlar; 4.3 kendi genel-yöntem sorularıyla aktif tutuldu çünkü 4.3.1 ve 4.3.5'in aktif ebeveyni olması gerekiyor (şema kuralı: aktif alt başlık altında aktif üst başlık) |
| Yeni | 6.3 | Bölüm 6'nın tez başlıkları çıkınca içeriği kalmıyordu; yapım maliyeti gövdesinden corpus desteği olan tek başlık |
| Pasif | 4.2, 4.3.2, 4.3.3, 4.3.4, 6.4, 6.5, 6.6 | Corpus'ta bu başlıklar için doğrudan destek yok (classification bu numaralara hiç belge atamamış); 2.2.3'te yaşanan destek sorununun büyüğünü önlemek için pasifleştirildi |

Aktif soru bölümü sayısı: 59 → 52 (20 pasif, 6 yeni). Soru sayısı: 2.950 → 628.
Bölüm başına soru sayısı sabit değildir; konteyner başlıklar (5.5.2) daha az soru taşır.

---

## 1 GİRİŞ {chapter}

## 1.1 Tünelin Tanımı {keep}
[corpus: 2/1]

1. Tünel mühendislik açısından nasıl tanımlanır; kazı, boşluk ve destekleme kavramları tanımda nasıl yer alır?
2. Tünel ile aç-kapa yapı, galeri, kuyu, yeraltı boşluğu ve derin yarma arasındaki ayrım nedir?
3. Tünelin taşıyıcı sistemi olarak "kaya/zemin–destek etkileşimi" ne anlama gelir?
4. Farklı disiplinler (jeoloji, geoteknik, yapı, ulaşım) tüneli hangi bakış açılarıyla tanımlar?
5. Ulusal mevzuat ve şartnamelerde (KGM Teknik Şartnamesi, Tünel İşletme Yönetmeliği) tünel nasıl tanımlanmıştır?
6. Uluslararası kaynaklarda (PIARC, ITA, AB 2004/54/EC direktifi) tünel tanımı ve asgari uzunluk eşikleri nelerdir?
7. Karayolu, demiryolu, metro, su/hidrolik ve altyapı tünelleri arasındaki temel işlev farkları nelerdir?
8. Bir tünelin temel geometrik büyüklükleri (uzunluk, kesit alanı, açıklık, örtü kalınlığı, eğim) nasıl tanımlanır?
9. Tünel kesitinin ana bölümleri (kalot, stros, taban kemeri, kemer, ayak, portal) nelerdir?
10. Tünel neden yapılır; hangi topoğrafik, çevresel, trafik ve ekonomik koşullar tünel çözümünü gerekli kılar?
11. Tünel çözümünün alternatif güzergâh, yarma veya viyadük çözümlerine göre avantaj ve dezavantajları nelerdir?
12. Tek tüp ve çift tüp tünel ayrımı nasıl yapılır ve bu ayrım işletmeyi nasıl etkiler?
13. Kısa, orta ve uzun tünel sınıflaması hangi uzunluk eşiklerine göre yapılır ve işletme gereksinimlerini nasıl belirler?
14. Tünelin yapım, işletme ve bakım aşamalarını kapsayan yaşam döngüsü nasıl tanımlanır?
15. Tünel ile ilgili temel Türkçe–İngilizce terminoloji ve sık karıştırılan terimler nelerdir?
16. Tünelin toplumsal ve ekonomik işlevi (erişilebilirlik, süre kazancı, güvenlik, çevre) nasıl açıklanır?
17. Türkiye'de karayolu tünellerinin ulaşım ağı içindeki yeri ve önemi nedir?

## 1.2 Tünellerin Sınıflandırılması {keep}
[corpus: 4/2]

1. Tüneller kullanım amacına göre nasıl sınıflandırılır (karayolu, demiryolu, metro, su, enerji, altyapı, madencilik)?
2. Tüneller içinden geçtikleri ortama göre (kaya, yumuşak zemin, su altı) nasıl sınıflandırılır?
3. Tüneller yapım yöntemine göre (delme-patlatma/NATM, TBM, aç-kapa, batırma tüp, mikrotünel) nasıl sınıflandırılır?
4. Tüneller uzunluğa göre nasıl sınıflandırılır ve uzunluk sınıfları hangi güvenlik donanımı gereksinimlerini tetikler?
5. Tüneller örtü kalınlığına/derinliğe göre (sığ, derin) nasıl sınıflandırılır ve bu ayrım tasarımı nasıl etkiler?
6. Tüneller kesit şekline göre (dairesel, at nalı, dikdörtgen, yumurta) nasıl sınıflandırılır?
7. Kesit şekli seçimi ile zemin koşulları ve yapım yöntemi arasındaki ilişki nedir?
8. Tek yönlü ve çift yönlü trafikli tüneller nasıl ayrılır ve bu ayrım güvenlik risklerini nasıl değiştirir?
9. Kentsel ve kent dışı tüneller hangi açılardan farklılaşır?
10. Dağ tünelleri, su altı tünelleri ve kentsel sığ tüneller için tipik tasarım ve yapım farkları nelerdir?
11. AB Direktifi 2004/54/EC ve KGM mevzuatında tünel sınıfları ve kategori tanımları nelerdir?
12. Trafik hacmi (YOGT) ve tünel uzunluğuna dayalı sınıflandırma nasıl yapılır?
13. Tehlikeli madde taşımacılığı açısından tüneller (ADR tünel kategorileri A–E) nasıl sınıflandırılır?
14. Tünellerin risk sınıflaması hangi ölçütlerle yapılır?
15. Norveç N500 ve benzeri ulusal standartlarda tünel sınıfları nasıl tanımlanır ve Türkiye uygulamasıyla nasıl karşılaştırılır?
16. Sınıflandırma sistemleri bakım-işletme organizasyonunu ve maliyet tahminini nasıl etkiler?
17. Türkiye'deki mevcut karayolu tünelleri bu sınıflara göre nasıl dağılır?

## 1.3 Tünellerin Tarihçesi {keep}
[corpus: 2/2]

1. Tünelciliğin tarihsel gelişimi hangi ana dönemlere ayrılır (antik çağ, sanayi devrimi, modern dönem)?
2. Antik çağda tüneller hangi amaçlarla (su, madencilik, savunma) ve hangi tekniklerle açılmıştır?
3. Barut ve dinamitin tünel kazısına girişi tünelciliği nasıl değiştirmiştir?
4. Demiryolu çağı (19. yüzyıl) tünel yapımını nasıl dönüştürmüştür?
5. Kalkan (shield) yönteminin ve Thames Tüneli'nin tarihsel önemi nedir?
6. Püskürtme beton, kaya bulonu ve NATM'nin ortaya çıkışı tünelciliği nasıl etkilemiştir?
7. TBM teknolojisinin gelişimi hangi kilometre taşlarından geçmiştir?
8. Batırma tüp tünel yönteminin tarihsel gelişimi nasıldır?
9. Tünel havalandırma, aydınlatma ve güvenlik sistemleri tarihsel olarak nasıl gelişmiştir?
10. Büyük tünel felaketleri tünel güvenliği mevzuatının gelişimini nasıl etkilemiştir?
11. Tünel tarihindeki teknolojik gelişmeler yapım maliyetlerini ve sürelerini nasıl değiştirmiştir?
12. Türkiye tünelcilik tarihi dünya tarihçesi içinde nasıl konumlandırılır?

## 1.3.1 Dünyadaki İlk Tüneller {keep}
[corpus: 0/2]

1. Bilinen en eski tüneller hangileridir; nerede, ne zaman ve hangi amaçla yapılmıştır?
2. Babil Fırat altı geçidi ve Kudüs Siloam (Hizkiya) tüneli gibi antik örnekler için kaynaklarda hangi bilgiler yer alır?
3. Samos Eupalinos Tüneli'nin mühendislik açısından önemi nedir?
4. Roma dönemi su kemeri ve yol tünelleri (Furlo, Cocceius) hangi tekniklerle açılmıştır?
5. Kanal çağı tünelleri (Malpas Tüneli vb.) hangi yenilikleri getirmiştir?
6. İlk demiryolu tünelleri hangileridir ve yapımlarında hangi sorunlarla karşılaşılmıştır?
7. Mont Cenis (Fréjus), Gotthard ve Simplon demiryolu tünellerinin tarihsel önemi nedir?
8. Thames Tüneli ilk kalkan uygulaması olarak neden önemlidir?
9. İlk metro tünelleri (Londra) hangi yöntemlerle yapılmıştır?
10. Dünyanın ilk karayolu tünelleri hangileridir?
11. İlk tünellerde kullanılan kazı, aydınlatma ve havalandırma teknikleri nelerdir?
12. İlk tünellerin yapım süreleri, iş kazaları ve maliyetleri hakkında hangi bilgiler mevcuttur?

## 1.3.2 Türkiye'de İlk Tünel {keep}
[corpus: 0/0]

1. Anadolu'da antik dönemden kalan tünel ve yeraltı su yapıları (örneğin Titus Tüneli) hangileridir?
2. Osmanlı döneminde yapılan ilk tüneller hangileridir?
3. İstanbul Tünel (1875) dünya kentsel raylı sistem tarihinde nasıl konumlanır?
4. Anadolu ve Bağdat demiryolu hatlarındaki tüneller (Toros geçişi) hangi koşullarda yapılmıştır?
5. Cumhuriyet döneminde ilk karayolu tünelleri hangileridir ve hangi tekniklerle yapılmıştır?
6. Türkiye'de ilk tünellerin yapımında hangi yabancı ve yerli mühendislik kaynakları kullanılmıştır?
7. Eski Zigana ve Bolu Dağı gibi erken karayolu tünelleri ilk tünel tarihçesi içinde nasıl yer alır?
8. Türkiye'de ilk hidrolik ve su iletim tünelleri hangileridir?
9. Türkiye'de tünelcilik bilgi birikiminin oluşmasında hangi kurumlar (KGM, DSİ, TCDD) rol oynamıştır?
10. Türkiye'de ilk tünellere ilişkin güvenilir arşiv ve belgesel kaynaklar nelerdir?

## 1.4 En İyi Tünel Mühendislik Uygulamaları {keep}
[corpus: 3/1]

1. "En iyi uygulama" kavramı tünel mühendisliğinde ne anlama gelir ve hangi ölçütlerle belirlenir?
2. Dünyadaki en uzun karayolu, demiryolu ve su altı tünelleri hangileridir ve hangi özellikleriyle öne çıkar?
3. Gotthard Baz Tüneli, Lærdal Tüneli, Kanal Tüneli ve Seikan Tüneli gibi projeler hangi mühendislik yeniliklerini içerir?
4. Uzun tünellerde güvenlik tasarımında (kaçış galerileri, paralel tüp, havalandırma) hangi en iyi uygulamalar öne çıkar?
5. Zor jeolojide (yüksek örtü, sıkışan zemin, su girişi) başarılı uygulamalar hangi yöntemleri kullanmıştır?
6. Kentsel tünellerde oturma kontrolü ve yapı koruma için hangi en iyi uygulamalar vardır?
7. Tünel projelerinde risk yönetimi ve sözleşme yönetimi için uluslararası en iyi uygulamalar (ITIG uygulama kodu vb.) nelerdir?
8. Tünel tasarım ve yapımında BIM, dijital ikiz ve izleme teknolojileri için örnek uygulamalar nelerdir?
9. Sürdürülebilirlik ve karbon azaltımı için tünel projelerinde hangi uygulamalar (CEEQUAL vb.) benimsenmiştir?
10. İşletme ve bakımda (SCADA, olay yönetimi, planlı bakım) örnek uygulamalar hangileridir?
11. Maliyet ve süre performansı açısından başarılı sayılan tünel projeleri hangileridir ve neden?
12. Norveç, İsviçre, Avusturya ve Japonya gibi ülkelerin tünelcilik yaklaşımlarının ayırt edici özellikleri nelerdir?
13. Türkiye'de uluslararası ölçekte öne çıkan tünel projeleri (Avrasya, Marmaray, Ovit, Yeni Zigana) hangileridir?
14. Tünel işletmesinde kalite güvence ve performans göstergeleri için en iyi uygulamalar nelerdir?
15. Uluslararası örneklerden Türkiye uygulamasına aktarılabilecek dersler nelerdir?

## 1.4.1 Dünyada Karayolu Tünelleri {keep}
[corpus: 0/2]

1. Dünyadaki en uzun karayolu tünelleri hangileridir (uzunluk, ülke, açılış yılı)?
2. Lærdal Tüneli'nin tasarım ve işletme özellikleri nelerdir?
3. Gotthard Karayolu Tüneli'nin özellikleri ve 2001 yangını sonrasında alınan önlemler nelerdir?
4. Alp geçişlerindeki karayolu tünelleri (Mont Blanc, Fréjus, Tauern, Arlberg) hangi özelliklere sahiptir?
5. Su altı karayolu tünelleri (Ryfast, Tokyo Bay Aqua-Line, Øresund) hangi yöntemlerle yapılmıştır?
6. Çin'in son dönem uzun karayolu tünel projeleri hangi özellikleriyle öne çıkar?
7. Kentsel karayolu tünelleri (Boston Big Dig, Madrid M-30, Stockholm) hangi sorunları çözmüştür?
8. Dünyada karayolu tünellerinin sayısı ve toplam uzunluğu hakkında hangi veriler mevcuttur?
9. Karayolu tünelleri için ülkelere göre tasarım standartları (N500, RABT, RVS, PIARC) nasıl karşılaştırılır?
10. Dünyadaki karayolu tünellerinde km başına tipik yapım maliyetleri hangi aralıktadır?
11. Uzun karayolu tünellerinde işletme organizasyonu nasıl kurulur?
12. Karayolu tünellerinde geçiş ücreti ve finansman modelleri nelerdir?
13. Dünya karayolu tünellerinden Türkiye için hangi teknik dersler çıkarılabilir?

## 1.4.2 Türkiye'de Karayolu Tünelleri {keep}
[corpus: 2/5]

1. KGM sorumluluğundaki karayolu tünellerinin sayısı, toplam uzunluğu ve bölgelere dağılımı nedir?
2. Türkiye'nin en uzun karayolu tünelleri hangileridir?
3. Ovit Tüneli'nin yapım koşulları, yöntemi ve özellikleri nelerdir?
4. Yeni Zigana Tüneli'nin tasarım, yapım ve işletme özellikleri nelerdir?
5. Avrasya Tüneli'nin yapım yöntemi, finansman modeli ve işletme yapısı nasıldır?
6. Bolu Dağı Tüneli'nin yapım süreci ve karşılaşılan jeolojik sorunlar nelerdir?
7. Otoyol tünelleri ile devlet ve il yolu tünelleri hangi açılardan farklılaşır?
8. Türkiye'de karayolu tünelleri hangi yöntemlerle (NATM, TBM, aç-kapa) yapılmaktadır ve dağılımı nedir?
9. Türkiye'deki karayolu tünellerinde tipik kesit, uzunluk ve tüp yapısı nasıldır?
10. Türkiye'de tünel yapımının yıllara göre gelişimi ve artış eğilimi nasıldır?
11. Türkiye'de karayolu tünellerinde uygulanan güvenlik ve elektromekanik standartları nelerdir?
12. Türkiye'de tünellerin işletmesinden sorumlu kurumsal yapı nasıldır?
13. Türkiye'deki karayolu tünellerinin yapım maliyeti verileri hakkında hangi bilgiler kamuya açıktır?
14. Türkiye'de yapımı süren ve planlanan büyük tünel projeleri hangileridir?
15. Türkiye tünelciliğinin dünya ölçeğindeki konumu nasıl değerlendirilir?

## 1.5 Tünel Felaketleri {keep}
[corpus: 22/6]

1. Tünel felaketi kavramı nasıl tanımlanır; kaza ile felaket ayrımı nasıl yapılır?
2. Tünellerde meydana gelen olaylar hangi türlere ayrılır (yangın, çarpışma, tehlikeli madde, göçük, su baskını, deprem)?
3. Tünel yangınlarının açık alandaki yangınlardan farkı nedir; ısı, duman ve tahliye açısından hangi riskler taşır?
4. Tünel felaketlerinin başlıca nedenleri (araç arızası, sürücü davranışı, tasarım eksikliği, işletme hatası) nelerdir?
5. Tünel felaketlerinde can kaybını belirleyen faktörler nelerdir?
6. Tünel felaketleri sonrasında uluslararası mevzuat (AB 2004/54/EC, PIARC tavsiyeleri) nasıl değişmiştir?
7. Tünel yangınlarında duman kontrolü ve havalandırma stratejileri nelerdir?
8. Tünel felaketlerinin ekonomik maliyeti (kapanma, onarım, dolaylı etkiler) nasıl hesaplanır?
9. Yapım aşamasındaki tünel kazaları (göçük, patlatma, TBM kazaları) hangi nedenlerle olur?
10. Deprem ve heyelanların tünellere etkisi nedir ve örnek olaylar hangileridir?
11. Tünel felaketlerinden çıkarılan tasarım dersleri (kaçış yolları, kaçış mesafeleri, yangın dayanımı) nelerdir?
12. Tünel risk analizi yöntemleri (nicel risk analizi, senaryo analizi) felaketleri önlemede nasıl kullanılır?
13. Tünel işletmecisinin acil durum planı ve tatbikat yükümlülükleri nelerdir?
14. Tünel felaketlerinin istatistiksel sıklığı ve eğilimi hakkında hangi veriler vardır?
15. Felaket sonrası tünel yapısının hasar tespiti ve onarımı nasıl yapılır?

## 1.5.1 Dünyada Gerçekleşen Önemli Tünel Felaketleri {keep}
[corpus: 4/2]

1. Mont Blanc Tüneli yangını (1999) nasıl gelişmiş, hangi kayıplara yol açmış ve hangi dersler çıkarılmıştır?
2. Tauern Tüneli yangını (1999) ve Gotthard Tüneli yangını (2001) nasıl gelişmiştir?
3. Kaprun füniküler tünel yangını (2000) hangi özellikleriyle farklıdır?
4. Daegu metro yangını (2003) ve diğer raylı sistem tünel felaketleri hangi dersleri vermiştir?
5. Fréjus (2005), Viamala ve Burnley (2007) gibi diğer önemli karayolu tünel yangınları nasıl olmuştur?
6. Tünel yapım kazaları (Heathrow Express göçüğü 1994, Nicoll Highway 2004 vb.) nasıl gerçekleşmiştir?
7. Tehlikeli madde taşıyan araç kazaları (Caldecott 1982, Nihonzaka 1979) hangi sonuçları doğurmuştur?
8. Su altı tünellerinde su baskını olayları nasıl gerçekleşmiştir?
9. Bu felaketlerde can kaybı, yaralanma, kapanma süresi ve maddi zarar hangi düzeydedir?
10. Felaket sonrası yapılan iyileştirmeler (paralel kaçış tüneli, havalandırma revizyonu, araç mesafesi kuralı) nelerdir?
11. Felaketlerin AB tünel güvenliği direktifinin doğuşundaki rolü nedir?
12. Dünya tünel felaketlerinin ortak nedenleri ve örüntüleri nelerdir?

## 1.5.2 Türkiye'de Gerçekleşen Önemli Tünel Kazaları {keep}
[corpus: 3/1]

1. Türkiye'de kayıtlara geçen önemli karayolu tünel kazaları hangileridir?
2. Türkiye'de karayolu tünellerinde yaşanan yangın olayları hangileridir ve nasıl müdahale edilmiştir?
3. Türkiye'de tünel yapımı sırasında yaşanan kazalar (göçük, patlatma, iş kazaları) hangileridir?
4. Türkiye'deki tünel kazalarının nedenleri hangi kategorilerde toplanır?
5. Türkiye'de tünel kazalarına ilişkin istatistikler hangi kurumlarca tutulmaktadır ve ne ölçüde erişilebilirdir?
6. Türkiye'deki tünellerde kaza sonrası kapanma süreleri ve onarım maliyetleri nasıl olmuştur?
7. Türkiye'de deprem ve heyelanların tünellere etkisine dair örnekler nelerdir?
8. Türkiye'de tünel kazaları sonrasında mevzuat ve işletme uygulamalarında hangi değişiklikler yapılmıştır?
9. Tünel İşletme Yönetmeliği kaza ve acil durum yönetimi konusunda hangi hükümleri içerir?
10. Türkiye'deki tünellerde acil durum tatbikatları ve müdahale organizasyonu nasıl yürütülmektedir?
11. Türkiye tünel kazalarından çıkarılan dersler dünya örnekleriyle nasıl karşılaştırılır?

## 2 TÜNEL ANA ELEMANLARI, ANA ÖZELLİKLERİ VE YAPIM TEKNİKLERİ {chapter}

## 2.1 Tünel Yapı/Destek Elemanları {keep}
[corpus: 42/37]

1. Tünel yapı sistemi hangi ana elemanlardan oluşur (kazı boşluğu, ön destek, kalıcı kaplama, taban kemeri, portal, yalıtım-drenaj, nişler)?
2. Geçici (birincil) destek ile kalıcı (ikincil) kaplama arasındaki işlev farkı nedir?
3. Kaya/zemin–destek etkileşimi ve yük paylaşımı ilkesi nasıl açıklanır?
4. Kalıcı iç kaplama türleri (yerinde dökme beton, segment, kalıcı püskürtme beton) ve seçim ölçütleri nelerdir?
5. Drenajlı ve drenajsız (su basıncına dayanan) tünel kavramları nasıl ayrılır?
6. Su yalıtım membranı, koruyucu keçe ve drenaj boruları nasıl yerleştirilir?
7. Taban kemeri (invert) hangi koşullarda gereklidir ve nasıl tasarlanır?
8. Portal yapıları ve portal şevleri hangi elemanlardan oluşur?
9. Tünel içi nişler, cepler, bağlantı ve kaçış galerileri nasıl konumlandırılır?
10. Kablo kanalları, kaldırımlar ve yol üstyapısı tünel yapı sistemine nasıl entegre edilir?
11. Elektromekanik ekipmanın (fan, armatür, tabela) yapıya bağlantısı nasıl tasarlanır?
12. Yapı elemanlarının kalite kontrol ve kabul esasları nelerdir?
13. Yapı/destek elemanlarının toplam yapım maliyeti içindeki payı nasıldır?
14. Yapı elemanlarının servis ömrü ve bakım gereksinimleri nasıl farklılaşır?
15. KGM Teknik Şartnamesi tünel yapı elemanları için hangi esasları belirler?

## 2.1.1 Tünellerle İlgili Tanımlamalar {keep}
[corpus: 1/1]

1. Kalot, stros, taban kemeri, ayna, ilerleme adımı ve örtü kalınlığı gibi temel tünel terimleri nasıl tanımlanır?
2. Portal, giriş yapısı, yaklaşım yarması, kaçış galerisi ve bağlantı tüneli terimleri neyi ifade eder?
3. Konverjans, deformasyon, gevşeme bölgesi ve kemerlenme (arching) kavramları nedir?
4. Kaya kütlesi, süreksizlik, RQD, RMR, Q ve GSI gibi kaya sınıflama terimleri nasıl tanımlanır?
5. Sıkışan (squeezing), şişen (swelling) ve kaya patlaması (rockburst) davranışları nasıl tanımlanır?
6. Ayna stabilitesi, yüzey oturması ve hacim kaybı kavramları nedir?
7. NATM, ADECO-RS, TBM türleri (EPB, slurry, açık tip), aç-kapa ve batırma tüp gibi yöntem terimleri nasıl tanımlanır?
8. Tünel havalandırma terimleri (boyuna, enine, yarı enine havalandırma, jet fan, kritik hız) nedir?
9. Tünel aydınlatma terimleri (eşik bölgesi, geçiş bölgesi, iç bölge, L20 parlaklığı) nedir?
10. Tünel işletme terimleri (SCADA, olay algılama, trafik yönetim merkezi, kapatma protokolü) nedir?
11. Bakım terimleri (koruyucu, düzeltici, öngörücü bakım; muayene sınıfları) nasıl tanımlanır?
12. Maliyet terimleri (birim fiyat, keşif, yaklaşık maliyet, metraj, iş kalemi) tünel bağlamında nasıl kullanılır?
13. Türkçe–İngilizce tünel terminolojisi için başvurulabilecek kaynaklar nelerdir?

## 2.1.2 Tünel Destekleme Elemanları {keep}
[corpus: 27/42]

1. Püskürtme beton için karışım, kalınlık, lif takviyesi, uygulama ve kalite kontrol esasları nelerdir?
2. Hasır çelik ve çelik lif takviyesi püskürtme betonda nasıl kullanılır?
3. Kaya bulonu türleri (SN, Swellex, kendinden delmeli, harçlı, mekanik ankrajlı) ve seçim ölçütleri nelerdir?
4. Bulon boyu, aralığı ve öngerme değerleri nasıl belirlenir?
5. Çelik iksa ve kafes kiriş (lattice girder) türleri ve montaj esasları nelerdir?
6. Süren (forepoling), boru şemsiye ve ayna bulonları hangi zemin koşullarında uygulanır?
7. Ayna desteklemesi (ayna püskürtme betonu, fiberglas ayna bulonu) nasıl yapılır?
8. Zemin dondurma, jet grout ve enjeksiyon destek sistemi olarak nasıl kullanılır?
9. Segment kaplama (TBM tünelleri) tasarımı, birleşim detayları ve contaları nasıldır?
10. Yerinde dökme beton kaplamada kalıp sistemleri ve beton sınıfı nasıl seçilir?
11. Destekleme sınıfları (NATM sınıfları, KGM kaya sınıfları) hangi destek kombinasyonlarını tanımlar?
12. Destek elemanlarının kurulum sırası ile ilerleme adımı arasındaki ilişki nasıldır?
13. Destek elemanlarında kalite kontrol ve deneyler (bulon çekme deneyi, beton dayanımı) nasıl yapılır?
14. Destek elemanlarının birim fiyatları ve toplam maliyet içindeki ağırlıkları nasıl değerlendirilir?
15. Destekleme sistemlerindeki yetersizlik ve göçük örnekleri hangi dersleri vermiştir?

## 2.2 Tünel Yapım Yöntemleri {keep}
[corpus: 50/54]

1. Tünel yapım yöntemleri hangi ana gruplara ayrılır?
2. Yöntem seçimini belirleyen faktörler (jeoloji, uzunluk, kesit, çevre, maliyet, süre) nelerdir?
3. Delme-patlatma yöntemi nasıl uygulanır; delik düzeni, patlayıcı seçimi ve ateşleme esasları nelerdir?
4. NATM'nin temel ilkeleri nelerdir ve gözlemsel yaklaşım nasıl işler?
5. Mekanik kazı (roadheader, kazı makineleri) hangi koşullarda tercih edilir?
6. TBM türleri (açık tip, tek/çift kalkanlı, EPB, slurry) ve kullanım alanları nelerdir?
7. Aç-kapa yöntemi nasıl uygulanır; aşağıdan yukarı ve yukarıdan aşağı (top-down) yaklaşımı nedir?
8. Batırma tüp tünel yöntemi nasıl uygulanır?
9. Mikrotünel ve boru itme yöntemleri hangi projelerde kullanılır?
10. Tam kesit, yarım kesit (kalot-stros) ve çoklu galeri kazı düzenleri ne zaman uygulanır?
11. Yöntemlerin ilerleme hızları ve tipik günlük/aylık ilerleme değerleri nelerdir?
12. Yöntemlerin maliyet karşılaştırması nasıl yapılır; TBM hangi uzunlukta ekonomik olur?
13. Yöntemlerin iş güvenliği ve çevresel etkileri nasıl karşılaştırılır?
14. Kazı sırasında ölçüm-izleme sonuçlarına göre destek uyarlaması nasıl yapılır?
15. Türkiye'de karayolu tünellerinde hangi yöntemler yaygındır ve neden?
16. KGM Teknik Şartnamesi tünel yapım yöntemleri için hangi esasları belirler?

## 2.2.1 Kayaç Zeminde Açılan Tüneller {keep}
[corpus: 15/50]

1. Kaya tünellerinde kaya kütlesi davranışı nasıl sınıflandırılır (RMR, Q, GSI) ve destek tasarımına nasıl dönüştürülür?
2. Kaya tünellerinde delme-patlatma tasarımı (kesme, kontur delikleri, düzgün patlatma) nasıl yapılır?
3. Aşırı kazı (overbreak) ve alt kazı nasıl kontrol edilir ve maliyete etkisi nedir?
4. Sıkışan kaya, şişen kaya ve kaya patlaması koşullarında hangi önlemler alınır?
5. Fay zonları ve zayıf kaya kesimlerinde geçiş nasıl yapılır?
6. Kaya tünellerinde su girişi ve enjeksiyon uygulamaları nasıl yönetilir?
7. Yüksek örtülü tünellerde gerilme ve sıcaklık sorunları nelerdir?
8. Kaya tünellerinde TBM seçimi (açık gripper, kalkanlı) ve performans tahmini nasıl yapılır?
9. Kaya tünellerinde destek sınıfı geçişleri sahada nasıl kararlaştırılır?
10. Kaya tünellerinde ölçüm-izleme (konverjans, ekstansometre, yük hücresi) nasıl uygulanır?
11. Kaya tünellerinde tipik ilerleme hızları ve maliyet düzeyleri nelerdir?
12. Türkiye'de kaya ortamında açılan örnek tüneller ve karşılaşılan sorunlar nelerdir?
13. Kaya tünellerinde iş sağlığı ve güvenliği riskleri (kaya düşmesi, patlatma, toz) nasıl yönetilir?

## 2.2.2 Yumuşak Zeminde Açılan Tüneller {keep}
[corpus: 24/15]

1. Yumuşak zemin tünelciliği kaya tünelciliğinden hangi açılardan farklıdır?
2. Zemin türü (kil, silt, kum, çakıl, dolgu) ve yeraltı suyu tünel davranışını nasıl etkiler?
3. Ayna stabilitesi nasıl değerlendirilir ve ayna desteği nasıl sağlanır?
4. Yüzey oturması nasıl tahmin edilir (Gauss/Peck yaklaşımı, hacim kaybı) ve sınırlandırılır?
5. EPB ve slurry TBM'lerin yumuşak zeminde çalışma ilkeleri ve seçim ölçütleri nelerdir?
6. Yumuşak zeminde konvansiyonel (NATM/püskürtme beton kaplamalı) tünel açma hangi koşullarda mümkündür?
7. Boru şemsiye, jet grout ve zemin dondurma gibi ön destek yöntemleri nasıl uygulanır?
8. Sığ ve kentsel tünellerde bina ve altyapı koruma önlemleri nelerdir?
9. Segment kaplama ve boşluk enjeksiyonu nasıl yapılır?
10. Yumuşak zemin tünellerinde ölçüm-izleme programı nasıl kurulur?
11. Yumuşak zeminde tünel maliyetlerini artıran faktörler nelerdir?
12. Türkiye'deki yumuşak zemin tünel örnekleri (İstanbul metro tünelleri vb.) hangi sorunlarla karşılaşmıştır?
13. Yumuşak zemin tünellerinde göçük ve oturma kaynaklı kaza örnekleri nelerdir?

## 2.2.3 Su Altında Açılan Tüneller {keep}
[corpus: 7/4]

1. Su altı tünelleri hangi yöntemlerle (batırma tüp, TBM ile delme, kaya altından delme-patlatma) yapılır?
2. Batırma tüp yönteminde eleman üretimi, yüzdürme, batırma ve birleştirme adımları nasıldır?
3. Su altı TBM tünellerinde yüksek su basıncına karşı hangi önlemler (hiperbarik müdahale, conta tasarımı) alınır?
4. Su altı tünellerinde su sızıntısı ve yalıtım nasıl sağlanır?
5. Su altı tünellerinde deprem tasarımı (sismik derz/bilezik) nasıl yapılır?
6. Su altı tünellerinde havalandırma, drenaj ve pompalama gereksinimleri nasıl farklılaşır?
7. Su altı tünellerinin yapım maliyeti ve maliyet etkenleri nelerdir?
8. Dünyadaki önemli su altı tünelleri (Kanal Tüneli, Seikan, Øresund, Ryfast) hangi yöntemlerle yapılmıştır?
9. Marmaray ve Avrasya Tüneli'nin su altı geçişleri nasıl tasarlanmış ve yapılmıştır?
10. Su altı tünellerinde işletme ve bakım açısından özel gereksinimler nelerdir?
11. Su altı tünellerinde yaşanan su baskını ve kaza örnekleri hangi dersleri vermiştir?

## 2.3 Tünellerin Yapım Maliyetine Etki Eden Unsurlar {keep}
[corpus: 1/7]

1. Tünel yapım maliyetinin ana bileşenleri (kazı, destek, kaplama, yalıtım, elektromekanik, portal, şantiye) nelerdir?
2. Jeolojik ve geoteknik koşullar yapım maliyetini nasıl etkiler?
3. Tünel uzunluğu, kesit alanı ve tüp sayısı ile maliyet arasındaki ilişki nedir?
4. Yapım yöntemi seçimi (NATM, TBM, aç-kapa) maliyeti nasıl değiştirir?
5. Yeraltı suyu ve drenaj gereksinimleri maliyeti nasıl etkiler?
6. Aşırı kazı (overbreak) maliyete nasıl yansır?
7. Destek sınıfı dağılımının tahmin edilenden farklı çıkması maliyeti nasıl etkiler?
8. Elektromekanik sistemler toplam maliyet içinde ne kadar pay alır?
9. Şantiye lojistiği, erişim yolları, pasa nakli ve depolama maliyetleri nasıl belirlenir?
10. İş gücü, makine-ekipman ve malzeme fiyatlarındaki değişimler maliyeti nasıl etkiler?
11. Sözleşme türü ve risk paylaşımı (birim fiyat, götürü, anahtar teslim) maliyet performansını nasıl etkiler?
12. Süre uzaması ile maliyet artışı arasındaki ilişki nedir?
13. Çevresel ve sosyal gereksinimler (gürültü, titreşim, kamulaştırma) maliyete nasıl yansır?
14. Tünel projelerinde maliyet aşımının yaygın nedenleri ve büyüklükleri nelerdir?
15. KGM birim fiyatları ve tünel iş kalemleri maliyet tahmininde nasıl kullanılır?
16. Türkiye'de tünel yapım maliyetlerinin km başına tipik aralığı nedir?

## 2.4 Tünellerin Projelendirilmesi {keep}
[corpus: 12/11]

1. Tünel projelendirme süreci hangi aşamalardan oluşur (etüt, ön proje, kesin proje, uygulama projesi)?
2. Projelendirmede hangi disiplinler yer alır ve nasıl koordine edilir?
3. Tünel tasarımında hangi yükler ve etkiler (kaya/zemin yükü, su basıncı, deprem, trafik) dikkate alınır?
4. Tünel kesit tasarımı (gabari, kaplama kalınlığı, kaçış yolu, banket) hangi esaslara göre yapılır?
5. Analitik, ampirik ve sayısal (sonlu elemanlar/sonlu farklar) tasarım yöntemleri nasıl kullanılır?
6. Gözlemsel yöntem tünel tasarımında nasıl uygulanır?
7. Havalandırma, aydınlatma, yangın güvenliği ve elektromekanik tasarımı hangi standartlara göre yapılır?
8. Tünel projelerinde risk kaydı ve risk yönetimi tasarıma nasıl entegre edilir?
9. Projelendirmede kullanılan yazılımlar ve BIM uygulamaları nelerdir?
10. Proje teslim dokümanları (raporlar, çizimler, metraj, teknik şartname) nelerdir?
11. Tasarımda bakım ve işletme kolaylığının gözetilmesi nasıl sağlanır?
12. Projelendirme maliyetinin toplam proje maliyeti içindeki payı nedir?
13. Türkiye'de tünel projelendirmesinde uygulanan yönetmelik ve şartnameler nelerdir?
14. Uluslararası standartlar (Eurocode 7, ITA, PIARC) Türkiye uygulamasına nasıl yansır?

## 2.4.1 Jeolojik ve Geoteknik İncelemeler {keep}
[corpus: 14/22]

1. Tünel projelerinde jeolojik-geoteknik incelemenin amacı ve kapsamı nedir?
2. İnceleme programı proje aşamalarına (fizibilite, ön proje, kesin proje, yapım) göre nasıl kademelendirilir?
3. Jeolojik haritalama, uzaktan algılama ve jeofizik yöntemler nasıl kullanılır?
4. Sondaj programı (sayı, derinlik, aralık) nasıl planlanır?
5. Arazi deneyleri (presiyometre, dilatometre, hidrolik iletkenlik/packer testi) neyi ölçer?
6. Laboratuvar deneyleri (tek eksenli basınç, üç eksenli, kesme, şişme, aşındırıcılık) hangi parametreleri sağlar?
7. Kaya kütlesi sınıflamaları (RMR, Q, GSI) nasıl uygulanır ve tasarımda nasıl kullanılır?
8. Yeraltı suyu koşulları ve hidrojeolojik model nasıl kurulur?
9. Jeolojik-geoteknik veri raporu ve temel (baseline) raporu nasıl hazırlanır ve sözleşmede nasıl kullanılır?
10. İnceleme yetersizliğinin yapım riskleri ve maliyete etkisi nedir?
11. Jeolojik belirsizlik risk paylaşımında nasıl yönetilir?
12. Türkiye'de tünel jeoteknik incelemeleri için KGM esasları ve rapor formatları nelerdir?
13. İnceleme bütçesinin proje maliyeti içindeki payı ne olmalıdır?

## 2.4.1.1 İnşaat Başlamadan Önce Yapılan Çalışmalar {keep}
[corpus: 5/10]

1. Yapım öncesi jeolojik-geoteknik çalışmalar hangi adımlardan oluşur?
2. Masa başı çalışması (mevcut haritalar, önceki projeler, literatür) nasıl yapılır?
3. Saha jeolojik haritalaması ve süreksizlik ölçümleri nasıl yürütülür?
4. Sondaj lokasyonları ve derinlikleri tünel güzergâhına göre nasıl belirlenir?
5. Jeofizik yöntemler (sismik kırılma, elektrik özdirenç, yer radarı) yapım öncesinde nasıl kullanılır?
6. Portal bölgelerinde şev stabilitesi incelemeleri nasıl yapılır?
7. Yeraltı suyu ölçümleri (piezometre, pompa testi) nasıl planlanır?
8. Zemin/kaya parametrelerinin tasarım değerlerine dönüştürülmesi nasıl yapılır?
9. Beklenen kaya sınıfı dağılımı ve destek tahmini nasıl hazırlanır?
10. Jeolojik-geoteknik rapor ve jeolojik boy kesit nasıl sunulur?
11. Yapım öncesi çalışmaların maliyeti ve süresi nasıl planlanır?

## 2.4.1.2 İnşaat Esnasındaki Çalışmalar {keep}
[corpus: 28/35]

1. Yapım sırasında jeolojik-geoteknik izleme neden gereklidir?
2. Ayna haritalaması nasıl yapılır ve kayıt altına alınır?
3. İleri sondaj (probe drilling) ve ön enjeksiyon ne zaman uygulanır?
4. Konverjans, oturma ve ekstansometre ölçümleri nasıl kurulur ve değerlendirilir?
5. Uyarı ve alarm eşik değerleri nasıl belirlenir?
6. Destek sınıfının sahada güncellenmesi (NATM karar süreci) nasıl işler?
7. Yeraltı suyu girişlerinin ölçümü ve yönetimi nasıl yapılır?
8. Patlatma titreşimi ve gürültü izleme nasıl yürütülür?
9. Yüzey yapılarının ve altyapıların izlenmesi nasıl yapılır?
10. Yapım sırasındaki bulguların as-built jeolojik kayıt olarak belgelenmesi nasıl olur?
11. Yapım sırasındaki izleme sonuçları ödeme ve hakediş süreçlerini nasıl etkiler?
12. Yapım esnasındaki çalışmalar iş güvenliği açısından nasıl değerlendirilir?
13. KGM tünel projelerinde yapım sırası izleme uygulaması nasıldır?

## 2.4.1.3 Kullanım Aşaması Çalışmaları {keep}
[corpus: 17/29]

1. İşletme aşamasında yapısal izleme neden gereklidir ve hangi büyüklükler izlenir?
2. Uzun dönem deformasyon, kaplama çatlakları ve su sızıntısı nasıl izlenir?
3. Kaplama muayeneleri (görsel, çekiç testi, yer radarı, lazer tarama) nasıl yapılır?
4. İşletme aşamasında yeraltı suyu ve drenaj sisteminin izlenmesi nasıl olur?
5. Sensör tabanlı sürekli yapısal izleme sistemleri tünellerde nasıl uygulanır?
6. Deprem sonrası tünel muayenesi nasıl yapılır?
7. İşletme verilerinin bakım planlamasına dönüştürülmesi nasıl sağlanır?
8. Muayene periyotları ve raporlama esasları hangi standartlarda tanımlanır?
9. Kullanım aşamasındaki jeoteknik sorunların (şişme, oturma, portal şev hareketleri) yönetimi nasıldır?
10. Tünel yaşlanması ve servis ömrü değerlendirmesi nasıl yapılır?
11. Kullanım aşaması çalışmalarının maliyeti ve organizasyonu nasıldır?

## 2.4.2 Tünel Güzergahının Seçimi ve Boykesit Belirlenmesinde Dikkat Edilecek Hususlar {keep}
[corpus: 4/4]

1. Tünel güzergâhı seçimi hangi aşamada ve hangi kriterlerle yapılır?
2. Güzergâh alternatiflerinin karşılaştırılmasında kullanılan yöntemler (çok kriterli analiz, fayda-maliyet) nelerdir?
3. Güzergâh ve boy kesit kararları birbirini nasıl etkiler?
4. Tünel uzunluğu ile yaklaşım yolları arasındaki optimizasyon nasıl yapılır?
5. Portal yerleşimi güzergâh ve boy kesit seçimini nasıl belirler?
6. Jeolojik yapı (tabaka doğrultusu, fay, süreksizlikler) güzergâh yönelimini nasıl etkiler?
7. Çevresel ve sosyal kısıtlar (koruma alanları, yerleşimler, kamulaştırma) güzergâh seçiminde nasıl değerlendirilir?
8. Güzergâh ve boy kesit kararlarının yapım ve işletme maliyetine etkisi nedir?
9. Güzergâh seçiminde KGM'nin uyguladığı esaslar nelerdir?
10. Güzergâh seçim kararları nasıl belgelenir ve onaylanır?

## 2.4.2.1 Güzergah Seçiminde Dikkat Edilecek Hususlar {keep}
[corpus: 13/26]

1. Topoğrafya ve yükseklik farkları güzergâh seçimini nasıl etkiler?
2. Jeolojik-geoteknik riskler (fay, heyelan, karst, gaz, yüksek örtü) güzergâh seçiminde nasıl değerlendirilir?
3. Yeraltı suyu ve su kaynaklarının korunması güzergâhı nasıl kısıtlar?
4. Mevcut yapılar, altyapılar ve madencilik alanları güzergâh seçiminde nasıl dikkate alınır?
5. Portal bölgesi seçiminde şev stabilitesi, çığ, heyelan ve erişim koşulları nasıl değerlendirilir?
6. Trafik güvenliği ve sürüş konforu (yatay kurp, görüş mesafesi) güzergâhı nasıl etkiler?
7. Çevresel etki değerlendirmesi, koruma alanları ve arkeolojik alanlar nasıl gözetilir?
8. Kamulaştırma ve arazi kullanımı güzergâh maliyetine nasıl yansır?
9. Şantiye erişimi, pasa depolama ve lojistik güzergâh seçiminde neden önemlidir?
10. Güzergâh seçiminde yapım yöntemi uygunluğu nasıl değerlendirilir?
11. Güzergâh alternatiflerinin maliyet ve risk karşılaştırması nasıl raporlanır?

## 2.4.2.2 Boykesit Belirlemede Dikkat Edilecek Hususlar {keep}
[corpus: 2/6]

1. Tünel boy kesitinde izin verilen azami ve asgari eğimler nelerdir ve neye göre belirlenir?
2. Drenaj için gerekli asgari eğim nasıl sağlanır; tek yönlü ve tepe noktalı boy kesit ne zaman tercih edilir?
3. Boy kesit eğimi ağır taşıt hızını, egzoz emisyonunu ve havalandırma gereksinimini nasıl etkiler?
4. Boy kesit ile örtü kalınlığı ve jeolojik profil ilişkisi nasıl kurulur?
5. Portal kotları ve yaklaşım yolları boy kesit kararını nasıl sınırlar?
6. Su altı ve derin tünellerde boy kesit ve pompalama gereksinimi nasıl belirlenir?
7. Boy kesit kararının kazı hacmi ve yapım maliyetine etkisi nedir?
8. Düşey kurp ve görüş mesafesi tünel içinde nasıl sağlanır?
9. KGM esaslarında tünel boy kesiti için tanımlı sınırlar nelerdir?

## 2.4.3 Karayolları Genel Müdürlüğünde Tünel Projelendirilmesi Esasları {keep}
[corpus: 15/9]

1. KGM'nin tünel projelendirmesinde uyguladığı temel mevzuat ve şartnameler nelerdir?
2. KGM Karayolu Teknik Şartnamesi tünel işleri için hangi esasları tanımlar?
3. KGM tünel projelerinde kesit tipleri ve gabari standartları nasıl belirlenmiştir?
4. KGM'de tünel proje aşamaları, onay süreçleri ve sorumlu birimler nasıldır?
5. KGM tünel projelerinde jeolojik-geoteknik rapor içeriği ve kaya sınıfı esasları nelerdir?
6. KGM'nin tünel elektromekanik sistemleri (havalandırma, aydınlatma, güvenlik) için tasarım kriterleri nelerdir?
7. Tünel İşletme Yönetmeliği projelendirme aşamasına hangi gereklilikleri getirir?
8. KGM'de tünel projelerinde kalite kontrol planı ve muayene esasları nasıldır?
9. KGM'nin birim fiyat ve poz sistemi tünel projelendirmesine nasıl yansır?
10. KGM tünel projelerinde uluslararası standartlara (AB direktifi, N500, PIARC) atıf nasıl yapılır?
11. KGM'de tünel projelerinde yaşanan tipik tasarım revizyonları ve nedenleri nelerdir?
12. KGM esaslarının Avrupa uygulamalarıyla karşılaştırıldığında güçlü ve gelişmeye açık yönleri nelerdir?

## 3 KARAYOLLARI GENEL MÜDÜRLÜĞÜ TÜNELLERİN TARİHÇESİ {chapter}

## 3.1 Türkiye'de Karayolu Tünelciliğinin Gelişim Dönemleri {new}
[corpus: bölüm 3'e sınıflanmış 4/6 belge]

1. KGM'nin kuruluşu (1950) öncesinde Türkiye'de karayolu tünelciliği hangi düzeydeydi?
2. 1950–1980 döneminde KGM tarafından yapılan tüneller ve kullanılan yöntemler nelerdir?
3. 1980–2000 döneminde (otoyol programı, Bolu Dağı) tünelcilik nasıl gelişmiştir?
4. 2000 sonrasında bölünmüş yol ve büyük tünel programı tünel sayısını nasıl değiştirmiştir?
5. NATM ve TBM'nin Türkiye karayolu tünelciliğine girişi ne zaman ve hangi projelerle olmuştur?
6. Türk müteahhitlik sektörünün tünel yapım kapasitesi nasıl gelişmiştir?
7. Tünel projelendirme ve danışmanlık hizmetlerinin yerlileşmesi nasıl olmuştur?
8. Tünel elektromekanik ve güvenlik sistemlerinin Türkiye'deki gelişimi nasıldır?
9. Tünel işletme ve bakım örgütlenmesinin (şeflikler) tarihsel gelişimi nasıldır?
10. Türkiye tünelciliğinde dönüm noktası sayılan projeler ve olaylar hangileridir?
11. Türkiye'de tünelcilikle ilgili meslek örgütleri, seminerler ve yayınlar nasıl gelişmiştir?

## 3.2 KGM Tünel Envanteri: Sayı, Uzunluk ve Dağılım {new}
[corpus: envanter belgeleri 5.8 ve 3 altında sınıflanmış]

1. KGM tünel envanteri hangi bilgileri içerir ve nasıl tutulur?
2. Devlet ve il yollarındaki tünellerin sayısı ve toplam uzunluğu nedir?
3. Otoyollardaki tünellerin sayısı ve toplam uzunluğu nedir?
4. Tünellerin KGM bölge müdürlüklerine göre dağılımı nasıldır?
5. Tünellerin uzunluk sınıflarına göre dağılımı nasıldır?
6. Tünellerin yapım yılı ve yaş dağılımı nasıldır?
7. Tünellerin tüp sayısı, kesit tipi ve yapım yöntemine göre dağılımı nasıldır?
8. Tünellerdeki elektromekanik donanım düzeyi (havalandırma, aydınlatma, SCADA) nasıl sınıflanır?
9. Envanter verileri bakım-işletme planlaması ve bütçelemesinde nasıl kullanılır?
10. Tünel envanter verilerinin güncelliği ve erişilebilirliği hangi düzeydedir?
11. Yıllara göre tünel sayısı ve uzunluğundaki artış eğilimi nasıldır?

## 3.3 Dönüm Noktası Karayolu Tünel Projeleri {new}
[corpus: Zigana, Ovit, Avrasya belgeleri 1.4.2 ve 3 altında]

1. Bolu Dağı Tüneli'nin tarihsel süreci, jeolojik sorunları ve tamamlanması nasıl olmuştur?
2. Eski Zigana Tüneli ile Yeni Zigana Tüneli arasındaki fark dönemsel gelişimi nasıl gösterir?
3. Ovit Tüneli'nin proje tarihçesi ve yapım süreci nasıldır?
4. Ilgaz, Cankurtaran, Sabuncubeli ve Honaz gibi tünellerin proje tarihçeleri nelerdir?
5. Avrasya Tüneli'nin yap-işlet-devret modeliyle gerçekleştirilmesi Türkiye tünelciliği için ne ifade eder?
6. Kentsel karayolu tünelleri (Ankara, İstanbul, İzmir) hangi dönemde gelişmiştir?
7. Bu projelerde kullanılan yöntem, süre ve maliyet verileri nelerdir?
8. Bu projelerden çıkarılan kurumsal ve teknik dersler nelerdir?
9. Dönüm noktası projelerin bölgesel ekonomiye ve ulaşım ağına etkileri nasıl değerlendirilmiştir?
10. Devam eden ve planlanan büyük projeler bu tarihçeyi nasıl sürdürmektedir?

## 4 MALİYET KAVRAMI, ÖNEMİ VE ULAŞIM MALİYETLERİ {chapter}

## 4.1 Maliyet Kavramı, Ulaşım Maliyetleri ve İlgili Tanımlar {keep}
[corpus: 0/0]

1. Maliyet kavramı nasıl tanımlanır; maliyet, harcama, gider ve fiyat arasındaki farklar nelerdir?
2. Sabit, değişken, doğrudan, dolaylı ve fırsat maliyeti tünel projelerinde nasıl ayrıştırılır?
3. Ulaşım maliyetleri hangi bileşenlerden oluşur (altyapı, işletme, kullanıcı, dışsal maliyetler)?
4. Kullanıcı maliyetleri (araç işletme, zaman, kaza maliyeti) nasıl tanımlanır ve hesaplanır?
5. Dışsal maliyetler (çevre, gürültü, emisyon) ulaşım maliyet analizine nasıl dahil edilir?
6. Yatırım maliyeti, işletme-bakım maliyeti ve yaşam döngüsü maliyeti kavramları nasıl ilişkilendirilir?
7. Yaklaşık maliyet, keşif, metraj, birim fiyat ve hakediş kavramları kamu ihale sisteminde nasıl tanımlanır?
8. Maliyet tahmini doğruluk sınıfları (fizibilite, ön proje, kesin proje) nasıl tanımlanır?
9. Enflasyon, fiyat farkı ve eskalasyon maliyet hesaplarına nasıl yansıtılır?
10. Bugünkü değer, iskonto oranı ve ekonomik ömür kavramları maliyet karşılaştırmasında nasıl kullanılır?
11. Ulaşım yatırımlarında maliyet etkinliği ve fayda-maliyet oranı nasıl tanımlanır?
12. Tünel maliyetleri diğer karayolu yapılarıyla (köprü, viyadük, yarma) nasıl karşılaştırılır?
13. Türkiye'de kamu yatırım maliyet terminolojisi ve mevzuatı (Kamu İhale Kanunu, KGM birim fiyatları) nasıldır?

## 4.2 Karayolu Altyapı Yatırımlarında Maliyet Bileşenleri {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 4.3 Tünel Maliyet Analizi Yöntemleri {new}

1. Tünel maliyet analizi hangi amaçlarla (bütçeleme, alternatif karşılaştırma, ihale, kontrol) yapılır?
2. Maliyet analizi yöntemleri proje aşamalarına göre nasıl seçilir?
3. Aşağıdan yukarı ve yukarıdan aşağı tahmin yaklaşımları arasındaki fark nedir?
4. Tünel maliyet analizinde veri kaynakları (tamamlanmış projeler, birim fiyatlar, uluslararası veri tabanları) nelerdir?
5. Maliyet analizinde belirsizlik ve risk nasıl temsil edilir?
6. Maliyet analizi sonuçları nasıl raporlanır ve doğrulanır?
7. Türkiye'de tünel maliyet analizinde karşılaşılan veri ve yöntem sınırlılıkları nelerdir?

## 4.3.1 Birim Fiyat ve Keşif Esaslı Maliyet Tahmini {new}
[corpus: KGM birim fiyat ve analiz belgeleri 2.4.3 ve 7.2 altında]

1. Birim fiyat esaslı maliyet tahmini nasıl yapılır; metraj ve poz yapısı nasıl kurulur?
2. KGM birim fiyat listeleri ve tünel iş kalemleri (kazı, püskürtme beton, bulon, kaplama) nasıl kullanılır?
3. Birim fiyat analizi (rayiç, işçilik, makine, malzeme) nasıl hazırlanır?
4. Kaya sınıfına göre değişen kazı ve destek pozları maliyet tahminine nasıl yansıtılır?
5. Keşif artışı ve iş artışı kavramları tünel sözleşmelerinde nasıl işler?
6. Yaklaşık maliyet hazırlamada kamu ihale mevzuatının gereklilikleri nelerdir?
7. Birim fiyat tahmininin doğruluk düzeyi ve tipik sapma nedenleri nelerdir?
8. Fiyat farkı ve eskalasyon birim fiyat sözleşmelerine nasıl uygulanır?
9. Elektromekanik iş kalemlerinin birim fiyat esaslı tahmini nasıl yapılır?
10. Tamamlanmış KGM tünel projelerinde keşif ile gerçekleşen maliyet nasıl karşılaştırılır?

## 4.3.2 Parametrik ve İstatistiksel Maliyet Modelleri {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 4.3.3 Fayda-Maliyet ve Yatırım Değerlendirme {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 4.3.4 Risk ve Belirsizliğin Maliyete Yansıtılması {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 4.3.5 Tünel Yaşam Döngü Maliyetleri {keep}
[corpus: 7/1]

1. Yaşam döngüsü maliyeti nedir ve tüneller için neden önemlidir?
2. Tünel yaşam döngüsü aşamaları (planlama, yapım, işletme, bakım, yenileme, hizmet dışı bırakma) nasıl tanımlanır?
3. Yaşam döngüsü maliyeti hesabında hangi maliyet kalemleri yer alır?
4. İskonto oranı, analiz süresi ve kalıntı değer nasıl seçilir?
5. Yapım maliyeti ile işletme-bakım maliyeti arasındaki ödünleşim nasıl değerlendirilir?
6. Elektromekanik sistemlerin yenileme döngüleri yaşam döngüsü maliyetine nasıl yansır?
7. Kaplama ve yapısal elemanların servis ömrü ve yenileme maliyeti nasıl tahmin edilir?
8. Enerji tüketimi (aydınlatma, havalandırma) yaşam döngüsü maliyeti içinde nasıl modellenir?
9. Risk tabanlı yaşam döngüsü maliyet analizi nasıl yapılır?
10. Uluslararası yaşam döngüsü maliyeti standartları ve kılavuzları (ISO 15686, PIARC) nelerdir?
11. Yaşam döngüsü maliyeti sonuçları tasarım kararlarını nasıl etkilemelidir?
12. Türkiye'de tünellerde yaşam döngüsü maliyeti uygulamasının mevcut durumu ve engelleri nelerdir?
13. Literatürdeki tünel yaşam döngüsü maliyeti örnekleri hangi sonuçları vermiştir?

## 5 TÜNEL BAKIM-ONARIM VE İŞLETME MALİYETLERİ {chapter}

## 5.1 Çalışmanın Amacı ve Önemi {inactive: tez yapısı; kitap içeriği değil}

## 5.2 Çalışmanın Kapsamı {inactive: tez yapısı; kitap içeriği değil}

## 5.3 Çalışmanın Yöntemi ve Kullanılan Veriler {inactive: tez yapısı; kitap içeriği değil}

## 5.4 Tünel Bakım-Onarım ve İşletme {keep}
[corpus: 52/46]

1. Tünel işletmesi ve tünel bakımı kavramları nasıl tanımlanır ve birbirinden nasıl ayrılır?
2. Tünel işletmesinin temel işlevleri (trafik yönetimi, izleme, olay müdahalesi, güvenlik) nelerdir?
3. Bakım türleri (rutin, koruyucu, öngörücü, düzeltici, acil) tünellerde nasıl uygulanır?
4. Tünel bakım-işletme organizasyonu nasıl yapılandırılır; roller ve sorumluluklar nelerdir?
5. Tünel muayene ve denetim sistemi (periyotlar, seviyeler, raporlama) nasıl kurulur?
6. Bakım yönetim sistemleri ve varlık yönetimi tünellerde nasıl uygulanır?
7. Tünel kapatma ve trafik yönlendirme planlaması bakım çalışmalarında nasıl yapılır?
8. Tünel işletmesinde personel gereksinimi ve eğitimi nasıl belirlenir?
9. Tünel İşletme Yönetmeliği'nin işletme ve bakım için getirdiği yükümlülükler nelerdir?
10. Uluslararası kılavuzlar (PIARC, N500, AB direktifi) bakım-işletme için hangi esasları tanımlar?
11. Tünel işletmesinde performans göstergeleri (kullanılabilirlik, olay müdahale süresi) nelerdir?
12. Bakım-işletmede dış hizmet alımı ile kurum içi işletme nasıl karşılaştırılır?
13. Tünel işletme merkezi (kontrol odası, SCADA) nasıl çalışır?
14. Kış işletmesi ve olağanüstü hava koşulları tünel işletmesini nasıl etkiler?
15. Türkiye'de tünel bakım-işletme uygulamasının mevcut durumu ve sorunları nelerdir?

## 5.4.1 Yapısal Bakım {keep}
[corpus: 13/14]

1. Yapısal bakım kapsamına giren tünel elemanları (kaplama, taban, portal, drenaj, yalıtım, kaldırım) nelerdir?
2. Kaplama bozulma türleri (çatlak, dökülme, su sızıntısı, kalsit oluşumu, donma hasarı) nelerdir ve nasıl teşhis edilir?
3. Yapısal muayene yöntemleri (görsel, çekiç, yer radarı, lazer tarama, karot) nasıl uygulanır?
4. Drenaj sistemi bakımı (tıkanma, kireçlenme temizliği) nasıl yapılır?
5. Su sızıntısı onarım teknikleri (enjeksiyon, membran, drenaj tamiri) nelerdir?
6. Kaplama onarım ve güçlendirme yöntemleri (püskürtme beton, kompozit sargı, ankraj) nelerdir?
7. Portal ve şev bakımı (kaya düşmesi, çığ, heyelan önlemleri) nasıl yapılır?
8. Yapısal bakım periyotları ve önceliklendirme nasıl belirlenir?
9. Yapısal bakım kayıtları ve durum derecelendirmesi nasıl tutulur?
10. Eski tünellerin yapısal rehabilitasyonu nasıl planlanır?
11. Yapısal bakımda iş güvenliği ve trafik güvenliği önlemleri nelerdir?

## 5.4.2 Elektrik-Elektronik ve Elektromekanik Sistemlerin Bakımı {keep}
[corpus: 23/45]

1. Tünel elektromekanik sistemleri hangi alt sistemlerden oluşur (enerji, aydınlatma, havalandırma, yangın, haberleşme, trafik, SCADA)?
2. Aydınlatma sistemi bakımı (armatür temizliği, lamba değişimi, LED dönüşümü, ışık ölçümü) nasıl yapılır?
3. Havalandırma sistemi (jet fan, aksiyal fan, damper) bakımı nasıl yapılır?
4. Yangın algılama ve söndürme sistemlerinin (lineer ısı sensörü, hidrant, söndürücü) bakımı nasıldır?
5. Enerji besleme, kesintisiz güç kaynağı ve jeneratör sistemlerinin bakımı nasıl yapılır?
6. Haberleşme, acil telefon, radyo yayını ve anons sistemlerinin bakımı nasıldır?
7. Trafik kontrol ekipmanlarının (değişken mesaj işareti, sinyal, kamera, olay algılama) bakımı nasıl yapılır?
8. SCADA ve kontrol yazılımlarının bakımı, güncellenmesi ve siber güvenliği nasıl sağlanır?
9. Elektromekanik bakım periyotları ve kontrol listeleri nasıl oluşturulur?
10. Elektromekanik sistemlerin servis ömrü ve yenileme planlaması nasıldır?
11. Elektromekanik bakımda yedek parça ve stok yönetimi nasıl yapılır?
12. Elektromekanik bakımın kapatma gereksinimi ve trafik etkisi nasıl azaltılır?
13. Türkiye'deki tünellerde elektromekanik sistemlerin standardizasyonu ve bakım uygulaması nasıldır?

## 5.4.3 Periyodik Bakım {keep}
[corpus: 2/14]

1. Periyodik bakım nedir ve rutin/koruyucu bakımdan farkı nedir?
2. Tünel periyodik bakım programı (günlük, haftalık, aylık, yıllık) nasıl oluşturulur?
3. Tünel yıkama ve temizlik (duvar, armatür, işaret) hangi sıklıkta ve nasıl yapılır?
4. Periyodik muayene sınıfları ve kapsamları (basit, ana, özel muayene) nelerdir?
5. Periyodik bakımda kontrol listeleri ve kayıt formları nasıl kullanılır?
6. Periyodik bakımın kapatma planlaması ve trafik yönetimi nasıl yapılır?
7. Periyodik bakım için gerekli ekipman ve araçlar nelerdir?
8. Periyodik bakımın maliyet planlaması ve bütçelemesi nasıl yapılır?
9. Uluslararası kılavuzlarda periyodik bakım sıklıkları nasıl tanımlanır?
10. KGM'de periyodik bakım uygulaması ve şefliklerin görev tanımları nasıldır?
11. Periyodik bakım verileri durum değerlendirmesi ve öngörücü bakıma nasıl dönüştürülür?

## 5.5 Tünel Bakım-Onarım ve İşletme Maliyetleri {keep}
[corpus: 0/4]

1. Tünel bakım-işletme maliyetleri hangi ana kalemlerden oluşur?
2. Bakım-işletme maliyetleri nasıl sınıflandırılır (sabit/değişken; yönetim/işletme/bakım/enerji)?
3. Tünel bakım-işletme maliyetlerinin yapım maliyetine oranı tipik olarak nedir?
4. Bakım-işletme maliyetleri tünel uzunluğu, tüp sayısı ve trafik hacmine göre nasıl değişir?
5. Bakım-işletme maliyetleri yıllık ve yaşam döngüsü bazında nasıl hesaplanır?
6. Maliyet verilerinin toplanması ve muhasebeleştirilmesi için hangi sistemler kullanılır?
7. Uluslararası literatürde tünel bakım-işletme maliyet göstergeleri (km başına yıllık) hangi aralıktadır?
8. Bakım-işletme maliyetlerinin bütçelenmesi ve ödenek planlaması nasıl yapılır?
9. Ertelenmiş bakımın uzun dönem maliyet etkisi nedir?
10. Türkiye'de tünel bakım-işletme maliyet verilerinin mevcut durumu ve erişilebilirliği nasıldır?
11. KGM'nin tünel bakım-işletme harcamaları nasıl raporlanmaktadır?
12. Bakım-işletme maliyetleri ile hizmet düzeyi ve güvenlik arasındaki ilişki nasıl kurulur?

## 5.5.1 Yönetim ve İşletme Maliyetleri {keep}
[corpus: 2/4]

1. Yönetim ve işletme maliyetleri hangi kalemleri kapsar (personel, kontrol merkezi, enerji, haberleşme, sigorta)?
2. Personel maliyetleri (operatör, teknisyen, güvenlik, yönetim) nasıl hesaplanır?
3. Enerji maliyetleri işletme maliyetleri içinde nasıl pay alır?
4. Kontrol merkezi ve SCADA işletme maliyetleri nasıl belirlenir?
5. Trafik yönetimi, olay müdahalesi ve acil durum hazırlığı maliyetleri nelerdir?
6. Dış hizmet alımı sözleşmelerinin işletme maliyetlerine etkisi nedir?
7. İşletme maliyetleri tünel uzunluğu ve donanım düzeyine göre nasıl değişir?
8. İşletme maliyetleri için uluslararası kıyas değerleri nelerdir?
9. Türkiye'de tünel işletme maliyetlerinin bütçelenmesi ve raporlanması nasıldır?
10. İşletme maliyetlerini etkileyen organizasyonel kararlar nelerdir?

## 5.5.2 Bakım-Onarım Maliyetleri {keep}
[corpus: 0/3]

1. Bakım-onarım maliyetleri hangi alt kalemlerden oluşur?
2. Yapısal ve elektromekanik bakım maliyetleri arasındaki pay dağılımı nasıldır?
3. Bakım-onarım maliyetleri tünel yaşına göre nasıl değişir?
4. Bakım-onarım maliyetlerinin tahmini için hangi yöntemler kullanılır?
5. Planlı ve plansız bakım maliyetleri nasıl ayrıştırılır?
6. Bakım-onarım maliyet verileri nasıl kaydedilir ve analiz edilir?
7. Bakım-onarım maliyetleri için uluslararası kıyaslama değerleri nelerdir?
8. Türkiye'de tünel bakım-onarım maliyet verilerinin durumu nasıldır?

## 5.5.2.1 Yapısal Bakım-Onarım Maliyetleri {keep}
[corpus: 2/6]

1. Yapısal bakım-onarım maliyet kalemleri (kaplama onarımı, su sızıntısı, drenaj, portal, kaldırım) nelerdir?
2. Yapısal onarım birim maliyetleri (m² püskürtme beton, m enjeksiyon vb.) hangi aralıktadır?
3. Kaplama rehabilitasyonu ve güçlendirme maliyetleri nasıl tahmin edilir?
4. Drenaj temizliği ve su sızıntısı onarım maliyetleri nasıl belirlenir?
5. Yapısal bakım maliyetlerinin tünel yaşı ve jeolojik koşullarla ilişkisi nedir?
6. Yapısal bakım için kapatma ve trafik yönetimi maliyetleri nasıl hesaplanır?
7. Yapısal bakım maliyetlerinin yaşam döngüsü içindeki dağılımı nasıldır?
8. Türkiye'de yapısal bakım-onarım için KGM birim fiyatları ve harcama verileri nelerdir?
9. Ertelenen yapısal bakımın maliyet artışına etkisi nasıl ölçülür?

## 5.5.2.2 Elektrik-Elektronik ve Elektromekanik Sistemlerin Bakım Maliyetleri {keep}
[corpus: 0/3]

1. Elektromekanik bakım maliyet kalemleri (periyodik bakım, arıza onarımı, yedek parça, yazılım, yenileme) nelerdir?
2. Aydınlatma, havalandırma, yangın ve SCADA sistemleri için tipik yıllık bakım maliyetleri hangi düzeydedir?
3. Elektromekanik sistemlerin yenileme maliyetleri ve döngüleri nasıl planlanır?
4. Elektromekanik bakım maliyetleri tünel uzunluğu ve donanım düzeyine göre nasıl değişir?
5. LED dönüşümü ve enerji verimli fanlar bakım maliyetlerini nasıl etkiler?
6. Bakım sözleşmeleri (garanti, servis anlaşmaları) elektromekanik bakım maliyetlerini nasıl şekillendirir?
7. Elektromekanik bakım maliyetleri için uluslararası kıyaslama değerleri nelerdir?
8. Türkiye'de elektromekanik bakım maliyetlerinin bütçelenmesi ve gerçekleşme verileri nasıldır?
9. Elektromekanik bakım maliyetlerinin toplam bakım-işletme maliyeti içindeki payı nedir?

## 5.6 Tünel Bakım-Onarım ve İşletme Maliyetlerini Etkileyen Faktörler {keep}
[corpus: 20/20]

1. Tünel uzunluğu ve tüp sayısı bakım-işletme maliyetini nasıl etkiler?
2. Trafik hacmi, ağır taşıt oranı ve trafik kompozisyonu maliyeti nasıl etkiler?
3. Elektromekanik donanım düzeyi ve teknolojisi maliyeti nasıl etkiler?
4. Tünel yaşı ve yapım kalitesi bakım maliyetini nasıl etkiler?
5. Jeolojik ve hidrojeolojik koşullar (su girişi, şişme, donma) bakım maliyetini nasıl etkiler?
6. İklim ve coğrafi konum (kar, buzlanma, yükseklik) işletme maliyetini nasıl etkiler?
7. Tasarım kararları (drenajlı/drenajsız, kaplama tipi, erişim kolaylığı) bakım maliyetini nasıl etkiler?
8. İşletme organizasyonu ve bakım stratejisi (koruyucu/düzeltici) maliyeti nasıl etkiler?
9. Enerji fiyatları ve tarife yapısı işletme maliyetini nasıl etkiler?
10. Mevzuat ve güvenlik gereklilikleri (AB direktifi, yönetmelik) maliyeti nasıl etkiler?
11. Kaza ve olaylar bakım-işletme maliyetini nasıl etkiler?
12. Dış hizmet alımı ve sözleşme yapısı maliyeti nasıl etkiler?
13. Bu faktörlerin göreli önemi literatürde nasıl ölçülmüştür?

## 5.7 Tünelde Verimli Bakım-İşletme ve Enerji Tüketimi {keep}
[corpus: 21/27]

1. Tünellerde enerji tüketimi hangi sistemlerden (aydınlatma, havalandırma, pompalar, kontrol) kaynaklanır ve dağılımı nasıldır?
2. Tünel aydınlatma enerji tüketimi tünel uzunluğu, tasarım sınıfı ve gündüz/gece rejimine göre nasıl değişir?
3. Havalandırma enerji tüketimi trafik, uzunluk ve kontrol stratejisine göre nasıl değişir?
4. Enerji verimliliği için hangi teknolojiler (LED, adaptif aydınlatma, frekans kontrollü fanlar, sensör tabanlı havalandırma) uygulanır?
5. Verimli bakım-işletme kavramı nedir ve hangi göstergelerle ölçülür?
6. Öngörücü bakım ve durum izleme verimliliği nasıl artırır?
7. Bakım-işletmede dijitalleşme (varlık yönetim sistemi, BIM, nesnelerin interneti) hangi kazanımları sağlar?
8. Enerji yönetim sistemi (ISO 50001) tünellerde nasıl uygulanır?
9. Yenilenebilir enerji ve enerji geri kazanımı tünellerde nasıl kullanılabilir?
10. Enerji tüketimi ve maliyeti için uluslararası kıyas değerleri (km başına yıllık kWh) nelerdir?
11. Türkiye'deki tünellerde enerji tüketimi ve tasarruf potansiyeli hakkında hangi veriler vardır?
12. Verimlilik iyileştirmelerinin geri ödeme süresi nasıl hesaplanır?

## 5.7.1 Bakım-İşletme Maliyetini Azaltma Yöntemleri {keep}
[corpus: 2/12]

1. Bakım stratejisinin düzeltici bakımdan koruyucu ve öngörücü bakıma kaydırılması maliyeti nasıl azaltır?
2. Varlık yönetimi ve önceliklendirme yaklaşımı maliyet azaltmada nasıl kullanılır?
3. Tasarım aşamasında bakım kolaylığının sağlanması maliyeti nasıl azaltır?
4. Standardizasyon ve ortak yedek parça yönetimi maliyeti nasıl azaltır?
5. Bakım çalışmalarının gruplanması ve kapatma sürelerinin optimizasyonu nasıl yapılır?
6. Uzaktan izleme ve otomasyon personel maliyetlerini nasıl azaltır?
7. Dış hizmet alımı ve performansa dayalı sözleşmeler maliyeti nasıl etkiler?
8. Bölgesel tünel işletme merkezleri (çoklu tünel yönetimi) maliyeti nasıl azaltır?
9. Personel eğitimi ve bakım kalitesi maliyet üzerinde nasıl etkilidir?
10. Uluslararası örneklerde uygulanan maliyet azaltma programları ve sonuçları nelerdir?
11. Türkiye koşullarında uygulanabilir maliyet azaltma önerileri nelerdir?

## 5.7.2 Enerji Maliyetini Azaltma Yöntemleri {keep}
[corpus: 1/8]

1. LED aydınlatmaya geçişin enerji ve bakım maliyetine etkisi nedir?
2. Adaptif aydınlatma kontrolü (dış parlaklık ve trafik sensörlü) nasıl tasarruf sağlar?
3. Portal bölgesi aydınlatma gereksinimini azaltan tasarım önlemleri (gölgeleme, yüzey kaplaması) nelerdir?
4. Havalandırmada talep kontrollü işletme (CO, NO2 ve görüş sensörleri) enerji tasarrufunu nasıl sağlar?
5. Frekans konvertörlü fanlar ve verimli motorlar enerji maliyetini nasıl düşürür?
6. Pompalama ve drenaj sistemlerinde enerji verimliliği nasıl sağlanır?
7. Enerji tarifesi optimizasyonu ve talep yönetimi tünellerde nasıl uygulanır?
8. Tünel yüzey temizliği ve yansıtıcılığın aydınlatma enerjisine etkisi nedir?
9. Yenilenebilir enerji üretimi tünel enerji maliyetini nasıl azaltabilir?
10. Enerji tasarruf önlemlerinin yatırım maliyeti ve geri ödeme süreleri nelerdir?
11. Uluslararası ve ulusal örneklerde elde edilen enerji tasarruf oranları nelerdir?

## 5.8 Devlet ve İl Yollarında Bulunan Tünel Bakım İşletme Şeflikleri {keep}
[corpus: 2/6]

1. Tünel bakım işletme şeflikleri KGM teşkilat yapısı içinde nasıl konumlanır?
2. Şefliklerin görev, yetki ve sorumlulukları nelerdir?
3. Şefliklerin sayısı, bölgelere dağılımı ve sorumlu oldukları tüneller nelerdir?
4. Şefliklerin personel yapısı, kadro ve uzmanlık gereksinimleri nasıldır?
5. Şefliklerin araç, ekipman ve teknik altyapı donanımı nasıldır?
6. Şefliklerin bütçe ve ödenek yapısı nasıl işler?
7. Şefliklerin bakım programı, kayıt ve raporlama uygulamaları nasıldır?
8. Şeflikler ile bölge müdürlükleri ve merkez birimleri arasındaki koordinasyon nasıl sağlanır?
9. Şefliklerin acil durum ve olay müdahalesindeki rolü nedir?
10. Şefliklerin karşılaştığı temel sorunlar (personel, bütçe, ekipman, eğitim) nelerdir?
11. Şeflik yapısının uluslararası tünel işletme organizasyonlarıyla karşılaştırması nasıldır?
12. Şefliklerin kurumsal gelişimi için öneriler nelerdir?

## 5.9 Ulusal ve Uluslararası Literatür Taraması {inactive: tez yapısı; kaynaklar kitap sonunda listelenir}

## 5.9.1 Ulusal Literatür Taraması {inactive: tez yapısı}

## 5.9.2 Uluslararası Literatür Taraması {inactive: tez yapısı}

## 6 TÜNEL YAPIM MALİYETLERİ {chapter}

## 6.1 Çalışmanın Amacı, Kapsamı, Yöntem ve Kullanılan Verileri {inactive: tez yapısı; 5.1–5.3 ile tekrar}

## 6.1.1 Çalışmanın Amacı ve Önemi {inactive: tez yapısı; 5.1 ile tekrar}

## 6.1.2 Çalışmanın Kapsamı {inactive: tez yapısı; 5.2 ile tekrar}

## 6.1.3 Çalışmanın Yöntemi {inactive: tez yapısı; 5.3 ile tekrar}

## 6.2 Ulusal ve Uluslararası Literatür Taraması (Mehmet Çelikkaya) {inactive: tez yapısı; başlıkta tez yazarı adı}

## 6.2.1 Ulusal Literatür Taraması {inactive: tez yapısı}

## 6.2.2 Uluslararası Literatür Taraması {inactive: tez yapısı}

## 6.3 Tünel Yapım Maliyet Kalemleri ve Birim Fiyat Analizleri {new}
[corpus: KGM birim fiyat, poz ve analiz belgeleri mevcut]

1. Tünel yapım maliyeti hangi iş gruplarına (şantiye, kazı, destek, kaplama, yalıtım-drenaj, portal, elektromekanik, yol üstyapısı) ayrılır?
2. Kazı maliyeti kaya sınıfı ve yönteme göre nasıl değişir?
3. Püskürtme beton, bulon, çelik iksa ve süren maliyetleri nasıl hesaplanır?
4. Kaplama betonu ve kalıp maliyetleri nasıl belirlenir?
5. Su yalıtımı ve drenaj sistemi maliyetleri nasıl hesaplanır?
6. Elektromekanik sistemlerin yapım maliyeti içindeki payı ve kalemleri nelerdir?
7. Portal ve yaklaşım yapılarının maliyeti nasıl belirlenir?
8. Şantiye kurulumu, enerji, havalandırma ve su boşaltma gibi genel giderler nasıl hesaplanır?
9. KGM birim fiyat analizlerinde tünel iş kalemleri (pozlar) nasıl yapılandırılmıştır?
10. Makine-ekipman (jumbo, roadheader, TBM) amortisman ve işletme maliyetleri birim fiyatlara nasıl girer?
11. Tamamlanmış tünel projelerinde iş gruplarının maliyet payı dağılımı nasıldır?
12. Maliyet kalemlerinin metraj ve hakediş süreçleriyle ilişkisi nasıldır?
13. Türkiye ve uluslararası birim maliyetler nasıl karşılaştırılır?

## 6.4 Yapım Yöntemine Göre Maliyet Karşılaştırması {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 6.5 Türkiye ve Dünya Tünel Yapım Maliyeti Örnekleri {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 6.6 Yapım Maliyeti Sapmaları: Bütçe Aşımı ve Nedenleri {inactive: corpus desteği yok; 2.2.3 türü destek riski}

## 7 ARAŞTIRMANIN BULGULARI, SONUÇLAR VE ÖNERİLER {chapter}

## 7.1 Tünel Bakım-İşletme Maliyetleri {keep, human-analysis}
[corpus: 1/1 — bu bölüm literatürden değil, proje analiz verisinden yazılır]

1. Çalışma kapsamında hangi tüneller ve hangi yıllar için bakım-işletme maliyet verisi toplanmıştır?
2. Toplanan verilerin kaynağı (KGM kayıtları, şeflik raporları, bütçe) ve güvenilirliği nasıldır?
3. Tünel başına ve km başına yıllık bakım-işletme maliyetleri hangi düzeyde bulunmuştur?
4. Maliyetlerin kalemlere (yönetim, enerji, yapısal bakım, elektromekanik bakım) dağılımı nasıldır?
5. Maliyetlerin tünel uzunluğu, trafik ve yaşa göre değişimi nasıl analiz edilmiştir?
6. Bulgular uluslararası göstergelerle nasıl karşılaştırılmıştır?
7. Analiz sonuçları hangi maliyet artırıcı faktörleri öne çıkarmıştır?
8. Bulgular temelinde bakım-işletme maliyetini azaltmaya yönelik öneriler nelerdir?
9. Veri sınırlılıkları ve gelecek çalışmalar için öneriler nelerdir?

## 7.2 Tünel Yapım Maliyetleri {keep, human-analysis}
[corpus: 1/2 — bu bölüm literatürden değil, proje analiz verisinden yazılır]

1. Çalışma kapsamında hangi tünel projelerinin yapım maliyet verileri incelenmiştir?
2. Verilerin kaynağı (ihale, sözleşme, hakediş, kesin hesap) ve güvenilirliği nasıldır?
3. Km başına ve m³ başına yapım maliyetleri hangi düzeyde bulunmuştur?
4. Maliyetlerin iş gruplarına dağılımı nasıl bulunmuştur?
5. Yöntem, kaya sınıfı ve uzunluğun maliyete etkisi verilerle nasıl doğrulanmıştır?
6. Keşif ile gerçekleşen maliyet arasındaki sapmalar hangi düzeydedir ve nedenleri nelerdir?
7. Bulgular uluslararası maliyet göstergeleriyle nasıl karşılaştırılmıştır?
8. Bulgular temelinde yapım maliyetini azaltmaya ve tahmin doğruluğunu artırmaya yönelik öneriler nelerdir?
9. Çalışmanın sonuçları ve gelecek araştırmalar için öneriler nelerdir?

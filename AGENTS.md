# TunnelBookAI Çalışma Kuralları

## Zorunlu çalışma günlüğü

Projede yapılan her anlamlı inceleme, veri işlemi, kod değişikliği, manuel karar,
corpus değişikliği ve doğrulama çalışması tamamlandığında
`reports/project_work_log.md` güncellenmelidir.

Her yeni kayıt en az şunları içermelidir:

- tarih ve işlem başlığı;
- ne yapıldığı ve neden yapıldığı;
- değişen belge/chunk sayıları veya dosyalar;
- kullanılan audit, rapor, manifest ya da test sonucu;
- doğrulama sonucu ve bilinen sınırlamalar;
- varsa sıradaki önerilen işlem.

Geçmiş kayıtlar silinmez veya sonucu daha iyi göstermek için yeniden yazılmaz. Bir bilgi
değiştiğinde eski gözlem tarihsel olarak korunur ve yeni kayıt onu açıkça geçersiz kılar.
Üretilen JSON auditleri `audit/` altında, insan tarafından okunabilir özetleri `reports/`
altında tutulur. Gerçek embedding/vektör araması yapılmadıysa sonuç “semantik arama” olarak
adlandırılmaz.

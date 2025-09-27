Beton-Yeşil Projesi, iki ana bileşenden oluşmaktadır: backend (arka uç) ve frontend (ön yüz).
Projenin düzgün şekilde çalışabilmesi için aşağıdaki adımlar takip edilmelidir:

1. Backend Servisini Başlat
İlk olarak terminal/komut istemcisinde proje ana klasöründe olduğunuzdan emin olun,
 ardından aşağıdaki komutu çalıştırarak backend servisini başlatın: python -m backend.app

2. Frontend Servisini Başlat
Backend çalıştıktan sonra, yeni bir terminal penceresi açarak frontend'i başlatmak için şu komutu girin: python -m http.server 8000

3. Uygulamayı Görüntüle
Tüm servisler başlatıldıktan sonra aşağıdaki bağlantıyı tarayıcınızda açarak projeyi görüntüleyebilirsiniz: http://localhost:8000
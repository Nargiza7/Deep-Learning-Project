🌿 Beton-Yeşil: AI ile Şehir Cephelerini Yeşillendirme  
Bu proje, şehirlerdeki beton bina cephelerini derin öğrenme teknikleri ile analiz ederek, yeşillendirmeye uygun alanları tespit eder ve bu alanlara otomatik bitkilendirme simülasyonları uygular.

🚀 Proje Amacı  
- Bina cephelerindeki pencere, kapı ve balkonların otomatik segmentasyonu  
- Yeşillendirmeye uygun yüzeylerin ayrıştırılması
- Bitki dokusu (ör. sarmaşık) bindirilerek görsel dönüşüm oluşturulması
- Harita tabanlı etkileşim ile kullanıcıya öneriler sunulması
- Yeşillendirme sonrası çevresel katkıların (ısı azalması, CO₂ emilimi) tahmini

🛠 Kullanılan Teknolojiler  
- Backend: Python (Flask) – API yönetimi ve model entegrasyonu
- Frontend: HTML, CSS, JavaScript (Leaflet.js) – Harita tabanlı görsel sunum
- Model: U-Net tabanlı segmentasyon modeli (TensorFlow & Keras)
- Kütüphaneler: NumPy, Matplotlib, Pillow, glob, os

🔄 Çalışma Mantığı  
1. Kullanıcı harita üzerinden bir alan seçer
2. Flask API ilgili görüntüyü işler
3. Segmentasyon modeli bina yüzeylerini ayırır
4. Uygun yüzeylere ivy_texture.png bitki dokusu uygulanır
5. Sonuç görseli frontend’de kullanıcıya sunulur

🌍 Harita ve Bitki Öneri Sistemi  
- Proje, farklı şehirlerdeki (İstanbul, Ankara, İzmir, Antalya, Bursa, Sakarya, Düzce) bina cephelerini analiz eder ve iklim koşullarına uygun bitki türleri önerir:
- Düzce: Orman Sarmaşığı, Camgüzeli
- Ankara: Karaçam, Mazı

📊 Eğitim Süreci  
- Eğitim Google Colab üzerinde GPU ile yapıldı
- 200+ görsel veri seti kullanıldı
- Dropout & L2 Regularization ile aşırı öğrenme engellendi
- EarlyStopping ile verimli eğitim sağlandı
- Model çıktı dosyası: unet_segmentation_model.h5

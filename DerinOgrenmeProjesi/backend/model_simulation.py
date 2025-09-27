# backend/model_simulation.py
import tensorflow as tf # Veya PyTorch kullanıyorsanız import torch
from PIL import Image
import numpy as np
import os # Dosya yolları için
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'unet_segmentation_model.h5')

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Model başarıyla yüklendi: {MODEL_PATH}")
    
    print("\n--- Model Özeti ---")
    model.summary() # Modelin katmanlarını ve giriş/çıkış boyutlarını gösterir

    # Veya sadece giriş boyutunu almak için:
    if hasattr(model, 'input_shape'):
        # input_shape genellikle (None, Yükseklik, Genişlik, Kanal) formatındadır
        # None, batch boyutunu temsil eder ve değişken olabilir.
        print(f"Model giriş boyutu: {model.input_shape}")
    elif hasattr(model.input, 'shape'): # Alternatif (özellikle Functional API ile oluşturulan modeller için)
        print(f"Model giriş boyutu (alternatif): {model.input.shape}")
    print("-------------------\n")
    
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    model = None # Model yüklenemezse None olarak ayarla

GENERATED_DESIGNS_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'static', 'generated_designs')
if not os.path.exists(GENERATED_DESIGNS_DIR):
    os.makedirs(GENERATED_DESIGNS_DIR) 
    

def preprocess_image(image_path, target_size=(256, 256)):
    """Görüntüyü modele uygun formata getirir."""
    img = Image.open(image_path).convert('RGB') # RGB formatına çevir
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0 # Normalizasyon (0-1 aralığına)
    img_array = np.expand_dims(img_array, axis=0) # Batch boyutu için boyut ekle (1, H, W, C)
    return img_array

IVY_TEXTURE_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'static', 'ivy_texture.png')

def postprocess_image(output_array, original_image_path):
    """Model çıktısını kaydetmek ve orijinal görselle birleştirmek için uygun formata getirir."""
    
    processed_array = output_array.squeeze(axis=0)
    print(f"DEBUG: postprocess_image squeeze sonrası şekil: {processed_array.shape}")
    print(f"DEBUG: postprocess_image squeeze sonrası veri tipi: {processed_array.dtype}")

    processed_array = (processed_array * 255).astype(np.uint8)

    original_img_pil = Image.open(original_image_path).convert('RGB')
    original_img_pil = original_img_pil.resize((processed_array.shape[1], processed_array.shape[0])) 
    original_img_array = np.array(original_img_pil) 

    debug_dir = os.path.join(GENERATED_DESIGNS_DIR, 'debug_channels')
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)
    for i in range(processed_array.shape[-1]):
        channel_img_array = processed_array[:, :, i]
        Image.fromarray(channel_img_array, 'L').save(os.path.join(debug_dir, f'channel_{i}.png'))


    building_mask_channel_index = 2 

    if processed_array.shape[-1] > building_mask_channel_index:
        binary_building_mask = (processed_array[:, :, building_mask_channel_index] > 128).astype(np.uint8) * 255
        
        refined_mask = np.copy(binary_building_mask) 

        original_grayscale = np.dot(original_img_array[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)
        
        brightness_threshold_low = 120 
        brightness_threshold_high = 200

        refined_mask[original_grayscale < brightness_threshold_low] = 0
        refined_mask[original_grayscale > brightness_threshold_high] = 0
        
        green_mask_pil = Image.fromarray(refined_mask, 'L') 

        try:
            ivy_texture_pil = Image.open(IVY_TEXTURE_PATH).convert('RGBA') 
            ivy_texture_pil = ivy_texture_pil.resize(original_img_pil.size, Image.Resampling.LANCZOS) # Yüksek kalite resize
        except FileNotFoundError:
            print(f"HATA: Sarmaşık dokusu dosyası bulunamadı: {IVY_TEXTURE_PATH}. Varsayılan yeşil renk kullanılacak.")
            ivy_texture_pil = None # Hata durumunda doku yok

        original_img_rgba = original_img_pil.convert('RGBA') # Orijinal resim şeffaflık için RGBA

        if ivy_texture_pil:
            ivy_textured_mask_pil = ivy_texture_pil.copy()
            ivy_textured_mask_pil.putalpha(green_mask_pil) # Maskeyi dokunun alpha kanalı olarak ata

            combined_img = Image.alpha_composite(original_img_rgba, ivy_textured_mask_pil)
            
        else: # Sarmaşık dokusu bulunamazsa veya hata olursa, eski yeşil renk bindirme
            green_layer = Image.new('RGBA', original_img_rgba.size, (0, 0, 0, 0))
            green_pixels = green_layer.load()
            mask_pixels = green_mask_pil.load() 
            for x in range(green_mask_pil.width):
                for y in range(green_mask_pil.height):
                    if mask_pixels[x, y] == 255: 
                        green_pixels[x, y] = (0, 200, 0, 150) # Varsayılan yeşil

            combined_img = Image.alpha_composite(original_img_rgba, green_layer)

        return combined_img.convert('RGB') # JPG olarak kaydedeceğimiz için RGB'ye çevir

    else:
        # Eğer building_mask_channel_index geçersizse veya 6 kanal yoksa
        print("UYARI: Bina maske kanalı bulunamadı veya geçersiz indeks. Varsayılan çıktı döndürülüyor.")
        if processed_array.shape[-1] >= 3:
            image_data = processed_array[:, :, :3]
            img = Image.fromarray(image_data, 'RGB')
            return img
        else:
            print("HATA: Model çıktısı görselleştirme için uygun değil (beklenenden az kanal).")
            return Image.new('RGB', (256, 256), (0, 0, 0))

def generate_green_design_simulation(area_type, original_image_path=None):
    """
    Derin öğrenme modelini kullanarak yeşil tasarım çıktısı üretir.
    """
    if model is None:
        # Model yüklenemezse veya bulunamazsa yedek bir görsel döndür
        print("Model yüklenemediği için varsayılan görsel kullanılıyor.")
        if area_type == "building":
            return {
                "design_url": "/static/green_building_design.jpg",
                "description": "AI modeli yüklenemediği için varsayılan bina1 tasarımı gösteriliyor."
            }
        else: 
            return {
                "design_url": "/static/green_road_design.png",
                "description": "AI modeli yüklenemediği için varsayılan bina2 tasarımı gösteriliyor."
            }


    if original_image_path:
        try:
            input_image = preprocess_image(original_image_path)
            # Modelden çıkarım yap
            if input_image is None:
                raise ValueError("Orijinal resim ön işlenemedi veya bulunamadı.")
                 # Modelden çıkarım yap
            generated_output = model.predict(input_image)
            print(f"DEBUG: Model çıktısının şekli (shape): {generated_output.shape}")
            print(f"DEBUG: Model çıktısının veri tipi (dtype): {generated_output.dtype}")
            # **************************
            # Üretilen görüntüyü static/generated_designs/ klasörüne kaydet
            output_image_pil = postprocess_image(generated_output, original_image_path)
            import uuid
            output_filename = f"generated_{uuid.uuid4()}.jpg"
            output_filepath = os.path.join(GENERATED_DESIGNS_DIR, output_filename)
            output_image_pil.save(output_filepath)

            # Frontend'e döndürülecek URL
            # Flask'ın static_url_path'ını kullanarak doğru URL'yi oluştur
            design_url = f"http://127.0.0.1:5000/static/generated_designs/{output_filename}"

            return {
                "design_url": design_url,
                "description": f"AI tarafından üretilmiş yeşil {area_type} tasarımı."
            }
        except Exception as e:
            print(f"Model çıkarımı veya görsel kaydı sırasında hata oluştu: {e}")
            # Hata durumunda varsayılan görsel döndür
            if area_type == "building":
                return {
                    "design_url": "/static/green_building_design.jpg",
                    "description": "Tasarım oluşturulurken hata oluştu, varsayılan bina tasarımı gösteriliyor."
                }
            else:
                return {
                    "design_url": "/static/green_road_design.png",
                    "description": "Tasarım oluşturulurken hata oluştu, varsayılan yol tasarımı gösteriliyor."
                }

    else:
        # original_image_path sağlanmazsa veya statik görseller kullanılmak istenirse
        if area_type == "building":
            return {
                "design_url": "/static/green_building_design.jpg",
                "description": "Varsayılan bina yeşillendirme tasarımı."
            }
        elif area_type == "road":
            return {
                "design_url": "/static/green_road_design.png",
                "description": "Varsayılan yol kenarı yeşillendirme tasarımı."
            }
        else:
            return {
                "design_url": "/static/green_road_design.png", # Veya başka bir varsayılan
                "description": "Yapay zeka tarafından oluşturulmuş genel yeşillendirme önerisi."
            }
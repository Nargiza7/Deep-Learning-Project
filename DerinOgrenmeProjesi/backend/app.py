# app.py (Projenizin ana dizininde)
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
from .data import MOCK_AREAS, MOCK_HEAT_SPOTS, PLANTS_DB, get_area_by_id
from .model_simulation import generate_green_design_simulation

app = Flask(__name__, static_folder='../static', static_url_path='/static')
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

# --- Yeni Eklenen Endpoint: input_images klasöründeki tüm görselleri işle ---
@app.route('/api/process-all-images', methods=['GET'])
def process_all_images_in_folder():
    input_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'input_images')
    processed_results = []
    
    if not os.path.exists(input_folder):
        return jsonify({"error": f"Input klasörü bulunamadı: {input_folder}"}), 404

    allowed_extensions = ('.png', '.jpg', '.jpeg')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(allowed_extensions):
            file_path = os.path.join(input_folder, filename)
            
            if "building" in filename.lower():
                area_type = "building"
            elif "road" in filename.lower():
                area_type = "road"
            else:
                area_type = "generic" 

            print(f"İşleniyor: {filename} (Tip: {area_type})")

            try:
                result = generate_green_design_simulation(area_type, original_image_path=file_path)
                
                processed_results.append({
                    "original_filename": filename,
                    "design_url": result.get("design_url", ""),
                    "description": result.get("description", ""),
                    "status": "success"
                })
            except Exception as e:
                print(f"Hata oluştu {filename} işlenirken: {e}")
                processed_results.append({
                    "original_filename": filename,
                    "status": "error",
                    "message": str(e)
                })

    return jsonify(processed_results)


@app.route('/api/map-data', methods=['GET'])
def get_map_data():
    return jsonify({
        "areas": MOCK_AREAS,
        "heat_spots": MOCK_HEAT_SPOTS
    })

@app.route('/api/generate-recommendation/<area_id>', methods=['GET'])
def generate_recommendation(area_id):
    selected_area = get_area_by_id(area_id)
    if not selected_area:
        return jsonify({"error": "Bölge bulunamadı"}), 404

    area_type = selected_area["area_type"]

    input_images_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'input_images')
    original_image_path = None
    
    allowed_extensions = ('.png', '.jpg', '.jpeg')
    
    for filename in os.listdir(input_images_folder):
        if (str(area_id) in filename.lower() or 
            selected_area["name"].lower().replace(" ", "_") in filename.lower()) \
            and filename.lower().endswith(allowed_extensions):
            
            original_image_path = os.path.join(input_images_folder, filename)
            print(f"DEBUG: {selected_area['name']} için bulunan resim: {original_image_path}")
            break # İlk bulunan eşleşen resmi al ve döngüden çık
    
    if not original_image_path:
        # Eğer input_images klasöründe eşleşen bir resim bulunamazsa
        print(f"UYARI: {selected_area['name']} (ID: {area_id}) için input_images klasöründe uygun resim bulunamadı.")
        if area_type == "building":
            original_image_path = os.path.join(app.static_folder, "original_building.jpg")
        elif area_type == "road":
            original_image_path = os.path.join(app.static_folder, "original_road.png")
        else:
            original_image_path = None 
            print(f"HATA: {selected_area['name']} için varsayılan statik resim de bulunamadı.")

        if original_image_path and not os.path.exists(original_image_path):
            print(f"HATA: Varsayılan resim de bulunamadı: {original_image_path}")
            return jsonify({"error": "İşlenecek görsel bulunamadı."}), 500

    # Modeli çağırın
    design_output = generate_green_design_simulation(area_type, original_image_path)

    if area_type == "building":
        plants_data = [
            {"name": "Orman Sarmaşığı (Clematis vitalba)", "description": "Karadeniz iklimine uygun, sarılıcı bitki."},
            {"name": "Camgüzeli (Impatiens walleriana)", "description": "Gölgeli alanlara renk katan çiçekli bitki."}
        ]
        benefits_data = {
            "temp_reduction_celsius": "3-6",
            "co2_absorption_kg_year": "60-120"
        }
    else: 
        plants_data = [
            {"name": "Karaçam (Pinus nigra)", "description": "Soğuk iklime dayanıklı, uzun ömürlü iğne yapraklı."},
            {"name": "Mazı (Thuja occidentalis)", "description": "Kuraklığa dayanıklı, süs bitkisi olarak ideal."}
        ]
        benefits_data = {
            "temp_reduction_celsius": "1-3",
            "co2_absorption_kg_year": "30-70"
        }

    return jsonify({
        "selected_area_name": selected_area["name"],
        "design": design_output,
        "plants": plants_data,
        "benefits": benefits_data
    })

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# data.py

MOCK_AREAS = [
    # Sakarya
    {"id": 1, "name": "Merkez Park", "area_type": "road", "coords": [40.783, 30.407], "city": "Sakarya"},
    {"id": 2, "name": "Kampüs Binası", "area_type": "building", "coords": [40.739, 30.342], "city": "Sakarya"},
    {"id": 3, "name": "Adapazarı Caddesi", "area_type": "road", "coords": [40.771, 30.380], "city": "Sakarya"},
    {"id": 4, "name": "Ferizli Sanayi", "area_type": "building", "coords": [40.850, 30.490], "city": "Sakarya"},

    # İstanbul (iklim: ılıman-karasal)
    {"id": 5, "name": "Kadıköy Sahil Yolu", "area_type": "road", "coords": [40.990, 29.028], "city": "İstanbul"},
    {"id": 6, "name": "Şişli İş Merkezi", "area_type": "building", "coords": [41.060, 28.987], "city": "İstanbul"},
    {"id": 7, "name": "Üsküdar Meydan", "area_type": "road", "coords": [41.025, 29.020], "city": "İstanbul"},

    # Antalya (iklim: sıcak-akdeniz)
    {"id": 8, "name": "Konyaaltı Sahili", "area_type": "road", "coords": [36.850, 30.650], "city": "Antalya"},
    {"id": 9, "name": "Kepez İş Merkezi", "area_type": "building", "coords": [36.920, 30.690], "city": "Antalya"},
    {"id":10, "name": "Lara Yolu", "area_type": "road", "coords": [36.860, 30.780], "city": "Antalya"},
    
    # Düzce (karadeniz)
    {"id": 11, "name": "Düzce Merkez Cadde", "area_type": "road", "coords": [40.8438, 31.1565], "city": "Düzce"},
    {"id": 12, "name": "Düzce Üniversite Binası", "area_type": "building", "coords": [40.8500, 31.1600], "city": "Düzce"},

    # Ankara (karasal)
    {"id": 13, "name": "Kızılay Meydanı", "area_type": "road", "coords": [39.9208, 32.8541], "city": "Ankara"},
    {"id": 14, "name": "ODTÜ Kampüsü", "area_type": "building", "coords": [39.9017, 32.7800], "city": "Ankara"},

    # İzmir (akdeniz)
    {"id": 15, "name": "Alsancak Sahili", "area_type": "road", "coords": [38.4192, 27.1287], "city": "İzmir"},
    {"id": 16, "name": "Ege Üniversitesi", "area_type": "building", "coords": [38.4563, 27.2224], "city": "İzmir"},

    # Bursa (marmara - geçiş)
    {"id": 17, "name": "Heykel Meydanı", "area_type": "road", "coords": [40.1828, 29.0663], "city": "Bursa"},
    {"id": 18, "name": "Uludağ Üniversitesi", "area_type": "building", "coords": [40.2222, 28.8515], "city": "Bursa"},
]

MOCK_HEAT_SPOTS = [
    # Sakarya
    {"id": 101, "coords": [40.785, 30.405], "intensity": 0.8},
    {"id": 102, "coords": [40.738, 30.345], "intensity": 0.9},
    {"id": 103, "coords": [40.770, 30.382], "intensity": 0.7},
    {"id": 104, "coords": [40.849, 30.491], "intensity": 0.95},

    # İstanbul
    {"id": 105, "coords": [41.060, 28.987], "intensity": 0.88},
    {"id": 106, "coords": [40.990, 29.028], "intensity": 0.82},
    {"id": 107, "coords": [41.025, 29.020], "intensity": 0.91},

    # Antalya
    {"id": 108, "coords": [36.850, 30.650], "intensity": 0.93},
    {"id": 109, "coords": [36.920, 30.690], "intensity": 0.89},
    {"id": 110, "coords": [36.860, 30.780], "intensity": 0.94},
    
     # Düzce
    {"id": 111, "coords": [40.8445, 31.1575], "intensity": 0.75},
    {"id": 112, "coords": [40.8505, 31.1615], "intensity": 0.80},

    # Ankara
    {"id": 113, "coords": [39.9215, 32.8555], "intensity": 0.85},
    {"id": 114, "coords": [39.9025, 32.7825], "intensity": 0.88},

    # İzmir
    {"id": 115, "coords": [38.4200, 27.1300], "intensity": 0.90},
    {"id": 116, "coords": [38.4570, 27.2235], "intensity": 0.87},

    # Bursa
    {"id": 117, "coords": [40.1835, 29.0670], "intensity": 0.78},
    {"id": 118, "coords": [40.2230, 28.8520], "intensity": 0.82},
]

PLANTS_DB = {
    "Sakarya": {
        "building": [
            {"name": "Sarmaşık (Hedera helix)", "description": "Hızlı büyüyen tırmanıcı, dört mevsim yeşil."},
            {"name": "Hanımeli (Lonicera caprifolium)", "description": "Kokulu çiçekleri olan tırmanıcı bitki."}
        ],
        "road": [
            {"name": "Sukulent (Sedum spp.)", "description": "Kuraklığa dayanıklı, bakım gerektirmeyen."},
            {"name": "Lavanta (Lavandula angustifolia)", "description": "Güzel kokulu, az su isteyen bitki."}
        ]
    },
    "İstanbul": {
        "building": [
            {"name": "Taflan (Euonymus japonicus)", "description": "Yaprak dökmeyen, cephe için uygun."},
            {"name": "Ortanca (Hydrangea macrophylla)", "description": "Yarı gölgeli alanlarda güzel çiçek açar."}
        ],
        "road": [
            {"name": "Akçaağaç (Acer campestre)", "description": "Yol kenarı için ideal, gölge sağlar."},
            {"name": "Fundalık (Erica carnea)", "description": "Düşük boylu, yoğun yeşil alan sağlar."}
        ]
    },
    "Antalya": {
        "building": [
            {"name": "Begonvil (Bougainvillea)", "description": "Güneşi seven, rengarenk çiçekli sarmaşık."},
            {"name": "Zakkum (Nerium oleander)", "description": "Sıcağa dayanıklı, bol çiçek açan bitki."}
        ],
        "road": [
            {"name": "Palmiye (Phoenix canariensis)", "description": "Akdeniz iklimine uygun yol ağacı."},
            {"name": "Cezayir Menekşesi (Vinca major)", "description": "Yol kenarında yer örtücü olarak kullanılır."}
        ]
    },
     "Düzce": {
        "building": [
            {"name": "Orman Sarmaşığı (Clematis vitalba)", "description": "Karadeniz iklimine uygun, sarılıcı bitki."},
            {"name": "Camgüzeli (Impatiens walleriana)", "description": "Gölgeli alanlara renk katan çiçekli bitki."}
        ],
        "road": [
            {"name": "Yalancı Akasya (Robinia pseudoacacia)", "description": "Gölgeli alan sağlar, nemi sever."},
            {"name": "Ortanca (Hydrangea)", "description": "Nemli iklimde gür çiçeklenme yapar."}
        ]
    },
    "Ankara": {
        "building": [
            {"name": "Karaçam (Pinus nigra)", "description": "Soğuk iklime dayanıklı, uzun ömürlü iğne yapraklı."},
            {"name": "Mazı (Thuja occidentalis)", "description": "Kuraklığa dayanıklı, süs bitkisi olarak ideal."}
        ],
        "road": [
            {"name": "Çınar (Platanus orientalis)", "description": "Geniş yapraklı, gölge sağlayan klasik şehir ağacı."},
            {"name": "Lavanta (Lavandula spp.)", "description": "Kuraklığa dayanıklı, hoş kokulu çalı bitkisi."}
        ]
    },
     "İzmir": {
        "building": [
            {"name": "Zakkum (Nerium oleander)", "description": "Akdeniz iklimine uygun, bol çiçekli çalı."},
            {"name": "Sardunya (Pelargonium)", "description": "Sıcağı seven, balkonlar için ideal çiçek."}
        ],
        "road": [
            {"name": "Palmiye (Washingtonia filifera)", "description": "Sıcak iklime uygun gösterişli yol ağacı."},
            {"name": "Biberiye (Rosmarinus officinalis)", "description": "Yer örtücü, az su isteyen aromatik bitki."}
        ]
    },
    "Bursa": {
        "building": [
            {"name": "Ortanca (Hydrangea macrophylla)", "description": "Gölge ve nemi seven, renkli çiçek açar."},
            {"name": "Kış Defnesi (Daphne mezereum)", "description": "Geçiş iklimine uygun hoş kokulu çalı."}
        ],
        "road": [
            {"name": "Ihlamur (Tilia cordata)", "description": "Gölge sağlayan, kokulu çiçekli yol ağacı."},
            {"name": "Ateş Dikeni (Pyracantha)", "description": "Çit olarak kullanılabilir, kuşlara barınak sağlar."}
        ]
    }
}

def get_area_by_id(area_id):
    """Verilen ID'ye sahip alanı MOCK_AREAS'tan bulur."""
    # area_id bir int olarak gelmeli, bu yüzden karşılaştırma yapmadan önce dönüştürüyoruz
    return next((area for area in MOCK_AREAS if area["id"] == int(area_id)), None)
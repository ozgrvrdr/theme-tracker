# Tema ve Ticker Eşleşmeleri (Genişletilmiş 40+ Tema Evreni)
THEME_MAP = {
    "Oil Services": "OIH", "Oil & Gas": "XLE", "Silver Miners": "SIL", "Drones": "UAV",
    "Cybersecurity": "BUG", "Medical Devices": "IHI", "Software": "IGV", 
    "Defense": "XAR", "China Internet": "KWEB", "Healthcare": "XLV", "Biotechnology": "IBB",
    "Steel": "SLX", "Gold Miners": "GDX", "Capital Markets": "KCE", "Banks": "KBE", "Fintech": "FINX",
    "Semiconductors": "SMH", "Solar": "TAN", "Nuclear": "URA", "Crypto": "IBIT",
    "Industrials": "XLI", "Construction": "ITB", "Insurance": "KIE", "Aerospace": "ITA",
    "Robotics": "BOTZ", "Consumer Growth": "XLY", "Retail": "XRT",
    "Photonics": "LOPT", "Optical Networking": "ITEK", "Memory": "SOXX", "AI Infrastructure": "AIQ",
    "Semiconductor Equipment": "PSI", "Neocloud / Data Center": "WCLD", "Grid Infrastructure": "GRID",
    "Data Center Infrastructure": "SRVR", "Power Generation": "XLU", "Space": "UFO",
    "Quantum": "QTUM", "AdTech": "SOCL", "Hyperscalers": "MAGS"
}

BENCHMARK = "SPY"
MA_PERIOD = 50  # İhtiyaç halinde eklenecek hareketli ortalamalar için

# Bileşik Skor Ağırlıkları (Hızlı Rotasyon Optimizasyonu)
WEIGHT_1W = 0.25  # Kısa vadeli ani momentum / Yeni para akışı (%25)
WEIGHT_1M = 0.50  # Ana trend yönü ve rotasyon merkezi (%50)
WEIGHT_3M = 0.25  # Uzun vadeli yapısal onay (%25)

import requests
import json
import os
from github import Github
import time

# Configurar variables desde los secrets de GitHub
METEOBLUE_API_KEY = os.getenv("https://my.meteoblue.com/warnings/feeds?apikey=DEMOKEY&sig=04dd5ae79c15b3e9c7fa6989fa219210")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "usuario/weather-warnings-map"

# Definir la rejilla de coordenadas para Europa (aproximada)
# Vamos a recorrer Europa con una separación de ~3 grados
LAT_MIN, LAT_MAX = 35.0, 70.0  # Desde España hasta el norte de Europa
LON_MIN, LON_MAX = -25.0, 40.0  # Desde Portugal hasta Rusia
STEP = 3  # Separación entre puntos (en grados)

geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Recorrer Europa en una cuadrícula de puntos
for lat in range(int(LAT_MIN), int(LAT_MAX) + 1, STEP):
    for lon in range(int(LON_MIN), int(LON_MAX) + 1, STEP):
        print(f"Consultando avisos en: lat={lat}, lon={lon}")
        url = f"https://my.meteoblue.com/warnings/list?apikey={METEOBLUE_API_KEY}&lat={lat}&lon={lon}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            warnings = response.json()
            
            for warning in warnings.get("warnings", []):
                feature = {
                    "type": "Feature",
                    "properties": {
                        "title": warning.get("title", "Aviso"),
                        "description": warning.get("description", ""),
                        "severity": warning.get("severity", "Moderate"),
                        "source": warning.get("source", "meteoblue")
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    }
                }
                geojson["features"].append(feature)
            
            # Esperar un poco para evitar sobrecargar la API
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {lat}, {lon}: {e}")

# Guardar GeoJSON
file_name = "warnings.geojson"
with open(file_name, "w") as f:
    json.dump(geojson, f, indent=4)

print(f"Archivo {file_name} generado con {len(geojson['features'])} avisos.")

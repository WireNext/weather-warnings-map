import requests
import json
import os
import time

# Leer la API Key desde las variables de entorno (GitHub Secrets)
METEOBLUE_API_KEY = os.getenv("METEOBLUE_API_KEY")

# Definir la rejilla de coordenadas para Europa
LAT_MIN, LAT_MAX = 35.0, 70.0
LON_MIN, LON_MAX = -25.0, 40.0
STEP = 3

geojson = {"type": "FeatureCollection", "features": []}

# Recorrer Europa en una cuadrícula de puntos
for lat in range(int(LAT_MIN), int(LAT_MAX) + 1, STEP):
    for lon in range(int(LON_MIN), int(LON_MAX) + 1, STEP):
        print(f"Consultando avisos en: lat={lat}, lon={lon}")
        url = f"https://my.meteoblue.com/warnings/list?apikey={METEOBLUE_API_KEY}&lat={lat}&lon={lon}"

        try:
            response = requests.get(url)
            response.raise_for_status()
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

            time.sleep(1)  # Pausa para evitar sobrecargar la API

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de {lat}, {lon}: {e}")

# Guardar los datos en un archivo GeoJSON
file_name = "warnings.geojson"
with open(file_name, "w") as f:
    json.dump(geojson, f, indent=4)

print(f"Archivo {file_name} generado con {len(geojson['features'])} avisos.")

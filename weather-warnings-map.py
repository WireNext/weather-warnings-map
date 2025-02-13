import requests
import json
from github import Github

# Configura tu API Key de meteoblue y tu repositorio de GitHub
METEOBLUE_API_KEY = "TU_API_KEY"
GITHUB_TOKEN = "TU_GITHUB_TOKEN"
REPO_NAME = "usuario/weather-warnings-map"

# Llamada a la API de meteoblue
lat, lon = 40.4168, -3.7038  # Madrid (ejemplo)
url = f"https://my.meteoblue.com/warnings/list?apikey={METEOBLUE_API_KEY}&lat={lat}&lon={lon}"
response = requests.get(url)
warnings = response.json()

# Crear el GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for warning in warnings.get("warnings", []):
    feature = {
        "type": "Feature",
        "properties": {
            "title": warning.get("title", "Aviso"),
            "description": warning.get("description", ""),
            "severity": warning.get("severity", "Moderate")
        },
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat]  # Usa coordenadas reales si meteoblue las proporciona
        }
    }
    geojson["features"].append(feature)

# Guardar el archivo localmente
file_name = "warnings.geojson"
with open(file_name, "w") as f:
    json.dump(geojson, f, indent=4)

# Subir el archivo a GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
contents = repo.get_contents(file_name)  # Intenta obtener el archivo actual
repo.update_file(contents.path, "Actualización de avisos", json.dumps(geojson, indent=4), contents.sha)

print("Archivo subido a GitHub.")

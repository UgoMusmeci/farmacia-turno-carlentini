import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

URL = "https://www.farmaciediturno.org/comune.asp?cod=89006"

farmacie = {

    "SANTUZZI": {
        "nome": "Farmacia Santuzzi",
        "indirizzo": "Via XXV Aprile 33-35, Carlentini",
        "telefono": "+39 095 16949397",
        "lat": 37.29758984109579,
        "lng": 15.005323012591258,
        "comune": "Carlentini",
        "frazione": "",
        "maps_query": "Farmacia Santuzzi Carlentini"
    },

    "SANGIORGIO": {
        "nome": "Farmacia Sangiorgio",
        "indirizzo": "Via Raffaello 150, Carlentini",
        "telefono": "+39 095 991030",
        "lat": 37.27230505166669,
        "lng": 15.016562356992173,
        "comune": "Carlentini",
        "frazione": "",
        "maps_query": "Farmacia Sangiorgio Carlentini"
    },

    "STRAZZERI": {
        "nome": "Farmacia Strazzeri",
        "indirizzo": "Via Guglielmo Marconi 71, Carlentini",
        "telefono": "+39 095 7611196",
        "lat": 37.2763652,
        "lng": 15.0161213,
        "comune": "Carlentini",
        "frazione": "",
        "maps_query": "Farmacia Strazzeri Carlentini"
    },

    "INSERRA": {
        "nome": "Farmacia Inserra",
        "indirizzo": "Via Camillo Benso Conte di Cavour 107, Carlentini",
        "telefono": "+39 095 991034",
        "lat": 37.2749998,
        "lng": 15.0153259,
        "comune": "Carlentini",
        "frazione": "",
        "maps_query": "Farmacia Inserra Carlentini"
    },

    "MORALE": {
        "nome": "Farmacia Morale",
        "indirizzo": "Via Principe Emanuele 52, Pedagaggi",
        "telefono": "+39 095 995288",
        "lat": 37.1936688777624,
        "lng": 14.937791220118037,
        "comune": "Carlentini",
        "frazione": "Pedagaggi",
        "maps_query": "Farmacia Morale Pedagaggi"
    }

}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}

try:

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    print("========== TESTO PAGINA ==========")
    print(text)
    print("==================================")

    farmacia_turno = None

    match = re.search(
        r"(SANTUZZI|SANGIORGIO|STRAZZERI|INSERRA|MORALE).*?Turno:",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        nome_trovato = match.group(1).upper()

        print(f"FARMACIA DI TURNO TROVATA: {nome_trovato}")

        farmacia_turno = farmacie.get(nome_trovato)

    else:

        print("Nessuna farmacia di turno trovata.")

    output = {
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "source": URL,
        "success": farmacia_turno is not None,
        "farmacia": farmacia_turno if farmacia_turno else {}
    }

except Exception as e:

    print("ERRORE:")
    print(str(e))

    output = {
        "last_update": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "source": URL,
        "success": False,
        "error": str(e),
        "farmacia": {}
    }

with open("data/farmacia.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("JSON aggiornato.")
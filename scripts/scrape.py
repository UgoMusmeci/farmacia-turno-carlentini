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
        "lng": 15.005323012591258
    },

    "SANGIORGIO": {
        "nome": "Farmacia Sangiorgio",
        "indirizzo": "Via Raffaello 150, Carlentini",
        "telefono": "+39 095 991030",
        "lat": 37.27230505166669,
        "lng": 15.016562356992173
    },

    "STRAZZERI": {
        "nome": "Farmacia Strazzeri",
        "indirizzo": "Via Guglielmo Marconi 71, Carlentini",
        "telefono": "+39 095 7611196",
        "lat": 37.2763652,
        "lng": 15.0161213
    },

    "INSERRA": {
        "nome": "Farmacia Inserra",
        "indirizzo": "Via Camillo Benso Conte di Cavour 107, Carlentini",
        "telefono": "+39 095 991034",
        "lat": 37.2749998,
        "lng": 15.0153259
    },

    "MORALE": {
        "nome": "Farmacia Morale",
        "indirizzo": "Via Principe Emanuele 52, Pedagaggi",
        "telefono": "+39 095 995288",
        "lat": 37.1936688777624,
        "lng": 14.937791220118037
    }

}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}

output = {
    "last_update": datetime.now().strftime("%d/%m/%Y %H:%M"),
    "source": URL,
    "success": False,
    "farmacia": {}
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

    turno_match = re.search(
        r"(SANTUZZI|SANGIORGIO|STRAZZERI|INSERRA|MORALE).*?Turno:\s*Tutto il giorno",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if turno_match:

        nome_turno = turno_match.group(1).upper()

        print(f"FARMACIA DI TURNO TROVATA: {nome_turno}")

        farmacia_turno = farmacie.get(nome_turno)

        if farmacia_turno:

            output["success"] = True
            output["farmacia"] = farmacia_turno

    else:

        print("NESSUNA FARMACIA DI TURNO TROVATA")

except Exception as e:

    print("ERRORE:")
    print(str(e))

    output["error"] = str(e)

with open("data/farmacia.json", "w", encoding="utf-8") as f:

    json.dump(output, f, ensure_ascii=False, indent=2)

print("JSON aggiornato.")
```

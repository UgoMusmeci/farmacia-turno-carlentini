import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import os

URL = "https://www.farmaciediturno.org/comune.asp?cod=89006"

OUTPUT_FILE = "data/farmacia.json"

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

    text_upper = text.upper()

    farmacia_trovata = None
    punteggio_massimo = 0

    indicatori = [
        ("TURNO", 100),
        ("TUTTO IL GIORNO", 80),
        ("FINO A DOMANI", 70),
        ("REPERIBILIT", 60),
        ("APERTA", 10)
    ]

    for nome_farmacia in farmacie.keys():

        print(f"\nAnalisi farmacia: {nome_farmacia}")

        pattern = rf"{nome_farmacia}(.*?)(SANTUZZI|SANGIORGIO|STRAZZERI|INSERRA|MORALE|LINK PERMANENTE)"

        match = re.search(
            pattern,
            text_upper,
            re.DOTALL
        )

        if not match:
            print("Blocco non trovato")
            continue

        blocco = match.group(1)

        punteggio = 0

        for indicatore, valore in indicatori:

            if indicatore in blocco:

                punteggio += valore

                print(f"Indicatore trovato: {indicatore} (+{valore})")

        print(f"Punteggio finale: {punteggio}")

        if punteggio > punteggio_massimo:

            punteggio_massimo = punteggio
            farmacia_trovata = nome_farmacia

    if farmacia_trovata:

        print(f"\nFARMACIA DI TURNO IDENTIFICATA: {farmacia_trovata}")

        output["success"] = True
        output["farmacia"] = farmacie[farmacia_trovata]

    else:

        print("\nNESSUNA FARMACIA IDENTIFICATA")

        # FALLBACK: mantieni ultimo JSON valido

        if os.path.exists(OUTPUT_FILE):

            print("Tentativo recupero ultimo JSON valido...")

            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:

                vecchio_output = json.load(f)

                if vecchio_output.get("success"):

                    output = vecchio_output

                    output["warning"] = (
                        "Impossibile aggiornare automaticamente. "
                        "Mostrato ultimo dato valido."
                    )

                    print("Ultimo JSON valido recuperato.")

except Exception as e:

    print("\nERRORE:")
    print(str(e))

    output["error"] = str(e)

    # FALLBACK SU ULTIMO JSON VALIDO

    if os.path.exists(OUTPUT_FILE):

        try:

            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:

                vecchio_output = json.load(f)

                if vecchio_output.get("success"):

                    output = vecchio_output

                    output["warning"] = (
                        "Errore aggiornamento automatico. "
                        "Mostrato ultimo dato valido."
                    )

                    print("Recuperato ultimo JSON valido.")

        except:
            pass

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(output, f, ensure_ascii=False, indent=2)

print("\nJSON aggiornato.")

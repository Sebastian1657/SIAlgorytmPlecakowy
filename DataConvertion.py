import csv
from typing import List, Dict, Any

def load_csv(sciezka_pliku: str) -> List[Dict[str, Any]]:
    ostatni_blad = None

    for encoding in ('utf-8', 'utf-8-sig', 'cp1250'):
        przedmioty = []
        try:
            with open(sciezka_pliku, mode='r', encoding=encoding, newline='') as plik:
                reader = csv.DictReader(plik)
                
                for wiersz in reader:
                    # Rzutowanie typów danych
                    wiersz['id'] = int(wiersz['id'])
                    wiersz['waga_kg'] = float(wiersz['waga_kg'])
                    wiersz['stackowalny'] = wiersz['stackowalny'] == 'True'
                    wiersz['pancerz'] = int(wiersz['pancerz'])
                    wiersz['zdrowie'] = int(wiersz['zdrowie'])
                    wiersz['mana'] = int(wiersz['mana'])
                    wiersz['obrazenia'] = int(wiersz['obrazenia'])
                    wiersz['charyzma'] = int(wiersz['charyzma'])
                    
                    przedmioty.append(wiersz)

            return przedmioty
        except UnicodeDecodeError as blad:
            ostatni_blad = blad

    if ostatni_blad is not None:
        raise ValueError(
            f"Nie udalo sie odczytac pliku '{sciezka_pliku}' jako UTF-8 ani CP1250."
        ) from ostatni_blad

    raise ValueError(f"Nie udalo sie odczytac pliku '{sciezka_pliku}'.")

# Przykład użycia:
# dataset = load_csv('przedmioty.csv')

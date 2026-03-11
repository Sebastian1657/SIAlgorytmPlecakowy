import csv
from typing import List, Dict, Any

def load_csv(sciezka_pliku: str) -> List[Dict[str, Any]]:
    przedmioty = []
    
    with open(sciezka_pliku, mode='r', encoding='utf-8') as plik:
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

# Przykład użycia:
# dataset = load_csv('przedmioty.csv')
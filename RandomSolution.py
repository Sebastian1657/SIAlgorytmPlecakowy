import argparse
import random
import time
from typing import List, Dict, Any

from DataConvertion import load_csv

def RandomSolution(przedmioty: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generuje pojedyncze, w pełni legalne rozwiązanie (wektor harmonii).
    """
    harmonia = {
        'zbroja': {},
        'plecak': [],
        'calkowita_waga': 0.0,
        'zajete_sloty': 0,
        'fitness_score': 0.0
    }
    
    # 1. Rozdzielenie puli przedmiotów
    zbroje = {'Glowa': [], 'Korpus': [], 'Nogi': [], 'Buty': [], 'Rekawice': []}
    plecak_pula = []
    
    for p in przedmioty:
        if p['kategoria'] == 'Zbroja' and p['slot'] in zbroje:
            zbroje[p['slot']].append(p)
        else:
            plecak_pula.append(p)
    
    # 2. Losowanie wyposażenia zbroi (MCKP)
    pusty_slot = {'id': None, 'waga_kg': 0.0, 'pancerz': 0, 'zdrowie': 0, 'mana': 0, 'obrazenia': 0}
    
    for slot, pula in zbroje.items():
        # Nie dopasowujemy do limitu wagi – losujemy z pełnej puli + pusty slot
        dostepne_opcje = list(pula)
        dostepne_opcje.append(pusty_slot)
        
        wybrany_pancerz = random.choice(dostepne_opcje)
        
        harmonia['zbroja'][slot] = wybrany_pancerz
        harmonia['calkowita_waga'] += float(wybrany_pancerz['waga_kg'])
        
    # 3. Losowanie zawartości plecaka (MDKP)
    random.shuffle(plecak_pula)
    
    for p in plecak_pula:
        if harmonia['zajete_sloty'] >= 20:
            break # Plecak pełny
            
        waga_bazowa = float(p['waga_kg'])
        ilosc = 1
        
        # 4. Obsługa stackowania do 5 sztuk dla przedmiotów użytkowych
        is_stackable = p.get('stackowalny') in ['True', True, '1'] 
        
        if is_stackable:
            ilosc = random.randint(1, 5)
            
        waga_calkowita_przedmiotu = waga_bazowa * ilosc
        
        # Nie dopasowujemy do limitu wagi – zawsze dodajemy, jeśli są sloty
        item_kopia = p.copy()
        item_kopia['wylosowana_ilosc'] = ilosc
        
        harmonia['plecak'].append(item_kopia)
        harmonia['calkowita_waga'] += waga_calkowita_przedmiotu
        harmonia['zajete_sloty'] += 1

    return harmonia

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Generowanie danych testowych do problemu plecakowego.")
#     parser.add_argument("-l", "--items-list", type=str, default="przedmioty.csv", help="Ścieżka do pliku z listą przedmiotów (domyślnie przedmioty.csv).")

#     args = parser.parse_args()
#     items = load_csv(args.items_list)
#     RandomSolution(items, args.max_weight)

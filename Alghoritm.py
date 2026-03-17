import argparse
import random
import RandomSolution

def CalculateFitnessScore(harmonia: dict, focus_stat: str) -> float:
    stats = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    
    if focus_stat not in stats:
        raise ValueError(f"Nieznana statystyka: {focus_stat}. Dostępne: {stats}")

    # Definicja mnożników (można je później przenieść do konfiguracji globalnej)
    WAGA_GLOWNA = 1.0
    WAGA_POBOCZNA = 0.5
    
    calkowity_wynik = 0.0

    # 1. Sumowanie statystyk ze zbroi
    for item in harmonia['zbroja'].values():
        if item.get('id') is not None:  # Pominięcie pustych slotów
            for statystyka in stats:
                mnoznik = WAGA_GLOWNA if statystyka == focus_stat else WAGA_POBOCZNA
                calkowity_wynik += item.get(statystyka, 0) * mnoznik
                
    # 2. Sumowanie statystyk z plecaka
    for item in harmonia['plecak']:
        ilosc = item.get('wylosowana_ilosc', 1)
        for statystyka in stats:
            mnoznik = WAGA_GLOWNA if statystyka == focus_stat else WAGA_POBOCZNA
            # Mnożymy wartość statystyki przez ilość sztuk w stacku i przez wagę
            calkowity_wynik += (item.get(statystyka, 0) * ilosc) * mnoznik
            
    # Zapis w strukturze dla łatwiejszego sortowania
    harmonia['fitness_score'] = round(calkowity_wynik, 2)
    
    return harmonia['fitness_score']

def ImplementPenalty(harmonia: dict, max_weight: float, max_slots: int) -> None:
    if harmonia['calkowita_waga'] > max_weight:
        nadwaga = harmonia['calkowita_waga'] - max_weight
        penalty = nadwaga * 2
        harmonia['fitness_score'] -= penalty
        
    if harmonia['zajete_sloty'] > max_slots:
        nadmiar_slotow = harmonia['zajete_sloty'] - max_slots
        penalty = nadmiar_slotow * 5
        harmonia['fitness_score'] -= penalty

def InitializeHarmonyMemory(HMS, focus_stat, max_weight=100.0):
    HM = []
    for i in range(HMS):
        harmonia = RandomSolution.RandomSolution("przedmioty.csv")
        CalculateFitnessScore(harmonia, focus_stat)
        ImplementPenalty(harmonia, max_weight)
        HM.append(harmonia)
    return HM

def HarmonySearch(focus_stat, max_weight, max_slots):
    HMS = 25
    HMCR = 0.7
    NI = 10000
    r1 = random.randint(1,100)/100
    HM = InitializeHarmonyMemory(HMS, focus_stat, max_weight)
    NewSolution = {}

    for iteration in range(NI):
        if r1 < HMCR:
            # losowanie nowego rozwiazania z losowych wartosci kolumn HM
            NewSolution = {}
            for key in HM[0].keys():
                NewSolution[key] = HM[random.randint(0, HMS-1)][key]
        else:
            NewSolution = HM[random.randint(0, HMS-1)]
        CalculateFitnessScore(NewSolution, focus_stat)
        ImplementPenalty(NewSolution, max_weight, max_slots)
        # porownanie NewSolution z najgorszym rozwiazaniem w HM
        HM.sort(key=lambda x: x['fitness_score'], reverse=True)
        if NewSolution['fitness_score'] > HM[-1]['fitness_score']:
            HM[-1] = NewSolution
    best = HM[0]
    armor = best.get('zbroja', {})
    backpack = best.get('plecak', [])

    print("Najlepsze rozwiazanie:")
    print(f"  Fitness: {best.get('fitness_score')}")
    print(f"  Calkowita waga: {best.get('calkowita_waga')}")
    print(f"  Zajete sloty: {best.get('zajete_sloty')}")
    print("  Zbroja:")
    for slot, item in armor.items():
        if item.get('id') is None:
            print(f"    - {slot}: (pusty)")
        else:
            print(f"    - {slot}: id={item.get('id')}, waga={item.get('waga_kg')}, pancerz={item.get('pancerz')}, zdrowie={item.get('zdrowie')}, mana={item.get('mana')}, obrazenia={item.get('obrazenia')}")
    print(f"  Plecak ({len(backpack)}):")
    for item in backpack:
        ilosc = item.get('wylosowana_ilosc', 1)
        print(f"    - id={item.get('id')}, ilosc={ilosc}, waga={item.get('waga_kg')}, pancerz={item.get('pancerz')}, zdrowie={item.get('zdrowie')}, mana={item.get('mana')}, obrazenia={item.get('obrazenia')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorytm Harmony Search dla problemu plecakowego.")
    parser.add_argument("-f", "--focus", type=str, default='pancerz', help="Statystyka, na której skupia się algorytm (domyślnie 'pancerz').")
    parser.add_argument("-w", "--max-weight", type=float, default=100.0, help="Maksymalna waga plecaka (domyślnie 100.0).")
    parser.add_argument("-s", "--max-slots", type=int, default=20, help="Maksymalna liczba zajętych slotów w plecaku (domyślnie 20).")
    args = parser.parse_args()

    HarmonySearch(focus_stat=args.focus, max_weight=args.max_weight, max_slots=args.max_slots)
    

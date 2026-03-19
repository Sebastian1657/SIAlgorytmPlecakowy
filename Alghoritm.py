import random
import RandomSolution
from DataConvertion import load_csv

def CalculateFitnessScore(harmonia: dict, focus_stat: str) -> float:
    stats = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    
    if focus_stat not in stats:
        raise ValueError(f"Nieznana statystyka: {focus_stat}. Dostępne: {stats}")

    # Definicja mnożników (można je później przenieść do konfiguracji globalnej)
    WAGA_GLOWNA = 0.5
    WAGA_POBOCZNA = 0.6
    
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
            mnoznik = WAGA_GLOWNA if statystyka == focus_stat else WAGA_POBOCZNA/(len(stats)-1)
            # Mnożymy wartość statystyki przez ilość sztuk w stacku i przez wagę
            calkowity_wynik += (item.get(statystyka, 0) * ilosc) * mnoznik
            
    # Zapis w strukturze dla łatwiejszego sortowania
    harmonia['fitness_score'] = round(calkowity_wynik, 2)
    
    return harmonia['fitness_score']

def ImplementPenalty(harmonia: dict, max_weight: float, max_slots: int) -> None:
    if harmonia['calkowita_waga'] > max_weight:
        nadwaga = harmonia['calkowita_waga'] - max_weight
        penalty = nadwaga
        harmonia['fitness_score'] -= penalty
        
    if harmonia['zajete_sloty'] > max_slots:
        nadmiar_slotow = harmonia['zajete_sloty'] - max_slots
        penalty = nadmiar_slotow * 2
        harmonia['fitness_score'] -= penalty

def BuildPlayerStats(harmonia: dict) -> dict:
    stats = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    totals = {stat: 0 for stat in stats}

    for item in harmonia['zbroja'].values():
        if item.get('id') is not None:
            for stat in stats:
                totals[stat] += item.get(stat, 0)

    for item in harmonia['plecak']:
        ilosc = item.get('wylosowana_ilosc', 1)
        for stat in stats:
            totals[stat] += item.get(stat, 0) * ilosc

    return totals

def InitializeHarmonyMemory(HMS, focus_stat, max_weight=100.0, max_slots=20, items_file="przedmioty.csv"):
    HM = []
    for i in range(HMS):
        harmonia = RandomSolution.RandomSolution(items_file, max_slots)
        CalculateFitnessScore(harmonia, focus_stat)
        ImplementPenalty(harmonia, max_weight, max_slots)
        HM.append(harmonia)
    return HM

def HarmonySearch(focus_stat, max_weight, max_slots, items_file="przedmioty.csv"):
    HMS = 25
    HMCR = 0.7
    NI = 50000
    items = load_csv(items_file)
    HM = InitializeHarmonyMemory(HMS, focus_stat, max_weight, max_slots, items)
    NewSolution = {}

    for iteration in range(NI):
        r1 = random.random()
        if r1 < HMCR:
            # losowanie nowego rozwiazania z losowych wartosci kolumn HM
            NewSolution = {}
            for key in HM[0].keys():
                NewSolution[key] = HM[random.randint(0, HMS-1)][key]
        else:
            NewSolution = RandomSolution.RandomSolution(items, max_slots)
        CalculateFitnessScore(NewSolution, focus_stat)
        ImplementPenalty(NewSolution, max_weight, max_slots)
        # porownanie NewSolution z najgorszym rozwiazaniem w HM
        HM.sort(key=lambda x: x['fitness_score'], reverse=True)
        if NewSolution['fitness_score'] > HM[-1]['fitness_score']:
            HM[-1] = NewSolution
    best = HM[0]
    best['player_stats'] = BuildPlayerStats(best)
    best['focus_stat'] = focus_stat
    return best

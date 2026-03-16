import RandomSolution

def CalculateFitnessScore(harmonia: dict, focus_stat: str) -> float:
    stats = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    
    if focus_stat not in stats:
        raise ValueError(f"Nieznana statystyka: {focus_stat}. Dostępne: {stats}")

    # Definicja mnożników (można je później przenieść do konfiguracji globalnej)
    WAGA_GLOWNA = 1.0
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
            mnoznik = WAGA_GLOWNA if statystyka == focus_stat else WAGA_POBOCZNA
            # Mnożymy wartość statystyki przez ilość sztuk w stacku i przez wagę
            calkowity_wynik += (item.get(statystyka, 0) * ilosc) * mnoznik
            
    # Zapis w strukturze dla łatwiejszego sortowania
    harmonia['fitness_score'] = round(calkowity_wynik, 2)
    
    return harmonia['fitness_score']

def HarmonySearch():
    HMS = 50
    HMCR = 0.7
    NI = 25000
    HM = []
    for i in range(HMS):
        HM.append(RandomSolution())
    
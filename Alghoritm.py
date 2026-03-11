import RandomSolution

def CalculateFitnessScore(harmonia, stat):
    stats = ['pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    if stat not in stats:
        raise ValueError(f"Nieznana statystyka: {stat}. Dostępne statystyki: {stats}")
    
    if stat == 'pancerz':
        return sum([item['pancerz'] for item in harmonia['zbroja'].values()])
    elif stat == 'zdrowie':
        return sum([item['zdrowie'] for item in harmonia['zbroja'].values()])
    elif stat == 'mana':
        return sum([item['mana'] for item in harmonia['zbroja'].values()])
    elif stat == 'obrazenia':
        return sum([item['obrazenia'] for item in harmonia['zbroja'].values()])
    # Prosty model oceny - można rozbudować o inne czynniki
    fitness_score = pancerz * 0.4 + zdrowie * 0.3 + mana * 0.2 + obrazenia * 0.1
    
    return fitness_score;

def HarmonySearch():
    HMS = 50
    HMCR = 0.7
    NI = 25000
    HM = []
    for i in range(HMS):
        HM.append(RandomSolution())
    
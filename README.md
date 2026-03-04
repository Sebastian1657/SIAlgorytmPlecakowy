# Projekt na przedmiot Sztuczna inteligencja
Problem optymalizacji ekwipunku gracza to Wielowymiarowy Problem Plecakowy z Wielokrotnym Wyborem (Multi-dimensional Multiple-choice Knapsack Problem - MMKP).
Polega na alokacji zasobów (przedmiotów) do zdefiniowanych struktur (slotów) w celu maksymalizacji wybranej metryki docelowej, pod rygorem ograniczeń przestrzennych i wagowych.

Parametry problemu:
Funkcja celu: Maksymalizacja całkowitej wartości punktowej zestawu. Wartość to ważona suma statystyk (pancerz, zdrowie, obrażenia, mana), determinowana przez wybrany priorytet gracza.

Struktury wyboru:
- Zbroja (MCKP): 5 rozłącznych zbiorów (głowa, korpus, nogi, buty, rękawice). Wymagany wybór dokładnie 1 elementu (lub domyślnego wariantu pustego) z każdego zbioru.
- Plecak: Pula elementów (broń, przedmioty jednorazowe) ograniczona twardym limitem 20 miejsc. Przedmioty jednorazowe są paczkowane do maksymalnie 5 sztuk na 1 miejsce w plecaku.

Ograniczenie globalne:
Całkowita masa (kg) wybranych elementów zbroi oraz zawartości plecaka nie może przekroczyć maksymalnego udźwigu postaci.

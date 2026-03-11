import argparse
import csv
import random

def generate_items(num_records: int, filename: str):
    num_armor = int(num_records * 0.20)
    num_backpack = num_records - num_armor
    num_weapons = int(num_backpack * 0.50)
    num_consumables = num_backpack - num_weapons

    armor_slots = ['Glowa', 'Korpus', 'Nogi', 'Buty', 'Rekawice']
    items = []
    current_id = 1

    # Generowanie zbroi (20%)
    for _ in range(num_armor):
        slot = random.choice(armor_slots)
        weight = round(random.uniform(1.0, 15.0), 2)
        armor = random.randint(5, 50)
        health = random.randint(0, 20)
        charisma = random.randint(0, 5)
        
        items.append([current_id, f"{slot}_Typ_{random.randint(1, 100)}", 'Zbroja', slot, weight, False, armor, health, 0, 0, charisma])
        current_id += 1

    # Generowanie broni (40%)
    for _ in range(num_weapons):
        weight = round(random.uniform(2.0, 10.0), 2)
        damage = random.randint(10, 100)
        mana = random.randint(0, 30)
        charisma = random.randint(0, 10)
        
        items.append([current_id, f"Bron_Typ_{random.randint(1, 100)}", 'Bron', 'Bron', weight, False, 0, 0, mana, damage, charisma])
        current_id += 1

    # Generowanie przedmiotów użytkowych (40%)
    for _ in range(num_consumables):
        weight = round(random.uniform(0.1, 0.5), 2)
        health = random.randint(0, 50) if random.random() > 0.5 else 0
        mana = random.randint(0, 50) if health == 0 else random.randint(0, 10)
        
        items.append([current_id, f"Mikstura_Typ_{random.randint(1, 100)}", 'Przedmiot_Uzytkowy', 'Brak', weight, True, 0, health, mana, 0, 0])
        current_id += 1

    # Zapis do CSV
    headers = ['id', 'nazwa', 'kategoria', 'slot', 'waga_kg', 'stackowalny', 'pancerz', 'zdrowie', 'mana', 'obrazenia', 'charyzma']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(items)

    print(f"Wygenerowano {len(items)} rekordów i zapisano do pliku {filename}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generowanie danych testowych do problemu plecakowego.")
    parser.add_argument("-n", "--number", type=int, default=200, help="Liczba rekordów do wygenerowania (domyślnie 200).")
    parser.add_argument("-o", "--output", type=str, default="przedmioty.csv", help="Nazwa pliku wyjściowego (domyślnie przedmioty.csv).")
    
    args = parser.parse_args()
    generate_items(args.number, args.output)
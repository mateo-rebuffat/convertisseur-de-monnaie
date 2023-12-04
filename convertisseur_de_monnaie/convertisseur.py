from forex_python.converter import CurrencyRates
import json
from datetime import datetime

def get_exchange_rate(base_currency, target_currency):
    c = CurrencyRates()
    try:
        rate = c.get_rate(base_currency, target_currency)
        return rate
    except:
        return None

def convert_currency(value, base_currency, target_currency, custom_rates):
    # Vérifier si le taux de conversion personnalisé existe
    if (base_currency, target_currency) in custom_rates:
        rate = custom_rates[(base_currency, target_currency)]
    else:
        rate = get_exchange_rate(base_currency, target_currency)

    if rate is not None:
        converted_value = value / rate
        return converted_value
    else:
        return None

def save_conversion_to_history(value, base_currency, target_currency, converted_value):
    conversion_history = load_conversion_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversion_record = {
        "timestamp": timestamp,
        "value": value,
        "base_currency": base_currency,
        "target_currency": target_currency,
        "converted_value": converted_value
    }
    conversion_history.append(conversion_record)
    with open('conversion_history.json', 'w') as file:
        json.dump(conversion_history, file)

def load_conversion_history():
    try:
        with open('conversion_history.json', 'r') as file:
            conversion_history = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        conversion_history = []
    return conversion_history

def main():
    print("Bienvenue dans le convertisseur de devises!")

    # Définir un dictionnaire pour stocker les taux de conversion personnalisés
    custom_rates = {}

    while True:
        value = float(input("Entrez la valeur à convertir : "))
        base_currency = input("Entrez la devise d'origine (par exemple, USD) : ").upper()
        target_currency = input("Entrez la devise cible (par exemple, EUR) : ").upper()

        converted_value = convert_currency(value, base_currency, target_currency, custom_rates)

        if converted_value is not None:
            print(f"{value} {base_currency} équivaut à {converted_value:.2f} {target_currency}")
            save_conversion_to_history(value, base_currency, target_currency, converted_value)
        else:
            print("Impossible d'effectuer la conversion. Vérifiez les devises fournies.")

        # Demander à l'utilisateur s'il souhaite ajouter un taux de conversion personnalisé
        add_custom_rate = input("Voulez-vous ajouter un taux de conversion personnalisé? (Oui/Non) : ").strip().lower()

        if add_custom_rate == "oui":
            custom_rate = float(input(f"Entrez le taux de conversion personnalisé pour {base_currency} vers {target_currency} : "))
            custom_rates[(base_currency, target_currency)] = custom_rate
            print(f"Taux de conversion personnalisé ajouté avec succès!")

        # Demander à l'utilisateur s'il souhaite effectuer une autre conversion
        another_conversion = input("Voulez-vous effectuer une autre conversion? (Oui/Non) : ").strip().lower()

        if another_conversion != "oui":
            break

if __name__ == "__main__":
    main()

__author__  = "Dmytro"
__version__ = "1.0.0"
__email__   = "dmytro.malanchuk@elev.ga.ntig.se"

import csv
import locale
import os
from colors import bcolors

# Represent a product
class Product:
    def __init__(self, product_id, name, desc, price, quantity):
        self.id = product_id
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity

    def __str__(self):
        # Set maximum column widths
        id_width = 4
        name_width = 40
        desc_width = 40 
        price_width = 15
        quantity_width = 10

        # Format each field to a specific width
        id_str = str(self.id).ljust(id_width)
        name_str = self.name[:name_width].ljust(name_width)
        desc_str = (self.desc[:desc_width] + '...') if len(self.desc) > desc_width else self.desc.ljust(desc_width)
        price_str = locale.currency(self.price, grouping=True).rjust(price_width)
        quantity_str = str(self.quantity).rjust(quantity_width)

        return f"{id_str:<5} {name_str:<30} {desc_str:<50} {price_str:<15} {quantity_str:<10}"

    def full_description(self):
        return f"ID: {self.id}\nName: {self.name}\nDescription: {self.desc}\nPrice: {locale.currency(self.price, grouping=True)}\nQuantity: {self.quantity}"

# Manage the inventory
class Inventory:
    def __init__(self):
        self.products = []

    def load_data(self, filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    product_id=int(row['id']),
                    name=row['name'],
                    desc=row['desc'],
                    price=float(row['price']),
                    quantity=int(row['quantity'])
                )
                self.products.append(product)

    def get_products(self):
        return "\n".join(str(product) for product in self.products)

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [product for product in self.products if product.id != product_id]

    def update_product(self, product_id, field, new_value):
        product = self.get_product_by_id(product_id)
        if product:
            setattr(product, field, new_value)

    def save_data(self, filename):
        fieldnames = ['id', 'name', 'desc', 'price', 'quantity']
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products:
                writer.writerow({
                    'id': product.id,
                    'name': product.name,
                    'desc': product.desc,
                    'price': product.price,
                    'quantity': product.quantity
                })

    def get_next_id(self):
        if not self.products:
            return 1
        return max(product.id for product in self.products) + 1

# Funktion för att visa inventarielistan
def show_inventory_list(inventory):
    print("-----------------------------------------------------------------------------------------------------------------------------------")
    print(bcolors.YELLOW + "#     NAME                                     DESC                                                   PRICE               QUANTITY")
    print(bcolors.DEFAULT + "-----------------------------------------------------------------------------------------------------------------------------------")
    print(inventory.get_products())
    print("-----------------------------------------------------------------------------------------------------------------------------------")

# Funktion för att rensa skärmen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main program
if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

    inventory = Inventory()
    inventory.load_data('db_products.csv')

    while True:
        # Huvudmeny för att välja alternativ
        print("\nAlternativ: 'L' - Lägg till produkt | 'U' - Uppdatera produkt | 'T' - Ta bort produkt | 'V' - Visa lista | 'S' - Visa produktdetaljer | 'Q' - Avsluta programmet")

        choice = input("Ange ditt val: ").upper()

        if choice == 'Q':
            print("\nProgrammet avslutas.")
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
            break
        elif choice == 'L':
            try:
                new_id = inventory.get_next_id()
                new_name = input("Ange produktens namn: ")
                new_desc = input("Ange produktbeskrivning: ")
                new_price = float(input("Ange pris: "))
                new_quantity = int(input("Ange antal: "))

                new_product = Product(new_id, new_name, new_desc, new_price, new_quantity)
                inventory.add_product(new_product)
                inventory.save_data('db_products.csv')

                print("\nNy produkt har lagts till.")
                print("-----------------------------------------------------------------------------------------------------------------------------------")
            except ValueError:
                print("\nFelaktig inmatning, försök igen.")
                print("-----------------------------------------------------------------------------------------------------------------------------------")
        elif choice == 'U':
            try:
                product_id = int(input("Ange ID på produkten du vill uppdatera: "))
                product = inventory.get_product_by_id(product_id)

                if product:
                    print(f"\nUppdaterar produkt med ID {product_id}:")
                    field = input("Vilket fält vill du ändra? (name, desc, price, quantity): ").lower()
                    new_value = input(f"Nytt värde för {field}: ")

                    # Convert input to correct type.
                    if field == 'price':
                        new_value = float(new_value)
                    elif field == 'quantity':
                        new_value = int(new_value)

                    inventory.update_product(product_id, field, new_value)
                    inventory.save_data('db_products.csv')

                    print("\nProdukten har uppdaterats.")
                    print("-----------------------------------------------------------------------------------------------------------------------------------")
                else:
                    print("\nIngen produkt med det ID:t hittades.")
                    print("-----------------------------------------------------------------------------------------------------------------------------------")
            except ValueError:
                print("\nFelaktig inmatning, försök igen.")
                print("-----------------------------------------------------------------------------------------------------------------------------------")
        elif choice == 'T':
            try:
                product_id_to_remove = int(input("Ange ID på produkten du vill ta bort: "))
                product = inventory.get_product_by_id(product_id_to_remove)

                if product:
                    inventory.remove_product(product_id_to_remove)
                    inventory.save_data('db_products.csv')
                    print(f"\nProdukt med ID {product_id_to_remove} har tagits bort.")
                    print("---------------------------------------------------------------------------------------------------------------------------------------------")
                else:
                    print("\nIngen produkt med det ID:t hittades.")
                    print("---------------------------------------------------------------------------------------------------------------------------------------------")
            except ValueError:
                print("\nFelaktigt ID, försök igen.")
                print("---------------------------------------------------------------------------------------------------------------------------------------------")
        elif choice == 'V':
            show_inventory_list(inventory)
        elif choice == 'S':
            try:
                product_id = int(input("Ange ID på produkten du vill visa: "))
                product = inventory.get_product_by_id(product_id)

                if product:
                    clear_screen()
                    print("\nProduktdetaljer:")
                    print(product.full_description())
                    print("---------------------------------------------------------------------------------------------------------------------------------------------")
                else:
                    print("\nIngen produkt med det ID:t hittades.")
                    print("---------------------------------------------------------------------------------------------------------------------------------------------")
            except ValueError:
                print("\nFelaktig inmatning, försök igen.")
                print("---------------------------------------------------------------------------------------------------------------------------------------------")
        else:
            print("\nOgiltigt val, försök igen.")
            print("---------------------------------------------------------------------------------------------------------------------------------------------")
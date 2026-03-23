balance = 0.0
warehouse_Item = {}
history = []

with open("dbfile.txt", "r") as file:
    lines = file.readlines()

if len(lines) > 0:
    for line in lines:
        line = line.strip()
        if line.startswith("BAL:"):
            balance = float(line.replace("BAL:", ""))
        elif line.startswith("INV:"):
            # Formato INV:nome,prezzo,quantità
            parts = line.replace("INV:", "").split(",")
            # parts[0]=nome, parts[1]=prezzo, parts[2]=quantità
            warehouse_Item[parts[0]] = [float(parts[1]), int(parts[2])]
        elif line.startswith("HIS:"):
            history.append(line.replace("HIS:", ""))

command = ["balance", "sale", "purchase", "account", "list", "warehouse", "review", "end"]

while True:

    print(f"Comand: {', '.join(command)}")
    insert_command = input("Insert Command: ").strip().lower()

    if insert_command == "end":
        with open("dbfile.txt", "w") as file:
            file.write(f"BAL:{balance}\n")
            for product in warehouse_Item:
                p_info = warehouse_Item[product]
                file.write(f"INV:{product},{p_info[0]},{p_info[1]}\n")
            for event in history:
                file.write(f"HIS:{event}\n")
        break

    elif insert_command == "balance":
        value = input("Insert amount to Add or subtract: ")


        check_number = value
        if value.startswith('-'):
            check_number = value[1:]


        is_valid = False
        if check_number.count('.') == 1:
            segment = check_number.split('.')
            if segment[0].isdigit() and segment[1].isdigit():
                is_valid = True
        elif check_number.isdigit():
            is_valid = True

        if is_valid:
            amount = float(value)
            balance += amount
            history.append(f"Balance update: {amount}")
        else:
            print("Error: Insert a correct value.")

    elif insert_command == "sale":
        product = input("Product name: ")
        price_in = input("Selling Price: ")
        quantity_in = input("Quantity: ")

        is_price_valid = False
        price_segments = price_in.split('.')

        if len(price_segments) == 1 and price_in.isdigit():
            is_price_valid = True
        elif len(price_segments) == 2 and price_segments[0].isdigit() and price_segments[1].isdigit():
            is_price_valid = True
            is_quantity_valid = quantity_in.isdigit()

        if is_price_valid and is_quantity_valid:
            price = float(price_in)
            quantity = int(quantity_in)

            if price < 0 or quantity < 0:
                print("Error: Insert a correct value.")
            elif product in warehouse_Item and warehouse_Item[product][1] >= quantity:
                warehouse_Item[product][1] -= quantity
                balance += (price * quantity)
                history.append(f"Sold: {product} x{quantity}")
            else:
                print("Errore: Product not in stock.")
        else:
            print("Error: Insert a correct value.")


    elif insert_command == "purchase":

        product = input("select Product: ")
        price_in = input("price: ")
        quantity_in = input("Quantity: ")

        price_segments = price_in.split('.')
        is_price_valid = False

        if len(price_segments) == 1 and price_segments[0].isdigit():
            is_price_valid = True

        elif len(price_segments) == 2 and price_segments[0].isdigit() and price_segments[1].isdigit():
            is_price_valid = True
        if is_price_valid and quantity_in.isdigit():

            price = float(price_in)
            quantity = int(quantity_in)
            total = price * quantity

            if price < 0 or quantity < 0:

                print("Error: Insert a correct value.")

            elif balance >= total:
                balance -= total

                if product in warehouse_Item:
                    warehouse_Item[product][1] += quantity

                else:
                    warehouse_Item[product] = [price, quantity]

                history.append(f"Purchase: {product} x{quantity}")
            else:
                print("Error: insufficient balance.")
        else:
            print("Error: Insert a correct value.")

    elif insert_command == "account":
        print(f"Balance: {balance}")

    elif insert_command == "list":
        print("List of products:")
        for product_name in warehouse_Item:
            print(f"- {product_name}: Price {warehouse_Item[product_name][0]}, Quantity {warehouse_Item[product_name][1]}")

    elif insert_command == "warehouse":
        Searched = input("search product: ")
        if Searched in warehouse_Item:
            print(f"details {Searched}: Price {warehouse_Item[Searched][0]}, Quantity {warehouse_Item[Searched][1]}")
        else:
            print("Errore: Inserisci un valore corretto.")

    elif insert_command == "review":
        From = input("From (indice): ")
        To = input("to (indice): ")

        if (From == "" or From.isdigit()) and (To == "" or To.isdigit()):
            idx_From = int(From) if From else 0
            idx_To = int(To) if To else len(history)

            if idx_From < 0 or idx_To > len(history) or idx_From > idx_To:
                print("Error: Insert a valid value.")
            else:
                for i in range(idx_From, idx_To):
                    print(f"{i}: {history[i]}")
        else:
            print("Error: Insert a valid value.")

    else:
        print("Error: Insert a valid value.")

print("Good bye!")
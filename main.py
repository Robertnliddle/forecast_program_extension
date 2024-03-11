import json
import os.path


class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, name):
        def wrapper(func):
            self.actions[name] = func

        return wrapper

    def execute(self, name, inventory, balance, history):
        if name not in self.actions:
            print(f"Error: {name} not in actions")
        else:
            return self.actions[name](inventory, balance, history)


def load_warehouse():
    if not os.path.exists("warehouse.json"):
        return {}
    with open("warehouse.json") as f:
        warehouse = json.load(f)
    return warehouse


def save_warehouse(warehouse):
    with open("warehouse.json", "w") as f:
        json.dump(warehouse, f)


def load_history():
    if not os.path.exists("history.json"):
        return []
    with open("history.json") as f:
        history = json.load(f)
    return history


def save_history(history):
    with open("history.json", "w") as f:
        json.dump(history, f)


def load_balance():
    if not os.path.exists("balance.json"):
        return 0
    with open("balance.json") as f:
        balance = json.load(f)
    return balance


def save_balance(balance):
    with open("balance.json", "w") as f:
        json.dump(balance, f)


balance = load_balance()
warehouse = load_warehouse()
history = load_history()
manager = Manager()


@manager.assign("balance")
def perform_balance(balance, history, warehouse):
    actions = input("add or subtract): ")
    value = int(input("Value: "))
    if actions == "add":
        balance += value
    elif actions == "subtract":
        if balance - value < 0:
            print("No money can be subtracted")
            return balance, history, warehouse
        balance -= value
        history.append(f"action: balance, cmd: {actions}, {value}")

        return balance, history, warehouse


@manager.assign("sale")
def perform_history(balance, history, warehouse):
    product_name = input("Enter the products name: ")
    price = int(input("Enter the price: "))
    quantity = int(input("Enter the quantity sold: "))
    if product_name in warehouse:
        if quantity <= warehouse[product_name]:
            total_price = price * quantity
            balance += total_price
            warehouse[product_name] -= quantity
            print(f"Products sold:{product_name},Quantity:{quantity}")
            history.append(product_name)
    else:
        print("Product not found in the warehouse or the quantity is not enough")

        return balance, history, warehouse


@manager.assign("purchase")
def perform_warehouse(balance, history, warehouse):
    product_name = input("Enter the name of the product: ")
    price = int(input("Enter the price: "))
    quantity = int(input("Enter the quantity: "))
    total_price = price * quantity
    if total_price > balance:
        print("You have to low balance in your account")
        balance -= total_price
        print(f"You purchase {product_name}{quantity} items for {total_price}")
        if product_name not in warehouse:
            warehouse[product_name] = 0
            warehouse[product_name] += quantity
            history.append(product_name)

            return balance, history, warehouse


@manager.assign("sale")
def perform_sale(balance, history, warehouse):
    product_name = input("Enter the products name: ")
    price = int(input("Enter the price: "))
    quantity = int(input("Enter the quantity sold: "))
    if product_name in warehouse:
        if quantity <= warehouse[product_name]:
            total_price = price * quantity
            balance += total_price
            warehouse[product_name] -= quantity
            print(f"Products sold:{product_name},Quantity:{quantity}")
            history.append(product_name)
    else:
        print("Product not found in the warehouse or the quantity is not enough")

        return balance, history, warehouse


@manager.assign("account")
def perform_account(balance, history, warehouse):
    print(f"Current account balance is: {balance} ")

    return balance, history, warehouse


@manager.assign("account")
def perform_warehouse_list(balance, history, warehouse):
    for product_name, quantity in warehouse.items():
        print(f"{product_name}: {quantity}")

    return balance, history, warehouse


@manager.assign("warehouse")
def perform_warehouse(balance, history, warehouse):
    product_name = input("Enter the products name: ")
    if product_name in warehouse:
        print(f"{product_name} is available at the warehouse: {warehouse[product_name]}")
    else:
        print(f"The product name you are looking for are not in the warehouse")

        return balance, history, warehouse


@manager.assign("review")
def perform_review(balance, history, warehouse):
    first_index = int(input("Enter the first index: "))
    second_index = int(input("Enter the second index: "))
    for entry in history[first_index:second_index]:
        print(entry)
    else:
        print(f"The command are not supported {action}. Please select another command.")

        return balance, history, warehouse


commands_list_msg = """Select a command: 
- balance: add or subtract from the account
- sale: name of product, quantity and update the warehouse accordingly
- purchase: name of the product, its price, quantity and update to warehouse and account
- account: display the current account balance
- warehouse_list: display the total inventory in the warehouse along with products prices and quantities
- warehouse: display a product and its status in the warehouse
- review: Review the history
- end: exit the program"""

commands_add_sub_msg = """Select if you want to add or subtract to the balance
- add 
- subtract"""

while True:
    print(commands_list_msg)
    action = input("Select a command: ")
    print("Selected command: ", action)
    if action == "end":
        print("Exiting the program...")
        break

    elif action == "balance":
        print(commands_add_sub_msg)
        balance, history, warehouse = manager.execute("balance", balance, warehouse, history)

    elif action == "sale":
        balance, history, warehouse = manager.execute("sale", balance, warehouse, history)

    elif action == "purchase":
        balance, history, warehouse = manager.execute("purchase", balance, warehouse, history)

    elif action == "account":
        balance, history, warehouse = manager.execute("account", balance, warehouse, history)

    elif action == "warehouse_list":
        balance, history, warehouse = manager.execute("warehouse_list", balance, warehouse, history)

    elif action == "warehouse":
        balance, history, warehouse = manager.execute("warehouse", balance, warehouse, history)

    elif action == "review":
        balance, history, warehouse = manager.execute("review", balance, warehouse, history)

save_balance(balance)
save_history(history)
save_warehouse(warehouse)

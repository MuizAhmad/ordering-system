import bcrypt
import random
import csv

"""Project 1, Mcmaster 2025
400643031, Ahmam47
400593338, houy767
400600259, espinc1
400620274, hajyounl
Warehouse ordering system. The main goal of this code system is to be able to implement a warehouse ordering that authenticates users, process orders and packs the products, log orders, and generates customer summaries. """


def main():
    """
    Runs the warehouse ordering system. Begins by welcoming the user, then calls authenticate to obtain a userid, then asks the user if they want to make an order. If input is 'Y' meaning 'yes' the scan_barcode function will scan the desired order and then the functions lookup_products, pack_products, and complete_order is called to complete the order. The user is then prompted to make another order as many times as they want. If the user inputs 'N' meaning 'no'. The function customer_summary is called to give a personal summary of the orders the user has made.

    Parameters:
        None
    Input:
        user input, barcode scanner input
    Output:
        receipts, summaries, Q-Arm actions, invalid entries
    Return Value:
        None
    """
    def ask_order():
        """
        Helper function used to avoid repetition in the code. Asks the user for an input (str) to make an order.
        """
        return input("\nWould you like to make an order? (Y/N): ").strip().upper()
        # ".strip().upper()" removes any spaces in the input and makes it uppercase in case the user inputted a space or gave input in lowercase

    print("===================================")
    print("      WAREHOUSE ORDER SYSTEM")
    print("===================================\n")

    print("Welcome, user! Please login below.\n")
    # userid value is required as an argument for complete_order and customer_summary functions
    userid = authenticate()

    print(f"\nWelcome, {userid}!")

    order = ask_order()

    while True:

        if order == "Y":

            # obtains a string of products needed as an argument for lookup_products function
            products = scan_barcode()

            # convert products into nested lists using products.csv: [[name, price], ...]. product_list is needed as an argument for pack_products and complete_order functions
            product_list = lookup_products(products)

            pack_products(product_list)

            complete_order(userid, product_list)

            # Ask the user if they want to make another order
            order = ask_order()

            # If user does not want to order, call customer_summary and end the program
        elif order == "N":
            print("\nHere is your customer summary...")
            customer_summary(userid)
            print("\nThank you for using the Warehouse Ordering System!")
            break  # ends program

        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            order = ask_order()


def sign_up():
    """
    Stores a userid and password in "users.csv" only if the user inputs a valid password. Function is called from authenticate() only if the user answers 'N' when asked if they have an account. A valid password contains one of the symbols in the symbol list, a capital letter, a lowercase letter, a number and has to be atleast 6 characters long. The password is then encrypted using hashing and stored into "users.csv".

    Parameters:
        None
    Input:
        userid, password
    Output:
        invalid entries, successful signup
    Return Value:
        None

    """

    print("\n-------Sign Up----------")

    symbols = ["!", ".", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "[", "]"]

    while True:

        userid = str(input("\nCreate your own userID: "))

        userid_file = open("users.csv", "r")

        unique_id = True

        for line in userid_file:
            if line.strip() == "":
                continue

            user_list = line.strip().split(",")

            if user_list[0] == userid:
                unique_id = False
                print("\nUser already exists. Try Again!")
                break

        userid_file.close()

        if unique_id == True:
            break

    while True:

        password = input("Create your password: ")

        has_upper = False
        has_lower = False
        has_digit = False
        has_symbol = False

        if len(password) < 6:
            print("Password must be at least 6 characters.")
            continue

        for i in password:

            if i >= 'A' and i <= 'Z':
                has_upper = True

            elif i >= 'a' and i <= 'z':
                has_lower = True

            elif i >= '0' and i <= '9':
                has_digit = True

            elif i in symbols:
                has_symbol = True

        if has_upper and has_lower and has_digit and has_symbol:

            userid_file = open("users.csv", "a")
            hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            userid_file.write(userid + "," + hash + "\n")
            userid_file.close()

            print("\nSign Up Successful")
            break

        else:
            print("Password must have at least:\n - 1 lowercase letter\n - 1 uppercase letter\n - 1 digit\n - 1 symbol (!.@#$%^&*()_[])")

def authenticate():
    """
    Logs the user into the system. Starts by asking the user if they have an account. If the user input "N" meaning "no", the function sign_up is called to allow the user to create an account. If the user inputs "Y" meaning "yes", the user is prompted to sign in by inputing their userid and password. If the input matches the values stored in "users.csv", the login is successful.

    Parameters:
        None
    Input:
        user credentials, users.csv
    Output:
        success or failure message
    Return Value:
        userid (str)

    """

    print("--------Login--------")

    # Ask the user if they already have an account
    while True:
        has_account = input("\nDo you have an account? (Y/N): ").strip().upper()

        if has_account == "Y":
            break
        elif has_account == "N":
            sign_up()
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    # Begin authentication loop
    while True:
        userid = input("\nEnter your userid: ").strip()
        password = input("Enter your password: ").strip()

        # Read users.csv to find matching userid
        try:
            file = open("users.csv", "r")
        except FileNotFoundError:
            print("ERROR: users.csv not found.")
            continue

        user_found = False
        correct_login = False

        for line in file:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(",")
            stored_userid = parts[0].strip()
            hash = parts[1].strip()

            if userid == stored_userid:   # userid exists
                user_found = True

                # check password
                if bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8')):
                    correct_login = True
                break

        file.close()

        if user_found == False:
            print("\nUserid not found. Please try again.")
            continue

        if correct_login == False:
            print("\nIncorrect password. Please try again.")
        else:
            print("\nLogin successful.")
            return userid


def lookup_products(products):
    """
    This function uses the return value from scan_barcode which is a string of product names for the order and compares it to the products in "products.csv" to determine which products exist in the database. Returns a list of products with prices that matches a scanned list. Products not found in "products.csv" are skipped and a warning message is printed to the console.

    Parameters:
        products (str)
    Input:
        products.csv file contents
    Output:
        Warning message if product not found
    Return Value:
        product_list
    """
    # Empty list to store product name and price from products.csv
    csv_products = []

    file = open("products.csv", "r")
    for line in file:
        line = line.strip()

        # skip empty lines
        if line == "":
            continue

        parts = line.split(",") # ["product_name", "price"]

        # make sure the list has both name and price
        if len(parts) < 2:
            continue # skips invalid lists

        name = parts[0].strip()       # product name
        price_text = parts[1].strip() # remove any extra spaces

        # convert price to a number or skip if invalid
        try:
            price = float(price_text)
        except ValueError:
            print("Warning: invalid price for product '" + name + "' in CSV. Skipping.")
            continue

        # add product (str) and price (float) to the empty list
        csv_products.append([name, price])

    file.close()

    # turn the argument (products) into a list of product names
    names = products.split(",")
    product_list = []  # needed for return list [[name, price], ...]

    for n in names: # for each product given in the argument
        n = n.strip() # removes spaces
        product_exists = False

        # check if product from argument exists in products.csv
        for item in csv_products:
            product_name, product_price = item[0], item[1]

            if product_name.lower() == n.lower():
                product_list.append([product_name, product_price])
                product_exists = True
                break

        # if product not found, show warning
        if product_exists == False:
            print("Warning: product '" + n + "' not found in products.csv.")

    return product_list

def pack_products(product_list):
    """
    Controls the Q-Arm robotic arm to physically place products into the packing zone based on the scanned list. It accepts the return value from the lookup_products function as its parameter.

    Parameters:
        product_list
    Input:
        None
    Output:
        Q-Arm motor commands. Printed messages confirming that a product was packed.
    Return Value:
        None
    """

## INPUT Q-ARM COMMANDS HERE
    def pack_sponge():
        """
        Controls the Q-Arm and end effector model to place product 'Sponge' into the packing zone
        """
        arm.rotate_base(16)
        sleep(2)
        arm.rotate_elbow(-5)
        sleep(2)
        arm.rotate_gripper(-20)
        sleep(2)
        arm.rotate_shoulder(42)
        sleep(2)
        arm.rotate_gripper(80)
        sleep(2)
        arm.rotate_shoulder(-42)
        sleep(2)
        arm.rotate_base(-60)
        sleep(2)
        arm.rotate_elbow(30)
        sleep(2)
        arm.rotate_gripper(-80)
        sleep(2)
        arm.rotate_gripper(80)

    def pack_bottle():
        """
        Controls the Q-Arm and end effector model to place product 'Bottle' into the packing zone
        """
        arm.home()
        arm.rotate_base(10)
        sleep(2)
        arm.rotate_elbow(-4)
        sleep(2)
        arm.rotate_gripper(-8)
        sleep(2)
        arm.rotate_shoulder(43)
        sleep(2)
        arm.rotate_gripper(30)
        sleep(2)
        arm.rotate_shoulder(-43)
        sleep(2)
        arm.rotate_base(-60)
        sleep(2)
        arm.rotate_elbow(20)
        sleep(2)
        arm.rotate_gripper(-80)
        sleep(2)
        arm.rotate_gripper(80)

    def pack_rook():
        """
        Controls the Q-Arm and end effector model to place product 'Rook' into the packing zone
        """
        arm.home()
        arm.rotate_base(4)
        sleep(2)
        arm.rotate_elbow(-4)
        sleep(2)
        arm.rotate_gripper(-8)
        sleep(2)
        arm.rotate_shoulder(45)
        sleep(2)
        arm.rotate_gripper(30)
        sleep(2)
        arm.rotate_shoulder(-43)
        sleep(2)
        arm.rotate_base(-60)
        sleep(2)
        arm.rotate_elbow(30)
        sleep(2)
        arm.rotate_gripper(-90)
        sleep(2)
        arm.rotate_gripper(80)

    def pack_d12():
        """
        Controls the Q-Arm and end effector model to place product 'D12' into the packing zone
        """

    def pack_witchhat():
        """
        Controls the Q-Arm and end effector model to place product 'WitchHat' into the packing zone
        """

    def pack_bowl():
        """
        Controls the Q-Arm and end effector model to place product 'Bowl' into the packing zone
        """

    print("\n----- PACKING PRODUCTS -----")

    if len(product_list) == 0:
        print("\nNo valid products to pack.")
        return

    for product in product_list:
        name = product[0]

        print(f"\nPacking: {name}")

        if name == "Sponge":
            pack_sponge()
        elif name == "Bottle":
            pack_bottle()
        elif name == "Rook":
            pack_rook()
        elif name == "D12":
            pack_d12()
        elif name == "Witchhat":
            pack_witchhat()
        elif name == "Bowl":
            pack_bowl()
        else:
            print(f"\nWARNING: No product called '{name}'. Skipping...")
            continue

        print(f"\n{name} successfully packed")

    print("\nAll products packed successfully!")


def complete_order(userid, product_list):
    """
    This function totals up the order, applies a random discount (5% to 50%) using the random module, calculates tax, and writes the completed order to "orders.csv". The function then outputs a professionally formatted order invoice to complete the order and tells the user how many orders they have made so far.

    Parameters:
        userid (str), product_list
    Input:
        None
    Output:
        Printed invoice and order summary, updates orders.csv with each new order
    Return Value:
        None
    """
    subtotal = 0.0
    tax_rate = 0.13

    valid_products = []

    # going through each product in the list
    for item in product_list:

        # checking that the sublist has two elements [0,1]
        if len(item) != 2:
            continue

        name, price = item[0], item[1]

        # checking if the price is a number
        try:
            price = float(price)
        except ValueError:
            print("Warning: price for", name, "is invalid. Skipping the product.")
            continue

        valid_products.append([name, price])
        subtotal += price

    # checking for empty order
    if len(valid_products) == 0:
        print("Error: No valid products in order. Order could not be completed.")
        return

    # applying the random discount
    discount_percent = random.randint(5, 50)
    discount_rate = discount_percent / 100.0
    discount_amount = subtotal * discount_rate
    subtotal_after_discount = subtotal - discount_amount

    # calculating tax and total
    tax_amount = subtotal_after_discount * tax_rate
    total = subtotal_after_discount + tax_amount

    file = open("orders.csv", "a")

    # start with userid and total
    line = userid + "," + f"{total:.2f}"

    # now add all product names
    i = 0
    while i < len(valid_products):
        line += "," + valid_products[i][0]
        i += 1

    file.write(line + "\n")
    file.close()

    # counting how many orders the user has placed
    order_count = 0
    file = open("orders.csv", "r")

    line = file.readline()
    while line != "":
        parts = line.strip().split(",")
        # first element is userid
        if len(parts) >= 1 and parts[0] == userid:
            order_count += 1
        line = file.readline()

    file.close()

    # printing the receipt
    print("\n==============================")
    print("        WAREHOUSE RECEIPT")
    print("==============================")
    print("Customer:", userid)
    print("------------------------------")
    print("Item                 Price ($)")
    print("------------------------------")

    # printing each product
    i = 0
    while i < len(valid_products):
        name = valid_products[i][0]
        price = valid_products[i][1]
        print(f"{name:<20} {price:>10.2f}")
        i += 1

    print("------------------------------")
    print(f"Subtotal:             {subtotal:.2f}")
    print(f"Discount ({discount_percent}%):     -{discount_amount:.2f}")
    print(f"Subtotal after disc: {subtotal_after_discount:.2f}")
    print(f"Tax:                 {tax_amount:.2f}")
    print("==============================")
    print(f"TOTAL:               {total:.2f}")
    print("==============================")

    # final message

    print(f"\nThank you! This was order #{order_count} for userid '{userid}'.")

def customer_summary(userid):
    """
    This functions reads "orders.csv" and outputs a professionally formatted summary of all previous orders for the given userid. This includes the total number of orders, total spent, and a count of each unique product ordered.

    Parameters:
        userid (str)
    Input:
        orders.csv
    Output:
        Printed order history summary
    Return Value:
        None
    """
    # open the file and put every line into a list
    file = open("orders.csv", "r")

    lines = []
    for line in file:
        lines.append(line)

    file.close()

    no_of_orders = 0
    total_spent = 0.0
    min_valid_row = 3

    # lists to track unique products and how many times each was ordered
    products = []
    quantities = []

    i = 0

    # go through each row in orders.csv
    while i < len(lines):

        line = lines[i].strip()
        parts = line.split(",")

        # valid row must have userid, total, and at least one product
        if len(parts) >= min_valid_row:

            file_userid = parts[0].strip()
            total = parts[1].strip()

            # check if this row belongs to the user
            if file_userid == userid:
                no_of_orders += 1

                # convert total to float
                total_spent += float(total)

                # count the products in the order
                index = 2 # skips userid and total
                while index < len(parts):
                    product = parts[index].strip()

                    if product not in products:
                        # adds new products to the product list
                        products.append(product)
                        # adds new quantity for the product to quantity list
                        quantities.append(1)
                    else:
                        # add 1 to the index of the current quantity for that product
                        quantities[products.index(product)] += 1


                    index += 1

        i += 1

    # print professionally formatted summary
    print("\n===============================")
    print(f" CUSTOMER SUMMARY: {userid}")
    print("===============================")
    print(f"User: {userid}")
    print(f"Number of Orders: {no_of_orders}")
    print(f"Total Spent: ${total_spent:.2f}")
    print("-------------------------------")
    print("Products Ordered:")

    if no_of_orders == 0:
        print("No products ordered.")
        print("===============================")
        return

    index = 0
    while index < len(products):
        print(f"{products[index]} - {quantities[index]}")
        index += 1

    print("===============================")

main() # runs the warehouse order system whenever the program is ran
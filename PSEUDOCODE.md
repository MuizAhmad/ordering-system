# Pseudocode — Warehouse Ordering System

## Main Program Flow

1.  START — display welcome message
2.  CALL authenticate()
      IF user has no account → CALL sign_up()
        Prompt for unique userid
        Validate password (≥6 chars, upper, lower, digit, symbol)
        Hash password with bcrypt → write userid + hash to users.csv
      ELSE
        Prompt for userid + password
        Read users.csv, find matching userid, verify hashed password
        REPEAT until login succeeds
      RETURN userid

3.  Prompt user: "Make an order? (Y/N)"

4.  WHILE user wants to order:

5.    CALL scan_barcode()
        RETURN product name string (e.g. "Sponge,Bottle")

6.    CALL lookup_products(products)
        Read products.csv into list of [name, price]
        For each scanned product, find match in CSV (case-insensitive)
        Warn and skip if not found
        RETURN product_list [[name, price], ...]

7.    CALL pack_products(product_list)
        For each product, dispatch to its QArm routine
        Print packing confirmation per item

8.    CALL complete_order(userid, product_list)
        Sum prices → subtotal
        Apply random discount (5–50%)
        Calculate tax (13%) on discounted subtotal → compute total
        Append "userid, total, product1, product2, ..." to orders.csv
        Count user's total orders in orders.csv
        Print formatted receipt with itemized prices, discount, tax, total

9.    Prompt user: "Make another order? (Y/N)"

10.   IF "N" → EXIT loop
      IF invalid input → re-prompt

11. CALL customer_summary(userid)
      Read all rows from orders.csv
      Filter rows matching userid
      Accumulate order count, total spent, and per-product quantities
      Print formatted summary

12. Print farewell message → END

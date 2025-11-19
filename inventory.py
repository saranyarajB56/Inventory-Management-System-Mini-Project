import sqlite3
import datetime

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Supplier table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS supplier (
        sid INTEGER PRIMARY KEY AUTOINCREMENT,
        s_name VARCHAR(20),
        contact INTEGER
    )
''')

# Product table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        p_name VARCHAR(20),
        p_price DECIMAL,
        qty INTEGER,
        sid INTEGER,
        FOREIGN KEY (sid) REFERENCES supplier(sid)
    )
''')

# add column category
# cursor.execute("ALTER TABLE product ADD COLUMN category TEXT;")

# orders table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        oid INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT,
        status INTEGER,
        uid INTEGER,
        pid INTEGER,
        qty INTEGER,
        FOREIGN KEY (uid) REFERENCES users(uid),
        FOREIGN KEY (pid) REFERENCES product(pid)
    )
''')
        
conn.commit() 
conn.close()


def init_db():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin', 'staff')) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Registration ---
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/staff): ").lower()

    if role not in ['admin', 'staff']:
        print("Invalid role. Must be 'admin' or 'staff'.")
        return

    try:
        conn = sqlite3.connect("inventory.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        print("✅Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()

# --- Login ---
def login():
    username = input("Username: ")
    password = input("Password: ")

    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()
    cur.execute("SELECT uid, role FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    conn.close()

    if result:
        user_id, role = result
        print(f"\n🤝 Welcome, {username}! Role: {role}")
        if role == "admin":
           return admin_menu(user_id)
        elif role == "staff":
           return staff_menu(user_id)
    else:
        print("Invalid credentials.")

# --- Admin Functions ---
def admin_menu(user_id):
     while True:
        print('\n-----------------------------------------------')
        print('\n Welcome to Inventory Management System 😍')
        print('\n-----------------------------------------------')
        print('Please select your option :')
        ch = int(input('''
🧺 Product Management
---------------------                       
1. Add New Product
2. Remove Product
3. Edit Product
4. Search Product by ID
5  Search Product by Category                    
6. Print Inventory Report
7. Stock Alert                       

👥 Supplier Management
---------------------                       
8. Add Supplier
9. View All Suppliers
10. Search Supplier
11. Update Supplier
12. Remove Supplier 
                                                                   
🚛 Order Management
---------------------                                             
13. Order Product
14. View All Orders
15. Search Order
16. Update Order
17. Cancel Order
                       
👤 User Management
---------------------                       
18. Add User
19. View All Users
20. Search User
21. Update User
22. Remove User
23. Update username&Password
                       
❌ Exit
---------------------                                  
24.Exit
Choice: '''))

        if ch == 1:
            addnewproduct(user_id)  
        elif ch == 2:
            removeanitem(user_id)
        elif ch == 3:
            editproduct(user_id)  
        elif ch == 4:
            searchanitem(user_id) 
        elif ch == 5:
            search_products_by_category(user_id)
        elif ch == 6:
            printinventoryreport(user_id)
        elif ch == 7:
            product_quantity_alert(user_id)      
        elif ch == 8:
            addsupplier(user_id)  
        elif ch == 9:
            viewallsupplier(user_id)  
        elif ch == 10:
            viewsupplier(user_id) 
        elif ch == 11:
            updatesupplier(user_id)  
        elif ch == 12:
            removesupplier(user_id)  
        elif ch == 13:
            orderproduct(user_id)  
        elif ch == 14:
             view_all_orders(user_id)
        elif ch == 15:
             search_an_order(user_id)  
        elif ch == 16:
             update_order(user_id)  
        elif ch == 17:
            delete_an_order(user_id) 
        elif ch == 18:
            add_user(user_id)  
        elif ch == 19:
            view_all_users(user_id)
        elif ch == 20:
            search_user(user_id)  
        elif ch == 21:
            update_user(user_id)  
        elif ch == 22:
            remove_user(user_id)
        elif ch == 23:
           print('Admin: changing username & Password......')
           change_user_namepass(user_id)     
        elif ch == 24:
            print('\n--------------------------------------------------')
            print('\n 👤Admin: Logging Out.\n 👏👏👏 Thank you for using this app')
            print('\n--------------------------------------------------')
            break
        else:
            print('No such option. Please try again.')

# --- Staff Functions ---
def staff_menu(user_id):
    while True:
        print('\n-----------------------------------------------')
        print('\n Welcome to Inventory Management System 😍')
        print('\n-----------------------------------------------')
        print('Please select your option :')
        ch = int(input('''
🧺 Product Management
---------------------                       
1. View Inventory
2. Add new product
3. Search Item by ID
4. Search Item by Category                                          

👥 Supplier Management
---------------------                       
5. Add Supplier
6. View All Suppliers
7. Search Supplier
                      
🚛 Order Management
-------------------                                             
8. Order Product
9. View All Orders
10. Search Order
11. Update an Order

👤 User Account Management
--------------------------                        
12. Change Username & Password                     
13. ❌Exit
                       
Choice: '''))

        if ch == 1:
            print('Staff:📄Viewing Inventory......')
            printinventoryreport(user_id)  
        elif ch == 2:
           print('Staff: Adding new Item......')
           addnewproduct(user_id) 
        elif ch == 3:
           print('Staff: 🔎Searching an Item......')
           searchanitem(user_id)
        elif ch == 4:
           print('Staff: 🔎Searching an Item by Category......')
           search_products_by_category(user_id)
        elif ch == 5:
           print('Staff: Adding Supplier Details......')
           addsupplier(user_id)   
        elif ch == 6:
           print('Staff: 📄Viewing all suppliers......')
           viewallsupplier(user_id)
        elif ch == 7:
           print('Staff: 🔎Searching Supplier......')
           viewsupplier(user_id)  
        elif ch == 8:
           print('Staff: Ordering product......')
           orderproduct(user_id)    
        elif ch == 9:
           print('Staff: 📄Viewing all ordered product......')
           view_all_orders(user_id) 
        elif ch == 10:
           print('Staff: 🔎Searching an Order......')
           search_an_order(user_id)
        elif ch == 11:
           print('Staff: Update an Order......')
           update_order(user_id)
        elif ch == 12:
           print('👤Staff: changing username & password......')
           return change_credentials(user_id)  
        elif ch == 13:
            print('\n--------------------------------------------------')
            print('\n 👤Staff: Logging Out.\n👏👏👏 Thank you for using this app')
            print('\n--------------------------------------------------')
            break
        else:
            print('No such option. Please try again.')


# add product
def addnewproduct(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    pname = input('Enter product name: ').strip()
    try:
        price = float(input('Enter price: '))
        qty = int(input('Enter quantity: '))
        sid = int(input('Enter supplier ID: '))
        category = input('Enter product category: ').strip()
    except ValueError:
        print("Invalid input. Price must be a number, quantity and supplier ID must be integers.")
        conn.close()
        return

    try:
        cursor.execute('''
            INSERT INTO product(p_name, p_price, qty, sid, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (pname, price, qty, sid, category))
        conn.commit()
        print('✅ Product Added Successfully')
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()


# remove product
def removeanitem(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        pid = int(input('Enter the product ID to delete: '))
    except ValueError:
        print("❌ Invalid input. Product ID must be an integer.")
        conn.close()
        return

    #  Check if the product exists
    cursor.execute('SELECT * FROM product WHERE pid = ?', (pid,))
    product = cursor.fetchone()

    if not product:
        print("❌ No product found with that ID.")
        conn.close()
        return

    choice = input('Are you sure you want to delete this item? (y/n): ').lower()
    if choice == 'y':
        cursor.execute('DELETE FROM product WHERE pid = ?', (pid,))
        conn.commit()
        print('✅ Product Deleted')
    else:
        print('❎ Product not deleted')

    conn.close()

# edit product
def editproduct(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        pid = int(input('Enter the product ID to edit: '))
    except ValueError:
        print("❌ Invalid input. Product ID must be an integer.")
        conn.close()
        return

    # Check if the product exists
    cursor.execute('SELECT * FROM product WHERE pid = ?', (pid,))
    product = cursor.fetchone()
    if not product:
        print("❌ No product found with that ID.")
        conn.close()
        return

    pname = input('Enter new product name: ').strip()
    try:
        price = float(input('Enter new price: '))
        qty = int(input('Enter new quantity: '))
        sid = int(input('Enter new supplier ID: '))
        category = input('Enter new product category: ').strip()
    except ValueError:
        print("❌ Invalid input. Price must be a number, quantity and supplier ID must be integers.")
        conn.close()
        return

    try:
        cursor.execute('''
            UPDATE product 
            SET p_name = ?, p_price = ?, qty = ?, sid = ?, category = ?
            WHERE pid = ?
        ''', (pname, price, qty, sid, category, pid))
        conn.commit()
        print('✅ Product updated successfully.')
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()



# search an item
def searchanitem(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        pid = int(input('Enter your product ID: '))
    except ValueError:
        print("❌ Invalid input. Product ID must be an integer.")
        conn.close()
        return
    cursor.execute('SELECT * FROM product WHERE pid = ?', (pid,))
    product = cursor.fetchone()

    if not product:
        print("❌ No such product found.")
    else:
        print("\n✅ Product Found:")
        print(f"Product ID     : {product[0]}")
        print(f"Name           : {product[1]}")
        print(f"Price          : {product[2]}")
        print(f"Quantity       : {product[3]}")
        print(f"Supplier ID    : {product[4]}")
        print(f"Category       : {product[5]}")

    conn.close()


# search item by its category
def search_products_by_category(user_id):
    category = input("Enter category: ").strip()
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT pid, p_name, p_price FROM product WHERE category=?", (category,))
    results = cursor.fetchall()
    
    if results:
        print(f"\nProducts in category: {category}")
        print("ID   Name                Price")
        print("-----------------------------------")
        for pid, name, price in results:
            print(f"{pid:<4} {name:<18} {price}")
    else:
        print(f"\nNo products found in category '{category}'.")
    
    conn.close()


#view inventory report
def printinventoryreport(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product')
    alldata = cursor.fetchall()
    if not alldata:
        print('😒 No products found in inventory.')
    else:
        print('\n📄 Products in Inventory:')
        print('ID   Name           Price     Quantity   Supplier ID   Category')
        print('-----------------------------------------------------------------------')
        for i in alldata:
            # Assuming table structure: pid, p_name, p_price, qty, sid, category
            print(f'{i[0]:<4} {i[1]:<14} ₹{i[2]:<9.2f} {i[3]:<10} {i[4]:<12} {i[5]}')
    conn.close()

# Product Alert function
def product_quantity_alert(user_id):
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    # Fetch product id, name, and quantity
    cur.execute("SELECT pid, p_name, qty FROM product")
    products = cur.fetchall()

    print("\n=== Product Quantity Alerts ===")
    print("------------------------------------\n")

    alert_found = False
    for pid, p_name, qty in products:   
        if qty == 0:
            print(f"❌  OUT OF STOCK | {p_name} (ID: {pid}) → No stock left!")
            alert_found = True
        elif qty <= 10:
            print(f"⚠️  LOW STOCK   | {p_name} (ID: {pid}) → Only {qty} left.")
            alert_found = True

    if not alert_found:
        print("✅ All products are sufficiently stocked!\n")

    print("------------------------------------")

    conn.close()

# add supplier
def addsupplier(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    s_name = input('Enter supplier name: ').strip()
    if not s_name:
        print("❌ Supplier name cannot be empty.")
        conn.close()
        return

    try:
        contact = int(input('Enter contact number: '))
    except ValueError:
        print("❌ Invalid contact number. It must be numeric.")
        conn.close()
        return

    try:
        cursor.execute('''
            INSERT INTO supplier(s_name, contact)
            VALUES (?, ?)
        ''', (s_name, contact))
        conn.commit()
        print('✅ Supplier added successfully.')
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

# view all suppler
def viewallsupplier(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM supplier')
    suppliers = cursor.fetchall()

    if not suppliers:
        print("😒 No suppliers found.")
    else:
        print("\n👍 List of All Suppliers:")
        print("ID   Name                Contact")
        print("----------------------------------------")
        for s in suppliers:
            print(f"{s[0]:<4} {s[1]:<20} {s[2]}")

    conn.close()

# view a supplier
def viewsupplier(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        sid = int(input('Enter Supplier ID to view: '))
    except ValueError:
        print("❌ Invalid input. Supplier ID must be an integer.")
        conn.close()
        return

    cursor.execute('SELECT * FROM supplier WHERE sid = ?', (sid,))
    supplier = cursor.fetchone()

    if not supplier:
        print("😒 No supplier found with that ID.")
    else:
        print("\n✅ Supplier Details:")
        print(f"Supplier ID   : {supplier[0]}")
        print(f"Name          : {supplier[1]}")
        print(f"Contact       : {supplier[2]}")

    conn.close()

# update supplier
def updatesupplier(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    sid = int(input('Enter Supplier ID to update: '))
    sname = input('Enter new supplier name: ')
    contact = int(input('Enter new contact number: '))

    cursor.execute('''
        UPDATE supplier SET s_name = ?, contact = ? WHERE sid = ?
    ''', (sname, contact, sid))

    conn.commit()
    print("✅ Supplier updated successfully.")
    conn.close()

# remove supplier
def removesupplier(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    sid = int(input('Enter Supplier ID to delete: '))
    cursor.execute('DELETE FROM supplier WHERE sid = ?', (sid,))
    conn.commit()

    print("✅ Supplier deleted successfully.")
    conn.close()


# order product
def orderproduct(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    order_date = datetime.datetime.now().strftime('%Y-%m-%d')
    status = 1
    cart = []

    while True:
        pid = int(input("Enter Product ID: "))
        qty = int(input("Enter Quantity: "))
        cursor.execute("SELECT p_name, qty, p_price FROM product WHERE pid=?", (pid,))
        product = cursor.fetchone()

        if product:
            pname, available, price = product
            if available >= qty:
                cart.append((pid, qty, pname, available, price))
                print(f"🛒 Added {qty} of '{pname}' to cart.")
            else:
                print(f"⚠️ Only {available} of '{pname}' available. Cannot order {qty}.")
        else:
            print(f"❌ Product ID {pid} not found.")

        more = input("Do you want to order another product? (y/n): ").lower()
        if more != 'y':
            break

    if cart:
        try:
            total_amount = 0
            for pid, qty, pname, available, price in cart:
                cursor.execute('''
                    INSERT INTO orders(order_date, status, uid, pid, qty)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_date, status, user_id, pid, qty))

                cursor.execute("UPDATE product SET qty = qty - ? WHERE pid=?", (qty, pid))
                print(f"✅ Ordered {qty} of '{pname}'. Remaining: {available - qty}")

                total_amount += qty * price

            conn.commit()
            print("\n🎉 All items successfully ordered!\n")

            # 🧾 Print Bill
            print("========== 🧾 BILL RECEIPT ==========")
            print(f"Customer ID: {user_id}")
            print(f"Order Date : {order_date}")
            print("-------------------------------------")
            print(f"{'Product':<15}{'Qty':<5}{'Price':<10}{'Total':<10}")
            print("-------------------------------------")
            for pid, qty, pname, available, price in cart:
                line_total = qty * price
                print(f"{pname:<15}{qty:<5}{price:<10}{line_total:<10}")
            print("-------------------------------------")
            print(f"{'Grand Total':<30}{total_amount}")
            print("=====================================")

        except Exception as e:
            conn.rollback()
            print(f"❌ Transaction failed. No orders placed. Error: {e}")
    else:
        print("🛒 Cart is empty. No orders placed.")

    conn.close()


    

# view all orders
def view_all_orders(user_id):
    import sqlite3
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    if not orders:
        print("😒 No order found.")
    else:
        print('👍 Orders found:')
        print('order_id   order_date   status    user_id   product_id   qty')
        print('---------------------------------------------------------------')
        for i in orders:
            print(f'{i[0]:<10} {i[1]:<12} {i[2]:<8} {i[3]:<8} {i[4]:<11} {i[5]}')
    conn.close()

# search an order
def search_an_order(user_id):

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        oid = int(input('Enter your Order ID: '))
    except ValueError:
        print("❌ Invalid input. Order ID must be an integer.")
        conn.close()
        return

    cursor.execute('SELECT * FROM orders WHERE oid = ?', (oid,))
    order = cursor.fetchone()

    if not order:
        print("❌ No such order found.")
    else:
        print("\n✅ Order Found:")
        print(f"Order ID     : {order[0]}")
        print(f"Order date   : {order[1]}")
        print(f"Status       : {order[2]}")
        print(f"User ID      : {order[3]}")
        print(f"Product ID   : {order[4]}")
        print(f"Quantity     : {order[5]}")
    conn.close()

# update an order
def update_order(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    #  Ask for order ID
    order_id = int(input("Enter Order ID to update: "))

    #  Fetch existing order
    cursor.execute('''
        SELECT pid, qty FROM orders WHERE oid=? AND uid=?
    ''', (order_id, user_id))
    order = cursor.fetchone()

    if not order:
        print("❌ Order not found for this user.")
        conn.close()
        staff_menu(user_id)
        return

    pid, old_qty = order

    #  Ask new quantity
    new_qty = int(input(f"Enter new quantity (current: {old_qty}): "))

    #  Check product availability
    cursor.execute("SELECT p_name, qty FROM product WHERE pid=?", (pid,))
    product = cursor.fetchone()

    if not product:
        print("❌ Product not found.")
        conn.close()
        staff_menu(user_id)
        return

    pname, available = product

    # Calculate difference
    diff = new_qty - old_qty

    if diff > 0 and available < diff:
        print(f"⚠️ Not enough stock. Only {available} more available.")
        conn.close()
        staff_menu(user_id)
        return

    try:
        #  Update order
        cursor.execute('''
            UPDATE orders SET qty=?, order_date=? WHERE oid=? AND uid=?
        ''', (new_qty, datetime.datetime.now().strftime('%Y-%m-%d'), order_id, user_id))

        #  Update product stock
        cursor.execute("UPDATE product SET qty = qty - ? WHERE pid=?", (diff, pid))

        conn.commit()
        print(f"✅ Order {order_id} updated: {new_qty} of '{pname}'")
    except Exception as e:
        conn.rollback()
        print(f"❌ Update failed. Error: {e}")

    conn.close()




    

# delete an order
def delete_an_order(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    oid = int(input('Enter Order ID to delete: '))

    #  Get product_id and qty from the order
    cursor.execute('SELECT pid, qty FROM orders WHERE oid = ?', (oid,))
    order = cursor.fetchone()

    if order:
        pid, qty = order

        #  Update product quantity back
        cursor.execute('UPDATE product SET qty = qty + ? WHERE pid = ?', (qty, pid))

        #  Delete the order
        cursor.execute('DELETE FROM orders WHERE oid = ?', (oid,))
        conn.commit()

        print("✅ Order deleted successfully and product quantity updated.")
    else:
        print("⚠️ Order not found.")

    conn.close()



# add user
def add_user(user_id):
    try:
        with sqlite3.connect('inventory.db') as conn:
            cursor = conn.cursor()

            username = input('Enter username: ').strip()
            password = input('Enter password: ').strip()
            role = input('Enter role: ').strip()

            if not username or not password or not role:
                print("❌ All fields are required.")
                return

            cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (username, password, role))

            conn.commit()
            print('✅ User added successfully.')

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")


#  view all users
def view_all_users(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    if not users:
        print("😒 No users found.")
    else:
        print("\n👍 List of All users:")
        print("User_ID   User_Name    Password    Role")
        print("----------------------------------------")
        for u in users:
            print(f"{u[0]:<4} {u[1]:<14} {u[2]:<10} {u[3]}")

    conn.close()

# view user
def search_user(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        uid = int(input('Enter user ID to view: '))
    except ValueError:
        print("❌ Invalid input. user ID must be an integer.")
        conn.close()
        return

    cursor.execute('SELECT * FROM users WHERE uid = ?', (uid,))
    users = cursor.fetchone()

    if not users:
        print("😒 No user found with that ID.")
    else:
        print("\n✅ User Details:")
        print(f"User ID   : {users[0]}")
        print(f"Username  : {users[1]}")
        print(f"Password  : {users[2]}")

    conn.close()

# update user details
def update_user(user_id):

    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    try:
        uid = int(input('Enter User ID to update: '))
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")
        return

    username = input('Enter new username: ').strip()
    password = input('Enter new password: ').strip()
    role = input('Enter new role: ').strip()

    if not username or not password or not role:
        print("❌ All fields are required.")
        return

    # Check if user exists
    cursor.execute("SELECT uid FROM users WHERE uid = ?", (uid,))
    if cursor.fetchone() is None:
        print("😒 No user found with that ID.")
        return

    # Update user
    cursor.execute('''
        UPDATE users
        SET username = ?, password = ?, role = ?
        WHERE uid = ?
    ''', (username, password, role, uid))

    conn.commit()
    print("✅ User updated successfully.")
    conn.close()


 # remove user
def remove_user(user_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    uid = int(input('Enter user ID to delete: '))
    cursor.execute('DELETE FROM users WHERE uid = ?', (uid,))
    conn.commit()

    print("✅ User deleted successfully.")
    conn.close()


# staff :change username & Password
def change_credentials(user_id):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    #  Ask for old username and verify
    old_username = input("Enter your current username: ")
    cursor.execute("SELECT username FROM users WHERE uid=?", (user_id,))
    result = cursor.fetchone()

    if not result:
        print("❌ User ID not found.")
        conn.close()
        staff_menu(user_id)   
        return

    if result[0] != old_username:
        print("❌ Old username does not match user ID.")
        conn.close()
        staff_menu(user_id)   
        return

    #  Proceed with menu if validation passes
    print("\n---  Menu ---")
    print("1. Change Username")
    print("2. Change Password")
    print("3. Exit ")
    
    choice = input("Select option: ")

    if choice == '1':
        new_username = input("New username: ")
        try:
            cursor.execute("UPDATE users SET username=? WHERE uid=?", (new_username, user_id))
            conn.commit()
            print("✅ Username updated.")
        except sqlite3.IntegrityError:
            print("❌ Username already exists.")
    elif choice == '2':
        new_password = input("New password: ")
        cursor.execute("UPDATE users SET password=? WHERE uid=?", (new_password, user_id))
        conn.commit()
        print("✅ Password updated.")
    elif choice == '3':
        print("👋 Returning to Staff Menu...")
        conn.close()
        staff_menu(user_id)
        return
    else:
        print("❌ Invalid option.")

    conn.close()
    staff_menu(user_id)               


# admin:username password changing
def change_user_namepass(user_id):
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    # Show users
    print("\n--- Users ---")
    for uid, uname in cur.execute("SELECT uid, username FROM users"):
        print(f"{uid}: {uname}")

    try:
        uid = int(input("\nEnter user ID to modify: "))
    except ValueError:
        print("❌ Invalid ID.")
        conn.close()
        return

    # Check if user exists
    cur.execute("SELECT uid FROM users WHERE uid=?", (uid,))
    if cur.fetchone() is None:
        print("❌ User ID not found.")
        conn.close()
        return

    while True:
        print("\n1. Change Username\n2. Change Password\n3. Exit")
        opt = input("Choose: ")

        if opt == '1':
            uname = input("New username: ").strip()
            if not uname:
                print("❌ Username cannot be empty.")
                continue
            try:
                cur.execute("UPDATE users SET username=? WHERE uid=?", (uname, uid))
                conn.commit()
                print("✅ Username updated.")
            except sqlite3.IntegrityError:
                print("❌ Username already taken.")

        elif opt == '2':
            pw = input("New password: ").strip()
            if not pw:
                print("❌ Password cannot be empty.")
                continue
            cur.execute("UPDATE users SET password=? WHERE uid=?", (pw, uid))
            conn.commit()
            print("✅ Password updated.")

        elif opt == '3':
            print("👋 Returning to Admin Menu...")
            break
        else:
            print("❌ Invalid choice.")

    conn.close()
    admin_menu(user_id)     


# --- Main Menu ---
def main():
    init_db()
    while True:
        print("\n--- Inventory Management System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        option = input("Select an option: ")
        if option == "1":
            register()
        elif option == "2":
            login()
        elif option == "3":
            print('\n--------------------------------------------------')
            print('\n👍👍👍 Exiting Inventory Management System.\n😍😍😍 Thank you for using this app')
            print('\n--------------------------------------------------')
            break
        else:
            print("Invalid option.Please try again.")

if __name__ == "__main__":
    main()
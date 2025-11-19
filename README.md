📦 Inventory Management System (IMS)

The Inventory Management System (IMS) is a lightweight, command-line application for managing products, stock levels, suppliers, and staff. It is designed for small businesses or individuals who prefer a simple, terminal-based workflow without the need for a graphical interface.

🚀 Project Overview

The IMS is a console-based Python application that helps manage:

•	🔗 Admin & User Registration & Login

•	🛒 Product Management: Add, update, delete, and list products

•	📊 Stock Tracking: View current stock levels and update quantities

•	🔔 Low Stock Alerts: CLI notifications when items fall below a threshold

•	👥 User Roles: Admin and Staff access levels

•	📑 Reports: Generate inventory reports

🛠️ Tech Stack

•	Language: Python

•	Database: SQLite

🖥️ Getting Started

Dependencies

Before installing, ensure you have the following:

•	Windows 10 or higher (Linux/Mac supported with minor adjustments)

•	Python 3.9+

•	SQLite3 (default database)

How to Run the Project

1️⃣ Install Python

Download from: Python Downloads

2️⃣ Install Required Libraries

Open terminal/command prompt and run:

pip install -r requirements.txt 

3️⃣ Open the Project Folder

Navigate to the folder where your inventory.py file is saved.

4️⃣ Run the Program

python inventory.py 

5️⃣ First Login (Admin)

•	The database will start empty.

•	Register and log in with the role Admin.

👥 Staff Features

•	Register & Login

•	View/Search products (by ID or Category)

•	View/Add suppliers

•	View inventory reports

•	Place, view, and update orders

•	Change username & password

👑 Admin Features

🔹 User Management

•	Add, view, update, and delete user details

🔹 Supplier Management

•	Add, view, update, and delete supplier details

🔹 Inventory Management

•	Add, view, update, and delete product details

•	Stock alerts when quantity < threshold

•	View inventory reports

•	Multi-domain support (electronics, pharmacy, groceries, books, clothing, automotive)

🔹 Order Management

•	Create, view, update, and cancel orders

•	Track order status (0 = Pending, 1 = Delivered)

•	Generate invoices

•	Generate inventory reports

📂 Database Tables

•	users

•	supplier

•	product

•	orders

(All tables are linked with foreign keys for clean relationships.)

🧪 Validations

•	✅ Name: alphabets only

•	✅ Unique usernames

•	✅ Contact: 10 digits (Regex)

•	✅ Stock availability check before purchase

•	✅ Prevent deletion of sold products

🌱 Beginner-Friendly Because

•	Simple console interface

•	No external DB setup (uses SQLite)

•	Clean outputs

•	Teaches CRUD operations, regex, and role-based access


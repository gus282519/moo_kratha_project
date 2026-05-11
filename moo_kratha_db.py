import sqlite3

DB_FILE = 'moo_kratha_project.db'

def create_moo_kratha_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meats (
        meat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        meat_name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        price REAL NOT NULL,
        spiciness_level TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Order_Details (
        order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        meat_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (meat_id) REFERENCES Meats(meat_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    )
    ''')

    categories_data = [
        ('หมูสันคอ', 'เนื้อหมูสันคอเนื้อนุ่ม เหมาะสำหรับปิ้งหมูกระทะ'),
        ('หมูสามชั้น', 'หมูสามชั้นมันกำลังดี ปิ้งแล้วกรอบนอกนุ่มใน'),
        ('ไก่', 'เนื้อไก่ชิ้นสไลซ์ พร้อมปรุงสำหรับ ย่างหมูกระทะ'),
        ('ซีฟู้ด', 'อาหารทะเลสดใหม่สำหรับย่างบนกระทะ'),
        ('เครื่องเคียง', 'ผักและอาหารทานเล่นเสริมมื้อหมูกระทะ')
    ]
    cursor.executemany(
        'INSERT INTO Categories (category_name, description) VALUES (?, ?)',
        categories_data
    )

    meats_data = [
        ('สันคอหมูสไลซ์', 1, 139.0, 'กลาง', 'สันคอหมูเนื้อนุ่มหนา 3 มม.'),
        ('สามชั้นหมู', 2, 129.0, 'กลาง', 'หมูสามชั้นมันแทรก ปิ้งแล้วหอม'),
        ('ไก่หมักซอส', 3, 115.0, 'อ่อน', 'ไก่หมักซอสสูตรหมูกระทะ'),
        ('กุ้งแม่น้ำ', 4, 189.0, 'อ่อน', 'กุ้งแม่น้ำสดขนาดกลาง'),
        ('ผักรวม', 5, 59.0, 'ไม่เผ็ด', 'ผักสดสำหรับย่างประกอบหมูกระทะ')
    ]
    cursor.executemany(
        'INSERT INTO Meats (meat_name, category_id, price, spiciness_level, description) VALUES (?, ?, ?, ?, ?)',
        meats_data
    )

    customers_data = [
        ('สมชาย ใจดี', '081-234-5678', 'somchai@example.com'),
        ('ปุณณภา ส้มหวาน', '089-765-4321', 'punapa@example.com'),
        ('วัฒน์ ยิ้มแย้ม', '086-111-2222', 'wat@example.com'),
        ('ธนิศา ปรุงรส', '080-999-8888', 'thanisa@example.com')
    ]
    cursor.executemany(
        'INSERT INTO Customers (customer_name, phone, email) VALUES (?, ?, ?)',
        customers_data
    )

    orders_data = [
        (1, 389.0, 'completed'),
        (2, 248.0, 'pending'),
        (3, 204.0, 'completed'),
        (4, 268.0, 'cancelled')
    ]
    cursor.executemany(
        'INSERT INTO Orders (customer_id, total_amount, status) VALUES (?, ?, ?)',
        orders_data
    )

    order_details_data = [
        (1, 1, 2, 139.0, 278.0),
        (1, 5, 1, 59.0, 59.0),
        (2, 2, 1, 129.0, 129.0),
        (2, 3, 1, 115.0, 115.0),
        (3, 1, 1, 139.0, 139.0),
        (3, 4, 1, 189.0, 189.0),
        (4, 5, 2, 59.0, 118.0)
    ]
    cursor.executemany(
        'INSERT INTO Order_Details (order_id, meat_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)',
        order_details_data
    )

    conn.commit()
    conn.close()

    print(f'Created database file: {DB_FILE}')

if __name__ == '__main__':
    create_moo_kratha_database()

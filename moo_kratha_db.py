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
        image_url TEXT,
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

    categories_count = cursor.execute('SELECT count(*) FROM Categories').fetchone()[0]
    meats_count = cursor.execute('SELECT count(*) FROM Meats').fetchone()[0]
    customers_count = cursor.execute('SELECT count(*) FROM Customers').fetchone()[0]
    orders_count = cursor.execute('SELECT count(*) FROM Orders').fetchone()[0]
    details_count = cursor.execute('SELECT count(*) FROM Order_Details').fetchone()[0]

    if categories_count != 10 or meats_count != 10 or customers_count != 10 or orders_count != 10 or details_count != 20:
        cursor.execute('PRAGMA foreign_keys = OFF')
        cursor.execute('DELETE FROM Order_Details')
        cursor.execute('DELETE FROM Orders')
        cursor.execute('DELETE FROM Meats')
        cursor.execute('DELETE FROM Customers')
        cursor.execute('DELETE FROM Categories')
        cursor.execute('PRAGMA foreign_keys = ON')

        categories_data = [
            ('หมูสันคอ', 'เนื้อหมูสันคอเนื้อนุ่ม เหมาะสำหรับปิ้งหมูกระทะ'),
            ('หมูสามชั้น', 'หมูสามชั้นมันแทรก ปิ้งแล้วกรอบนอกนุ่มใน'),
            ('ไก่', 'ไก่หมักซอสกลมกล่อมสำหรับย่าง'),
            ('ซีฟู้ด', 'อาหารทะเลสดใหม่สำหรับย่างบนกระทะ'),
            ('เครื่องเคียง', 'ผักสดและของทานเล่นเสริมมื้อหมูกระทะ'),
            ('เนื้อวัว', 'เนื้อวัวสไลซ์คุณภาพสูง'),
            ('ของหวาน', 'น้ำแข็งใสและของหวานปิดท้ายมื้ออาหาร'),
            ('น้ำจิ้ม', 'ซอสและน้ำจิ้มพิเศษสำหรับหมูกระทะ'),
            ('อาหารทะเล', 'กุ้ง หอย ปลาหมึกสด'),
            ('ผัก', 'ผักรวมสำหรับกรอบสดและย่าง')
        ]
        cursor.executemany(
            'INSERT INTO Categories (category_name, description) VALUES (?, ?)',
            categories_data
        )

        cursor.execute('SELECT category_id, category_name FROM Categories')
        category_id_map = {name: cid for cid, name in cursor.fetchall()}

        meats_data = [
            ('สันคอหมูสไลซ์', 'หมูสันคอ', 139.0, 'กลาง', 'หมูสันคอหั่นชิ้นหนาพอเหมาะ'),
            ('สามชั้นหมู', 'หมูสามชั้น', 129.0, 'กลาง', 'สามชั้นหมูมันแทรกย่างอร่อย'),
            ('ไก่หมักซอส', 'ไก่', 115.0, 'อ่อน', 'ไก่หมักซอสสูตรพิเศษ'),
            ('กุ้งขาว', 'ซีฟู้ด', 175.0, 'อ่อน', 'กุ้งขาวสดสำหรับย่าง'),
            ('ผักรวม', 'ผัก', 59.0, 'ไม่เผ็ด', 'ผักหลากหลายสำหรับย่าง'),
            ('เนื้อวัวสไลซ์', 'เนื้อวัว', 199.0, 'กลาง', 'เนื้อวัวคุณภาพสูง'),
            ('ไส้กรอกหมู', 'หมูสามชั้น', 85.0, 'อ่อน', 'ไส้กรอกหมูไทยรสกลมกล่อม'),
            ('ปลาหมึก', 'ซีฟู้ด', 149.0, 'อ่อน', 'ปลาหมึกสดฉ่ำย่างหอม'),
            ('สาหร่ายกรอบ', 'เครื่องเคียง', 45.0, 'ไม่เผ็ด', 'เครื่องเคียงกรอบเคี้ยวสนุก'),
            ('ปลา', 'อาหารทะเล', 95.0, 'ไม่เผ็ด', 'ปลาไทยสดใหม่ย่างหอม')
        ]
        cursor.executemany(
            'INSERT INTO Meats (meat_name, category_id, price, spiciness_level, description) VALUES (?, ?, ?, ?, ?)',
            [(name, category_id_map[category], price, spiciness_level, description) for name, category, price, spiciness_level, description in meats_data]
        )

        cursor.execute('SELECT meat_id, meat_name FROM Meats')
        meat_id_map = {name: mid for mid, name in cursor.fetchall()}

        customers_data = [
            ('สมชาย ใจดี', '081-234-5678', 'somchai@example.com'),
            ('ปุณณภา ส้มหวาน', '089-765-4321', 'punapa@example.com'),
            ('วัฒน์ ยิ้มแย้ม', '086-111-2222', 'wat@example.com'),
            ('ธนิศา ปรุงรส', '080-999-8888', 'thanisa@example.com'),
            ('ณัฐพล กลิ่นโสม', '082-222-3333', 'nutpol@example.com'),
            ('อรทัย สดใส', '083-444-5555', 'orathai@example.com'),
            ('กิตติภพ พัลลภ', '084-666-7777', 'kittipob@example.com'),
            ('พิมพ์ชนก แซ่ลี้', '085-888-9999', 'pimchanok@example.com'),
            ('ชลธิชา ร่มเย็น', '086-123-4567', 'chon@example.com'),
            ('สุรชาติ ยิ้มสู้', '087-321-7654', 'surachat@example.com')
        ]
        cursor.executemany(
            'INSERT INTO Customers (customer_name, phone, email) VALUES (?, ?, ?)',
            customers_data
        )

        orders_data = [
            (1, 278.0, 'completed'),
            (2, 244.0, 'completed'),
            (3, 115.0, 'pending'),
            (4, 224.0, 'completed'),
            (5, 104.0, 'completed'),
            (6, 372.0, 'pending'),
            (7, 89.0, 'cancelled'),
            (8, 189.0, 'completed'),
            (9, 98.0, 'pending'),
            (10, 164.0, 'completed')
        ]
        cursor.executemany(
            'INSERT INTO Orders (customer_id, total_amount, status) VALUES (?, ?, ?)',
            orders_data
        )

        order_details_data = [
            (1, 'สันคอหมูสไลซ์', 2, 139.0, 278.0),
            (1, 'ผักรวม', 1, 59.0, 59.0),
            (2, 'สามชั้นหมู', 1, 129.0, 129.0),
            (2, 'ไก่หมักซอส', 1, 115.0, 115.0),
            (3, 'เนื้อวัวสไลซ์', 1, 199.0, 199.0),
            (4, 'กุ้งขาว', 1, 175.0, 175.0),
            (4, 'สาหร่ายกรอบ', 1, 45.0, 45.0),
            (5, 'ปลา', 1, 95.0, 95.0),
            (5, 'ไส้กรอกหมู', 1, 85.0, 85.0),
            (6, 'สันคอหมูสไลซ์', 1, 139.0, 139.0),
            (6, 'สามชั้นหมู', 1, 129.0, 129.0),
            (6, 'ไก่หมักซอส', 1, 115.0, 115.0),
            (7, 'กุ้งขาว', 1, 175.0, 175.0),
            (7, 'สาหร่ายกรอบ', 1, 45.0, 45.0),
            (8, 'สามชั้นหมู', 1, 129.0, 129.0),
            (8, 'ผักรวม', 1, 59.0, 59.0),
            (9, 'ปลาหมึก', 1, 149.0, 149.0),
            (10, 'ปลา', 2, 95.0, 190.0),
            (10, 'สันคอหมูสไลซ์', 1, 139.0, 139.0),
            (10, 'เนื้อวัวสไลซ์', 1, 199.0, 199.0)
        ]
        cursor.executemany(
            'INSERT INTO Order_Details (order_id, meat_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)',
            [(order_id, meat_id_map[meat_name], quantity, unit_price, total_price) for order_id, meat_name, quantity, unit_price, total_price in order_details_data]
        )

    conn.commit()
    conn.close()

    print(f'Created database file: {DB_FILE}')


if __name__ == '__main__':
    create_moo_kratha_database()

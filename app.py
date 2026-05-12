from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename
from moo_kratha_db import create_moo_kratha_database

app = Flask(__name__)
app.secret_key = "mookratha"

DATABASE = "moo_kratha_project.db"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# สร้างโฟลเดอร์ถ้ายังไม่มี
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def init_db():
    create_moo_kratha_database()


# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# HOME
# =========================
@app.route("/")
def home():
    conn = get_db_connection()

    products = conn.execute("""
        SELECT Meats.*, Categories.category_name
        FROM Meats
        LEFT JOIN Categories
        ON Meats.category_id = Categories.category_id
    """).fetchall()

    categories = conn.execute("""
        SELECT * FROM Categories
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        page="home",
        products=products,
        categories=categories
    )


# =========================
# ADD PRODUCT
# =========================
@app.route("/product/add", methods=["GET", "POST"])
def add_product():

    conn = get_db_connection()
    categories = conn.execute(
        "SELECT * FROM Categories"
    ).fetchall()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        category_id = request.form["category_id"]
        description = request.form["description"]
        spiciness_level = request.form["spiciness_level"]

        image_file = request.files["image_file"]

        image_url = ""

        # upload image
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image_file.save(image_path)

            # เก็บแค่ชื่อไฟล์
            image_url = filename

        conn.execute("""
            INSERT INTO Meats
            (
                meat_name,
                price,
                category_id,
                description,
                spiciness_level,
                image_url
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            price,
            category_id,
            description,
            spiciness_level,
            image_url
        ))

        conn.commit()
        conn.close()

        flash("เพิ่มสินค้าสำเร็จ", "success")

        return redirect(url_for("home"))

    conn.close()

    return render_template(
        "index.html",
        page="product_form",
        action="เพิ่ม",
        product=None,
        categories=categories
    )


# =========================
# EDIT PRODUCT
# =========================
@app.route("/product/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    conn = get_db_connection()

    product = conn.execute("""
        SELECT * FROM Meats
        WHERE meat_id = ?
    """, (product_id,)).fetchone()

    categories = conn.execute("""
        SELECT * FROM Categories
    """).fetchall()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        category_id = request.form["category_id"]
        description = request.form["description"]
        spiciness_level = request.form["spiciness_level"]

        image_file = request.files["image_file"]

        # ใช้รูปเดิมก่อน
        image_url = request.form.get("existing_image_url")

        # ถ้ามีอัปโหลดรูปใหม่
        if image_file and image_file.filename != "":

            filename = secure_filename(image_file.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image_file.save(image_path)

            image_url = filename

        conn.execute("""
            UPDATE Meats
            SET
                meat_name = ?,
                price = ?,
                category_id = ?,
                description = ?,
                spiciness_level = ?,
                image_url = ?
            WHERE meat_id = ?
        """, (
            name,
            price,
            category_id,
            description,
            spiciness_level,
            image_url,
            product_id
        ))

        conn.commit()
        conn.close()

        flash("แก้ไขสินค้าสำเร็จ", "success")

        return redirect(url_for("home"))

    conn.close()

    return render_template(
        "index.html",
        page="product_form",
        action="แก้ไข",
        product=product,
        categories=categories
    )


# =========================
# DELETE PRODUCT
# =========================
@app.route("/product/delete/<int:product_id>")
def delete_product(product_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM Meats
        WHERE meat_id = ?
    """, (product_id,))

    conn.commit()
    conn.close()

    flash("ลบสินค้าสำเร็จ", "success")

    return redirect(url_for("home"))


# =========================
# ADD CATEGORY
# =========================
@app.route("/category/add", methods=["GET", "POST"])
def add_category():

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO Categories
            (
                category_name,
                description
            )
            VALUES (?, ?)
        """, (
            name,
            description
        ))

        conn.commit()
        conn.close()

        flash("เพิ่มหมวดหมู่สำเร็จ", "success")

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        page="category_form",
        action="เพิ่ม",
        category=None
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

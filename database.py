import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sailee@999",
        database="bizcardx"
    )

def insert_data(data, image_bytes):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO business_cards
        (company_name, card_holder, designation, phone,
         email, website, area, city, state, pincode, image)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["company_name"],
        data["card_holder"],
        data["designation"],
        data["phone"],
        data["email"],
        data["website"],
        data["area"],
        data["city"],
        data["state"],
        data["pincode"],
        image_bytes
    ))

    conn.commit()
    conn.close()

def fetch_all():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM business_cards")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_data(record_id, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE business_cards SET
        company_name=%s, card_holder=%s, designation=%s,
        phone=%s, email=%s, website=%s,
        area=%s, city=%s, state=%s, pincode=%s
        WHERE id=%s
    """, (
        data["company_name"],
        data["card_holder"],
        data["designation"],
        data["phone"],
        data["email"],
        data["website"],
        data["area"],
        data["city"],
        data["state"],
        data["pincode"],
        record_id
    ))

    conn.commit()
    conn.close()

def delete_data(record_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM business_cards WHERE id=%s", (record_id,))
    conn.commit()
    conn.close()

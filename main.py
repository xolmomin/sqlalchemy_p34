
import psycopg2

conn = psycopg2.connect(
    host='localhost', port='5432',
    user='postgres', password='1', database='p34_db'
)


def init_db():
    with conn.cursor() as cursor:
        q = """
            CREATE TABLE IF NOT EXISTS products
            (
                id
                SERIAL
                PRIMARY
                KEY,
                name
                VARCHAR
            (
                255
            ) NOT NULL,
                price INTEGER NOT NULL
                );
            """
        cursor.execute(q)
        conn.commit()

init_db()

while True:
    menu = """
    1. add product
    2. update product
    3. delete product
    4. show product
    """
    _key = input(menu)
    match _key:
        case '1':
            name = input('Enter product name: ')
            price = input('Enter product price: ')
            with conn.cursor() as cursor:
                q = "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING *;"
                cursor.execute(q, (name, price))
                conn.commit()
                print("Product added ", *cursor.fetchone())
        case '3':
            _id = input('Enter product ID: ')
            with conn.cursor() as cursor:
                q = "DELETE FROM products WHERE id = %s RETURNING *;"
                cursor.execute(q, (_id,))
                conn.commit()
                print("Product deleted ", *cursor.fetchone())
        case '4':
            with conn.cursor() as cursor:
                q = "SELECT * FROM products;"
                cursor.execute(q)
                for product in cursor.fetchall():
                    print(*product)

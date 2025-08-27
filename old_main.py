from models import User, Product
from models.base import db


def main(user: User):
    menu = """
    1. add product 
    2. update product 
    3. delete product 
    4. show product 
    5. show all products 
    6. exit
    """
    while True:
        _key = input(menu)
        match _key:
            case '1':
                _name = input('Product name: ')
                _price = input('Product price: ')
                product = Product.create(name=_name, price=_price, created_by_id=user.id)
                print("Added product: ", product)
            case '2':
                _id = input('Product id: ')
                _name = input('Product name: ')
                _price = input('Product price: ')
                updated_product = Product.update(_id=_id, name=_name, price=_price)
                print("Updated product: ", updated_product)
            case '5':
                products = Product.get_all()
                for product in products:
                    print(product)
                    # print(product.id, product.name, product.price, product.created_by.first_name)
            case _:
                exit()


def auth():
    menu = """
    1. register 
    2. login 
    3. exit or (any key)
    """
    while True:
        _key = input(menu)
        match _key:
            case '1':
                first_name = input('Firstname: ')
                last_name = input('Lastname: ')
                username = input('Username: ')
                password = input('Password: ')
                confirm_password = input('Confirm password: ')
                if password != confirm_password:
                    print("Passwords don't match")
                    continue
                user = User.get_by_username(username)
                if user is not None:
                    print("Username already exists")
                    continue

                user = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'username': username,
                    'password': User.get_hash_password(password)
                }
                user = User.create(**user)
                print("Successfully registered: ", user)

            case '2':
                username = input('Username: ')
                password = input('Password: ')
                user = User.get_by_username(username)
                if user is None:
                    print("Username does not exist")
                    continue
                is_valid_password = User.check_hash_password(password, user.password)
                if not is_valid_password:
                    print("Wrong password")
                    continue
                print("Login successful: ", user.first_name)
                main(user)
            case _:
                exit(1)


if __name__ == '__main__':
    db.create_all()
    auth()

"""
product owneri belgilab ketamiz

alembic
user is_verified
register pochtaga 6xonali random son yuboramiz
"""

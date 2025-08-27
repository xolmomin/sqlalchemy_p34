from datetime import datetime
import bcrypt

from sqlalchemy import Integer, String, Text, Float, create_engine, insert, select as sqlalchemy_select, \
    update as sqlalchemy_update, delete as sqlalchemy_delete, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, mapped_column, sessionmaker, declared_attr, \
    relationship


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        _name = self.__name__
        new_name = _name[0]
        for i in _name[1:]:
            if i.isupper():
                new_name += '_'
            new_name += i

        if new_name.endswith('y'):
            new_name = new_name[:-1] + 'ies'
        else:
            new_name = new_name + 's'
        return new_name.lower()


class Database:

    def __init__(self):
        self._engine = None
        self._session = None

    def init(self):
        self._engine = create_engine('postgresql://postgres:1@localhost:5432/p34_db')
        self._session = sessionmaker(self._engine, expire_on_commit=False)()

    def __getattr__(self, item):
        return getattr(self._session, item)

    def create_all(self):
        Base.metadata.create_all(self._engine)

    def drop_all(self):
        Base.metadata.drop_all(self._engine)


db = Database()
db.init()


class AbstractClass:
    @classmethod
    def commit(cls):
        try:
            db.commit()
        except Exception as e:
            db.rollback()

    @classmethod
    def create(cls, **kwargs):
        _obj = cls(**kwargs)
        db.add(_obj)
        cls.commit()
        return _obj

    @classmethod
    def get_all(cls):
        query = sqlalchemy_select(cls)
        results = db.execute(query)
        return results.scalars()

    @classmethod
    def get(cls, _id):
        query = sqlalchemy_select(cls).where(cls.id == _id)
        results = db.execute(query)
        return results.scalar()

    @classmethod
    def update(cls, _id, **kwargs):
        query = sqlalchemy_update(cls).where(cls.id == _id).values(**kwargs).returning(cls)
        new_obj = db.execute(query)
        cls.commit()
        return new_obj.scalar()

    @classmethod
    def delete(cls, _id):
        query = sqlalchemy_delete(cls).where(cls.id == _id).returning(cls)
        new_obj = db.execute(query)
        cls.commit()
        return new_obj.scalar()

    @classmethod
    def truncate(cls):
        query = sqlalchemy_delete(cls).returning(cls)
        new_obj = db.execute(query)
        cls.commit()
        return new_obj.scalars()


class Model(AbstractClass, Base):
    __abstract__ = True


class User(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='created_by')

    def __str__(self):
        return f"{self.id} - {self.username}"

    @classmethod
    def get_by_username(cls, _username: str):
        query = sqlalchemy_select(cls).where(cls.username == _username)
        results = db.execute(query)
        return results.scalar()

    @staticmethod
    def get_hash_password(_password: str):
        hashed_password = bcrypt.hashpw(_password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def check_hash_password(_password: str, hashed_password: str):
        return bcrypt.checkpw(_password.encode(), hashed_password.encode())


class Product(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_by: Mapped['User'] = relationship('User', back_populates='products')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __str__(self):
        return f"{self.id} - {self.name}"


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
                product = Product.create(name=_name, price=_price, created_by=user.id)
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
                    print(product.id, product.name, product.price, product.created_by.first_name)
            case _:
                exit()


def auth():
    user = None
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

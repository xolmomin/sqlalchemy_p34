from sqlalchemy import Integer, String, Text, Float, create_engine, insert, select as sqlalchemy_select, \
    update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, mapped_column, sessionmaker, declared_attr


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


class Category(Model):
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    def __str__(self):
        return f"{self.id} - {self.name}"


def main():
    # db.create_all()
    # db.drop_all()
    menu = """
    1. add category 
    2. update category 
    3. delete category 
    4. show all categories 
    5. exit
    """
    while True:
        _key = input(menu)
        match _key:
            case '1':
                _name = input('Category name: ')
                category = Category.create(name=_name)
                print("Added category: ", category)

            case '2':
                _id = input('Category id: ')
                _name = input('Category name: ')
                category = Category.update(_id, name=_name)
                print("Updated category: ", category)
            case '3':
                _id = input('Category id: ')
                category = Category.delete(_id)
                print("Deleted category: ", category)
            case '4':
                categories = Category.get_all()
                for category in categories:
                    print(category)
            case '5':
                exit()
            case _:
                print("Invalid input")
    # Product.create(name='Uzum')  # Create
    # products = Product.get_all()  # Read
    # for product in products:
    #     print(product)
    # product = Product.get(1) # Read
    # print(product.name)
    # product = Product.update(2, name='Kok olma')  # Update
    # product = Product.delete(1)
    # print(product)


if __name__ == '__main__':
    db.create_all()
    main()

"""
models ni ajratish
config yozish
relationship sqlalchemy

aiogram
"""

# db.add(Product())
# db.add(Category())
#
# db.add(Category(name='Yangi'))
# db.commit()
#
# q = delete(Category).where(Category.id == 6)
# db.execute(q)
# db.commit()
#
# # Create
# with Session() as session:
#     # session.add(Category(name='Uy-joy'))
#     category_list = [Category(name='Texnika'), Category(name='Mevalar')]
#     session.add_all(category_list)
#     session.commit()

# # Read
# with Session() as session:
#     categories = session.scalars(select(Category))
#     for category in categories:
#         print(category)

# # Update
# with Session() as session:
#     query = update(Category).where(Category.id == 5).values(name='Qurilish')
#     session.execute(query)
#     session.commit()

# # Delete
# with Session() as session:
#     query = delete(Category).where(Category.id == 4)
#     session.execute(query)
#     session.commit()

# # Create
# with engine.connect() as conn:
#     query = insert(Category).values(
#         name='Uy-joy',
#         description='zor 123',
#         price=7.99,
#         slug='texnika1'
#     )
#     conn.execute(query)
#     conn.commit()

# # Read
# with engine.connect() as conn:
#     query = select(Category)
#     results = conn.execute(query).fetchall()
#     for i in results:
#         print(i)
#

# # Update
# with engine.connect() as conn:
#     query = update(Category).where(Category.id == 2).values(description='...')
#     conn.execute(query)
#     conn.commit()


# # Update
# with engine.connect() as conn:
#     query = delete(Category).where(Category.id == 2)
#     conn.execute(query)
#     conn.commit()
#


"""

#Homework
User(first_name, last_name, username, password)


1. register
2. login (username, password)
    1. add product
    2. delete product
    3. update product
    4. show products
    5. show one product
    5. logout
3. exit

"""
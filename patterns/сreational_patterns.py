from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect
from patterns.architectural_system_pattern_unit_of_work import DomainObject
from patterns.behavioral_patterns import FileWriter, Subject


# abstract user
class User:
    def __init__(self, name):
        self.name = name


# Admin
class Admin(User):
    pass


# content creator
class ContentCreator(User):
    pass


# content consumer
class Customer(User, DomainObject):
    def __init__(self, name):
        # self.content = []
        super().__init__(name)


class UserFactory:
    types = {
        'admin': Admin,
        'content creator': ContentCreator,
        'user': Customer,
    }

    # generating pattern Factory method
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# generating pattern Prototype
class ContentPrototype:
    # content prototype

    def clone(self):
        return deepcopy(self)


class Content(ContentPrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.content.append(self)
        self.customers = []
        super().__init__()

    def __getitem__(self, item):
        return self.customers[item]
    
    def add_customer(self, customer: Customer):
        self.customers.append(customer)
        # customer.content.append(self)
        self.notify()
        

# the first type of content
class FirstTypeContent(Content):
    pass


# the second type of content
class SecondTypeContent(Content):
    pass


class ContentFactory:
    types = {
        'first type': FirstTypeContent,
        'second type': SecondTypeContent,
    }

    # generating pattern Factory method
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# category
class CategoryContent:
    auto_id = 0

    def __init__(self, name, category):
        self.id = CategoryContent.auto_id
        CategoryContent.auto_id += 1
        self.name = name
        self.category = category
        self.content = []

    def content_count(self):
        result = len(self.content)
        if self.category:
            result += self.category.content_count()
        return result


# the main interface of the project
class Engine:
    def __init__(self):
        self.admin = []
        self.content_creator = []
        self.customers = []
        self.content = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return CategoryContent(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_content(type_, name, category):
        return ContentFactory.create(type_, name, category)

    def get_content(self, name):
        for item in self.content:
            if item.name == name:
                return item
        return None
    
    def get_customer(self, name) -> Customer:
        for item in self.customers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# Singleton generating pattern
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class CustomerMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'customer'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            customer = Customer(name)
            customer.id = id
            result.append(customer)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Customer(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


# architectural system pattern - Data Mapper
class MapperRegistry:
    mappers = {
        'customer': CustomerMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Customer):

            return CustomerMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

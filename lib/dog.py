import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    all=[]
    
    def __init__(self,name,breed):
        self.name=name
        self.breed=breed
        self.id=None

    @classmethod
    def create_table(cls):
        sql="""
        CREATE TABLE IF NOT EXISTS dogs(
        id INTEGER PRIMARY KEY,
        name TEXT,
        breed TEXT
        )       
        """ 
        CURSOR.execute(sql)
        CONN.commit()
    @classmethod
    def drop_table(cls):
        sql="""
        DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql="""
        INSERT INTO dogs(name,breed)
        VALUES (?,?)
        """
        CURSOR.execute(sql,(self.name,self.breed)) 
        self.id=CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0] 

    @classmethod
    def create(cls,name,breed):
              dog=Dog(name,breed)
              dog.save()
              dog_id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
              dog_with_id = cls.find_by_id(dog_id)
              return dog_with_id
    
    @classmethod
    def new_from_db(cls,row):
         dog=cls(row[1],row[2])
         dog.id=row[0]
         return dog
    @classmethod
    def get_all(cls):
         sql="""SELECT * FROM dogs"""

         all=CURSOR.execute(sql).fetchall()
         cls.all=[cls.new_from_db(row)for row in all]
         return cls.all
    @classmethod
    def find_by_name(cls,name):
         sql="""
         SELECT *
         FROM dogs
         WHERE name=?
         LIMIT 1
         """ 
         dog=CURSOR.execute(sql,(name,)).fetchone()
         return cls.new_from_db(dog) 
    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
        SELECT * FROM dogs
        WHERE id = ?
        """
        dog_found = CURSOR.execute(sql, (dog_id,))
        for dog in dog_found:
            return cls.new_from_db(dog)
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
        SELECT * FROM dogs WHERE name = ? and breed = ?
        """
        dogs = CURSOR.execute(sql,(name, breed))
        if dogs is None:
            print("dog found")
            for dog in dogs:
                return Dog.new_from_db(dog)
        else:
            print("no dog found")
            created_dog = Dog.create(name, breed)
            return created_dog
    
        


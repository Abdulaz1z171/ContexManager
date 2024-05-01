import psycopg2
db_parameters = {
    'host' : 'localhost',
    'database' : 'my_project',
    'user' : 'postgres',
    'password' : 'temur_1336',
    'port' : 5432
}

# DbConnect contex manager yaratamiz
class DbConnect:
    def __init__(self,db_parameters):
        # print('Init function called')
        self.db_parameters = db_parameters
        self.conn = psycopg2.connect(**db_parameters)
    
    def __enter__(self):
        # print('Enter function called')
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self,exc_tb,exc_type,exc_val):
        if self.conn and not self.conn.closed:
            self.conn.commit()
            self.conn.close()

# Perso  degan class yaratamiz 
class Person:
    def __init__(self,
                id:int|None = None,
                full_name:str|None = None,
                age:int|None = None,
                email:str|None = None
                ):
                self.id = id
                self.full_name = full_name
                self.age = age
                self.email = email

    # save degan methodimizda classdan object oganimizni bazaga saqlaydi
    def save(self):
        with DbConnect(db_parameters) as cur:
            insert_query = 'INSERT INTO person(full_name,age,email)  VALUES (%s,%s,%s);'
            insert_parametres = (self.full_name,self.age,self.email)
            cur.execute(insert_query,insert_parametres)
            print('Insert 0 1')

#   get_all bazadagi hamma malumotlarni people degan listga saqlab consolga chiqaruvchi funksiya
    def get_all(self):
        with DbConnect(db_parameters) as cur:
             select_query = 'SELECT * FROM person;'
             cur.execute(select_query)
             people:List[Person] = []
             for human in cur.fetchall():
                people.append(Person(id = human[0],full_name=human[1],age = human[2],email = human[3]))

        return people

#  Bazada faqaat bitta odamni qiymatini oluvchi funksiya
    def get_person(self):
        with DbConnect(db_parameters) as cur:
             select_query = 'SELECT * FROM person WHERE id = %s;'
             person_id = int(input('Enter id! '))
             cur.execute(select_query,(person_id,))
             return cur.fetchone()

# Bazadagi malumotni id orqali uchiradigan funksiya 
    def delete(self):
         with DbConnect(db_parameters) as cur:
            
            delete_query = 'DELETE FROM person WHERE id = %s'
            person_id = int(input('Enter id! '))
            cur.execute(delete_query,(person_id,))
            print(f'{person_id} id succesfully deleted')

# Bazadagi ma'lumotni id si orqali update qiladigan funksiya
    def update(self):

        with DbConnect(db_parameters) as cur:
            select_query = 'SELECT * FROM person;'
            cur.execute(select_query)
            print(cur.fetchall())
            update_query = 'UPDATE person SET full_name = %s,age = %s,email = %s WHERE id = %s'
            full_name = input('Enter full name! ')
            age = int(input('Enter age!'))
            email = input('Enter email! ')
            person_id = int(input('Enter id! '))
            data = (full_name,age,email,person_id)
            cur.execute(update_query,data)
            print(f'This {person_id} succesfully updated')




# Consolga chiroyliroq qilib chiqarib beruchi dunder method
    def __repr__(self):
        return f'''
Person(ID: {self.id}, Full name: {self.full_name}, Age: {self.age}, Email: {self.email})'''


# print(Person().get_person())

# person1 = Person(full_name = 'Megliyev Sherzod',age = 38,email = 'msherzod@gmail.com')
# person1.save()
# person2 = Person(full_name = 'Adxam Tursunov',age = 35,email = 'atursunov@gmail.com')
# person2.save()

Person().update()
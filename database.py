'''
Reference: https://youtu.be/pd-0G0MigUA

Code Template - https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-SQLite/employee.py
'''

import sqlite3
from customer import Customer

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE customers (
            phone integer PRIMARY KEY,
            name text,
            address text,
            email text,
            online_orders integer DEFAULT 0,
            total_online_purchase_amount real DEFAULT 0,
            offline_orders integer DEFAULT 0,
            total_offline_purchase_amount real DEFAULT 0
            )""")


def insert_customer(cust):
    '''method to insert customer details into the database'''
    with conn:
        c.execute("INSERT INTO customers (phone, name, address, email, online_orders, offline_orders) \
                                         VALUES (   :phone, \
                                                    :name, \
                                                    :address, \
                                                    :email, \
                                                    :online_orders, \
                                                    :offline_orders )", 
                                                    {'phone': cust.phone, 
                                                    'name': cust.name, 
                                                    'address': cust.address,
                                                    'email': cust.email,
                                                    'online_orders': cust.online_orders,
                                                    'offline_orders': cust.offline_orders})



def get_cust_by_phone(phone):
    '''method to get customer details by phone number'''
    c.execute("SELECT * FROM customers WHERE phone=:phone", {'phone': phone})
    return c.fetchone()


def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})


cust_1 = Customer(8447389366, 
                 'Anubhav', 
                 'Flat 1523, Block C, Sector 7, Gurgaon',
                 'anubhavpatrick@gmail.com',
                 0,
                 0.0,
                 0,
                 0.0)
#emp_2 = Employee('Jane', 'Doe', 90000)

insert_customer(cust_1)
#insert_emp(emp_2)

cust = get_cust_by_phone(8447389368)
print(cust)

'''update_pay(emp_2, 95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)
'''
conn.close()



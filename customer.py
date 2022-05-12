'''
Code Template -
https://github.com/CoreyMSchafer/code_snippets/blob/master/Python-SQLite/employee.py
'''


class Customer:
    def __init__(self, 
                phone, 
                name, 
                email, 
                address, 
                total_online_orders = 0, 
                total_offline_orders = 0,
                total_online_purchase_amount = 0,
                total_offline_purchase_amount = 0):

        self.phone = phone
        self.name = name
        self.address = address 
        self.email = email
        self.online_orders = total_online_orders
        self.total_online_purchase_amount = total_online_purchase_amount
        self.offline_orders = total_offline_orders
        self.total_offline_purchase_amount = total_offline_purchase_amount



'''
A module for GUI for customer sales
'''

from pywebio.input import input, select, radio,input_group, actions, NUMBER, TEXT, FLOAT
from pywebio import start_server #for quick testing
from pywebio.output import put_markdown, put_table,clear, put_button,put_row
from pywebio.platform.flask import webio_view
from flask import Flask
import datetime


order_no = 1

#variables to temporarily store product details entered by user
product_quantity_temp = 1
original_price_per_item_temp = 0
discount_overall_temp = 0

def put_header():
    '''method to put header on each page'''
    
    #Headers for the GUI
    put_markdown("# Welcome to the `Neo Dash ERP` v0.3")
    put_markdown("*Made with ❤️ by [Anubhav Patrick](https://www.linkedin.com/in/anubhavpatrick/)*")
    put_markdown(f"### Order No: *{order_no}*")
    put_markdown(f"### Date: *{datetime.datetime.now().strftime('%d-%m-%Y')}*")

def customer_info_GUI():
    '''method to create a GUI for customer sales'''
    put_header()
    customer_info = input_group("Enter Customer Details:", [
        input("Customer Phone Number:", type=NUMBER, required=True, name = "cust_phone",validate = lambda x: None if len(str(x)) == 10 else 'Phone number must be 10 digits'),
        input("Customer Name", type= TEXT,name = "cust_name", placeholder="Anonymous", help_text="This field is optional", required=False, value = "Anonymous"),
        radio("Pet Type", name="pet_type", value="Dog", options=["Dog", "Cat", "Bird", "Other"], required=True),
        radio("Payment Method", name="payment_method", options=["Cash", "Card", "PayTM/GPay/PhonePay"], required=True, value="Cash"),
    ], cancelable=True)
    clear()
    return customer_info

def product_detail_GUI():
    '''method to input product(s) details
    
    Returns: A tuple containing 
        -dictionary of product details
        -product count
        -total price
    '''

    ch = "Yes"
    product_count = 0
    products_dict = dict()

    while ch== "Yes":
        put_header()
        product_count += 1
        info = input_group(f"Enter Details of Product #{product_count}:", [
            select("Product Category", ["Accessory", "Bowls", "Food", "Dental", "Shampoo/Conditioner", "Toys", "Treats","Other"], name=f"product_category_{product_count}", required=True),
            input("Product Name", type=TEXT, name=f"product_name_{product_count}", placeholder = "Beautiful Product", help_text="This field is optional", value="Beautiful Product", required=False),
            input("Product Quantity", type=NUMBER, name=f"product_quantity_{product_count}", placeholder = "1", help_text="This field is optional", value="1", required=False, onchange=update_product_quantity),
            input("Original Price (Per Item)", type= NUMBER,name = f"original_price_{product_count}", validate = lambda x: None if x >= 0 else 'Price must be greater than 0', help_text="This field is optional", value=0,  onchange= update_original_price_per_item),
            input("Discount %", type= NUMBER,name = f"discount_{product_count}", validate = lambda x: None if x >= 0 and x <= 100 else 'Discount must be between 0 and 100', help_text="This field is optional", value=0, onchange= update_overall_discount),
            input("Final Price (Overall)", type= FLOAT,name = f"final_price_{product_count}", required=True, value =0, placeholder=0, action = ('Calculate',calculate_final_price))
            ], cancelable=True)
        products_dict.update(info)

        #display purchase summary
        clear()
        total_price = purchase_running_summary_GUI(products_dict,product_count)

        ch = actions('Do you want to add more items', ['Yes', 'No'], help_text="Do note you can update the final details of the products later")
        clear()

    return products_dict, product_count, total_price

def update_product_quantity(x):
    global product_quantity_temp
    product_quantity_temp = x

def update_original_price_per_item(x):
    global original_price_per_item_temp
    original_price_per_item_temp = x

def update_overall_discount(x):
    global discount_overall_temp
    discount_overall_temp = x

def calculate_final_price(set_value):
    '''method to calculate final price of the product'''
    set_value(original_price_per_item_temp * product_quantity_temp - (original_price_per_item_temp * product_quantity_temp * discount_overall_temp / 100))

def purchase_running_summary_GUI(products_dict, pc):
    '''method to generate purchase summary of the products added till now
    
    Args:
        products_dict: A dictionary containing product details
        pc: product count
        
    Returns:
        total_price: total price of the products added till now
    '''

    put_header()
    total_price = 0
    put_markdown("### Purchase Summary")
    for product_count in range(1, pc+1):
        put_table([[f"# Product Number:",product_count],
                [f"Product Category:",products_dict[f"product_category_{product_count}"]],
                [f"Product Name:",products_dict[f"product_name_{product_count}"]],
                [f"Original Price:",products_dict[f"original_price_{product_count}"]],
                [f"Discount %:",products_dict[f"discount_{product_count}"]],
                [f"Final Price:",products_dict[f"final_price_{product_count}"]],
                ])
        total_price += products_dict[f"final_price_{product_count}"]
    put_markdown(f"### Total Price: *{total_price}*")
    return total_price
    
def final_purchase_summary_GUI(customer_info, products_dict, product_count, total_price):
    '''method to display final summary of the products

    Args: 
        customer_info: A dictionary containing customer details
        products_dict: A dictionary containing product details
        product_count: product count'''

    #Headers for the GUI
    put_markdown("# Welcome to the `Neo Dash ERP` v0.3")
    put_markdown("*Made with ❤️ by [Anubhav Patrick](https://www.linkedin.com/in/anubhavpatrick/)*")

    customer_receipt_str = f"""# <center>NeoDash Pet Universe</center> \n \
                *<p align='center'>Near Signature Homes Market, Main Road, Raj Nagar Extension, Ghaziabad, Uttar Pradesh-201017</p>* \
                *<p align='center'>Phone - 8929570427</p>* \n \
                ### Order Details: \n \
                *Date : {datetime.datetime.now().strftime('%d-%m-%Y')}* \n \
                *Order Number : {order_no}* \n \
                *Customer Name: {customer_info["cust_name"]}* \n \
                *Customer Phone Number: {customer_info["cust_phone"]}* \n \
                *Payment Method: {customer_info["payment_method"]}* \n\n \
                """
    
    put_markdown(customer_receipt_str)

    #create a list of lists for purchased products
    purchased_products = []
    for product_count in range(1, product_count+1):
        temp = []
        temp.append(product_count)
        temp.append(products_dict[f"product_category_{product_count}"])
        temp.append(products_dict[f"product_name_{product_count}"])
        temp.append(products_dict[f"product_quantity_{product_count}"])
        temp.append(products_dict[f"original_price_{product_count}"])
        temp.append(products_dict[f"discount_{product_count}"])
        temp.append(products_dict[f"final_price_{product_count}"])
        purchased_products.append(temp)

    put_table(tdata = purchased_products ,
        header =["SNo", "Product Category", "Product Name", "Quantity","Original Price", "Discount %", "Discounted Price"])

    put_markdown(f"""\n<h3><p align='right'>Total Price: {total_price}</p></h3>
    <i><p align='center'>Thank You For Shopping With Us!</p></i>""")

    '''put_buttons([dict(label = 'Generate and Log Final Receipt', color='success', value ='generate'), 
                dict(label ='Cancel and Restart', color = 'danger', value ='cancel')],onclick=None)
    '''
    put_row([None, put_button(label = 'Generate and Log Final Receipt', color='success', onclick=None), 
                put_button(label ='Cancel and Restart', color = 'danger',onclick=None)], size ='23% 30% 47%')


def create_purchase_report(customer_info, products_dict, product_count, total_price):
    pass




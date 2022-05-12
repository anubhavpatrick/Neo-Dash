'''
A module for GUI for customer sales
'''

from functools import partial
from pywebio.input import input, select, radio,input_group, actions, NUMBER, TEXT, FLOAT
from pywebio import start_server #for quick testing
from pywebio.output import put_markdown, put_table,clear, put_button,put_row, put_tabs, put_link, span, put_buttons, toast, put_image
from pywebio.platform.flask import webio_view
from pywebio.session import eval_js
from flask import Flask
import datetime


order_no = 0

#variables to temporarily store product details entered by user
product_quantity_temp = 1
original_price_per_item_temp = 0
discount_overall_temp = 0

#total price
total_price = 0

#product count of the products entered by user
product_count = 0

#tax calculation
tax = 0
total_price_after_tax = 0


def set_tax(x):
    global tax
    tax = x


def set_total_price_after_tax(tp = None):
    global total_price_after_tax
    if tp is None:
        total_price_after_tax = total_price + (tax/100.0 * total_price)
    else:
        total_price_after_tax = tp


def set_product_count(x):
    global product_count
    product_count = x


def set_order_no(o):
    global order_no 
    order_no = o

def put_header_minimal():
    '''method to put minimal header containing name and develper info'''
    put_markdown("# Welcome to the `Neo Dash ERP` v0.5")
    put_markdown("*Made with ❤️ by [Anubhav Patrick](https://www.linkedin.com/in/anubhavpatrick/)*")

def put_header():
    '''method to put header on each page'''
    put_header_minimal()

    #Headers for the GUI
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
    products_dict = dict()

    while ch== "Yes":
        put_header()
        pc = product_count + 1
        info = input_group(f"Enter Details of Product #{pc}:", [
            select("Product Category", ["Accessory", "Bowls", "Food", "Dental", "Shampoo/Conditioner", "Toys", "Treats","Other"], name=f"product_category_{pc}", required=True),
            input("Product Name", type=TEXT, name=f"product_name_{pc}", placeholder = "Beautiful Product", help_text="This field is optional", value="Beautiful Product", required=False),
            input("Product Quantity", type=NUMBER, name=f"product_quantity_{pc}", placeholder = "1", help_text="This field is optional", value="1", required=False, onchange=update_product_quantity),
            input("Original Price (Per Item)", type= NUMBER,name = f"original_price_{pc}", validate = lambda x: None if x >= 0 else 'Price must be greater than 0', help_text="This field is optional", value=0,  onchange= update_original_price_per_item),
            input("Discount %", type= FLOAT,name = f"discount_{pc}", validate = lambda x: None if x >= 0 and x <= 100 else 'Discount must be between 0 and 100', help_text="This field is optional", value=0, onchange= update_overall_discount),
            input("Final Price (Overall)", type= FLOAT,name = f"final_price_{pc}", required=True, value =0, placeholder=0, action = ('Calculate',calculate_final_price))
            ], cancelable=True)

        #Update global product count
        set_product_count(pc)

        products_dict.update(info)

        #display purchase summary
        purchase_running_summary_GUI(products_dict)

        #Reset the global variables for product quantity, product price and discount
        update_product_quantity(1)
        update_overall_discount(0)
        update_original_price_per_item(0)

        ch = actions('Do you want to add more items', ['Yes', 'No'], help_text="Do note you can update the final details of the products later")
        clear()

    return products_dict


def update_product_quantity(x):
    global product_quantity_temp
    product_quantity_temp = x


def update_original_price_per_item(x):
    global original_price_per_item_temp
    original_price_per_item_temp = x


def update_overall_discount(x):
    global discount_overall_temp
    discount_overall_temp = x


def update_total_price(x):
    global total_price
    total_price = x


def calculate_final_price(set_value):
    '''method to calculate final price of the product'''
    set_value(original_price_per_item_temp * product_quantity_temp - (original_price_per_item_temp * product_quantity_temp * discount_overall_temp / 100))


def purchase_running_summary_GUI(products_dict):
    '''method to generate purchase summary of the products added till now
    
    Args:
        products_dict: A dictionary containing product details
        pc: product count
        
    Returns:
        total_price: total price of the products added till now
    '''

    clear()
    put_header()
    global total_price
    total_price = 0
    put_markdown("### Purchase Summary")
    for pc in range(1, product_count+1):
        try:
            put_table([[f"# Product Number:",pc],
                [f"Product Category:",products_dict[f"product_category_{pc}"]],
                [f"Product Name:",products_dict[f"product_name_{pc}"]],
                [f"Product Quantity:",products_dict[f"product_quantity_{pc}"]],
                [f"Original Price Per Item:",products_dict[f"original_price_{pc}"]],
                [f"Discount %:",products_dict[f"discount_{pc}"]],
                [f"Final Price:",products_dict[f"final_price_{pc}"]],
                [span(put_buttons([{"label":"Edit", "value":f"Edit_{pc}",
                    "color":"warning","disabled":False}, {"label":"Delete", "value":f"Delete_{pc}",
                    "color":"danger","disabled":False}], 
                    onclick=partial(edit_delete_products,pc,products_dict)),col = 2)]
                ])
            total_price = total_price + products_dict[f"final_price_{pc}"]
        except KeyError as k:
            put_markdown(f"No Product is added yet")
            set_product_count(0)
    put_markdown(f"### Total Price: *{total_price}*")

    
def edit_delete_products(product_number, products_dict, action):
    '''method to edit or delete products
    
    Args:
        action: action to be performed
        product_dict: A dictionary containing product details
        product_number: number of the product to be edited or deleted
    '''
    if action == f"Edit_{product_number}":
        clear()
        put_header()
        put_markdown(f"### Edit Product #{product_number}")
        info = input_group(f"Update Details of Product #{product_number}:", [
            select("Product Category", ["Accessory", "Bowls", "Food", "Dental", "Shampoo/Conditioner", "Toys", "Treats","Other"], name=f"product_category_{product_number}", value= products_dict[f"product_category_{product_number}"], required=True),
            input("Product Name", type=TEXT, name=f"product_name_{product_number}", help_text="This field is optional", value= products_dict[f"product_name_{product_number}"], required=False),
            input("Product Quantity", type=NUMBER, name=f"product_quantity_{product_number}", placeholder =  products_dict[f"product_quantity_{product_number}"], help_text="This field is optional", value = products_dict[f"product_quantity_{product_number}"], required=False, onchange=update_product_quantity),
            input("Original Price (Per Item)", type= NUMBER,name = f"original_price_{product_number}",  help_text="This field is optional", value=products_dict[f"original_price_{product_number}"], onchange= update_original_price_per_item),
            input("Discount %", type= FLOAT,name = f"discount_{product_number}", value=products_dict[f"discount_{product_number}"], help_text="This field is optional", onchange= update_overall_discount),
            input("Final Price (Overall)", type= FLOAT,name = f"final_price_{product_number}", value=products_dict[f"final_price_{product_number}"], required=True, placeholder=0, action = ('Calculate',calculate_final_price))
            ], cancelable=True)
        products_dict[f"product_category_{product_number}"] = info[f"product_category_{product_number}"]
        products_dict[f"product_name_{product_number}"] = info[f"product_name_{product_number}"]
        products_dict[f"product_quantity_{product_number}"] = info[f"product_quantity_{product_number}"]
        products_dict[f"original_price_{product_number}"] = info[f"original_price_{product_number}"]
        products_dict[f"discount_{product_number}"] = info[f"discount_{product_number}"]
        products_dict[f"final_price_{product_number}"] = info[f"final_price_{product_number}"]
        toast("Product Details Updated")
        purchase_running_summary_GUI(products_dict)
        clear()

    elif action == f"Delete_{product_number}":
        for i in range(product_number, product_count):
            products_dict[f"product_category_{i}"] = products_dict[f"product_category_{i+1}"]
            products_dict[f"product_name_{i}"] = products_dict[f"product_name_{i+1}"]
            products_dict[f"product_quantity_{i}"] = products_dict[f"product_quantity_{i+1}"]
            products_dict[f"original_price_{i}"] = products_dict[f"original_price_{i+1}"]
            products_dict[f"discount_{i}"] = products_dict[f"discount_{i+1}"]
            products_dict[f"final_price_{i}"] = products_dict[f"final_price_{i+1}"]
        del products_dict[f"product_category_{product_count}"]
        del products_dict[f"product_name_{product_count}"]
        del products_dict[f"product_quantity_{product_count}"]
        del products_dict[f"original_price_{product_count}"]
        del products_dict[f"discount_{product_count}"]
        del products_dict[f"final_price_{product_count}"]
        #Notice the value 2 is subtracted from product_count due to logic in customer_sales_GUI
        set_product_count(product_count-1) 
        toast("Product Details Deleted")
        clear()
        purchase_running_summary_GUI(products_dict)



def final_purchase_summary_GUI(customer_info, products_dict):
    '''method to display final summary of the products

    Args: 
        customer_info: A dictionary containing customer details
        products_dict: A dictionary containing product details
        product_count: product count'''

    #Headers for the GUI
    put_header_minimal()

    set_total_price_after_tax()

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
    for pc in range(1, product_count+1):
        temp = []
        temp.append(pc)
        temp.append(products_dict[f"product_category_{pc}"])
        temp.append(products_dict[f"product_name_{pc}"])
        temp.append(products_dict[f"product_quantity_{pc}"])
        temp.append(products_dict[f"original_price_{pc}"])
        temp.append(products_dict[f"discount_{pc}"])
        temp.append(products_dict[f"final_price_{pc}"])
        purchased_products.append(temp)

    put_table(tdata = purchased_products ,
        header =["SNo", "Product Category", "Product Name", "Quantity","Original Price", "Discount %", "Discounted Price"])

    put_markdown(f"""\n<h3><p align='right'>Total Price: {total_price}</p></h3>
    <p align='right' style='color:red;'>Tax (GST/CGST): {tax}%</p></h3>
    <h3><p align='right' style='color:green;'>Total Price After Tax: {total_price_after_tax:.2f}</p></h3>
    <i><p align='center'>Thank You For Shopping With Us!</p></i>""")
    
    put_row([put_button(label ='Enter or Update Tax Details', color = 'primary',onclick=partial(add_tax, customer_info, products_dict)), 
                put_button(label = 'Update Product Details', color='warning', onclick=partial(update_product_detail_GUI, products_dict)),
                put_button(label = 'Manually Update Final Price', color='warning', onclick=partial(manually_update_final_price, customer_info, products_dict)),
                put_button(label = 'Generate & Log Final Receipt', color='success', onclick=partial(generate_final_receipt_and_log)), 
                put_button(label ='Cancel and Restart', color = 'danger',onclick=pageReload),
                ])


def add_tax(customer_info, products_dict):
    '''method to add tax to the total price'''
    '''input
    global total_price
    total_price = total_price + (total_price * 0.18)
    toast("Tax Added")
    purchase_running_summary_GUI(products_dict)'''
    t = input("Enter Tax %: ", type = FLOAT, validate = lambda x: None if x >= 0 and x <= 100 else 'Tax must be between 0 and 100')
    set_tax(t)
    set_total_price_after_tax()
    clear()
    final_purchase_summary_GUI(customer_info, products_dict)


def manually_update_final_price(cutomer_info, products_dict):
    updated_final_price = input("Enter Updated Final Price (including Tax) %: ", type = FLOAT, validate = lambda x: None if x >= 0 else 'Final price (after tax) must be between > Rs 100')
    set_total_price_after_tax(updated_final_price)
    clear()
    final_purchase_summary_GUI(cutomer_info, products_dict)


def update_product_detail_GUI(products_dict):
    '''method to update/insert new product(s) details after items were added and final summary is generated
    It then calls the final summary GUI to display the summary of updated product details
    
    Returns: 
        None 
    '''

    #display purchase summary
    purchase_running_summary_GUI(products_dict)

    #Reset the global variables for product quantity, product price and discount
    update_product_quantity(1)
    update_overall_discount(0)
    update_original_price_per_item(0)

    ch = actions('Do you want to add more items', ['Yes', 'No'], help_text="Do note you can update the final details of the products later")
    clear()
    
    while ch== "Yes":
        put_header()
        pc = product_count + 1
        info = input_group(f"Enter Details of Product #{pc}:", [
            select("Product Category", ["Accessory", "Bowls", "Food", "Dental", "Shampoo/Conditioner", "Toys", "Treats","Other"], name=f"product_category_{pc}", required=True),
            input("Product Name", type=TEXT, name=f"product_name_{pc}", placeholder = "Beautiful Product", help_text="This field is optional", value="Beautiful Product", required=False),
            input("Product Quantity", type=NUMBER, name=f"product_quantity_{pc}", placeholder = "1", help_text="This field is optional", value="1", required=False, onchange=update_product_quantity),
            input("Original Price (Per Item)", type= NUMBER,name = f"original_price_{pc}", validate = lambda x: None if x >= 0 else 'Price must be greater than 0', help_text="This field is optional", value=0,  onchange= update_original_price_per_item),
            input("Discount %", type= FLOAT,name = f"discount_{pc}", validate = lambda x: None if x >= 0 and x <= 100 else 'Discount must be between 0 and 100', help_text="This field is optional", value=0, onchange= update_overall_discount),
            input("Final Price (Overall)", type= FLOAT,name = f"final_price_{pc}", required=True, value =0, placeholder=0, action = ('Calculate',calculate_final_price))
            ], cancelable=True)

        #Update global product count
        set_product_count(pc)

        products_dict.update(info)

        #display purchase summary
        purchase_running_summary_GUI(products_dict)

        #Reset the global variables for product quantity, product price and discount
        update_product_quantity(1)
        update_overall_discount(0)       
        update_original_price_per_item(0)

        ch = actions('Do you want to add more items', ['Yes', 'No'], help_text="Do note you can update the final details of the products later")
        clear()

    final_purchase_summary_GUI(products_dict)


def generate_final_receipt_and_log():#customer_info, products_dict, total_price, order_no):
    '''clear()
    put_header_minimal()
    try:
        save_as_xlsx.generate_final_receipt_and_log(customer_info, products_dict, product_count, total_price, order_no)
        put_markdown("- *Receipt succesfully generated and logged!*")
        display_additional_options()
    except Exception as e:
        put_markdown(f"""### Error in generating final receipt and logging!!!\n \
                        {str(e)} \n\
                        *Please contact admin [Anubhav Patrick](https://www.linkedin.com/in/anubhavpatrick/) 😎 for further assistance* """)
'''
    put_image("https://media.giphy.com/media/LQXPmp4hdcwPRue8b3/giphy.gif")

def pageReload():
    eval_js("location.reload()")


def display_additional_options():
    '''method to display additional options for the user'''
    put_markdown("### What would you like to do next? \n ")
    put_tabs([
    {'title': 'Download Receipt', 'content': 'Hello world'},
    {'title': 'Send SMS to Customer', 'content': put_markdown('~~Strikethrough~~')},
    {'title': 'Send Email to Customer', 'content': [
        put_table([
            ['Commodity', 'Price'],
            ['Apple', '5.5'],
            ['Banana', '7'],
        ]),
        put_link('pywebio', 'https://github.com/wang0618/PyWebIO')
    ]},
    ])

    put_button(label = 'Cancel and Restart', color='danger', onclick=pageReload)

def create_purchase_report(customer_info, products_dict, product_count, total_price):
    pass




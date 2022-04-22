'''
A module containing helper methods for the application
'''

from tabulate import tabulate
import datetime

def convert_list_to_table(product_list, product_header_details=["Sno", "Prod\nCategory", "Product\nName", "Quantity", "Original\nPrice", "Discount\n%", "Final\nPrice"]):
    '''
    A method to convert a list to a table
    Reference -https://stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
    '''
    product_list_str = tabulate(product_list, headers= product_header_details, tablefmt="fancy_grid")
    return product_list_str

def create_sales_summary_html(customer_info, products_dict, product_count, total_price, txt):
    '''method to create final sales summary of the products in HTML

    Args: 
        products_dict: A dictionary containing product details
        product_count: product count'''
    customer_receipt_str_html = f"""<html><body><h1> <center>NeoDash Pet Universe</center></h1> <br> \
                <i><p align='center'>Near Signature Homes Market, Main Road, Raj Nagar Extension, Ghaziabad, Uttar Pradesh-201017</p></i> \
                <i><p align='center'>Phone - 8929570427</p></i> <br> \
                <h3> Customer Details: </h3><br>\
                <i>Date : {datetime.datetime.now().strftime('%d-%m-%Y')}</i> <br> \
                <i>Customer Name: {customer_info["cust_name"]}</i> <br> \
                <i>Customer Phone Number: {customer_info["cust_phone"]}</i> <br> \
                <i>Payment Method: {customer_info["payment_method"]}</i> <br><br>\
                {txt} \
                </body></html>\
                """
    #put_html(customer_receipt_str_html) 

def generate_order_number():
    '''method to generate  unique order number'''
    order_no = datetime.datetime.now().strftime('%d%m%y%H%M%S')
    return order_no

print(generate_order_number())
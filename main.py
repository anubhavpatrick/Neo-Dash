from cutomer_sales_GUI import customer_info_GUI, final_purchase_summary_GUI, product_detail_GUI, set_order_no
from pywebio import start_server #for quick testing
import threading
import time
import schedule
import save_as_xlsx
import helpers


def send_scheduled_mail_to_owner():
    '''A function that sends email to the owner at schedule time'''
    #simulation of sending email
    print("Hi Anubhav!!! This is a scheduled email to you")


def email_scheduler_thread(name):
    '''Thread to send scheduled mails
    Reference - https://realpython.com/python-async-features/#building-a-synchronous-web-server
    Reference - https://schedule.readthedocs.io/en/stable/
    '''
    schedule.every().day.at("22:30").do(send_scheduled_mail_to_owner)
    while True:
        schedule.run_pending()
        time.sleep(1)

def sales_controller():
    '''Product sales controller'''

    #generate order number
    order_no = helpers.generate_order_number()
    set_order_no(order_no)

    #start a thread for sending scheduled emails containing daily reports
    threading.Thread(target=email_scheduler_thread, args=(1,),daemon=True).start()
    
    #a method for displaying customer GUI and input customer details
    customer_info = customer_info_GUI()

    #a method for displaying product details GUI and enter details of items purchased
    products_dict, product_count, total_price = product_detail_GUI()

    #a method for displaying final purchase summary
    final_purchase_summary_GUI(customer_info, products_dict, product_count, total_price)     

    '''print(get_generate_log_final_receipt_button())

    #check whether the user wants to generate the data and save the data as an excel file   
    if get_generate_log_final_receipt_button():
        print("Generating data and saving as an excel file")
        
        #unfurl data into list of lists for writing to xlsx
        unfurled_data = save_as_xlsx.unfurl_data(customer_info, products_dict, product_count, total_price, order_no)
        
        #save data to xlsx
        save_as_xlsx.save_data(unfurled_data)'''
        

if __name__ == '__main__':
    start_server(sales_controller, host='',remote_access=True, reconnect_timeout=1000, max_payload_size='1000M', websocket_ping_interval=50)#, websocket_ping_timeout=5000)
    '''app = Flask(__name__)
    app.add_url_rule('/', 'webio_view', webio_view(customer_sales_GUI), methods =['GET','POST', 'OPTIONS'])
    app.run(host='0.0.0.0')'''
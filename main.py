from cutomer_sales_GUI import customer_info_GUI, final_purchase_summary_GUI, product_detail_GUI, put_header
from pywebio import start_server #for quick testing
import threading
import time

def test_thread(name):
    '''Thread to send scheduled mails
    Reference - https://realpython.com/python-async-features/#building-a-synchronous-web-server
    '''
    counter =0
    while True:
        with open("test.txt", "a") as f:
            f.write(f"{counter}\n")
        time.sleep(30)   
        counter+=1
        print("Test thread")



def sales_controller():
    '''Product sales module'''

    threading.Thread(target=test_thread, args=(1,)).start()
    
    customer_info = customer_info_GUI()

    products_dict, product_count, total_price =product_detail_GUI()

    final_purchase_summary_GUI(customer_info, products_dict, product_count, total_price)



if __name__ == '__main__':
    start_server(sales_controller, host='',remote_access=True, reconnect_timeout=1000, max_payload_size='1000M', websocket_ping_interval=50)#, websocket_ping_timeout=5000)
    '''app = Flask(__name__)
    app.add_url_rule('/', 'webio_view', webio_view(customer_sales_GUI), methods =['GET','POST', 'OPTIONS'])
    app.run(host='0.0.0.0')'''
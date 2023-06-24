
"""----------------------extract_initial_data----------------------------

Function Explanation: Segregates the information from the invoice into five
categories: business details, invoice details, customer details and
bill details.

Input   : JSON data

Output  : Business details (list, business_name)
          Invoice details  (list)
          Customer details (list) 
          Bill Details     (Table Id, Table Path, tax)


-------------------------------------------------------------------------"""

def extract_initial_data(data):

    elementId = 0
    invoice_details  = []
    business_details = []
    customer_details = []
    tax = 0

    for ele in data["elements"]:

        try:

            if int(ele["Bounds"][0]) == 76:
                if int(ele["TextSize"]) == 24 :
                    business_name = ele["Text"]
                else :
                    business_details.append(ele["Text"])


            elif int(ele["Bounds"][2]) == 543 or int(ele["Bounds"][0]) == 240 or int(ele["Bounds"][2] == 567) :
                invoice_details.append(ele["Text"])


            elif "Due date" in ele["Text"]:
                words = ele["Text"].split(" ")
                for word in words:
                    if "-" in word:
                        invoice_details.append(word)

            
            elif int(ele["Bounds"][0]) == 81:
                customer_details.append(ele["Text"])


            elif "ITEM" in ele["Text"] :
                if ele["Path"][-9] == "]":
                    items_table_no = int(ele["Path"][-10]) + 1
                    table_path = ele["Path"][:-10] + str(items_table_no) + "]"
                    table_details_id = elementId + 7
                else :
                    items_table_no = 2
                    table_path = ele["Path"][:-8] +"[" + str(items_table_no) + "]"
                    table_details_id = elementId + 7
                    
            
            if "Tax" in ele["Text"]:

                if len(ele["Text"]) > 6:
                    tax = ele["Text"][-3:]
                    continue
                if "Table" in ele["Path"]:
                    tax_id = elementId +  2
                else:
                    tax_id = elementId + 1
                tax = (data["elements"][tax_id]["Text"]).strip()
            elementId +=1

        except KeyError:
            elementId +=1
            continue
    if (tax == 0 or "$" in tax):
        tax = 10
    
    return business_details, business_name, invoice_details, customer_details, table_details_id, table_path, tax


"""-------------------------get_Invoice_Details--------------------------

Function Explanation: Extracts useful data from the raw invoice details and then segregates into invoice number, issue date, due date and description.

Input   : invoice_details (list)

Output  : correct_invoice_details (list)
          correct_invoice_details[0] - invoice number
          correct_invoice_details[1] - issue date
          correct_invoice_details[2] - due date
          correct_invoice_details[3] - description

-------------------------------------------------------------------------"""

def get_Invoice_Details(invoice_details):

    seperated_invoice_details = []
    for detail in invoice_details:
        seperated_detail = detail.strip().split(" ")
        for sep_det in seperated_detail:
            seperated_invoice_details.append(sep_det)

    if "Invoice#" not in seperated_invoice_details[0]:
        correct_invoice_details = [seperated_invoice_details[0], seperated_invoice_details[3]]
        invoice_description = ""

        for i in range(5,len(seperated_invoice_details)):
            if ("-" in seperated_invoice_details[i]):
                invoice_date = seperated_invoice_details[i]
            else :
                invoice_description += seperated_invoice_details[i] + " "
        correct_invoice_details.append(invoice_description.strip())
        correct_invoice_details.append(invoice_date)


    else :
        correct_invoice_details = [seperated_invoice_details[1], seperated_invoice_details[4]]
        invoice_description = ""
        invoice_date = "2"
        for i in range(6,len(seperated_invoice_details)-1):
            if ("-" in seperated_invoice_details[i]):
                invoice_date = seperated_invoice_details[i]
            else :
                invoice_description += seperated_invoice_details[i] + " "
        correct_invoice_details.append(invoice_description.strip())
        if (invoice_date != "2"):
            correct_invoice_details.append(invoice_date)
        else:
            correct_invoice_details.append(invoice_details[-1])

    return correct_invoice_details


"""----------------------------get_Business_Details-------------------------------


Function Explanation: Extracts useful data from the raw business details and then segregates into name, address and description

Input   : business_details (list)
          buisness_name

Output  : business_details (list)
          business_details[0] - business_name
          business_details[1] - business_description
          business_details[2] - business_address
          business_details[3] - business_city
          business_details[4] - business_country
          business_details[5] - business_zipcode

-----------------------------------------------------------------------------------"""

def get_Business_Details(business_details, business_name):

    seperated_business_details = []
    for detail in business_details:
        seperated_detail = detail.split(" ")[:-1]
        for sep_det in seperated_detail:
            seperated_business_details.append(sep_det)

    length_business_name = len(business_name.split(" "))


    i = length_business_name - 1

    business_address = seperated_business_details[i] + " " + seperated_business_details[i+1] + " "+ seperated_business_details[i+2][:-1]
    business_city = seperated_business_details[i+3][:-1]
    business_country = seperated_business_details[i+4] + " " +seperated_business_details[i+5]
    business_zipcode = seperated_business_details[i+6]

    business_description = ""
    for i in range(i+7, len(seperated_business_details)):
        business_description += seperated_business_details[i] + " "
    business_description = business_description.strip()

    business_name = business_name.strip()

    correct_business_details = [business_name, business_description, business_address, business_city, business_country, business_zipcode]
    return correct_business_details


"""---------------------------get_customer_details-------------------------------

Function Explanation: Extracts useful data from the raw customer details and then segregates into name, address, email and phone number.

Input   : customer_details (list)

Output  : correct_customer_details (list)
          correct_customer_details[0] - customer name
          correct_customer_details[1] - customer email
          correct_customer_details[2] - customer phone no
          correct_customer_details[3] - customer address line 1
          correct_customer_details[4] - customer address line 2

---------------------------------------------------------------------------------"""

def get_customer_details(customer_details):

    seperated_customer_details = []
    for detail in customer_details:
        seperated_detail = detail.split(" ")[:-1]
        for sep_det in seperated_detail:
            seperated_customer_details.append(sep_det)
    
    cust_name = seperated_customer_details[2]
    i = 3

    while("@" not in seperated_customer_details[i]):
        cust_name += " " + seperated_customer_details[i]
        i+=1
    
    correct_customer_details = [cust_name]
    
    cust_email = seperated_customer_details[i]
    i +=1

    while("-" not in seperated_customer_details[i]):
        cust_email += seperated_customer_details[i]
        i+=1

    correct_customer_details.append(cust_email)
    correct_customer_details.append(seperated_customer_details[i])

    customer_address1 = seperated_customer_details[i+1] + " " + seperated_customer_details[i+2] + " " + seperated_customer_details[i+3]
    customer_address2 = seperated_customer_details[i+4]
    index = i+4
    for i in range(index, len(seperated_customer_details) - 1):
        customer_address2 += " " + seperated_customer_details[i]
    
    correct_customer_details.append(customer_address1)
    correct_customer_details.append(customer_address2)

    return correct_customer_details


"""---------------------------------get_Items_Info-------------------------------

Function Explanation: Uses table path and table id of the table with items to get their name, rate and quantity.

Input   : JSON data
          table_path
          table_details_id

Output  : items_name_list
          items_qty_list
          items_rate_list

......................................................................"""

def get_Items_Info(data, table_path, table_details_id):

    item_name_list = []
    item_qty_list = []
    item_rate_list = []


    while(True):

        print(table_path)
        print(data["elements"][table_details_id]["attributes"])

        for ele in data["elements"]:
            if table_path == ele["Path"]:
                numItems = ele["attributes"]["NumRow"]
                break

        for ele in data["elements"]:
            if table_path in ele["Path"]:
                if "/TD/P" in ele["Path"]:
                    item_name_list.append(ele["Text"])

                elif "/TD[2]/P" in ele["Path"]:
                    item_qty_list.append(ele["Text"])
                
                elif "/TD[3]/P" in ele["Path"]:
                    item_rate_list.append(ele["Text"])
            
        if "table" in data["elements"][table_details_id + numItems*8]["Path"] :
            if "Subtotal" in data["elements"][table_details_id + numItems*8 + 2]["Text"]:
                break
            else:
                table_details_id += numItems*8 + 1
                continue
        else:
            break

    return item_name_list, item_qty_list, item_rate_list


"""-----------------------------combine_details--------------------------------------

Function Explanation: Combines business details, invoice details, customer details, and bill details and stores them in rows to write into the csv
file. 

Input   : Business_Details
          Invoice_details
          Customer_details
          Items_name_list
          Items_qty_list
          Items_rate_list
          Tax

Output  : rows

------------------------------------------------------------------------------------------"""

def combine_details(Business_Details, Invoice_details, Customer_details, Items_name_list, Items_qty_list, Items_rate_list, tax):
    rows = []
    

    for i in range(len(Items_name_list)):
        row = []
        row.append(Business_Details[3])
        row.append(Business_Details[4])
        row.append(Business_Details[1])
        row.append(Business_Details[0])
        row.append(Business_Details[2])
        row.append(Business_Details[5])
        row.append(Customer_details[3])
        row.append(Customer_details[4])
        row.append(Customer_details[1])
        row.append(Customer_details[0])
        row.append(Customer_details[2])
        row.append(Items_name_list[i].strip())
        row.append(Items_qty_list[i].strip())
        row.append(Items_rate_list[i].strip())  
        row.append(Invoice_details[2])
        row.append(Invoice_details[1])
        row.append(Invoice_details[3])
        row.append(Invoice_details[0])
        row.append(tax)
        rows.append(row)  
    
    return rows

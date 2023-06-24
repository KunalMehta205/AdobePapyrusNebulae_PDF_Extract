import logging
import os.path
import extract_from_pdf as extr_pdf
import zipfile as zip
import manage_data as manage
import json
import csv

"""---------------------------update_csv---------------------------

Function Explanation: Add rows to the csv file

Input: rows        (rows to be appended)
       source_file (name of source pdf file)

-------------------------------------------------------------------"""

def update_csv(rows, source_file_pdf):
    with open("Extracted_Data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print("Successfully Extracted Data from JSON file of: "+ source_file_pdf)


#add heading to csv file
try:
    with open("Extracted_Data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bussiness__City", "Bussiness__Country", "Bussiness__Description",	"Bussiness__Name",	"Bussiness__StreetAddress",	"Bussiness__Zipcode",	"Customer__Address__line1",	"Customer__Address__line2"	,"Customer__Email",	"Customer__Name"	,"Customer__PhoneNumber",	"Invoice__BillDetails__Name",	"Invoice__BillDetails__Quantity",	"Invoice__BillDetails__Rate",	"Invoice__Description",	"Invoice__DueDate",	"Invoice__IssueDate",	"Invoice__Number",	"Invoice__Tax"] )
except Exception as e:
    print(f"An error occured: {e}")


#access TestDataSet directory
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
base_path = os.path.dirname(os.path.abspath(__file__))
dir_list = os.listdir(base_path + "/TestDataSet")


#convert json file to csv
for pdf in dir_list:
    extr_pdf.zipped_json(pdf, base_path)
    print(pdf)
    with zip.ZipFile(base_path + "/ZippedOutput/"+ pdf[:-4]+".zip") as myzip:
        with myzip.open('structuredData.json') as myfile:

            data = json.load(myfile)

    raw_business_details, business_name, raw_invoice_details, raw_customer_details, table_Details_id, table_path, tax = manage.extract_initial_data(data)

    business_details = manage.get_Business_Details(raw_business_details, business_name)
    invoice_details = manage.get_Invoice_Details(raw_invoice_details)
    customer_details = manage.get_customer_details(raw_customer_details)
    items_name, items_qty, items_rate = manage.get_Items_Info(data, table_path, table_Details_id)

    #combining all the details
    rows = manage.combine_details(business_details, invoice_details, customer_details, items_name, items_qty, items_rate, tax)
    update_csv(rows, pdf[:-4])
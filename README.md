# AdobePapyrusNebulae_PDF_Extract
Extracting information from PDF invoices using Adobe PDF Services Extract API 

Main aim of the project is to extract information from the PDF invoices and store it in csv file in a specified format.

# Installation and Setup
Clone the repository and run the command:
```
pip install pdfservices-sdk
```
Executing the code:
```
python main.py
```

# Project Structure
There are three Python code files:

### extract_from_pdf.py
Connects the user to the API and extracts text elements from the input pdf.

### manage_data.py
Segregates the information from the invoice into five categories: business details, invoice details, customer details and bill details.

### main.py
Iterates over each pdf file in the TestDataSet directory and calls the extract_from_pdf.py to get the JSON files and then calls the manage_data.py for getting appropriate data. Finally, the output is written in the "Extracted_Data.csv" file.





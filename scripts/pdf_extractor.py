import fitz
import csv

bonds_by_parties = fitz.open("Bonds_Encashed_by_Parties.pdf")
bonds_purchased = fitz.open("Bonds_Purchased.pdf")

parties_out = open("bonds_encashed_by_parties.csv", "w")
purchased_out = open("bonds_purchased.csv", "w")

for file in [(bonds_by_parties, parties_out), (bonds_purchased, purchased_out)]:
    writer = csv.writer(file[1])
    page_number = 1
    for page in file[0]: 
        tabs = page.find_tables()
        if tabs.tables:
            page_data = tabs[0].extract()
            data = page_data[1:] if page_number != 1 else page_data ## removing headers from all pages except the 1st page
            writer.writerows(data)
        page_number += 1
    file[1].close()



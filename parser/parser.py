import pymupdf
from .table import table_rect,parse_table1,parse_table2,parse_table3,parse_table4

with pymupdf.open("parser/icc-stmt.pdf") as doc:
    page=doc[0]
    #1st table
    cord1_from=page.search_for("ACCOUNT DETAILS - INR")
    cord1_to=page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")
    rect1=table_rect(page,cord1_from,cord1_to)
    table1_data=parse_table1(page,rect1)
    #2nd table
    cord2_from=page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")
    cord2_to=page.search_for("Total:")
    rect2=table_rect(page,cord2_from,cord2_to)
    table2_data=parse_table2(page,rect2)
    #3rd table
    cord3_from=page.search_for("REWARD POINTS SUMMARY")
    cord3_to=page.search_for("To get current reward points balance")
    rect3=table_rect(page,cord3_from,cord3_to)
    table3_data=parse_table3(page,rect3)
    #4th table
    cord4_from=page.search_for("Account Related Other Information")
    cord4_to=page.search_for("* Nominee name is displayed only on specific consent of customer.")
    rect4=table_rect(page,cord4_from,cord4_to)
    table4_data=parse_table4(page,rect4)


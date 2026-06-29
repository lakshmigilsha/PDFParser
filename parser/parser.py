import pymupdf
from .table import rect_table,parse_table1,parse_table2,parse_table3,parse_table4

with pymupdf.open("icc-stmt.pdf") as doc:
    page=doc[0]
    #1st table
    cord1_from=page.search_for("ACCOUNT DETAILS - INR")
    cord1_to=page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")
    rect1=rect_table(cord1_from,cord1_to)
    table1_data=parse_table1(rect1)
    #2nd table
    cord2_from=page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")
    cord2_to=page.search_for("Total:")
    rect2=rect_table(cord2_from,cord2_to)
    table2_data=parse_table2(rect2)
    #3rd table
    cord3_from=page.search_for("REWARD POINTS SUMMARY")
    cord3_to=page.search_for("To get current reward points balance")
    rect3=rect_table(cord3_from,cord3_to)
    table3_data=parse_table3(rect3)
    #4th table
    cord4_from=page.search_for("Account Related Other Information")
    cord4_to=page.search_for("* Nominee name is displayed only on specific consent of customer.")
    rect4=rect_table(cord4_from,cord4_to)
    table4_data=parse_table4(rect4)


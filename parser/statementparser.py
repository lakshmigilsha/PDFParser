import pymupdf,re
class StatementParser:

    def __init__(self,path):
        self.doc=pymupdf.open(path)

    def get_region(self, page, cord_top=None, cord_bottom=None,cord_left=None, cord_right=None):

        top = cord_top[0].y1 if cord_top else page.rect.y0
        left = cord_left[0].x1 if cord_left else page.rect.x0
        right = cord_right[0].x0 if cord_right else page.rect.x1
        bottom = cord_bottom[0].y0 if cord_bottom else page.rect.y1

        return pymupdf.Rect(left, top, right, bottom)
    
    def get_lines(self, page, rect):
        text = page.get_text(clip=rect, sort=True)
        return [line.strip() for line in text.splitlines() if line.strip()]
    
    def parse_table1(self):
        for page in self.doc:
            top = page.search_for("ACCOUNT DETAILS - INR")
            bottom = page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")

            rect = self.get_region(page, cord_top=top, cord_bottom=bottom)
            lines=self.get_lines(page, rect)

            headers=["ACCOUNT TYPE","A/C. BALANCE (I)","FIXED DEPOSITS (LINKED) BAL. (II)","TOTAL BALANCE (I+II)","NOMINATION"]
            values=re.split(r"\s{2,}",lines[1])
            return dict(zip(headers,values))
        
    def parse_table2(self):
        '''parse second table into a list of dictionary with keys DATE,MODE,PARTICULARS,DEPOSITS,WITHDRAWLS,BALANCE'''
        for page in self.doc:
            top = page.search_for("Statement of Transactions in Savings Account Number: 035701533681 in INR for the period November 01, 2016 - November 30, 2016")
            bottom = page.search_for("Total:")

            rect = self.get_region(page, cord_top=top, cord_bottom=bottom)
            ft=page.find_tables(clip=rect,strategy="text")
            table=ft.tables[0]
            contents=[]
            rows=table.extract()
            headers=rows[0]
            for index,row in enumerate(table.extract()):        
                if index==0 or all(value in ('','_') for value in row):
                    continue
                contents.append(dict(zip(headers,row)))
            return contents
        
    def parse_table3(self):
        for page in self.doc:
            top = page.search_for("REWARD POINTS SUMMARY")
            bottom = page.search_for("To get current reward points balance")

            rect = self.get_region(page, cord_top=top, cord_bottom=bottom)
            lines=self.get_lines(page, rect)

            values_list=re.split(r"\s{2,}",lines[4])
            values=[int(value) for value in values_list]
            table3={"SAVINGS ACCOUNT NUMBER":values[0],
                                "LINKED PAYBACK NUMBER":values[1],
                                "Points earned for the month of October, 2016":{"My Savings REWARD":values[2],"DEBIT CARD":values[3]},
                                "POINTS BALANCE*":values[4]}
            return table3

    def parse_table4(self):
        
        for page in self.doc:
                top = page.search_for("Account Related Other Information")
                bottom = page.search_for("* Nominee name is displayed only on specific consent of customer.")

                rect = self.get_region(page, cord_top=top, cord_bottom=bottom)
                lines=self.get_lines(page, rect)

                fields=re.split(r"\s{2,}",lines[0].strip())
                values=re.split(r"\s{2,}",lines[1].strip())
                contents=dict(zip(fields,values))
                return contents
    def parse(self):
        return {
            "table1": self.parse_table1(),
            "table2": self.parse_table2(),
            "table3": self.parse_table3(),
            "table4": self.parse_table4()
        }
if __name__ == "__main__":
    parser = StatementParser("icc-stmt.pdf")

    result = parser.parse()
    print(result["table1"])
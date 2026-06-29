import pymupdf,re
import parser


def rect_table(cord_from,cord_to):
    '''Selct particular portion of pdf using rectangle coordinates'''
    
    ry0=cord_from[0].y1
    rx0=parser.page.rect.x0
    rx1=parser.page.rect.x1
    ry1=cord_to[0].y0
    
    cr=pymupdf.Rect(rx0,ry0,rx1,ry1)
    return cr

def parse_table1(rect1):

    text=parser.page.get_text(clip=rect1,sort=True)
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    headers=["ACCOUNT TYPE","A/C. BALANCE (I)","FIXED DEPOSITS (LINKED) BAL. (II)","TOTAL BALANCE (I+II)","NOMINATION"]
    values=re.split(r"\s{2,}",lines[1])
    contents=dict(zip(headers,values))
    return contents

def parse_table2(rect2):
    '''parse second table into a list of dictionary with keys DATE,MODE,PARTICULARS,DEPOSITS,WITHDRAWLS,BALANCE'''
    ft=parser.page.find_tables(clip=rect2,strategy="text")
    table=ft.tables[0]
    contents=[]
    rows=table.extract()
    headers=rows[0]
    for index,row in enumerate(table.extract()):        
        if index==0 or all(value in ('','_') for value in row):
            continue
        contents.append(dict(zip(headers,row)))
    return contents

def parse_table3(rect3):
    text=parser.page.get_text(clip=rect3,sort=True)
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    values_list=re.split(r"\s{2,}",lines[4])
    values=[int(value) for value in values_list]
    table3={"SAVINGS ACCOUNT NUMBER":values[0],
                        "LINKED PAYBACK NUMBER":values[1],
                        "Points earned for the month of October, 2016":{"My Savings REWARD":values[2],"DEBIT CARD":values[3]},
                        "POINTS BALANCE*":values[4]}
    return table3

def parse_table4(rect4):
    
    text=parser.page.get_text(clip=rect4,sort=True)
    mod_values=[x for x in text.split("\n") if x.strip()]  #strip invalid values
    fields=re.split(r"\s{2,}",mod_values[0].strip())
    values=re.split(r"\s{2,}",mod_values[1].strip())
    contents=dict(zip(fields,values))
    return contents
   

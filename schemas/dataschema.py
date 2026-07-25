from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime,date

@dataclass
class CustomerData:
    name:str
    address:str
    cust_id:int
    date:date
    account_number:int
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=str(data["name"]),
            address=str(data["address"]),
            cust_id=int(data["cust_id"]),
            date=datetime.strptime(data["date"],"%B %d, %Y").date(),
            account_number=int(data["account_number"])
        )
@dataclass
class AccountData:
    account_type:str
    ac_balance:Decimal
    fixed_deposits_linked_balance:Decimal
    total_balance:Decimal
    nomination:str
    @classmethod
    def from_dict(cls, data):
        return cls(
            account_type=str(data["ACCOUNT TYPE"]),
            ac_balance=Decimal(data["A/C. BALANCE (I)"]),
            fixed_deposits_linked_balance=Decimal(data["FIXED DEPOSITS (LINKED) BAL. (II)"]),
            total_balance=Decimal(data["TOTAL BALANCE (I+II)"]),
            nomination=str(data["NOMINATION"])
        )

@dataclass
class TransactionData:
    date: date
    particulars:str
    balance:Decimal
    mode: str|None=None
    deposits:Decimal|None=None
    withdrawals:Decimal|None=None   
    @classmethod
    def from_dict(cls, data):
        return cls(
        date=datetime.strptime(data["DATE"],"%d-%m-%Y").date(),
                   
        mode=str(data["MODE"])
        if data["MODE"] != ""
        else None,

        particulars=str(data["PARTICULARS"]),

        deposits=Decimal(data["DEPOSITS"].replace(",", ""))
        if data["DEPOSITS"] != ""
        else None,

        withdrawals=Decimal(data["WITHDRAWALS"].replace(",", ""))
        if data["WITHDRAWALS"] != ""
        else None,

        balance=Decimal(data["BALANCE"].replace(",", ""))
        )
    
@dataclass
class PointsData:
     savings_acc_number:int
     linked_payback_number:int
     savings_reward:int
     debit_card:int
     points_balance:int
     @classmethod
     def from_dict(cls,data):
         point=data["Points earned for the month october"]
      
         return cls(
             savings_acc_number=int(data["SAVINGS ACCOUNT NUMBER"]),
             linked_payback_number=int(data["LINKED PAYBACK NUMBER"]),
             savings_reward=int(point["My Savings REWARD"]),
             debit_card=int(point["DEBIT CARD"]),
             points_balance=int(data["POINTS BALANCE*"])
             )

@dataclass
class OtherData:
    account_type:str
    account_number:int
    micr_code:int
    ifsc_code:str
    nominee:str
    @classmethod
    def from_dict(cls, data):
        return cls(
            account_type=str(data["ACCOUNT TYPE"]),
            account_number=int(data["ACCOUNT NUMBER"]),
            micr_code=int(data["MICR CODE"]),
            ifsc_code=str(data["IFSC CODE"]),
            nominee=str(data["NAME OF NOMINEE*"])
        )
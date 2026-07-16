from sqlalchemy.orm import Session
from database.database import engine
from database.models import CustomerDetails,AccountDetails,Transactions,RewardPoints,OtherInfo
from schemas.dataschema import CustomerData,AccountData,TransactionData,PointsData,OtherData
from parser.statementparser import StatementParser
class StatementService:

    def save_statement(self,result):
        with Session(engine) as session:

            cust_id = self.save_customer(
                session,result["customer_details"])
            self.save_account(
                session,result["table1"],cust_id)
            self.save_transactions(
                session,result["table2"],cust_id)
            self.save_points(
                session,result["table3"],cust_id)
            self.save_other_data(
                session,result["table4"],cust_id)
            session.commit()

    def save_customer(self,session,customer):
        customer=CustomerData.from_dict(customer)
        
        customer_db=CustomerDetails(
            name=customer.name,
            address=customer.address,
            cust_id=customer.cust_id,
            date=customer.date,
            account_number=customer.account_number)
        session.add(customer_db)
        session.flush()   
        return customer_db.cust_id


    def save_account(self,session,account,cust_id):
        account=AccountData.from_dict(account)
        account_db=AccountDetails(
            cust_id=cust_id,
            account_type=account.account_type,
            ac_balance=account.ac_balance,
            fixed_deposits_linked_balance=account.fixed_deposits_linked_balance,
            total_balance=account.total_balance,
            nomination=account.nomination)
        session.add(account_db)

    def save_transactions(self, session, transactions, cust_id):
        transaction_objects = []
        for row in transactions:
            transaction = TransactionData.from_dict(row)
            transaction_info = Transactions(
                cust_id=cust_id,
                date=transaction.date,
                particulars=transaction.particulars,
                balance=transaction.balance,
                mode=transaction.mode,
                deposits=transaction.deposits,
                withdrawals=transaction.withdrawals)
            transaction_objects.append(transaction_info)

        session.add_all(transaction_objects)
    
    def save_points(self,session,points,cust_id):
        points=PointsData.from_dict(points)
        points_db=RewardPoints(
            cust_id=cust_id,
            savings_acc_number=points.savings_acc_number,
            linked_payback_number=points.linked_payback_number,
            savings_reward=points.savings_reward,
            debit_card=points.debit_card,
            points_balance=points.points_balance)
        session.add(points_db)
    
    def save_other_data(self,session,others,cust_id):
        others=OtherData.from_dict(others)
        others_db=OtherInfo(
            cust_id=cust_id,
            account_type=others.account_type,
            account_number=others.account_number,
            micr_code=others.micr_code,
            ifsc_code=others.ifsc_code,
            nominee=others.nominee)
        session.add(others_db)

if __name__ == "__main__":
    from database.database import Base, engine
    from database import models

    Base.metadata.create_all(engine)
    parser = StatementParser("parser/icc-stmt.pdf")

    result = parser.parse()

    service = StatementService()

    service.save_statement(result)
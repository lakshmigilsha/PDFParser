from sqlalchemy.orm import Session
from database.database import engine
from database.models import CustomerDetails,AccountDetails,Transactions,RewardPoints,OtherInfo
from dataclasses import asdict
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
        customer_db = CustomerDetails(**asdict(customer))
        session.add(customer_db)
        session.flush()   
        return customer_db.cust_id


    def save_account(self,session,account,cust_id):
        account_db=AccountDetails(cust_id=cust_id,**asdict(account))
        session.add(account_db)

    def save_transactions(self, session, transactions, cust_id):
        transaction_objects = []
        for row in transactions:
            transaction_info = Transactions(cust_id=cust_id,**asdict(row))
            transaction_objects.append(transaction_info)

        session.add_all(transaction_objects)
    
    def save_points(self,session,points,cust_id):
        points_db=RewardPoints(cust_id=cust_id,**asdict(points))
        session.add(points_db)
    
    def save_other_data(self,session,others,cust_id):
        others_db=OtherInfo(cust_id=cust_id,**asdict(others))
        session.add(others_db)

if __name__ == "__main__":
    from database.database import Base, engine
    from database import models

    Base.metadata.create_all(engine)
    parser = StatementParser("parser/icc-stmt.pdf")

    result = parser.parse()

    service = StatementService()

    service.save_statement(result)
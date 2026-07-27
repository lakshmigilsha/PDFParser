from sqlalchemy.orm import Session
from sqlalchemy import select
from database.database import engine
from database.models import (
    CustomerDetails,
    FileDetails,
    AccountDetails,
    Transactions,
    RewardPoints,
    OtherInfo,
)
from dataclasses import asdict
from parser.statementparser import StatementParser
class StatementService:

    def save_statement(self,result,original_name):
        with Session(engine) as session:

            cust_id = self.save_customer(
                session,
                result["customer_details"],
                )
            file_id = self.save_file(
                session,
                cust_id,
                original_name,
                )
            self.save_account(
                session,result["table1"],cust_id,file_id)
            self.save_transactions(
                session,result["table2"],cust_id,file_id)
            self.save_points(
                session,result["table3"],cust_id,file_id)
            self.save_other_data(
                session,result["table4"],cust_id,file_id)
            session.commit()

    def save_customer(self, session, customer):
        old_customer = session.get(
        CustomerDetails,
        customer.cust_id
        )
        if old_customer:
            return old_customer.cust_id
        customer_db = CustomerDetails(**asdict(customer))
        session.add(customer_db)
        session.flush()   
        return customer_db.cust_id

    def save_file(self, session, cust_id, original_name):
        file_db = FileDetails(
        cust_id=cust_id,
        filename="temp_file",
        original_name=original_name,
        status="processing"
        )

        session.add(file_db)
        session.flush()

        return file_db.file_id


    def save_account(self,session,account,cust_id,file_id):
        account_db=AccountDetails(cust_id=cust_id,
                                  file_id=file_id,
                                  **asdict(account),
                                  )
        session.add(account_db)

    def save_transactions(self, session, transactions, cust_id,file_id):
        transaction_objects = []
        for row in transactions:
            transaction_info = Transactions(cust_id=cust_id,
                                            file_id=file_id,
                                            **asdict(row),
                                            )
            transaction_objects.append(transaction_info)

        session.add_all(transaction_objects)
    
    def save_points(self,session,points,cust_id,file_id):
        points_db=RewardPoints(cust_id=cust_id,
                               file_id=file_id,
                               **asdict(points),
                               )
        session.add(points_db)
    
    def save_other_data(self,session,others,cust_id,file_id):
        others_db=OtherInfo(cust_id=cust_id,
                            file_id=file_id,
                            **asdict(others),
                            )
        session.add(others_db)

    def list_uploaded_pdf(self):
        """Return the list of all uploaded pdf files"""
        with Session(engine) as session:
            get_pdf_stmt=select(FileDetails)
            return session.scalars(get_pdf_stmt).all()

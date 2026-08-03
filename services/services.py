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
from uuid import UUID

class StatementService:

    def save_statement(self,result,original_name,temp_path):
        with Session(engine) as session:
            file = self.save_file(
                session,
                original_name,
                temp_path,
                )
            file_id=file.file_id
            session.commit()   #Transaction 1
            try:
                cust_id = self.save_customer(
                                session,
                                result["customer_details"],
                                file_id,
                                )
                self.save_account(
                    session,result["table1"],cust_id,file_id)
                self.save_transactions(
                    session,result["table2"],cust_id,file_id)
                self.save_points(
                    session,result["table3"],cust_id,file_id)
                self.save_other_data(
                    session,result["table4"],cust_id,file_id)
                file.status="completed"
                session.commit()  #Transaction 2

            except Exception as e:
              session.rollback()
              file.error_message=str(e)
              file.status="Failed"
              session.commit()    #Transaction 2

    def save_file(self, session,original_name,temp_path):
        file_db = FileDetails(
        filename= temp_path,
        original_name= original_name,
        status= "processing",
        )

        session.add(file_db)
        session.flush()

        return file_db

    def save_customer(self, session, customer,file_id):
            customer_db = CustomerDetails(file_id=file_id,**asdict(customer))
            session.add(customer_db)
            session.flush()   
            return customer_db.cust_id

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
        """Return all uploaded pdf files"""
        with Session(engine) as session:
            get_pdf_stmt=select(FileDetails)
            return session.scalars(get_pdf_stmt).all()

    def selected_pdf_transaction(self,file_id):
        with Session(engine) as session:
            get_transaction_stmt = select(Transactions).where(
                Transactions.file_id == file_id
                )
            return session.scalars(get_transaction_stmt).all()

    def selected_pdf_customer(self,file_id):
        with Session(engine) as session:
                get_customer_stmt = select(CustomerDetails).where(
                    CustomerDetails.file_id == file_id
                    )
                return session.scalars(get_customer_stmt).all()

    def selected_pdf_account(self,file_id):
            with Session(engine) as session:
                    get_account_stmt = select(AccountDetails).where(
                        AccountDetails.file_id == file_id
                        )
                    return session.scalars(get_account_stmt).all()

    def selected_pdf_points(self,file_id):
                with Session(engine) as session:
                        get_points_stmt = select(RewardPoints).where(
                            RewardPoints.file_id == file_id
                            )
                        return session.scalars(get_points_stmt).all()

    def selected_pdf_other(self,file_id):
                    with Session(engine) as session:
                            get_other_stmt = select(OtherInfo).where(
                                OtherInfo.file_id == file_id
                                )
                            return session.scalars(get_other_stmt).all()   
        
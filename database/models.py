from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Numeric,
    Date,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date,datetime
from decimal import Decimal
from database.database import Base
import uuid

class FileDetails(Base):
    """
    Metadata of files uploaded by customers.
    """
    __tablename__="file_details"
    file_id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    filename:Mapped[str]=mapped_column(String(260))   #temporary file name saved to device
    original_name:Mapped[str]=mapped_column(String(100)) #original filename uploaded by customer
    status: Mapped[str] = mapped_column(default="processing")
    uploaded_at: Mapped[datetime] = mapped_column(default=datetime.now)
    error_message: Mapped[str | None] = mapped_column(nullable=True)

class CustomerDetails(Base):
    __tablename__ = "customer_details"
    file_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("file_details.file_id"),
            primary_key=True
        )
    name:Mapped[str]=mapped_column(String(40))
    address:Mapped[str]=mapped_column(String(150))
    cust_id:Mapped[int]=mapped_column(primary_key=True)
    date:Mapped[date] = mapped_column(Date)
    account_number:Mapped[int] = mapped_column(Integer)

class AccountDetails(Base):
    __tablename__ = "Account_details"
    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_details.file_id"),
        primary_key=True
    )
    cust_id: Mapped[int] = mapped_column(
            ForeignKey("customer_details.cust_id"))
    account_type:Mapped[str]=mapped_column(String(80))
    ac_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    fixed_deposits_linked_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    total_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    nomination:Mapped[str]=mapped_column(String(40))

class Transactions(Base):
    __tablename__ = "Transactions_details"
    transaction_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_details.file_id"))
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"))
    date:Mapped[date] = mapped_column(Date)
    mode:Mapped[str| None] = mapped_column(String(50),nullable=True)
    particulars:Mapped[str] = mapped_column()
    deposits:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    withdrawals:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    balance:Mapped[Decimal] = mapped_column(Numeric(10, 2))

class RewardPoints(Base):
    __tablename__ = "Reward_Points_Summary"
    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_details.file_id"),
        primary_key=True
    )
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"))
    savings_acc_number:Mapped[int] = mapped_column(Integer)
    linked_payback_number:Mapped[int] = mapped_column(Integer)
    savings_reward:Mapped[int] = mapped_column(Integer)
    debit_card:Mapped[int] = mapped_column(Integer)
    points_balance:Mapped[int] = mapped_column(Integer)

class OtherInfo(Base):
    __tablename__ = "Extra_Account_Information"
    file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_details.file_id"),
        primary_key=True
    )
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"))
    account_type:Mapped[str] = mapped_column(String(50))
    account_number:Mapped[int] = mapped_column(Integer)
    micr_code:Mapped[int] = mapped_column(Integer)
    ifsc_code:Mapped[str] = mapped_column(String(50))
    nominee:Mapped[str] = mapped_column(String(50))
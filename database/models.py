from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Numeric
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date
from decimal import Decimal
from database.database import Base

class CustomerDetails(Base):
    __tablename__ = "customer_details"
    name:Mapped[str]=mapped_column(String(40))
    address:Mapped[str]=mapped_column(String(150))
    cust_id:Mapped[int]=mapped_column(primary_key=True)
    date:Mapped[date] = mapped_column(Date)
    account_number:Mapped[int] = mapped_column(Integer)

class AccountDetails(Base):
    __tablename__ = "Account_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    cust_id: Mapped[int] = mapped_column(ForeignKey("customer_details.cust_id"))
    account_type:Mapped[str]=mapped_column(String(80))
    ac_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    fixed_deposits_linked_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    total_balance:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    nomination:Mapped[str]=mapped_column(String(40))

class Transactions(Base):
    __tablename__ = "Transactions_details"
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"),primary_key=True)
    date:Mapped[date] = mapped_column(Date)
    mode:Mapped[str| None] = mapped_column(String(50),nullable=True)
    particulars:Mapped[str] = mapped_column(primary_key=True)
    deposits:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    withdrawals:Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    balance:Mapped[Decimal] = mapped_column(Numeric(10, 2))

class RewardPoints(Base):
    __tablename__ = "Reward_Points_Summary"
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"),primary_key=True)
    savings_acc_number:Mapped[int] = mapped_column(Integer)
    linked_payback_number:Mapped[int] = mapped_column(Integer)
    savings_reward:Mapped[int] = mapped_column(Integer)
    debit_card:Mapped[int] = mapped_column(Integer)
    points_balance:Mapped[int] = mapped_column(Integer)

class OtherInfo(Base):
    __tablename__ = "Extra_Account_Information"
    cust_id: Mapped[int] = mapped_column(
        ForeignKey("customer_details.cust_id"),primary_key=True)
    account_type:Mapped[str] = mapped_column(String(50))
    account_number:Mapped[int] = mapped_column(Integer)
    micr_code:Mapped[int] = mapped_column(Integer)
    ifsc_code:Mapped[str] = mapped_column(String(50))
    nominee:Mapped[str] = mapped_column(String(50))
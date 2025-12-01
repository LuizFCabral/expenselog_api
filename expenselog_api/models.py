import math
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class TransectionType(str, Enum):
    income = 'income'
    expense = 'expense'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    balance: Mapped[float] = mapped_column(default=0.0)
    total_income: Mapped[float] = mapped_column(default=0.0)
    total_expenses: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    transections: Mapped[list['Transection']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    def increase_balance(self, amount: float):
        if math.isnan(amount):
            return False

        self.balance += amount
        self.updated_at = func.now()
        return True

    def decrease_balance(self, amount: float):
        if math.isnan(amount):
            return False

        self.balance -= amount
        self.updated_at = func.now()
        return True

    def add_transections(
        self,
        transection_type: TransectionType,
        amount: float,
        description: str | None = None,
    ):
        balance_before = self.balance

        if transection_type == TransectionType.income:
            self.increase_balance(amount)
        elif transection_type == TransectionType.expense:
            self.decrease_balance(amount)

        transection = Transection(
            account_id=self.id,
            type=transection_type,
            amount=amount,
            description=description,
            balance_before=balance_before,
            balance_after=self.balance,
        )

        self.transections.append(transection)
        self.updated_at = func.now()

class Transection:
    __tablename__ = 'transections'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey('accounts.id', ondelete='CASCADE')
    )

    type: Mapped[TransectionType]
    amount: Mapped[float]
    description: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    balance_before: Mapped[float]
    balance_after: Mapped[float]

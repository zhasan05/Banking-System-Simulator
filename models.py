import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from enums import AccountType, TransactionType
from exceptions import InsufficientFundsError, InvalidAmountError

class Transaction():

    # create a transaction object
    def __init__(self, type:TransactionType, amount: float, balance_after: float):
        self.type = type
        self.amount = amount
        self.balance_after = balance_after
        self.transaction_id = str(uuid.uuid4().hex[:8])
        self.timestamp = datetime.now()

    # prints how transaction looks like
    def __repr__(self):
        sign = ""
        if self.type == TransactionType.WITHDRAWAL:
            sign = "-"
        else:
            sign = "+"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]  {self.type.value:<12}  {sign}${self.amount:.2f}  |  Balance: ${self.balance_after:.2f}"

    # convert the Transaction object into a plain dictionary that JSON can save to disk
    def to_dict(self):
        data = {
            "transaction_id" : self.transaction_id, 
            "type" : self.type.value,          
            "amount" : self.amount,         
            "balance_after" : self.balance_after, 
            "timestamp" : self.timestamp.isoformat()
        }
        return data

    # convert a plain dictionary JSON from the disk to Transaction object
    @classmethod
    def from_dict(cls, data: dict):
        trans = cls(TransactionType(data['type']),amount=data['amount'], balance_after=data['balance_after'])
        trans.transaction_id = data['transaction_id']
        trans.timestamp = datetime.fromisoformat(data['timestamp'])        
        return trans

class Account(ABC):
    # sets up the shared data every account needs - Checking & Savings
    def __init__(self, account_id: str, owner_name: str, account_type: AccountType, initial_balance: float ):
        self.account_id = account_id
        self.owner_name = owner_name
        self.account_type = account_type 
        self._balance = initial_balance
        self._transactions = []

    # safe read-only window into _balance but can not set anyhing
    @property # --> turns a method into an attribute-style access
    def balance(self) -> float:
        return self._balance

    # shared behaviour between accounts — ALL accounts must deposit the same way
    def deposit(self, amount: float) -> Transaction:
        if amount <= 0:
            raise InvalidAmountError(amount)
        self._balance += amount
        trans = Transaction(
            TransactionType.DEPOSIT,
            amount,
            self._balance
            )
        self._transactions.append(trans)
        return trans

    # Different behaviour per account type - CheckingAccount allows overdraft - SavingsAccount never goes negative 
    # No implementation only declaration
    @abstractmethod # --> marks a method as "must be implemented by subclasses"
    def withdraw(self, amount: float) -> Transaction:
        pass

    def get_balance(self):
        return self._balance

    # return a copy of the transactions not the original list
    def get_statement(self):
        copy_trans = list(self._transactions) 
        return copy_trans

    # return the account details
    def __repr__(self):
       return (
           f"[{self.account_id}] {self.owner_name:<20}     {self.account_type.value}  Balance: ${self._balance:,.2f}"
        )
    
    # convert the account object into a plain dictionary that JSON can save to disk
    def to_dict(self):
        trans = []
        for t in self._transactions:
            trans.append(t.to_dict()) # converts python object from transaction to json type
        data = {
            "account_id" : self.account_id,
            "owner_name" : self.owner_name,
            "account_type" : self.account_type.value,
            "balance" : self._balance,
            "transactions" : trans  
        }
        return data

class CheckingAccount(Account):
    def __init__(self, account_id: str, owner_name: str, initial_balance: float = 0.00, overdraft_limit: float = 200.00):
        super().__init__(
            account_id=account_id,
            owner_name=owner_name,
            account_type=AccountType.CHECKING,
            initial_balance=initial_balance,
        )
        self.overdraft_limit = overdraft_limit


    def withdraw(self, amount):   
        if amount <= 0:
            raise InvalidAmountError(amount)

        if (self._balance - amount) < -self.overdraft_limit:
            raise InsufficientFundsError(amount, self._balance + self.overdraft_limit)

        self._balance -= amount
        trans = Transaction(
            TransactionType.WITHDRAWAL,
            amount,
            self._balance
        )
        self._transactions.append(trans)
        return trans

    def to_dict(self): 
        data = super().to_dict()
        data['overdraft_limit'] = self.overdraft_limit
        return data

class SavingsAccount(Account):
    def __init__(self, account_id: str, owner_name: str, initial_balance: float, interest_rate: float = 0.02 ):
        super().__init__(
            account_id=account_id,
            owner_name=owner_name,
            account_type=AccountType.SAVINGS,
            initial_balance=initial_balance,
        )
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError(amount)

        if amount > self._balance:
            raise InsufficientFundsError(amount, self._balance)

        self._balance -= amount
        trans = Transaction(
            TransactionType.WITHDRAWAL,
            amount,
            self._balance
        )
        self._transactions.append(trans)
        return trans

    def apply_interest(self):
        interest_amount = round(self._balance * self.interest_rate, 2)
        self._balance += interest_amount
        trans = Transaction(
            TransactionType.INTEREST,
            interest_amount,
            self._balance
        )
        self._transactions.append(trans)
        return trans

    def to_dict(self): 
        data = super().to_dict()
        data['interest_rate'] = self.interest_rate
        return data

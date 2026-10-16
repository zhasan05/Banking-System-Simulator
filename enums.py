from enum import Enum

# Represents the type of a bank account
class AccountType(Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

# Represents the type of a financial transaction recorded on an account.
class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    INTEREST = "INTEREST"
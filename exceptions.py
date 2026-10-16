class BankError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InsufficientFundsError(BankError):
    def __init__(self, requested: float, available: float):
        self.requested = requested
        self.available = available
        super().__init__(f"Cannot withdraw ${requested:.2f} — maximum available is ${available:.2f}.")

class InvalidAmountError(BankError):
    def __init__(self, amount: float):
        self.amount = amount 
        super().__init__(f"Amount must be positive, got ${amount:.2f}.")

class AccountNotFoundError(BankError):
    def __init__(self, account_id: str):
        self.account_id = account_id 
        super().__init__(f"No account found with ID '{account_id}'.")

class AccountClosureError(BankError):
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id 
        self.balance = balance 
        super().__init__(f"Cannot close '{account_id}' — balance is ${balance:.2f}")
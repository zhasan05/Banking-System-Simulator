from enums import AccountType
from exceptions import AccountClosureError, AccountNotFoundError
from models import Account, CheckingAccount, SavingsAccount, Transaction

class Bank():
    def __init__(self, name: str = "ZEE Bank") -> None:
        self.name = name
        self._accounts = {}
        self._next_id = 1

    def _generate_id(self) -> str:
        account_id = f"ACC-{self._next_id:04d}"
        self._next_id += 1
        return account_id

    def create_account(self, owner_name: str, account_type: AccountType, initial_balance: float = 0.00, **kwargs) -> Account:
        if not owner_name or not owner_name.strip():
            raise ValueError("Owner name cannot be empty.")

        account_id = self._generate_id()
        if account_type == AccountType.CHECKING:
            new_account = CheckingAccount(
                account_id,
                owner_name,
                initial_balance,
                kwargs.get("overdraft_limit", 200.00)
            )
        elif account_type == AccountType.SAVINGS:
            new_account = SavingsAccount(
                account_id,
                owner_name,
                initial_balance,
                kwargs.get("interest_rate", 0.02)
            )
        else:
            raise ValueError("Invalid account type.")

        self._accounts[account_id] = new_account
        return new_account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise AccountNotFoundError(account_id)
        return self._accounts[account_id]

    def list_accounts(self) -> list:
        sorted_accounts = sorted(self._accounts.values(), key=lambda account: account.account_id)
        return sorted_accounts

    def total_assets(self) -> float:
        total = 0
        for acc in self._accounts.values():
            total += acc.balance 
        return total

    def close_account(self, account_id: str) -> Account:
        account = self.get_account(account_id) 
        if account.balance != 0:
            raise AccountClosureError(account_id, account.balance)
        self._accounts.pop(account_id)
        return account

    def to_dict(self) -> dict:
        accounts = []
        for acc in self._accounts.values():
            accounts.append(acc.to_dict())
        base_dict = {
            "name" : self.name,
            "accounts" : accounts,
            "next_id" : self._next_id
        }
        return base_dict

        
    @classmethod
    def from_dict(cls, data: dict) -> "Bank":
        bank = cls(name = data["name"]) # creates a new bank - creates empty Bank("ZEE Bank")
        bank._next_id = data["next_id"]

        for acc_data in data["accounts"]:
            account_type = acc_data["account_type"]
            if account_type == AccountType.CHECKING.value:
                account = CheckingAccount(
                    acc_data["account_id"],
                    acc_data["owner_name"],
                    acc_data["balance"],
                    acc_data.get("overdraft_limit", 200.00),
                )
            elif account_type == AccountType.SAVINGS.value:
                account = SavingsAccount(
                    acc_data["account_id"],
                    acc_data["owner_name"],
                    acc_data["balance"],
                    acc_data.get("interest_rate", 0.01),
                )
            else:
                raise ValueError(f"Unknown account type: {account_type}")

            # Reconstruct transaction history for this account
            for txn_data in acc_data.get("transactions", []):
                account._transactions.append(Transaction.from_dict(txn_data))
            bank._accounts[account.account_id] = account
        return bank
        
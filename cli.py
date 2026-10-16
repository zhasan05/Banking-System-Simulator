from bank import Bank
from enums import AccountType
from exceptions import BankError
from models import SavingsAccount

# Display
def _header(bank: Bank) -> None:
    print()
    print(f"{bank.name}  —  Total assets: ${bank.total_assets():,.2f}")
    print()

def _separator() -> None:
    print(60 * "=")

def _success(message: str) -> None:
    print(f"  ✓ {message}")

def _error(message: str) -> None:
    print(f"  ✗ Error: {message}")

# read input and return None if blank
def _get_float(prompt: str) -> float | None:
    user_prompt = input(f"{prompt}").strip()
    if not user_prompt:
        return None
    else:
        try:
            convert_prompt = float(user_prompt)
            return convert_prompt
        except ValueError:
            _error(f"'{user_prompt}' is not a valid number.")
            return None

# read input and format it 
def _get_account_id(prompt: str = "Account ID: ") -> str:
    user_prompt = input(f"{prompt}").strip().upper()
    return user_prompt

# ====== Action Functions =========

def action_deposit(bank):
    print("--- Deposit ---")
    account_id = _get_account_id()
    amount = _get_float("Amount to deposit: $")

    if amount == None:
        return None
    try:
        account = bank.get_account(account_id)
        txn = account.deposit(amount)
        _success("Deposit successful")
        print(f"  {txn}")
        print(f"\n  New balance: ${account.balance:,.2f}")
    except BankError as e:
        _error(e.message)

def action_withdraw(bank):
    print("--- Withdrawal ---")
    account_id = _get_account_id()
    amount = _get_float("Amount to withdraw: $")

    if amount == None:
        return None
    try:
        account = bank.get_account(account_id)
        txn = account.withdraw(amount)
        _success("Withdrawal successful")
        print(f"Transaction: {txn} and new balance: {bank.balance}")
    except BankError as e:
        _error(e.message)

def action_check_balance(bank):
    account_id = _get_account_id()
    try:
        account = bank.get_account(account_id)
        print(account)
        if isinstance(account, SavingsAccount):
            print(f"  Interest rate: {account.interest_rate * 100:.1f}%")
        else:
            print(f"  Overdraft limit: ${account.overdraft_limit:,.2f}")
    except BankError as e:
        _error(e.message)

def action_view_statement(bank):
    account_id = _get_account_id()
    try:
        account = bank.get_account(account_id)
        transactions = account.get_statement()
        print()
        print(f"Owner Name: {account.owner_name}) and Account id: {account_id}")
        print()
        if not transactions: 
            print ("No transactions yet")
        else:
            for txn in transactions:
                print(txn) 
        print()
        print(f"Account balance: {account.balance}")
    except BankError as e:
        _error(e.message)

def action_list_accounts(bank):
    accounts = bank.list_accounts()
    if not bank.account:
        print ("No accounts yet")
    print()
    for acc in accounts:
        print(f"Account: {acc}")
    print()
    print(f"Total count {account.total_count} and Total assets {account.total_count}")

def action_create_account(bank):

# 3. print account type menu [1] Checking [2] Savings
# 4. get choice from input()
# 5. if "1" → account_type = CHECKING, get overdraft_limit
#    if "2" → account_type = SAVINGS, get interest_rate
#    else   → _error() → return
# 6. get initial_balance from _get_float()
# 7. try:
#       account = bank.create_account(...)
#       _success("Account created!")
#       print(account)
#    except (BankError, ValueError) as e:
#       _error(str(e))

    print("\n  --- Create New Account ---")

    # Step 1: owner name
    owner_name = input("  Owner name: ").strip()
    if not owner_name:
        _error("Owner name cannot be empty.")
        return

    # Step 2: account type
    print("  Account type:")
    print("    [1] Checking  (overdraft allowed)")
    print("    [2] Savings   (earns interest)")
    choice = input("  Choose (1/2): ").strip()

    if choice == "1":
            account_type = AccountType.CHECKING
            raw_limit = _get_float("Overdraft limit (default $200): ")
            overdraft_limit = raw_limit if raw_limit is not None else 200.00
    
    elif choice == "2":
        account_type = AccountType.SAVINGS
        raw_rate = _get_float("Interest rate e.g. 0.02 for 2% (default 0.02): ")
        interest_rate = raw_rate if raw_rate is not None else 0.02

    else:
        _error("Invalid choice. Please enter 1 or 2.")
        return



def action_apply_interest(bank):

    print("\n  --- Apply Interest (Savings only) ---")
    account_id = _get_account_id()
    try:
        account = bank.get_account(account_id)
        if not isinstance(account, SavingsAccount):
            _error("Interest can only be applied to Savings accounts.")
            return
        txn = account.apply_interest()
        _success(f"Interest applied at {account.interest_rate * 100:.1f}%.")
        print(f"  {txn}")
        print(f"\n  New balance: ${account.balance:,.2f}")
    except BankError as e:
        _error(e.message)

def action_close_account(bank):

    print("\n  --- Close Account ---")
    account_id = _get_account_id()
    try:
        account = bank.get_account(account_id)
        print(f"\n  {account}")
        confirm = input("  Type 'YES' to confirm closure: ").strip()
        if confirm != "YES":
            print("  Cancelled — account not closed.")
            return
        bank.close_account(account_id)
        _success(f"Account {account_id} closed successfully.")
    except BankError as e:
        _error(e.message)

# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU_OPTIONS = {
    "1": ("Create account",           action_create_account),
    "2": ("Deposit",                  action_deposit),
    "3": ("Withdraw",                 action_withdraw),
    "4": ("Check balance",            action_check_balance),
    "5": ("View statement",           action_view_statement),
    "6": ("List all accounts",        action_list_accounts),
    "7": ("Apply interest (Savings)", action_apply_interest),
    "8": ("Close account",            action_close_account),
    "9": ("Exit",                     None),
}


def show_menu(bank: Bank) -> None:
    """
    Display the main menu options.

    Parameters:
        bank (Bank): passed to _header() for the bank name display.
    """
    _header(bank)
    print()
    for key, (label, _) in MENU_OPTIONS.items():
        print(f"  [{key}] {label}")
    print()


def run(bank: Bank) -> None:
    """
    Run the main CLI loop until the user selects Exit.

    This is the only function called from main.py. It loops forever,
    showing the menu, reading input, and dispatching to the right action.

    Parameters:
        bank (Bank): the Bank instance to operate on.
    """
    print(f"\n  Welcome to {bank.name}!")

    while True:
        show_menu(bank)
        choice = input("  Your choice: ").strip()

        if choice not in MENU_OPTIONS:
            _error(f"'{choice}' is not valid. Choose 1-9.")
            continue

        label, action_fn = MENU_OPTIONS[choice]

        if action_fn is None:
            print("\n  Goodbye!\n")
            break

        try:
            action_fn(bank)
        except BankError as e:
            _error(e.message)
        except KeyboardInterrupt:
            print("\n  (Interrupted — returning to menu)")
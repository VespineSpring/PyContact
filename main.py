import typer
import os
import json
import uuid

from rich import print

app = typer.Typer()
SETTINGS_FILE = "database/settings.json"
ACCOUNTS_FILE = "database/accounts.json"


def is_initialized() -> bool:
    try:
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)
    except:
        return False

    if not data:
        return False

    if not data.get("initialized", False):
        return False

    return True


def setup_database(username: str, password: str) -> None:
    os.makedirs(f"database/accounts/{username.lower()}", exist_ok=True)

    settings_entry = {
        "initialized": True,
        "current_account": None,
        "accounts": [username],
    }

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_entry, file, indent=4)

    account_id = str(uuid.uuid4())

    if not os.path.exists(ACCOUNTS_FILE) or os.path.getsize(ACCOUNTS_FILE) == 0:
        with open(ACCOUNTS_FILE, "w") as file:
            json.dump([], file, indent=4)

    account_data_entry = {"id": account_id, "username": username, "password": password}

    with open(ACCOUNTS_FILE, "r") as file:
        account_data = json.load(file)

    account_data.append(account_data_entry)

    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(account_data, file, indent=4)

    USER_FILE = f"database/accounts/{username.lower()}/settings.json"
    CONTACTS_FILE = f"database/accounts/{username.lower()}/contacts.json"

    user_data_entry = {"id": account_id, "username": username, "password": password}

    with open(USER_FILE, "w") as file:
        json.dump(user_data_entry, file, indent=4)

    if not os.path.exists(CONTACTS_FILE) or os.path.getsize(CONTACTS_FILE) == 0:
        with open(CONTACTS_FILE, "w") as file:
            json.dump([], file, indent=4)


is_app_initialized = is_initialized()


@app.command(name="init")
def initialize() -> None:
    if is_app_initialized:
        print("[red]App has been already initialized![/red]")
        return

    while True:
        username: str = input("Username: ")

        if len(username) <= 3:
            print("[red]Your username should be of 4 letters.[/red]")
            continue

        password: str = input("Password: ")

        break

    setup_database(username=username, password=password)

    print("[green]App has been initialized.[/green]")


@app.command()
def add_user() -> None:
    if not is_app_initialized:
        print("[red]App has not been initialized yet.\nRun 'init' command to initialize it.[/red]")
        return

    while True:
        username: str = input("Username: ")

        if len(username) <= 3:
            print("[red]Your username should be of 4 letters.[/red]")
            continue

        password: str = input("Password: ")

        break

    with open(SETTINGS_FILE, "r") as file:
        settings_entry = json.load(file)

    accounts_list = settings_entry.get("accounts", [])

    accounts_list.append(username)

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_entry, file, indent=4)

    account_id = str(uuid.uuid4())

    account_data_query = {"id": account_id, "username": username, "password": password}

    with open(ACCOUNTS_FILE, "r") as file:
        account_data = json.load(file)

    account_data.append(account_data_query)

    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(account_data, file, indent=4)

    os.makedirs(f"database/accounts/{username.lower()}", exist_ok=True)

    USER_FILE = f"database/accounts/{username.lower()}/settings.json"
    CONTACTS_FILE = f"database/accounts/{username.lower()}/contacts.json"

    user_data_entry = {"id": account_id, "username": username, "password": password}

    with open(USER_FILE, "w") as file:
        json.dump(user_data_entry, file, indent=4)

    if not os.path.exists(CONTACTS_FILE) or os.path.getsize(CONTACTS_FILE) == 0:
        with open(CONTACTS_FILE, "w") as file:
            json.dump([], file, indent=4)

    print("[green]User has been added![/green]")


if __name__ == "__main__":
    app()

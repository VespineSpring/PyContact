import typer
import os
import json
import uuid

from rich import print
from rich.console import Console
from rich.table import Table

app = typer.Typer()
SETTINGS_FILE = "database/settings.json"
ACCOUNTS_FILE = "database/accounts.json"
console = Console()


def initialization_check() -> bool:
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

    user_file = f"database/accounts/{username.lower()}/settings.json"
    contacts_file = f"database/accounts/{username.lower()}/contacts.json"

    user_data_entry = {"id": account_id, "username": username, "password": password}

    with open(user_file, "w") as file:
        json.dump(user_data_entry, file, indent=4)

    if not os.path.exists(contacts_file) or os.path.getsize(contacts_file) == 0:
        with open(contacts_file, "w") as file:
            json.dump([], file, indent=4)


@app.command(name="init")
def initialize() -> None:
    if initialization_check():
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


def command_initialization_check() -> None:
    if not initialization_check():
        print(
            "[red]App has not been initialized yet.\nRun 'init' command to initialize it.[/red]"
        )
        return


@app.command()
def add_user() -> None:
    command_initialization_check()

    while True:
        username: str = input("Username: ")

        if len(username) <= 3:
            print("[red]Your username should be of 4 letters.[/red]")
            continue

        password: str = input("Password: ")

        break

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    accounts_list = settings_data.get("accounts", [])

    accounts_list.append(username)

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_data, file, indent=4)

    account_id = str(uuid.uuid4())

    account_data_query = {"id": account_id, "username": username, "password": password}

    with open(ACCOUNTS_FILE, "r") as file:
        account_data = json.load(file)

    account_data.append(account_data_query)

    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(account_data, file, indent=4)

    os.makedirs(f"database/accounts/{username.lower()}", exist_ok=True)

    user_file = f"database/accounts/{username.lower()}/settings.json"
    contacts_file = f"database/accounts/{username.lower()}/contacts.json"

    user_data_entry = {"id": account_id, "username": username, "password": password}

    with open(user_file, "w") as file:
        json.dump(user_data_entry, file, indent=4)

    if not os.path.exists(contacts_file) or os.path.getsize(contacts_file) == 0:
        with open(contacts_file, "w") as file:
            json.dump([], file, indent=4)

    print("[green]User has been added![/green]")


@app.command()
def login(username: str) -> None:
    command_initialization_check()

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    current_account = settings_data.get("current_account", None)

    if current_account != None:
        print(
            f"[red]You are currently logged in to {current_account}.\nUse switch or logout command.[/red]"
        )
        return

    user_file = f"database/accounts/{username.lower()}/settings.json"

    try:
        with open(user_file, "r") as file:
            user_data = json.load(file)
    except:
        print("[red]User does not exists.[/red]")
        return

    if not user_data:
        print("[red]Error in loading data.[/red]")

    account_password = user_data.get("password")

    while True:
        password = input("Password: ")

        if account_password != password:
            print("[red]Wrong password.")
            continue

        break

    settings_data["current_account"] = username

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_data, file, indent=4)

    print(f"[green]Successfully logged in as {username}.[/green]")


@app.command()
def switch_account(username: str) -> None:
    command_initialization_check()

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    current_account = settings_data.get("current_account", None)

    if current_account == None:
        print("[red]You haven't logged in yet.\nUse login command to login.")
        return

    user_file = f"database/accounts/{username.lower()}/settings.json"

    try:
        with open(user_file, "r") as file:
            user_data = json.load(file)
    except:
        print("[red]User does not exists.[/red]")
        return

    if not user_data:
        print("[red]Error in loading data.[/red]")

    account_password = user_data.get("password")

    while True:
        password = input("Password: ")

        if account_password != password:
            print("[red]Wrong password.")
            continue

        break

    settings_data["current_account"] = username

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_data, file, indent=4)

    print(f"[green]Successfully switched to {username}.[/green]")


@app.command()
def logout() -> None:
    command_initialization_check()

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    username = settings_data.get("current_account", None)

    if username == None:
        print("[red]You haven't logged in yet.[/red]")
        return

    settings_data["current_account"] = None

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_data, file, indent=4)

    print(f"[yellow]Successfully logged out of {username}[/yellow]")


@app.command()
def add_contact() -> None:
    command_initialization_check()

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    username = settings_data.get("current_account", None)

    if username == None:
        print("[red]You haven't logged in yet.\nUse login command to login.[/red]")
        return

    while True:
        contact_name = input("Name: ")

        if contact_name == 0:
            print("[red]Please enter a valid name.[/red]")
            continue

        contact_number = input("Number: ")

        if len(contact_number) != 10:
            print("[red]Please enter a valid number.[/red]")
            continue

        break

    contacts_file = f"database/accounts/{username.lower()}/contacts.json"

    with open(contacts_file, "r") as file:
        contacts_data = json.load(file)

    contact_data_entry = {"name": contact_name, "number": contact_number}

    contacts_data.append(contact_data_entry)

    with open(contacts_file, "w") as file:
        json.dump(contacts_data, file, indent=4)

    print("[green]Contact has been added.")


@app.command()
def contacts() -> None:
    command_initialization_check()

    with open(SETTINGS_FILE, "r") as file:
        settings_data = json.load(file)

    username = settings_data.get("current_account", None)

    if username == None:
        print("[red]You haven't logged in yet.\nUse login command to login.[/red]")
        return
    
    contacts_file = f"database/accounts/{username}/contacts.json"

    table = Table("Name", "Number")

    with open(contacts_file, "r") as file:
        contacts_data = json.load(file)

    if contacts_data == []:
        print("[red]No contact found.[/red]")
        return

    for query in contacts_data:
        contact_name = query.get("name", None)
        contact_number = query.get("number", None)
        if contact_name is None or contact_number is None:
            print("[yellow]Skipping incomplete contact entry.[/yellow]")
            continue
        table.add_row(contact_name, contact_number)

    console.print(table)



if __name__ == "__main__":
    app()

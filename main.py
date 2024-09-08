import typer
import os
import json
import uuid

from rich import print

app = typer.Typer()
SETTINGS_FILE = "database/settings.json"
ACCOUNTS_FILE = "database/accounts.json"


@app.command(name="init")
def initialize():
    while True:
        username: str = input("Username: ")

        if len(username) <= 3:
            print("[red]Your username should be of 4 letters.[/red]")
            continue

        password: str = input("Password: ")

        break

    create_files(username=username, password=password)

    print("[green]App has been initialized.[/green]")


def create_files(username: str, password: str):
    settings_data = {
        "initialized": True,
        "current_account": None,
        "accounts": [username]
    }

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings_data, file, indent=4)

    account_id = str(uuid.uuid4())

    if not os.path.exists(ACCOUNTS_FILE) or os.path.getsize(ACCOUNTS_FILE) == 0:
        with open(ACCOUNTS_FILE, "w") as file:
            json.dump([], file, indent=4)

    account_data_query = {
        "id": account_id,
        "username": username,
        "password": password
    }

    with open(ACCOUNTS_FILE, "r") as file:
        account_data = json.load(file)

    account_data.append(account_data_query)

    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(account_data, file, indent=4)


if __name__ == "__main__":
    app()

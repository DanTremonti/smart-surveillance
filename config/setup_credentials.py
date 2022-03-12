import toml
from pathlib import Path

def setup_credentials():
    p = Path('.')
    config_file = list(p.glob('**/*.toml'))

    config = toml.load(config_file)
    print("\nCredentials stored:")
    print(">> Name:", config['user']['name'])
    print(">> Email id:", config['user']['email'])
    print(">> Password:", config['user']['password'])
    print(">> Phone number:", config['user']['mobile'], end='\n\n')

    if (input("Do you want to update the credentials stored? (y/n): ") == "y"):
        print("\nEnter your credentials:")
        config["user"]["name"] = input(">> Name: ").strip()
        config["user"]["email"] = input(">> Email id: ").strip()
        config["user"]["password"] = input(">> Password: ").strip()
        config["user"]["mobile"] = input(">> Phone number: ").strip()

        toml.dump(config, open(config_file[0], "w"))
        print("Credentials saved successfully!")

    else:
        print("Credentials not updated!")
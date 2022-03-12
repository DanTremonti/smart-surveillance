import smtplib
import toml
from pathlib import Path

def load_config_data() -> dict:
    curr_file_path = Path(__file__).parent
    config_path = curr_file_path.parent.parent / 'config' / 'config.toml'

    config = toml.load(config_path)
    return config

def send_email(config: dict, message: str) -> None:
    server = smtplib.SMTP('smtp.gmail.com', config['user']['port'])
    server.starttls()
    server.login(config['user']['email'], config['user']['password'])
    server.sendmail(config['user']['email'], config['user']['email'], message)
    server.quit()

def main():
    credentials = load_config_data()
    send_email(credentials, 'Test message')

if __name__ == '__main__':
    main()
import os
from dotenv import load_dotenv
def main_load_env(file_path: str = "ops.env"):
    if os.path.exists(file_path):
        load_dotenv(file_path)
    else :
        print(f'{file_path} not found, using ops_env.env default file')
        load_dotenv('ops_env.env')

main_load_env()
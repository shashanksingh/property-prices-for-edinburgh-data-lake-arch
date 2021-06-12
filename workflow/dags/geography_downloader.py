import requests
import shutil
import zipfile
import os

download_geography_data_url = "https://api.os.uk/downloads/v1/products/OpenNames/downloads?area=GB&format=CSV&redirect"
LOCAL_FILE_NAME = "opname_csv_gb.zip"
EXECUTION_DATE = "2021-08-10/"
DATA_FOLDER = "data/bronze/"


def download_file(url: str, file_name: str):
    with requests.get(url, stream=True) as r:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def unzip_file(file_name: str):
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(f"{DATA_FOLDER}{EXECUTION_DATE}{LOCAL_FILE_NAME.split('.')[0]}")


def remove_zip_file(file_name: str):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        print(f"file doesnt exist {file_name}")


def run():
    try:
        download_file(download_geography_data_url, LOCAL_FILE_NAME)
        unzip_file(LOCAL_FILE_NAME)
        remove_zip_file(LOCAL_FILE_NAME)
    except requests.exceptions.RequestException as e:
        print(e)

import os
import datetime
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi


def check_and_download(competition, path='../data/input'):
    api = KaggleApi()
    api.authenticate()

    # Check if any file in the directory is newer than a week
    need_download = True
    if os.path.exists(path):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                last_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if (datetime.datetime.now() - last_modified_time).days < 7:
                    need_download = False
                    break
    else:
        # Create directory if it doesn't exist
        os.makedirs(path)

    # Download the files if needed
    if need_download:
        print("Downloading or re-downloading the data...")
        api.competition_download_files(competition, path=path, quiet=False, force=True)

        # Unzip files if the downloaded file is a zip
        for file in os.listdir(path):
            if file.endswith(".zip"):
                zip_path = os.path.join(path, file)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(path)
                os.remove(zip_path)  # Remove the zip file after extraction

        print(f"Data for {competition} downloaded and extracted to {path}.")
    else:
        print("Existing files are up-to-date.")

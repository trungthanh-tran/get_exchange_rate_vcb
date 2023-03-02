import wget
import os
from zipfile import ZipFile

class Utils:
    @staticmethod
    def create_dir_if_missing(dir: str):
        MYDIR = (dir)
        CHECK_FOLDER = os.path.isdir(MYDIR)
        if not CHECK_FOLDER:
            os.makedirs(MYDIR)
            print("created folder : ", MYDIR)
        else:
            print(MYDIR, "folder already exists.")

    @staticmethod
    def check_existed(dir: str):
        MYDIR = (dir)
        CHECK_FILE = os.path.isfile(MYDIR)
        if not CHECK_FILE:
            return False
        else:
            return True

    @staticmethod
    def download_file(url: str, dir: str):
        Utils.create_dir_if_missing(dir)
        os.chdir(dir)
        fileName = wget.download(url)
        # Unzip it
        zf = ZipFile(fileName, 'r')
        zf.extractall()
        zf.close()


    
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os,time
from datetime import datetime

from .utils import Utils
from .exchange_rate_base import ExchangeRateBase

class VCBExchangeRate (ExchangeRateBase):
    supported_currency_codes = [
            'AUD',
            'CAD',
            'CHF',
            'CNY',
            'DKK',
            'EUR',
            'GBP',
            'HKD',
            'INR',
            'JPY',
            'KRW',
            'RUB',
            'SGD',
            'THB',
            'USD'
            ]
    website = "https://portal.vietcombank.com.vn/en-Us/Personal/TG/Pages/exchange-rate.aspx"
    delay = 5
    chrome_dir = "drivers/win32"
    chrome_file = "chromedriver.exe"
    chrome_download_file = "https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_win32.zip"

    def getExchangeRate(self,src: str, dest: str, dateString : str):
        if not VCBExchangeRate.validate_code(src):
            print ("Unsupported code")
            exit(1)

        if not VCBExchangeRate.validate_date(dateString):
            print ("Invalid date time")
            exit(1)
        # headless option
        options = Options()
        if not Utils.check_existed(os.path.join(self.chrome_dir, self.chrome_file)):
            Utils.download_file(self.chrome_download_file, self.chrome_dir)
        service = Service(executable_path=os.path.join(self.chrome_dir, self.chrome_file))
        driver = webdriver.Chrome(service=service)
        driver.get(self.website)
        # Open then wait for ready
        while True:
            try:
                WebDriverWait(driver, self.delay).until(EC.presence_of_element_located((By.ID, 'txttungay')))
                break # it will break from the loop once the specific element will be present. 
            except TimeoutException:
                print ("Loading took too much time!-Try again")
                exit(1)
        # Enter date
        datefield = driver.find_element('id', 'txttungay')
        datefield.click()
        time.sleep(2)
        datefield.clear()
        datefield.send_keys(dateString)
        datefield.send_keys(Keys.RETURN)
        while True:
            try:
                WebDriverWait(driver, self.delay).until(EC.text_to_be_present_in_element((By.ID, 'UpdateTime'), VCBExchangeRate.vcb_date(dateString)))
                break # it will break from the loop once the specific element will be present. 
            except TimeoutException:
                print ("Loading took too much time!-Try again")
                exit(1)
        #  Get element
        exchangeTable = pd.read_html(driver.find_element('id', 'ctl00_Content_ExrateView').get_attribute('outerHTML'))        
        df = exchangeTable[0]
        value = df[df['Currency']['Currency Code'] == 'USD'].iloc[0]
        print(value.get('Selling Rates').get('Selling Rates'))

    @staticmethod
    def validate_code(currency_code: str):
        if currency_code in VCBExchangeRate.supported_currency_codes:
            return True
        return False

    @staticmethod
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def vcb_date(date_text):
        try:
            return datetime.strptime(date_text, '%d/%m/%Y').strftime('%d/%m/%Y')
        except ValueError:
            return False
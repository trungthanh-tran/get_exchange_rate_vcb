from ExchangeRate.vcb import VCBExchangeRate

def main():
    
    objectBank =  VCBExchangeRate()
    objectBank.getExchangeRate("USD", "2", "1/1/2023")

if __name__=="__main__":
    main()
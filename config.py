import sys

selenium_arguments = [
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/97.0.4692.99 Safari/537.36',
    '--disable-blink-features=AutomationControlled'
]

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.99 Safari/537.36'
}

chromedriver_mac_path = 'selenium_drivers/chromedriver_mac'
chromedriver_linux_path = 'selenium_drivers/'
match sys.platform:
    case 'linux':
        browser_path = chromedriver_linux_path
    case 'darwin':
        browser_path = chromedriver_mac_path
    case _:
        print("ERROR: can't found selenium driver")

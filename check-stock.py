import datetime
import json
from lxml import etree
import os
import random
from selenium import webdriver
from termcolor import colored
import time
import urllib.request

def main():
    with open('config.json') as f:
        config = json.load(f)
        random.shuffle(config)

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    for check in config:
        try:
            response = driver.get(check['url'])
            current_text = str(driver.find_element_by_xpath(check['xpath']).text)
            is_expected = current_text.strip().lower() == check['expected_text'].lower()
            is_available = not is_expected if ('negate_check' in check.keys()
                                               and check['negate_check']) else is_expected
            if is_available:
                print(datetime.datetime.now(), '[' + check['name'] + ']', colored('IN STOCK!!!', 'green'))
            else:
                print(datetime.datetime.now(), '[' + check['name'] + ']', colored(current_text, 'red'))
                
            if is_available:
                with open('recent.txt', 'a') as f:
                    f.write('[' + check['name'] + ']: ' + str(datetime.datetime.now()) + '\n')

            time.sleep(random.randint(5, 10))
        except Exception as e:
            print('Failed check:', check['name'])
            print(e)

    driver.close()
    print('Done one round...')


if __name__ == '__main__':
    main()

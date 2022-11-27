# pip3 install selenium
# you also need a chromedriver according to your chrome version, available at https://chromedriver.chromium.org/downloads

from selenium import webdriver
from enum import Enum
import time

try:
    from flag import getflag
except:
    def getflag(index):
        return [
            'fake{congrats, now get flag 1 from the real xss bot}',
            'fake{congrats, now get flag 2 from the real xss bot}',
        ][index-1]

VULN_URL = 'http://prob06-vuln.geekgame.pku.edu.cn'

def remove_protocols(t):
    for prefix in ['http://', 'https://', 'file://']:
        if t.startswith(prefix):
            return t[len(prefix):]
    return t

class SafetyLevel(Enum):
    dangerous = 1
    safe = 2
    very_safe = 3

def check_safety(driver, text):
    if '%' in text:
        return SafetyLevel.dangerous
    
    text = remove_protocols(text)
    
    driver.get('chrome://omnibox')
    time.sleep(.5)
    
    shadow = driver.find_element('id', 'omnibox-input').shadow_root
    shadow.find_element('id', 'zero-suggest').click()
    shadow.find_element('id', 'input-text').send_keys(text)
    time.sleep(.5)
    
    result = ( # it looks stupid that chrome://omnibox uses so many shadow doms :(
        driver
            .find_element('id', 'omnibox-output').shadow_root
            .find_element('css selector', 'output-results-group').shadow_root
            .find_element('css selector', 'output-results-details').shadow_root
            .find_element('id', 'type').text
    )
    
    if result=='query':
        return SafetyLevel.very_safe
    elif result=='unknown':
        return SafetyLevel.safe
    else:
        return SafetyLevel.dangerous

try:
    print('\nYOU-Chan is going to visit a vulnerable website:', VULN_URL)
    print('Send some text to YOU-Chan, and she will paste it in that website.')
    
    text = input('> ')
    assert all(0x20<=ord(c)<=0x7e for c in text) and len(text)<=4000
    
    print('\nStarting up her browser...')
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox') # sandbox not working in docker :(
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome(options=options) as driver:
        ua = driver.execute_script('return navigator.userAgent')
        print('She is using:', ua)
        
        print('\nFirst of all, she checks the safety of your text,')
        safety = check_safety(driver, text)
        print('  which is %s.'%safety.name)
        
        if safety==SafetyLevel.dangerous:
            print('\nShe feels afraid because of this.')
            assert False
        
        print('\nThen she visits the vulnerable website,')
        driver.get(VULN_URL)
        time.sleep(1)
        print('  and put her flag for you.')
        driver.execute_script('document.querySelector(".flag").textContent = "%s"'%getflag(2))
        time.sleep(1)
        
        print('\nNow she pastes your text into the text field,')
        driver.find_element('id', 'filename').clear()
        driver.find_element('id', 'filename').send_keys(text)
        time.sleep(.5)
        print('  and clicks on the button.')
        driver.find_element('id', 'go').click()
        time.sleep(5)
        
        title = driver.title
        print('\nThe page title is:', title)
        
        if safety==SafetyLevel.very_safe and title=='GIVE-ME-FLAG-1 #=_= @!+!@ ^~^ %[*.*]%':
            print('  so here is your flag 1:', getflag(1))
        
    print('\nSee you later :)')
    
except Exception as e:
    print('ERROR', type(e))
    #raise
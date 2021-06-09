from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from telethon.sync import TelegramClient

import platform
import requests


import time
import configparser
import codecs
import csv
import sys, os

import socket

import threading as th

import traceback


if len(sys.argv) < 3: # 2 args
    print("Usage: " + sys.argv[0] + " [config file] [accounts file]")
    exit(-1)

print("Open Selenya(trashazart)")
print("Project is deprecated, no future support")

runlink = 'https://csgorun.pro'

opts = Options()
opts.headless = True
opts.add_argument("--width=800")
opts.add_argument("--height=600")

def loadaccs(path):
    data = []
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        first = True
        for row in reader:
            if first:
                first = False
                continue

            data.append(row)
        return data

def closebrowsers():
    print("Closing browsers...")
    for b in browsers:
        b.quit()

def exec_cmd(cmd):
    try:
        c = cmd.split(" ")

        if c[0].lower() == "ex": #execute any command
            exec(cmd[3:len(cmd)], globals())
            return True

        elif c[0].lower() == "go": #get output/variable
            exec("dbg_out = (" + cmd[3:len(cmd)] + ")", globals())
            return dbg_out

        elif c[0].lower() == "sc": #screenshot
            global browsers
            idx = cmd[3:len(cmd)]
            if idx == "all":
                for i in range(browsers):
                    browsers[i].save_screenshot("dgbshot" + str(idx) + ".png")
            browsers[int(idx)-1].save_screenshot("dbgshot" + str(idx) + ".png")
            return True
    except Exception as e:
        return str(e)

def manualactive(promo):
    global accounts, browsers
    results = [False] * len(accounts)
    for i in range(0, len(browsers)):
        status = activate_promo(browsers[i], promo, i)
        print(accounts[i][0] + ": " + status)
        if "You have successfully applied" in status:
            results[i] = True
        elif "Вы успешно активировали" in status:
            results[i] = True
    print("\n")

def dbg():
    try:
        sock = socket.socket()
        sock.bind(('', 4546))
    except Exception as e:
        print("Socket error: " + str(e))

    sock.listen(1)
    conn, addr = sock.accept()
    print("Debugger attached! Address:" + str(addr))


    #wait for cmd and execute

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
        except Exception as e:
            print("Socket Error: " + str(e))
            sock.close()

        out = exec_cmd(data.decode()) #run exec handler
        if out != True: #if something returned
            conn.send(str(out).encode())

        else: #if not returned - say that command executed without output
            conn.send(b"[EXECUTED]")



def wait_for_elem(browser, class_name, method=By.CLASS_NAME):
    return WebDriverWait(browser, 10).until(EC.presence_of_element_located((method, class_name)))

def wait_for_page(browser):
    return WebDriverWait(browser, 10).until(lambda browser: browser.execute_script("return document.readyState") == "complete")

def wait_for_run(browser):
    try:
        while len(wait_for_elem(browser, "//*[@id=\"page-content\"]", By.XPATH).find_elements_by_xpath("div")) == 2:
            time.sleep(0.2)

        while len(wait_for_elem(browser, "//*[@id=\"page-content\"]", By.XPATH).find_elements_by_xpath("div")) < 1:
            time.sleep(0.2)

        while "show" in wait_for_elem(browser, "//*[@id=\"page-content\"]/div", By.XPATH).get_attribute("class"):
            time.sleep(0.2)
    except:
        print(browser.page_source)
        raise

def creds(browser, account, idx):

    try:
        wait_for_page(browser)

        namefield = wait_for_elem(browser, "steamAccountName", By.ID)
        passfield = wait_for_elem(browser, "steamPassword", By.ID)
        namefield.send_keys(account[0])
        passfield.send_keys(account[1])
        passfield.submit()
        time.sleep(2)

    except Exception as e:
        print("Error logging in (browser " + str(idx+1) + "): " + str(e))
        browser.save_screenshot("error" + str(idx+1) + ".png")
        closebrowsers()
        os._exit(-1)

def guards(browser, idx):
    global codes

    while codes[idx] == "":
        pass

    try:
        guard = wait_for_elem(browser, "twofactorcode_entry", By.ID)
        guard.send_keys(codes[idx])
        guard.submit()
    except Exception as e:
        print("Error entering guard (browser " + str(idx+1) + "): " + str(e))
        browser.save_screenshot("error" + str(idx+1) + ".png")
        closebrowsers()
        os._exit(-1)

    while True:

        wait_for_page(browser)

        code_elems = browser.find_elements_by_id("login_twofactorauth_message_incorrectcode")
        wait_elems = browser.find_elements_by_id("login_twofactorauth_buttonset_waiting")

        try:
            msg = code_elems[0]
            wait = wait_elems[0]

            if msg.get_attribute("style") != "display: none;":
                print("\n\nInvalid guard code on browser " + str(idx+1))

            elif wait.get_attribute("style") != "display: none;":
                continue

            else:
                print("Error entering guard (browser " + str(idx+1) + ")")
                browser.save_screenshot("error" + str(idx+1) + ".png")

            closebrowsers()
            os._exit(-1)
        except: # When everything is good
            break


def activate_promo(browser, promo, idx):
    try:

        if "profile" not in browser.current_url:
            browser.find_element_by_class_name("header-user__about").click()
            time.sleep(3)

        inp = browser.find_elements_by_id("enter-promo-input")[0]
        inp.send_keys(promo)
        browser.find_elements_by_class_name("btn--blue")[3].click()

        #browser.find_elements_by_class_name("btn--blue")[0].click()

        msg = wait_for_elem(browser, "noty_body").text
        while msg == '':
            msg = wait_for_elem(browser, "noty_body").text

        inp.clear()
        time.sleep(0.5)
        inp.clear() #why BLYAT??? RUN??? idk

        return msg


    except Exception as e:
        browser.save_screenshot("error" + str(idx+1) + ".png")
        return "Error: " + str(e)

def loadcfg(path):
    try:
        config = configparser.ConfigParser()
        config.read(path)
        api_id = config.get("SelPromo", "api_id")
        api_hash = config.get("SelPromo", "api_hash")
        channel = config.get("SelPromo", "channel")
        name = config.get("SelPromo", "name")
        timeout = float(config.get("SelPromo", "timeout"))
    except Exception as e:
        print("Error reading config: " + str(e))
        exit(-1)

    return api_id, api_hash, channel, name, timeout

def load_filters(ppath, fpath, f2path):
    with codecs.open(ppath, encoding="utf8") as f:
        phrases = f.readlines()
        phrases = [x.strip() for x in phrases]

    with codecs.open(fpath, encoding="utf8") as f:
        filters = f.readlines()
        filters = [x.strip() for x in filters]

    with codecs.open(f2path, encoding="utf8") as f:
        filters2 = f.readlines()
        filters2 = [x.strip() for x in filters2]
    return phrases, filters, filters2

def checker(promo, phrases, filters, filters2):
    for c in filters2:
        if c == promo.lower():
            return None

    for c in filters:
        if c in promo:
            return None

    for c in phrases:
        promo = promo.replace(c, "")
        return promo

def bet(browser, idx):

    try:
        if "profile" in browser.current_url:
            browser.get(runlink + "/inventory")
            time.sleep(3)

        browser.find_element_by_class_name("checkbox-control").click() # Select all

        time.sleep(2)
        browser.get(runlink)

        input = browser.find_element_by_id("auto-upgrade-input")
        input.clear()
        time.sleep(0.5)
        input.clear() # For some reason
        input.send_keys("1.01") # Lowest coefficient


        timer = wait_for_elem(browser, "graph-svg__counter")
        button = browser.find_element_by_class_name("make-bet")
        print("Waiting for bet...")

        while 's' not in timer.text: # Countdown
            time.sleep(1)

        print("Betting")
        time.sleep(0.5)
        button.click()
        browser.save_screenshot("bet" + str(idx+1) + ".png")

    except Exception as e:
        print("Error betting: " + str(e))
        print("Trying again...\n")
        # bet(browser)

def createbrowser():
    if platform.system() != "Windows":
        browsers.append(Firefox(options=opts, service_log_path="/dev/null"))
    else:
        browsers.append(Firefox(options=opts))
    print("Started browser " + str(len(browsers)))

dbg_thread = th.Thread(target=dbg)
dbg_thread.start()

api_id, api_hash, channel, name, timeout = loadcfg(sys.argv[1])
if platform.system() != "Windows":
    phrases, filters, filters2 = load_filters("filters/phrases.txt", "filters/filter.txt", "filters/filter2.txt")
else:
    phrases, filters, filters2 = load_filters("filters\\phrases.txt", "filters\\filter.txt", "filters\\filter2.txt")

accounts = loadaccs(sys.argv[2])
browsers = []

threads = []

# Create browsers
for i in range(len(accounts)):
    threads.append(th.Thread(target=createbrowser))
    threads[i].start()

# Wait for finish
for i in range(len(threads)):
    threads[i].join()
threads.clear()

for i in range(len(browsers)):
    browsers[i].get(runlink)

    while True:
        try:
            browsers[i].find_elements_by_class_name("hide-above-l")[0].click()
            break
        except:
            pass


    print("Got run on browser " + str(i+1))

time.sleep(1)
print("")

# Enter creds
for i in range(len(browsers)):
    threads.append(th.Thread(target=creds, args=(browsers[i], accounts[i], i)))
    threads[i].start()

# Wait for finish
for i in range(len(threads)):
    threads[i].join()
threads.clear()

codes = [""] * len(accounts)

for i in range(len(browsers)):
    threads.append(th.Thread(target=guards, args=(browsers[i], i)))
    threads[i].start()

for i in range(len(accounts)):
    codes[i] = input("Enter guard code for " + accounts[i][0] + ": ")

print("")

# Wait for finish
for i in range(len(threads)):
    threads[i].join()
threads.clear()

for i in range(len(browsers)):
    # while(len(browsers[i].find_elements_by_class_name("loading")) != 2):
    #     time.sleep(0.2)
    wait_for_run(browsers[i])

    time.sleep(0.5)
    wait_for_elem(browsers[i], "header-user__about").click()

    time.sleep(2)
    try:
        browsers[i].find_element_by_class_name("account-btns").find_elements_by_xpath(".//*")[1].click()
    except Exception as e:
        print(i)
        print(str(e))
        print("-----------")
        pass
    print("Set page on browser " + str(i+1))

print("Waiting for messages...\n")

def check_new_msgs(tgclient, old_msgs, new_msgs):
    num = 0
    new_msgs.clear()
    for m in tgclient.iter_messages(channel):
        if num < 3:
            new_msgs.append(m.text)
        else:
            break
        num += 1

    if old_msgs[0] == new_msgs[0]:
        return None

    if old_msgs[0] == new_msgs[1]:
        return new_msgs[0]
    elif old_msgs[0] == new_msgs[2]:
        return new_msgs[1]
    else: # edited message
        return new_msgs[0]

#wait for new message
with TelegramClient(name, api_id, api_hash) as tgclient:

    new_msgs = []

    num = 0
    old_msgs = []
    for m in tgclient.iter_messages(channel):
        if num < 3:
            old_msgs.append(m.text)
        else:
            break
        num += 1

    try:

        while True:
            time.sleep(1)
            promo_raw = check_new_msgs(tgclient, old_msgs, new_msgs)

            if promo_raw == None:
                continue

            old_msgs = new_msgs.copy()

            promo = checker(promo_raw.lower(), phrases, filters, filters2)

            if promo == None:
                print("Ignoring message: " + promo_raw)
                continue

            print("Found promo: " + promo)

            results = [False] * len(browsers)

            first_res = activate_promo(browsers[0], promo, 0)

            st = True

            while first_res == "Not found!" or first_res == "Такой код не найден!":
                promo = input("Promo not found, please enter manually(skip to skip): ")
                if promo.lower() == "skip":
                	st = False
                	break

                while len(browsers[0].find_elements_by_class_name("noty_body")) > 0:
                    time.sleep(0.2)

                first_res = activate_promo(browsers[0], promo, 0)

            print(accounts[0][0] + ": " + first_res)
            if st == True:
                if "You have successfully applied" in first_res:
                    results[0] = True

                elif "Вы успешно активировали" in first_res:
                    results[0] = True

                for i in range(1, len(browsers)):
                    status = activate_promo(browsers[i], promo, i)
                    print(accounts[i][0] + ": " + status)
                    if "You have successfully applied" in status:
                        results[i] = True
                    elif "Вы успешно активировали" in status:
                        results[i] = True
            else:
                continue

            print('\n')

            time.sleep(5)

    except:
        print("Stopping!")
        closebrowsers()
        conn.close()
        raise

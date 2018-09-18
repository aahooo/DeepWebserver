import socket
import random
import hashlib
import os,sys

STAT_MEANING={
    200 : "OK",
    404 : "FUCK",
    400 : "INV"
    }
FILETYPES = {
    "txt" : "text/html",
    "html" : "text/html",
    "jpg" : "image/jpg",
    "png" : "image/png",
    "mp4" : "video/mp4",
    "js"  : "application/json",
    "ico" : "image/x-icon"
    }

class connection_status :
    Closed = "close"
    KeepAlive = "keep-alive"

def GetRandom(digits):
    rand_num = ""
    for i in range(digits):
        rand = int(random.random() * 36)
        if rand <= 9:
            rand_num += str(rand)
        else:
            rand_num += chr(rand+87)
    return rand_num



def sha256(string):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def NameToHash(string, location=""):
    begining_loc = os.getcwd()
    if location!="" :os.chdir(location)
    contains = os.listdir()
    os.chdir(begining_loc)
    temp=""
    if not(string in contains):
        return False
    for i in contains:
        temp+=i+":"
    temp+=string
    
    rand = GetRandom(2)
    #Zfill makes sure that random string has total length of 2

    temp = rand + temp + rand
    return rand+(sha256(temp)[:8])

def HashToName(cipher, location=False):
    begining_loc = os.getcwd()
    if location :os.chdir(location)
    contains = os.listdir()
    os.chdir(begining_loc)
    temp=""
    for i in contains:
        temp+=i+":"
    for i in contains:
        if sha256(temp+i)[:8]==cipher:return i
    return False

def AddressToHash(address):
    address = address.split("/")
    cipher=""
    current=""
    for i in address:
        if len(i)==0:continue
        try:
            cipher+= NameToHash(i,current)
        except:
            return False
        current+=i+r"/"
    return cipher

def HashToAddress(cipher):
    final = ""
    cipher = cipher.replace("/","")
    if len(cipher)%10!=0:
        return False
    cipher2=[]
    while cipher:
        cipher2.append(cipher[0:10:1])
        cipher = cipher[10:]
    begining_loc = os.getcwd()
    address = ""
    for sh in cipher2:
        rand = sh[:2]
        sh = sh[2:]
        was_ok = False
        temp = ""
        if os.path.isdir(address[1:]) : os.chdir(address[1:])
        #if not(os.path.isdir(address)):print("beeboo beeboo ==> "+address)
        contains = os.listdir()
        for i in contains: temp += i+":"
        main_str = temp
        for i in contains:
            if sha256(rand + main_str + i + rand)[:8]==sh:
                address+="/"+i
                was_ok = True
                break
        if not(was_ok):
            return False
        os.chdir(begining_loc)
    try:
        open(address[1:])
    except:
        return False
    return address[1:]

def HideLinks(message):
    links = message.split('href="')
    links = links[1:]
    for i in range(len(links)):
        links[i] = links[i].split('"')[0]
        temp = AddressToHash(links[i])
        if temp:
            links[i] = 'href="'+links[i]+'"'
            temp = 'href="'+temp+'"'
            message = message.replace(links[i] , temp)

    
    links = message.split('action="')
    links = links[1:]
    for i in range(len(links)):
        links[i] = links[i].split('"')[0]
        temp = AddressToHash(links[i].split('"')[0])
        if temp:
            links[i] = 'action="'+links[i]+'"'
            temp = 'action="'+temp+'"'
            message = message.replace(links[i] , temp)
    return message

if __name__=="__main__":
    if len(sys.argv)<2:sys.exit()
    print(sys.argv[1])
    print(HashToAddress(sys.argv[1]))

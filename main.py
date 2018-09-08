#!/usr/bin/env python3
import socket
import webserver
import threading
import sys
import re
import os
import importlib
BLOCKED_IP = []





def LoadConfig(conf = "config.conf"):
    conf_raw = open(conf).read().split("\n")
    if "" in conf_raw: conf_raw.remove("")
    config = dict()
    for i in conf_raw:
        temp = i.split("=")
        config[temp[0]] = temp[1]

    if config["403_PAGE"] == "" : config["403_PAGE"] = config["404_PAGE"]

    if config["ORIGIN"] not in config["403_PAGE"] or config["ORIGIN"] not in config["404_PAGE"] or config["ORIGIN"] not in config["INDEX_FILE"]:
        print("Check Default Pages in Config File")
        sys.exit()
    config["403_PAGE"] = config["403_PAGE"].split(config["ORIGIN"])[-1]
    config["404_PAGE"] = config["404_PAGE"].split(config["ORIGIN"])[-1]
    config["INDEX_FILE"] = config["INDEX_FILE"].split(config["ORIGIN"])[-1]
    return config


def TakeArgs(raw_string):
    raw_string = raw_string[raw_string.find("?")+1:]
    #print("Its The string ==> " +raw_string)
    if len(raw_string)==0:
        return False
    args = dict()
    args["NONAME"] = []

    while len(raw_string)>0:
        temp = raw_string[: raw_string.find("&")]
        print(temp)
        if "&" in raw_string:
            raw_string = raw_string[raw_string.find("&")+1:]
            #print("not")
        else:
            #print("no & ==> "+raw_string)
            temp = raw_string
            raw_string = ""
        if "=" in temp:
            eqloc = temp.find("=")
            args[ temp[:eqloc] ] = temp[eqloc+1:]
        else:
            args["NONAME"].append(temp)
    return args


def RunFile(sock , args , details , recursion = 0):
    
    #Cleaning asked_file argument by removing
    #'/' characters and parameters after ?
    if "?" in details["asked_file"] : file = details["asked_file"][:details["asked_file"].find("?")].replace("/","")
    else : file = details["asked_file"]

    #Checking if the asked File Exist's or not
    if file == "/":
        #User is asking for main index
        print (Config.get("INDEX_FILE"))
        file = Config.get("INDEX_FILE")
    else:
        file = webserver.HashToAddress(file)
        if not(file):
            #returning 404 Page
            Show404Page(sock , details)
            return


    #Detaching file format from file name
    file = file[:file[::-1].find(".")*-1-1]
    
    try:
        #Importing Asked module
        file = importlib.import_module(file.replace("/","."))
        message = file.main(args , details)
        file = None
    except AttributeError:
        #File Cannot Be opened (Does not have main function or has runtime error)
        Show404Page(sock , details)
        return
        
    
    

    connection_status = message[1]
    status_code = message[2]
    Content_size = len(message[0])
    if len(message) == 3:
        Content_type = webserver.FILETYPES["html"]
    elif len(message) == 4:
        Content_type = message[3]
    else:
        Show404Page(sock , details)
        return
    if Content_type == webserver.FILETYPES["html"]:
        #Hiding links if response was html text
        message[0] = webserver.HideLinks(message[0])

    
    SendHTTPHeaders(sock , details , status_code , Content_size , Content_type , connection_status)
    if type(message[0]) == str:
        sock.send( message[0].encode("utf-8") )
    else:
        sock.send( message[0] )


#def Log(ip , kind):

def Show404Page(sock , details):
    details["asked_file"] = webserver.AddressToHash(Config.get("404_PAGE"))
    RunFile(sock , False, details)
    return



def HTTPHandler(message):
    message = message.split(b"\r\n")
    details = dict()
    for i in range(len(message)):
        message[i] = message[i].decode('utf-8')
    details["method"] = message[0].split()[0]
    details["asked_file"] = message[0].split()[1]
    details["http_version"] = message[0].split()[2]


    if details.get("method")=="POST":
        data_dict = dict()
        data_dict["NONAME"] = []
        data = message[-1].split('&')
        for i in data:
            if '=' in i:
                data_dict[i.split('=')[0]] = i.split('=')[1]
            else:
                data_dict['NONAME'].append(i)
        details['data'] = data_dict


    message = message[1:]
    for i in message:
        if len(i)==0:break
        temp = i.split(": ")
        details[temp[0]] = temp[1]
    return details


def SendHTTPHeaders(sock , details , status_code , Content_size , Content_type , connection_status):
    message  = details["http_version"] + " "
    message += str(status_code) + " " + webserver.STAT_MEANING[status_code]
    message += "\r\n"
    message += "Date: Thu, 5 Nov 0666 0:0:0 GMT"
    message += "\r\n"
    message += "Server: ABrandNewThing/0.0.1 (Win32)"
    message += "\r\n"
    message += "Content-Length: " + str(Content_size)
    message += "\r\n"
    message += "Content-Type: " + Content_type
    message += "\r\n"
    message += "Connection: " + connection_status
    message += "\r\n"
    message += "\r\n"
    sock.send(message.encode("utf-8"))
    return

def SendFile(sock , file, details, connection_status, status_code):
    if len(file.split("."))!=2 or webserver.FILETYPES.get(file.split(".")[-1])==None : file_type = "text/html"
    else: file_type = webserver.FILETYPES[file.split(".")[-1].lower()]

    if file_type == "text/html":
            with open(file,'r') as f:
                tmp = f.read()
                tmp = webserver.HideLinks(tmp)
            file_size = len(tmp)
            SendHTTPHeaders(sock , details , status_code , file_size , file_type , connection_status)
            sock.send(tmp.encode("utf-8"))
            if connection_status == webserver.connection_status.Closed: sock.close()
            return


    file_size = os.stat(file).st_size
    SendHTTPHeaders(sock , details , status_code , file_size , file_type , connection_status)

    with open(file,'rb') as f:
        tmp = f.read( int ( Config.get("BUFFER") ) )
        while tmp!="" :
            sock.send(tmp)
            tmp = f.read( int ( Config.get("BUFFER") ) )
    return


def GetHandler(sock , details):
    if details["asked_file"]=="/":
        RunFile(sock, False , details)
        return
    else:
        #details["asked_file"]
        #Spliting parameters and '/' character from webpage
        if "?" in details["asked_file"]: file = details["asked_file"][:details["asked_file"].find("?")].replace("/","")
        else : file = details["asked_file"].replace("/","")
        file = webserver.HashToAddress( file )
        #print(details["asked_file"])
        if file==False:
            details["asked_file"] = Config.get("404_PAGE")
            RunFile(sock , False, details)
            return
    #print(details["asked_file"])
    if "?" in details["asked_file"] or ".py" in webserver.HashToAddress(details["asked_file"]):
        if "?" in details["asked_file"]:
            args = TakeArgs( details["asked_file"] )
        else:
            args = False
        RunFile(sock , args , details)
        return

    else:
        SendFile(sock,file,details,webserver.connection_status.Closed, 200)
        return


def PostHandler(sock , details):
    if details["asked_file"]=="/":
        RunFile(sock, False , details)
        return
    else:
        #Spliting parameters and '/' character from webpage
        if "?" in details["asked_file"]: file = details["asked_file"][:details["asked_file"].find("?")].replace("/","")
        else : file = details["asked_file"].replace("/","")
        file = webserver.HashToAddress( file )
        if file==False:
            details["asked_file"] = Config.get("404_PAGE")
            RunFile(sock , False, details)
            return

    args = details.get('data')
    print(args)
    RunFile(sock , args , details)
    return

        
    return




def SocketHandler(sock , address):
    while True:
        try:
            message = sock.recv(2048)
        except OSError :
            print("socket died")
            return

        if len(message)==0:
            continue
        
        message = HTTPHandler(message)
        message["Address"] = address
 
        #if message["connection"]!="keep-alive":return
        if message["method"]=="GET": GetHandler(sock, message)
        elif message["method"]=="POST": PostHandler(sock, message)
        break
        #print("message sent")
    print("socket died")

if __name__ == "__main__":
    Config = LoadConfig()
    os.chdir( Config.get("ORIGIN") )
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.bind(("" , int(Config["HOST_PORT"])))
    sock.listen()

    while True:
        try:
            client , address = sock.accept()
            print("socket created")
            if address[0] in BLOCKED_IP: continue
            threading._start_new_thread(SocketHandler , (client,address))
            continue
        except KeyboardInterrupt:
            sys.exit()

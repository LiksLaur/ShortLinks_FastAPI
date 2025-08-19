import psycopg2
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
import string
import random
import json
import requests

with open('./data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

conn = psycopg2.connect(database=data["database"], user=data["user"], password=data["password"], host=data["host"], port=data["port"])
cur = conn.cursor()
app = FastAPI()

dn = "127.0.0.1:8000" # Переменная domen name которая вставляется в короткую ссылку, мю потом поменять 
dnProtocol = "" # Пртокол которые потом поменять на http:// или https://

cur.execute(""" CREATE TABLE IF NOT EXISTS links (
            id SERIAL PRIMARY KEY,
            link TEXT NOT NULL,
            shortlink VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );""")    
conn.commit()

def random_text(length: int = 10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class get_link_args():
    def __init__(
        self,
        link, 
        whishes: Optional[str] = None
        ):
        self.link = link
        self.whishes = whishes
class SRequestLink(BaseModel):
    linksInfo: 'LinksInfo'
    errorLogs: 'ErrorLogs'
    
    class LinksInfo(BaseModel):
        link: str
        shortLink: str
    
    class ErrorLogs(BaseModel):
        errNumber: int
        errDescription: str

    
@app.get('/link', response_model=SRequestLink)
def get_link(args: get_link_args = Depends()):
    try:
        requests.get(f"{args.link}")
    except requests.exceptions.ConnectionError as err: 
        return{
            "linksInfo": {
                "link": f"{args.link}",
                "shortLink": ""
            },
            "errorLogs": {
                "errNumber": 2,
                "errDescription": "Looks like the link is not valid"
            }
        }
    except requests.exceptions.MissingSchema as err: 
        return{
            "linksInfo": {
                "link": f"{args.link}",
                "shortLink": ""
            },
            "errorLogs": {
                "errNumber": 3,
                "errDescription": "The link must start with the protocol"
            }
        }
    else:
        

        if args.whishes:
            cur.execute(" SELECT EXISTS ( SELECT 1 FROM links WHERE shortlink LIKE %s );", (f"%{args.whishes}%",))
            if cur.fetchone()[0]:
                print("err")
                return{
                    "linksInfo": {
                        "link": "https://example.com",
                        "shortLink": ""
                    },
                    "errorLogs": {
                        "errNumber": 1,
                        "errDescription": "Short link already taken"
                    }
                }
            else:
                cur.execute(
                    "INSERT INTO links (link, shortlink) VALUES (%s, %s)",
                    (args.link, args.whishes)
                )
                conn.commit()
                print("added")
                return{
                    "linksInfo": {
                        "link": f"{args.link}",
                        "shortLink": f"{dnProtocol}{dn}/{args.whishes}"
                    },
                    "errorLogs": {
                        "errNumber": 0,
                        "errDescription": "None"
                    }
                }
        else:
            urlKey = random_text(random.randint(5, 15))
            cur.execute(" SELECT EXISTS ( SELECT 1 FROM links WHERE shortlink LIKE %s );", (f"%{urlKey}%",))
            flag = cur.fetchone()[0]
            while flag == True:
                urlKey = random_text(random.randint(5, 15))
                cur.execute(" SELECT EXISTS ( SELECT 1 FROM links WHERE shortlink LIKE %s );", (f"%{urlKey}%",))
                if not cur.fetchone()[0]:
                    flag = False
                    break
            cur.execute(
                "INSERT INTO links (link, shortlink) VALUES (%s, %s)",
                (args.link, urlKey)
                )
            conn.commit()
            print("added")
            return{
                    "linksInfo": {
                        "link": f"{args.link}",
                        "shortLink": f"{dnProtocol}{dn}/{urlKey}"
                    },
                    "errorLogs": {
                        "errNumber": 0,
                        "errDescription": "None"
                    }
                }


@app.get("/infolink")
def info_link(shortlink: str, apiKey: str):
    with open('./apikey.json', 'r', encoding='utf-8') as file:
        key = json.load(file)
    if apiKey == key["key"]:
        cur.execute("SELECT * FROM links WHERE shortlink = %s;", (shortlink,))
        res = cur.fetchall()
        return{
                "status": {
                    "id":res[0][0],
                    "link":res[0][1],
                    "shortlink": f"{dnProtocol}{dn}/{res[0][2]}",
                    "created_at":res[0][3]
                }
            }
        
    else: 
        return{
            "err": "Uncorrect apikey"
        }
    

@app.get('/{shortlink}')
def res(shortlink: str):
    cur.execute(" SELECT EXISTS ( SELECT 1 FROM links WHERE shortlink LIKE %s );", (f"%{shortlink}%",))
    if cur.fetchone()[0]:
        cur.execute("SELECT link FROM links WHERE shortlink = %s;", (shortlink,))
        res = cur.fetchall()
        changeurl = list(res[0])

        cur.execute("SELECT transitions FROM links WHERE shortlink = %s;",  (shortlink,))
        res = cur.fetchall()
        res = list(list(res)[0])[0]
        
        cur.execute("UPDATE links SET transitions = transitions + 1 WHERE shortlink = %s;", (shortlink,))
        print(f"transitions + 1")
        conn.commit()
        return RedirectResponse(changeurl[0], status_code=302)   


        
    return {
        404: "not found"
    }

@app.delete("/del")
def del_link(shortLink: str, apiKey):
    with open('./apikey.json', 'r', encoding='utf-8') as file:
        key = json.load(file)
    if apiKey == key["key"]:
        cur.execute("DELETE FROM links WHERE shortlink = %s;", (shortLink,))
        conn.commit()
        return{
            "status": "deleted"
        }
    else: 
        return{
            "err": "Uncorrect apikey"
        }

@app.patch("/change")
def change_link(shortlink: str, newShortLink: str, apiKey):
    with open('./apikey.json', 'r', encoding='utf-8') as file:
        key = json.load(file)
    if apiKey == key["key"]:
        cur.execute("UPDATE links SET shortlink = %s WHERE shortlink = %s;", (newShortLink, shortlink))
        conn.commit()
        return{
                "status": "changed"
            }
    else: 
        return{
            "err": "Uncorrect apikey"
        }
    

        


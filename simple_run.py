from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bsoup
import json
from time import strptime,strftime,mktime,gmtime,localtime

from configs import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    codechefURL,
    codeforceURL,
    leetcodeURL,
    hackerearthURL,
    DIRECTORY
)

posts= {"ongoing":[] , "upcoming":[]}
DIRECTORY = 'reports'

def get_duration(duration):
    days = duration/(60*24)
    duration %= 60*24
    hours = duration/60
    duration %= 60
    minutes = duration
    ans=""
    if days==1: ans+=str(days)+" day "
    elif days!=0: ans+=str(days)+" days "
    if hours!=0:ans+=str(hours)+"h "
    if minutes!=0:ans+=str(minutes)+"m"
    return ans.strip()

def fetch_hackerearth():
    cur_time = localtime()
    ref_date =  strftime("%Y-%m-%d",  localtime(mktime(localtime())   - 432000))
    duplicate_check=[]

    page = urlopen("https://www.hackerearth.com/chrome-extension/events/")
    data = json.load(page)["response"]
    # print(data)
    for item in data:
        start_time = strptime(item["start_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        end_time = strptime(item["end_tz"].strip()[:19], "%Y-%m-%d %H:%M:%S")
        duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
        duplicate_check.append(item["title"].strip())

        if item["challenge_type"]=='hiring':challenge_type = 'hiring'
        else: challenge_type = 'contest'

        if item["status"].strip()=="UPCOMING" and challenge_type == 'contest':
            posts["upcoming"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "StartTime" : strftime("%a, %d %b %Y %H:%M", start_time),"EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Duration":duration,"Platform":"HACKEREARTH","challenge_type": challenge_type  })
        elif item["status"].strip()=="ONGOING" and challenge_type =='contest':
            posts["ongoing"].append({ "Name" :  item["title"].strip()  , "url" : item["url"].strip() , "EndTime" : strftime("%a, %d %b %Y %H:%M", end_time),"Platform":"HACKEREARTH","challenge_type": challenge_type  })
        print("Completed founding hackerearth contests")

def fetch_codeforces():
    page = urlopen("http://codeforces.com/api/contest.list")
    data = json.load(page)["result"]
    for item in data:

        if item["phase"]=="FINISHED": break

        start_time = strftime("%a, %d %b %Y %H:%M",gmtime(item["startTimeSeconds"]+19800))
        end_time   = strftime("%a, %d %b %Y %H:%M",gmtime(item["durationSeconds"]+item["startTimeSeconds"]+19800))
        duration = get_duration( item["durationSeconds"]/60 )

        if item["phase"].strip()=="BEFORE":
            posts["upcoming"].append({ "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"]) , "StartTime" :  start_time,"EndTime" : end_time,"Duration":duration,"Platform":"CODEFORCES"  })
        else:
            posts["ongoing"].append({  "Name" :  item["name"] , "url" : "http://codeforces.com/contest/"+str(item["id"])  , "EndTime"   : end_time  ,"Platform":"CODEFORCES"  })
        print("completed founded codeforces contest")

def fetch_hackerrank():
    cur_time = str(int(mktime(localtime())*1000))
    req = Request("https://www.hackerrank.com/rest/contests/upcoming?offset=0&limit=5&contest_slug=active&_="+cur_time, headers={'User-Agent': 'Mozilla/6.0'})
    page = urlopen(req)
    data = json.load(page)["models"]
    for item in data:
        if not item["ended"] and ("https://www.hackerrank.com/"+item["slug"]):
            start_time = strptime(item["get_starttimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            end_time = strptime(item["get_endtimeiso"], "%Y-%m-%dT%H:%M:%SZ")
            duration = get_duration(int(( mktime(end_time)-mktime(start_time) )/60 ))
            if not item["started"]:
                posts["upcoming"].append({ "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"] , "StartTime" :  strftime("%a, %d %b %Y %H:%M", localtime(mktime(start_time)+19800)),"EndTime" : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800)),"Duration":duration,"Platform":"HACKERRANK"  })
            elif   item["started"]:
                posts["ongoing"].append({  "Name" :  item["name"] , "url" : "https://www.hackerrank.com/"+item["slug"]  , "EndTime"   : strftime("%a, %d %b %Y %H:%M", localtime(mktime(end_time)+19800))  ,"Platform":"HACKERRANK"  })


def fetch():

    # fetch_codeforces()
    fetch_hackerrank()
    # fetch_hackerearth()
    posts["upcoming"] = sorted(posts["upcoming"], key=lambda k: strptime(k['StartTime'], "%a, %d %b %Y %H:%M"))
    posts["ongoing"] = sorted(posts["ongoing"], key=lambda k: strptime(k['EndTime'], "%a, %d %b %Y %H:%M"))
    posts["timestamp"] = strftime("%a, %d %b %Y %H:%M:%S", localtime())

def GenerateReport():
    print("Creating report...")
    with open(f'{DIRECTORY}/output.json', 'w') as f:
        json.dump(posts, f)
    print("Done...")

if __name__ == '__main__':
    fetch()
    GenerateReport()
    
    
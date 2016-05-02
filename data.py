
import xml.etree.ElementTree as ET
import glob
import json
import time
import re

files = glob.glob("data/*/*/*") #all data files
name_re = re.compile("^(.*).(D|R).(..).*$")
with open("data.json", "w") as f:
    for bill in files:
        tree = ET.parse(bill)
        root = tree.getroot().find('bill') #load the child of root as root, cuz real root is useless
        session = root.find("congress").text #get the session 
        #get the full name of all sponsors and cosponsors
        cosponsors = []
        for i in root.find("cosponsors").findall("item"):
            rep = name_re.match(i.find("fullName").text)
            if type(rep) == tuple:
                cosponsors.append({"name": rep[0], "party" : rep[1], "state" : rep[2]})
            elif rep != None:
                rep = rep.groups()
                cosponsors.append({"name": rep[0], "party" : rep[1], "state" : rep[2]})
        sponsors = []
        for i in root.find("sponsors").findall("item"):
            rep = name_re.match(i.find("fullName").text)
            if type(rep) == tuple:
                sponsors.append({"name": rep[0], "party" : rep[1], "state" : rep[2]})
            elif rep != None:
                rep = rep.groups()
                sponsors.append({"name": rep[0], "party" : rep[1], "state" : rep[2]})
        #get a summary of the bill
        try:
            most_recent_summary = root.find("summaries").findall("billSummaries/item")[-1].find("text").text
        except IndexError as e:
            most_recent_summary = "N/A"
        title = root.find("title").text
        bill_type = root.find("billType").text
        bill_number = root.find("billNumber").text
        actions = {}
        #get all actions and their counts. can't use action codes because not consitent
        for i in root.find("actions").find("actionTypeCounts"):
            actions[i.tag] = int(i.text)

        #get dates of all the actions
        action_dates = [time.strptime(i.find("actionDate").text, "%Y-%m-%d") for i in root.find("actions").findall("item")]
        action_dates = list(set(action_dates))
        action_dates.sort()
        action_dates = [time.strftime("%Y-%m-%d",i) for i in action_dates]

        info = {"{}-{}-{}".format(session,bill_number,bill_type) : {"cosponsors" : cosponsors, "sponsors" : sponsors, "title" : title, "summary" : most_recent_summary, "actions" : actions, "dates" : action_dates}}
        
        json.dump(info, f)
        f.write(',\n')


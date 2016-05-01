from progressbar import ProgressBar
import xml.etree.ElementTree as ET
import glob
import json
import time

files = glob.glob("data/*/*/*") #all data files

pbar = ProgressBar()
info = {}


for bill in pbar(files):
    tree = ET.parse(bill)
    root = tree.getroot().find('bill') #load the child of root as root, cuz real root is useless
    session = root.find("congress").text #get the session 
    #get the full name of all sponsors and cosponsors
    cosponsors = [i.find("fullName").text for i in root.find("cosponsors").findall("item")]
    sponsors = [i.find("fullName").text for i in root.find("sponsors").findall("item")]
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

    info["{}-{}-{}".format(session,bill_number,bill_type)] = {"cosponsors" : cosponsors, "sponsors" : sponsors, "title" : title, "summary" : most_recent_summary, "actions" : actions, "dates" : action_dates}
    

with open("data.json","w") as f:
    json.dump(info,f)

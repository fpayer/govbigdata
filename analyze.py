import json
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime


data = {}
with open("data.json","r") as f:
    data = json.load(f)


def cosponsors_v_pass(data):
    cosp_v_pass = {}
    count = 0
    for session in data.values():
        for typ in session.values():
            for bill in typ.values():
                count += 1
                if "becamePublicLaw" in bill['actions']:
                    cosp_v_pass[len(bill['cosponsors'])] = cosp_v_pass.get(len(bill['cosponsors']),0) + 1

    size = int(max(cosp_v_pass.keys())) + 1
    width = 1
    occurrences = [cosp_v_pass.get(key,0)/count for key in range(size)]
    num_cosp = range(size)

    fig, ax = plt.subplots()
    chart1 = ax.bar(np.arange(size), occurrences, width)

    fig.canvas.set_window_title("cosponsors_vs_bills_passed")
    ax.set_ylabel("Percent of bills passed")
    ax.set_xlabel("Number of cosponsors")
    ax.set_title("Number of cosponsors Vs Percent of bills passed")
    ax.set_xticks(np.arange(0,size,10))

    plt.show()


def times(data):
    type_times = {k:{"count":0,"sum":0} for k in data['113'].keys()}
    for session in data.values():
        for typ, bills in session.items():
            for bill in bills.values():
                if "becamePublicLaw" in bill['actions']:
                    type_times[typ]["count"] += 1
                    start = datetime.fromtimestamp(time.mktime(time.strptime(bill['dates'][0],"%Y-%m-%d")))
                    end = datetime.fromtimestamp(time.mktime(time.strptime(bill['dates'][-1],"%Y-%m-%d")))
                    type_times[typ]["sum"] += (end - start).days


    size = len(type_times)
    width = 1
    types = type_times.keys()
    times = [type_times[k]["sum"]/type_times[k]["count"] if type_times[k]["count"] else 0 for k in types]

    fig, ax = plt.subplots()
    chart1 = ax.bar(np.arange(size), times, width)

    fig.canvas.set_window_title("bill_type_vs_average_days")
    ax.set_ylabel("Average days to pass")
    ax.set_xlabel("Bill Type")
    ax.set_title("Bill Type vs average days to pass")
    ax.set_xticks(np.arange(size) + .5)
    ax.set_xticklabels(types)

    plt.show()


def states_and_parties(data):
    state_counts = {}
    party_counts = {}
    for session in data.values():
        for typ,bills in session.items():
            if typ != "s":
                continue
            for bill in bills.values():
                if "becamePublicLaw" in bill['actions']:
                    for rep in bill['sponsors']:
                        state_counts[rep["state"]] = state_counts.get(rep["state"],0) + 1
                        party_counts[rep["party"]] = party_counts.get(rep["party"],0) + 1
                    for rep in bill['cosponsors']:
                        state_counts[rep["state"]] = state_counts.get(rep["state"],0) + 1
                        party_counts[rep["party"]] = party_counts.get(rep["party"],0) + 1
                                                  
    states = state_counts.keys()
    bills = [state_counts[k] for k in states]

    plt.pie(bills,labels=states,autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

    parties = party_counts.keys()
    bills = [party_counts[k] for k in parties]

    plt.pie(bills,labels=parties,autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

def amendments(data):
    amendments = {k:{"days":0,"passed":0,"count":0} for k in range(1000)}
    maximal = 0
    passed = 0
    for session in data.values():
        for typ in session.values():
            for bill in typ.values():
                if bill['amendments'] > 0:
                    maximal = max([maximal,bill['amendments']])
                    amendments[bill['amendments']]['count'] += 1
                    start = datetime.fromtimestamp(time.mktime(time.strptime(bill['dates'][0],"%Y-%m-%d")))
                    end = datetime.fromtimestamp(time.mktime(time.strptime(bill['dates'][-1],"%Y-%m-%d")))
                    amendments[bill['amendments']]["days"] += (end - start).days
                    if "becamePublicLaw" in bill['actions']:
                        passed += 1
                        amendments[bill['amendments']]['passed'] += 1 

    num_amendments = range(maximal)
    days = [amendments[k]["days"]/amendments[k]["count"] if amendments[k]["count"] != 0 else 0 for k in num_amendments]
    passed = [amendments[k]["passed"]/passed for k in num_amendments]
    width = 1

    fig, ax = plt.subplots()
    chart1 = ax.bar(np.arange(maximal), days, width)

    fig.canvas.set_window_title("amendments_vs_average_days")
    ax.set_ylabel("Average days to pass")
    ax.set_xlabel("Number of amendments")
    ax.set_title("Amendments vs average days to pass")
    ax.set_xticks(np.arange(0,maximal,10))

    plt.show()

    fig, ax = plt.subplots()
    chart2 = ax.bar(np.arange(maximal), passed, width)

    fig.canvas.set_window_title("amendments_vs_passed")
    ax.set_ylabel("Percent of Bills Passed")
    ax.set_xlabel("Number of amendments")
    ax.set_title("Amendments vs Percent of Bills Passed")
    ax.set_xticks(np.arange(0,maximal,10))

    plt.show()

cosponsors_v_pass(data)

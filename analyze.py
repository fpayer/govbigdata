import json
import numpy as np
import matplotlib.pyplot as plt


data = {}
with open("data.json","r") as f:
    data = json.load(f)

cosp_v_pass = {}

for session in data.values():
    for typ in session.values():
        for bill in typ.values():
            if "becamePublicLaw" in bill['actions']:
                cosp_v_pass[len(bill['cosponsors'])] = cosp_v_pass.get(len(bill['cosponsors']),0) + 1

size = int(max(cosp_v_pass.keys())) + 1
width = 1
occurrences = [cosp_v_pass.get(key,0) for key in range(size)]
num_cosp = range(size)

fig, ax = plt.subplots()
chart1 = ax.bar(np.arange(size), occurrences, width)

fig.canvas.set_window_title("cosponsors_vs_bills_passed")
ax.set_ylabel("Number of bills passed")
ax.set_xlabel("Number of cosponsors")
ax.set_title("Number of cosponsors per passed bill")
ax.set_xticks(np.arange(0,size,10))

plt.show()

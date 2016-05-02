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

size = len(cosp_v_pass)
width = 1
occurrences = [value for key,value in sorted(cosp_v_pass.items())]
num_cosp = sorted(cosp_v_pass)
ind = np.arange(size)

fig, ax = plt.subplots()
chart1 = ax.bar(ind, occurrences, width)

ax.set_ylabel("Number of bills passed")
ax.set_xlabel("Number of cosponsors")
ax.set_title("Number of cosponsors per passed bill")
ax.set_xticks(ind)

plt.show()

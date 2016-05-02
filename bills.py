import json
import re
#12 becamePublicLaw 114-891-HR
data = []
publicLaw = {}
notPublicLaw = {}
passed = 0
not_passed = 0
types = {"HR": {"passed": 0, "not passed": 0, "% passed": 0},
        "S": {"passed": 0, "not passed": 0, "% passed": 0},
        "HJRES": {"passed": 0, "not passed": 0, "% passed": 0},
        "SJRES": {"passed": 0, "not passed": 0, "% passed": 0},
        "HCONRES": {"passed": 0, "not passed": 0, "% passed": 0},
        "SCONRES": {"passed": 0, "not passed": 0, "% passed": 0},
        "HRES": {"passed": 0, "not passed": 0, "% passed": 0},
        "SRES": {"passed": 0, "not passed": 0, "% passed": 0}}
i = 1
with open('data.json') as f:
    for line in f:
        line = line[:-2]
        d = json.loads(line)
        data.append(d) 
#        if (i == 12):
#            break
#        i += 1

for bill in data:
    name = bill.keys()[0]
    actions = bill[name]['actions'].keys()
    cosponsors = bill[name]['cosponsors']
    num_cosponsors = len(cosponsors)
    bill_type = re.match('\d+-\d+-(\w+)', name).group(1)
    
    if 'becamePublicLaw' in actions:
        if publicLaw.has_key(num_cosponsors): 
            publicLaw[num_cosponsors] += 1
        else:
            publicLaw[num_cosponsors] = 1
        passed += 1
        types[bill_type]["passed"] += 1
    else:
        if notPublicLaw.has_key(num_cosponsors): 
            notPublicLaw[num_cosponsors] += 1
        else:
            notPublicLaw[num_cosponsors] = 1
        not_passed += 1
        types[bill_type]["not passed"] += 1

for bill_type in types:
    p = types[bill_type]["passed"]
    total = p + types[bill_type]["not passed"]
    if total != 0:
        types[bill_type]["% passed"] = round(p / float(total), 5)
    print bill_type, types[bill_type]

print "\nPASSED BILLS    total: ", passed
print "# cosponsors: # bills passed"
print publicLaw
print "\nNOT PASSED BILLS    total: ", not_passed
print "# cosponsors: # bills not passed"
print notPublicLaw



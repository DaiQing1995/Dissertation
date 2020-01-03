from operator import itemgetter

# dict = {"a":1.5434, "b":0.9}

def delete_duplicate_data():
    data = [('derivative', 0.037411973398779656), ('complex value', 0.03524804177545692), ('application', 0.031174833590946405), ('issue', 0.02775668250516399), ('device', 0.02378854625550661), ('device', 0.02378854625550661), ('factor', 0.020099666641670476), ('factor', 0.020099666641670476), ('factor', 0.020099666641670476), ('relational database', 0.019092689295039166)]
    concepts = set()
    ret = []
    for d in data:
        if d[0] in concepts:
            continue
        ret.append(d)
        concepts.add(d[0])
    print(ret)

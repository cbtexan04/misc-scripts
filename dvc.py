#!/usr/bin/python

import requests
import re
import json

# Go to www.disneydvcresale.com and create a new filter. The filter you build
# will show up in the url bar. Copy and use that here
url="<insert url>"
output="<listings output directory>"

listings = dict()
with open(output) as json_data:
    try:
        listings = json.load(json_data)
    except:
        pass

def get_current_listings():
    r = requests.get(url)

    matches = re.findall('getListingInfo\(([^)]+)\)', r.content)

    l = dict()
    for item in matches:
        l[item] = True

    return l

def alert_new_listings():
    # I used mailgun for the simplicity of not having to deal with
    # snmp servers. Sign up for an account, get your API key, and
    # off you go.
    return requests.post(
        "https://api.mailgun.net/v3/sandboxSOME-UUID-HERE.mailgun.org/messages",
        auth=("api", "YOUR-API-KEY-HERE"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxSOME-UUID-HERE.mailgun.org>",
              "to": "<insert email>",
              "subject": "Found a new dvc listing",
              "text": "We found a new dvc listing. Better go check!\n{0}".format(url) })

def write_listings(listings):
    with open(output, 'w') as f:
        f.write(json.dumps(listings))

alert = False
current_listings = get_current_listings()
for item in current_listings:
    if item not in listings:
        alert=True
        listings[item] = True

if alert:
    alert_new_listings()

# Write out listings we've already seen
write_listings(listings)

import json
from pprint import pprint

json_file = 'data/QKSMS-noAnalytics-debug.apk_com.moez.QKSMS.ui.compose.ComposeActivity.json'

with open(json_file) as data_file:
    # Parse JSON into an object with attributes corresponding to dict keys.
    data = json.load(data_file)
# pprint(data)
print(data['componentName'])
print(data['sensEntries'])
for sens_entry in data['sensEntries']:
    print(sens_entry)



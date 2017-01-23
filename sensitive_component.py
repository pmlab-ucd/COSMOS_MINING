import json
import utils
from pprint import pprint

"""
A class to represent a sensitive component
"""


class SensitiveComponent:
    debug = True

    class SensEntryPoint:
        def __init__(self, entry_data):
            self.entryName = entry_data['sensEntry']
            self.sensTargets = entry_data['sensTargets']
            self.views = {}
            print(entry_data['views'])
            for view_name in entry_data['views']:
                self.views[view_name] = SensitiveComponent.SensitiveView(entry_data['views'][view_name])

    class SensitiveView:
        def __init__(self, view_data):
            view = utils.Dict2obj(view_data)
            self.rid = view.rid
            self.srid = view.srid
            self.layoutFile = view.layoutFile
            self.xmlFile = view.xmlFile

    def __init__(self, json_file):
        with open(json_file) as data_file:
            # Parse JSON into an object with attributes corresponding to dict keys.
            data = json.load(data_file)
        if self.debug:
            pprint(data)
        self.componentName = data['componentName']
        self.layoutFile = data['layoutFile']
        self.sensEntries = {}
        for sens_entry_name in data['sensEntries']:
            entry_data = data['sensEntries'][sens_entry_name]
            self.sensEntries[sens_entry_name] = SensitiveComponent.SensEntryPoint(entry_data)


if __name__ == '__main__':
    json_file = 'data/QKSMS-noAnalytics-debug.apk_com.moez.QKSMS.ui.compose.ComposeActivity.json'
    sens_comp = SensitiveComponent(json_file)
    # print(sens_comp.componentName, sens_comp.layoutFile)
    for entry_name in sens_comp.sensEntries:
        sens_entry = sens_comp.sensEntries[entry_name]
        # print(entry_name, sens_entry.entryName)
        sens_views = sens_entry.views
        print(sens_entry.entryName, sens_entry.views)
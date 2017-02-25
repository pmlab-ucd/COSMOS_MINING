import json
import utils
from pprint import pprint
import re
from word_spliter import WordSpliter

"""
A class to represent a sensitive component
"""


class SensitiveComponent:
    debug = False

    class SensEntryPoint:
        def __init__(self, entry_data):
            self.entryName = entry_data['sensEntry']
            self.sensTargets = entry_data['sensTargets']
            self.views = {}
            if SensitiveComponent.debug:
                print(entry_data['views'])
            for view_name in entry_data['views']:
                self.views[view_name] = SensitiveComponent.SensitiveView(entry_data['views'][view_name])

        def get_views(self):
            return self.views

        @staticmethod
        def split_entry_name(entry_name):
            entry_name = str(entry_name)
            entry_name = entry_name.split('(')[0]
            sub_names = entry_name.split(': ')
            method_name = sub_names[1]
            class_name = sub_names[0].replace(' ', '')
            class_name = SensitiveComponent.SensEntryPoint.sep_class_name(class_name)
            return class_name + ' ' + method_name

        @staticmethod
        def sep_class_name(class_name):
            name = []
            class_sub_names = str(class_name).split('.')
            for sub_name in class_sub_names:
                cap_sub_name = ' '.join(re.findall('[A-Z][^A-Z]*', sub_name))
                if len(cap_sub_name) > 0:
                    name.append(cap_sub_name)
                else:
                    if len(sub_name) == len(WordSpliter.infer_spaces(sub_name).split(' ')):
                        name.append(sub_name)
                    else:
                        name.append(WordSpliter.infer_spaces(sub_name))

            return ' '.join(name)

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

    def get_entry(self, entry_name):
        return self.sensEntries[entry_name]

    def get_entries(self):
        return self.sensEntries

if __name__ == '__main__':
    json_file = 'data/QKSMS-noAnalytics-debug/QKSMS-noAnalytics-debug.apk_com.moez.QKSMS.ui.compose.ComposeActivity.json'
    sens_comp = SensitiveComponent(json_file)
    # print(sens_comp.componentName, sens_comp.layoutFile)
    for entry_name in sens_comp.sensEntries:
        sens_entry = sens_comp.sensEntries[entry_name]
        # print(entry_name, sens_entry.entryName)
        sens_views = sens_entry.views
        print(sens_entry.entryName, sens_entry.views)
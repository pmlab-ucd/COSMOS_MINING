import sensitive_component
from xml.dom.minidom import parseString
import os


class TriggerOutHandler:
    category = ''
    loc_words = []
    sens_comp = None
    apk_name = None

    def __init__(self, category):
        TriggerOutHandler.category = category

    def handle_dynamic_xml(self, dynamic_xml):
        text = []
        if os.path.exists(dynamic_xml):
            data = ''
            with open(dynamic_xml, 'r') as f:
                try:
                    data = f.read()
                except UnicodeDecodeError as e:
                    print(e)
                    return
            dom = parseString(data)
            nodes = dom.getElementsByTagName('node')
            # Iterate over all the uses-permission nodes
            ignore = True
            for node in nodes:
                if node.getAttribute('text') != '':
                    text.append(node.getAttribute('text'))
                # print(node.getAttribute('text'))
                # print(node.toxml())
                if node.getAttribute('package') == self.apk_name:
                    ignore = False
            if ignore or len(text) == 0:
                return

            for entry_name in self.sens_comp.sensEntries:
                for sens_target in self.sens_comp.get_entry(entry_name).sensTargets:
                    if 'Location' in str(sens_target):
                        self.loc_words.append(text)


    def handle_out_json(self, json_file):
        #print(json_file)
        self.apk_name = os.path.basename(os.path.dirname(json_file))
        activity_name = json_file.split('_')[1].replace('.json', '')
        self.sens_comp = sensitive_component.SensitiveComponent(json_file)
        #print(sens_comp.componentName, sens_comp.layoutFile)


        trigger_py_out_dir = 'data\\'
        dynamic_xml_dir = trigger_py_out_dir + self.category + "\\" + self.apk_name
        dymamic_xml = dynamic_xml_dir + "\\" + activity_name + '.xml'
        self.handle_dynamic_xml(dymamic_xml)

import sensitive_component
from xml.dom.minidom import parseString
import os

class TriggerOutHandler:
    category = ''

    def __init__(self, category):
        TriggerOutHandler.category = category

    def handle_out_json(self, json_file):
        #print(json_file)
        apk_name = os.path.basename(os.path.dirname(json_file))
        activity_name = json_file.split('_')[1].replace('.json', '')
        sens_comp = sensitive_component.SensitiveComponent(json_file)
        #print(sens_comp.componentName, sens_comp.layoutFile)
        #for entry_name in sens_comp.sensEntries:
            #print(entry_name, sens_comp.get_entry(entry_name).sensTargets)

        trigger_py_out_dir = 'data\\'
        dynamic_xml_dir = trigger_py_out_dir + self.category + "\\" + apk_name
        dymamic_xml = dynamic_xml_dir + "\\" + activity_name + '.xml'

        if os.path.exists(dymamic_xml):
            data = ''
            with open(dymamic_xml, 'r') as f:
                data = f.read()
            dom = parseString(data)
            nodes = dom.getElementsByTagName('node')
            # Iterate over all the uses-permission nodes
            for node in nodes:
                print(node.getAttribute('text'))
                # print(node.toxml())
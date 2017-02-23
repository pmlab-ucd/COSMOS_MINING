from xml.dom.minidom import parseString
import os
from sensitive_component import SensitiveComponent
from utils import Utilities


class TriggerOutHandler:
    category = ''
    instances = {}
    sens_comp = None
    apk_name = None
    perm_keywords = None
    logger = None
    TAG = 'TriggerOutHandler'

    def __init__(self, category, perm_keywords, trigger_py_out_dir):
        TriggerOutHandler.category = category
        TriggerOutHandler.perm_keywords = perm_keywords
        self.trigger_py_out_dir = trigger_py_out_dir
        print(trigger_py_out_dir)
        if not TriggerOutHandler.logger:
            TriggerOutHandler.logger = Utilities.set_logger(TriggerOutHandler.TAG)

    def handle_dynamic_xml(self, dynamic_xml, use_event=True):
        text = []
        if os.path.exists(dynamic_xml):
            data = ''
            with open(dynamic_xml, 'r') as f:
                try:
                    data = f.read()
                except UnicodeDecodeError as e:
                    TriggerOutHandler.logger.error(e)
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
                    for perm_keyword in self.perm_keywords:
                        if perm_keyword in str(sens_target):
                            self.instances[entry_name] = {}
                            self.instances[entry_name]['text'] = text
                            self.instances[entry_name]['dynamic_xml'] = dynamic_xml
                            self.instances[entry_name]['png'] = str(dynamic_xml).replace('xml', 'png')
                            self.instances[entry_name]['api'] = sens_target
                            self.instances[entry_name]['views'] = self.sens_comp.get_entry(entry_name).views
                            break
            """
            found = False
            included_events = []
            for entry_name in self.sens_comp.sensEntries:
                if found and not use_event:
                    break
                for sens_target in self.sens_comp.get_entry(entry_name).sensTargets:
                    for perm_keyword in self.perm_keywords:
                        if perm_keyword in str(sens_target):
                            if use_event and entry_name not in included_events:
                                included_events.append(entry_name)
                                text.append(SensitiveComponent.SensEntryPoint.simplify_name(entry_name))
                            found = True
                            break
            if found:
                 self.words[dynamic_xml] = text
            """
        else:
            TriggerOutHandler.logger.error(dynamic_xml + ' does not exist!')

    def handle_out_json(self, json_file):
        #print(json_file)
        self.apk_name = os.path.basename(os.path.dirname(json_file))
        activity_name = str(os.path.basename(json_file))
        activity_name = activity_name.split('_')[1].replace('.json', '')
        self.sens_comp = SensitiveComponent(json_file)
        #print(sens_comp.componentName, sens_comp.layoutFile)

        dynamic_xml_dir = self.trigger_py_out_dir + self.category + "\\" + self.apk_name
        dymamic_xml = dynamic_xml_dir + "\\" + activity_name + '.xml'
        self.handle_dynamic_xml(dymamic_xml)

    def get_sens_comp(self):
        return self.sens_comp

import sensitive_component
from xml.dom.minidom import parseString

if __name__ == '__main__':
    trigger_java_out_dir = 'D:\COSMOS\output\java\\'
    category = 'Weather'
    apk_dir = 'Hurricane.Software'
    json_dir = trigger_java_out_dir + category + '\\' + apk_dir

    json_file = json_dir + '\\Hurricane.Software.apk_com.gencode.hurricanesoftware.AlertsActivity.json'
    activity_name = json_file.split('_')[1].replace('.json', '')
    sens_comp = sensitive_component.SensitiveComponent(json_file)
    print(sens_comp.componentName, sens_comp.layoutFile)
    for entry_name in sens_comp.sensEntries:
        print(entry_name, sens_comp.get_entry(entry_name).sensTargets)

    trigger_py_out_dir = 'data\\'
    dynamic_xml_dir = trigger_py_out_dir + category + "\\" + apk_dir
    dymamic_xml = dynamic_xml_dir + "\\" + activity_name + '.xml'

    data = ''
    with open(dymamic_xml, 'r') as f:
        data = f.read()
    dom = parseString(data)
    nodes = dom.getElementsByTagName('node')
    # Iterate over all the uses-permission nodes
    for node in nodes:
        print(node.getAttribute('text'))
        # print(node.toxml())
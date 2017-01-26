import os
from trigger_out_handler import TriggerOutHandler

if __name__ == '__main__':
    trigger_java_out_dir = 'D:\COSMOS\output\java\\'
    category = 'Weather'
    trigger_out_handler = TriggerOutHandler(category)
    for root, dirs, files in os.walk(trigger_java_out_dir + category):
        for file_name in files:
            if file_name.endswith('.json'):
                trigger_out_handler.handle_out_json(os.path.join(root, file_name))


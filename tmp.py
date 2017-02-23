import os
from trigger_out_handler import TriggerOutHandler
from miner import Miner
"""
Generate a markdown file
class name | screen shot | entry point | rsid
"""


class DataFormatter:
    @staticmethod
    def combining_data(trigger_out_dir='D:\COSMOS\output\\', super_out_dir='Play_win8', perm_type='Location'):
        trigger_java_out_dir = trigger_out_dir + '\java\\' + super_out_dir + '\\'
        trigger_py_out_dir = trigger_out_dir + '\py\\' + super_out_dir + '\\'
        categories = {}

        for filename in os.listdir(trigger_py_out_dir):
            if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
                category = filename
                categories[category] = []

        rm_category = []

        for category in categories:
            print('Try to read xml files for ' + category)
            perm_keywords = Miner.perm_types[perm_type]
            trigger_out_handler = TriggerOutHandler(category, perm_keywords, trigger_py_out_dir)
            if not os.path.exists(trigger_java_out_dir + category):
                rm_category.append(category)
                print(category + ' does not exist.')
                continue
            for root, dirs, files in os.walk(trigger_java_out_dir + category):
                for file_name in files:
                    if file_name.endswith('.json'):
                        try:
                            trigger_out_handler.handle_out_json(os.path.join(root, file_name))
                        except Exception as e:
                            print(e)
                            print(os.path.join(root, file_name))
            print(trigger_out_handler.instances)
            instances = trigger_out_handler.instances
            with open("Output.md", "w") as text_file:
                print('### {}'.format(perm_type), file=text_file)
                print("| Entry Point & APIs | Screen shot | Resource id | Label |", file=text_file)
                print('| ------------- | ------------- |-------------|-------------|', file=text_file)
                for instance in instances:
                    png_file = '![](' + str(os.path.abspath(instances[instance]['png'])) + ')'
                    sens_view = ''
                    if len(instances[instance]['views']) > 0:
                        sens_view = str(instance['views'])
                    print("| {} | {} | {} | |".format(instance + ';' + instances[instance]['api'].split(':')[1].split('(')[0], png_file, sens_view), file=text_file)

if __name__ == '__main__':
    DataFormatter.combining_data(trigger_out_dir=os.curdir + '\\test\output')
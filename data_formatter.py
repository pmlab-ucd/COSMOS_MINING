import os
from trigger_out_handler import TriggerOutHandler
from miner import Miner

"""
Generate a markdown file
class name | screen shot | entry point | rsid
"""


class DataFormatter:
    @staticmethod
    def combining_data(trigger_out_dir='D:\COSMOS\output\\', super_out_dir='Play_win8', perm_type='Location', num=50):
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
            out_base_path = os.path.abspath(os.path.join(os.path.curdir, 'output\gnd\\' + perm_type + '\\'))
            if not os.path.isdir(out_base_path):
                os.makedirs(out_base_path)
            count = -1
            for instance in instances:
                count += 1
                if count % num == 0:
                    md_file_path = out_base_path + '/' + category + '_' + str(num) + '_' + str(int(count / num)) + '.md'
                    if os.path.exists(md_file_path):
                        os.remove(md_file_path)
                    text_file = open(md_file_path, 'a')
                    text_file.write('### {}\n'.format(perm_type))

                    text_file.write("| Index | Entry Point & APIs | Screen shot | Resource id | Label |\n")
                    text_file.write('| ------------- | ------------- | ------------- |-------------|-------------|\n')
                else:
                    png_file = '![](' + str(os.path.abspath(instances[instance]['png'])) + ')'
                    sens_view = ''
                    if len(instances[instance]['views']) > 0:
                        sens_view = str(instances[instance]['views'])
                    # print(instances[instance]['api'])
                    text_file.write("| {} | {} | {} | {} | |\n".format(count, instance + ';' + instances[instance]['api'].
                                                                     split(':')[1].split('(')[0], png_file, sens_view))


if __name__ == '__main__':
    DataFormatter.combining_data(num=50)  # trigger_out_dir=os.curdir + '\\test\output')

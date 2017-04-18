from utils import Utilities
import os
from sensitive_component import SensitiveComponent
import shutil
from data_formatter import DataFormatter
import csv

pngs = []

'''
To handle user study feedback
'''
class SimpleDataFormatter:
    TAG = 'DataFormatter'
    logger = Utilities.set_logger(TAG)
    gnd_dir = None

    @staticmethod
    def handle_md(md_file, headers, instances):
        counter = len(instances)
        SimpleDataFormatter.logger.info(md_file)
        with open(md_file, 'r') as text_file:
            for line in text_file:
                sub_lines = line.split('|')

                #if not (('T' or 't' or 'F' or 'f' or 'D' or 'd') in sub_lines[len(sub_lines) - 2]):
                 #   continue

                if line.startswith('#') or line.startswith('| Index ') or line.startswith('| --'):
                    continue
                SimpleDataFormatter.logger.info(line)
                png_path = sub_lines[len(sub_lines) - 4].split('(')[1]
                png_path = png_path.split(')')[0]

                '''
                if ('D' or 'd') in sub_lines[len(sub_lines) - 2]:
                    label = 'labelled_D'
                    print(line)
                else:
                    continue
                '''

                found = False
                for header in headers:
                    act = str(header)
                    act.replace('- Copy', '')
                    if act in png_path:
                        SimpleDataFormatter.logger.info(header)
                        found = True
                        break
                if not found or line in md_targets:
                    continue
                md_targets.append(line)

                if png_path not in pngs:
                    pngs.append(png_path)
                xml_path = png_path.split('.png')[0] + '.xml'
                SimpleDataFormatter.logger.info(xml_path + ', ' + line)
                doc = []
                DataFormatter.handle_dynamic_xml(xml_path, doc)
                SimpleDataFormatter.logger.info(doc)

                entry_name = sub_lines[len(sub_lines) - 5].split(';')[0]
                entry_sub_words = SensitiveComponent.SensEntryPoint.split_entry_name(entry_name)
                doc.append(entry_sub_words)
                instance = {}
                instance['doc'] = doc
                instance['entry_name'] = entry_name
                instance['xml_path'] = xml_path
                instance['png_path'] = png_path
                instances.append(instance)
                counter += 1

    @staticmethod
    def parse_labelled(gnd_dir, headers, instances):
        SimpleDataFormatter.gnd_dir = gnd_dir
        for root, dirs, files in os.walk(gnd_dir):
            for file_name in files:
                if file_name.endswith('.md'):
                    # try:
                    SimpleDataFormatter.handle_md(os.path.join(root, file_name), headers, instances)
                    # except Exception as e:
                    #   DataFormatter.logger.error(e)

    @staticmethod
    def read_user_csv(csv_path):
        f = open(csv_path)
        reader = csv.reader(f)
        headers = next(reader, None)
        #columns = {}
        #for h in headers:
         #   columns[h] = []
        users = []
        for row in reader:
            user = dict()
            for h, v in zip(headers, row):
                user[h] = v
                #columns[h].append(v)
            users.append(user)
        #print(columns)
        print(users)
        return headers, users


read_md = False
if __name__ == '__main__':
    instances = []
    md_targets = []
    gnd_based_dir = 'output/gnd/'
    perm_type = 'users'
    instance_dir = gnd_based_dir + '/' + perm_type + '/'
    headers, users = SimpleDataFormatter.read_user_csv(instance_dir + 'Location.csv')
    SimpleDataFormatter.parse_labelled(gnd_based_dir + '/Location/', headers, instances)
    # print(len(pngs))
    print(len(md_targets))
    md_file_path = instance_dir + 'Location.md'
    if os.path.exists(md_file_path):
        os.remove(md_file_path)
    text_file = open(md_file_path, 'a')
    text_file.write('### {}\n'.format(perm_type))

    text_file.write("| Index | Entry Point & APIs | Screen shot | Resource id | Label |\n")
    text_file.write('| ------------- | ------------- | ------------- |-------------|-------------|\n')
    for md_target in md_targets:
        SimpleDataFormatter.logger.debug(md_target)
        text_file.write(md_target)
    print(len(users))
    for user in users:
        new_instances = []
        for header in user:
            if str(user[header]).startswith('Al') or str(user[header]).startswith('De'):
                pass
            else:
                continue
            act = str(header)
            act = act.replace(' - Copy', '')
            act = act.replace('- Copy', '')
            SimpleDataFormatter.logger.info(act + ',' + user[header])
            for instance in instances:
                if act in instance['png_path']:
                    instance['label'] = user[header]
                    new_instances.append(instance)
        outdir = instance_dir + '/' + str(users.index(user)) + '/'
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        DataFormatter.instances2txtdocs(outdir, new_instances)

    '''
    for png in pngs:
        print(png)
        srcfile = png
        dstroot = 'C:\\Users\hao\Pictures\\tmp'

        dstdir = os.path.join(dstroot, os.path.basename(png))

        shutil.copy(srcfile, dstdir)
    '''
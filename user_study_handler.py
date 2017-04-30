from utils import Utilities
import os
from sensitive_component import SensitiveComponent
import shutil
from data_formatter import DataFormatter
import csv

pngs = []
examined = []


class UserStudyHandler:
    """
    Handle users' study feedback
    """
    TAG = 'UserStudyHandler'
    logger = Utilities.set_logger(TAG)
    gnd_dir = None

    @staticmethod
    def parse_md(md_file, headers, instances):
        counter = len(instances)
        UserStudyHandler.logger.info(md_file)
        with open(md_file, 'r') as text_file:
            for line in text_file:
                sub_lines = line.split('|')

                if line.startswith('#') or line.startswith('| Index ') or line.startswith('| --'):
                    continue
                #UserStudyHandler.logger.info(line)
                png_path = sub_lines[len(sub_lines) - 4].split('(')[1]
                png_path = png_path.split(')')[0]

                found = False
                click = False
                for header in headers:
                    act = str(header)
                    if '- Copy' in act:
                        act = act.replace('- Copy', '')
                        click = True
                    if act in png_path:
                        #UserStudyHandler.logger.info(header)
                        found = True
                        break
                if not found or line in md_targets:
                    continue


                if png_path not in pngs:
                    pngs.append(png_path)
                xml_path = png_path.split('.png')[0] + '.xml'
                UserStudyHandler.logger.info(xml_path + ', ' + line)
                texts = []
                DataFormatter.handle_dynamic_xml(xml_path, texts)
                #UserStudyHandler.logger.info(texts)

                entry_name = sub_lines[len(sub_lines) - 5].split(';')[0]
                if 'Click' in entry_name and not click:
                    continue
                class_name, method_name = SensitiveComponent.SensEntryPoint.extract_class_method(entry_name)
                if class_name in examined:
                    continue
                else:
                    examined.append(class_name)
                md_targets.append(line)
                UserStudyHandler.logger.info(class_name)
                class_name, method_name = SensitiveComponent.SensEntryPoint.split_entry_name(entry_name)

                texts.append(class_name)
                texts.append(method_name)
                instance = {}
                instance['texts'] = texts
                instance['entry_name'] = entry_name
                instance['xml_path'] = xml_path
                instance['png_path'] = png_path
                instances.append(instance)
                counter += 1


    @staticmethod
    def parse_mds(gnd_dir, headers, instances):
        """
        Given elements extracted from CSV, search all instances matched with the elements in all markdown files 
        """
        UserStudyHandler.gnd_dir = gnd_dir
        for root, dirs, files in os.walk(gnd_dir):
            for file_name in files:
                if file_name.endswith('.md'):
                    # try:
                    UserStudyHandler.parse_md(os.path.join(root, file_name), headers, instances)
                    # except Exception as e:
                    #   DataFormatter.logger.error(e)

    @staticmethod
    def read_user_csv(csv_path):
        f = open(csv_path)
        reader = csv.reader(f)
        headers = next(reader, None)

        users = []
        for row in reader:
            user = dict()
            for h, v in zip(headers, row):
                user[h] = v
                # columns[h].append(v)
            users.append(user)
        # print(columns)
        print(users)


        columns = {}

        for h in headers:
            columns[h] = []

        for row in reader:
            for h, v in zip(headers, row):
                columns[h].append(v)
        print(len(columns))

        headers = []
        for h in columns:
            if len(str(h)) == 0:
                continue
            headers.append(h)

        return headers, users


read_md = False
if __name__ == '__main__':
    instances = []
    md_targets = []
    gnd_based_dir = 'output/gnd/'
    perm_type = 'users'
    instance_dir = gnd_based_dir + '/' + perm_type + '/'
    headers, users = UserStudyHandler.read_user_csv(instance_dir + 'Location.csv')
    print(len(headers), len(users))
    UserStudyHandler.parse_mds(gnd_based_dir + '/Location/', headers, instances)
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
        UserStudyHandler.logger.debug(md_target)
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
            UserStudyHandler.logger.info(act + ',' + user[header])
            for instance in instances:
                if act in instance['png_path']:
                    instance['label'] = user[header]
                    new_instances.append(instance)
        outdir = instance_dir + '/' + str(users.index(user)) + '/'
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        DataFormatter.instances2txtdocs(outdir, new_instances, who=False)

    '''
    for png in pngs:
        print(png)
        srcfile = png
        dstroot = 'C:\\Users\hao\Pictures\\tmp'

        dstdir = os.path.join(dstroot, os.path.basename(png))

        shutil.copy(srcfile, dstdir)
    '''
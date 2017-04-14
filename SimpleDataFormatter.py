from utils import Utilities
import os
from sensitive_component import SensitiveComponent


class SimpleDataFormatter:
    TAG = 'DataFormatter'
    logger = Utilities.set_logger(TAG)
    gnd_dir = None

    @staticmethod
    def handle_md(md_file, instances):
        counter = len(instances)
        SimpleDataFormatter.logger.info(md_file)
        with open(md_file, 'r') as text_file:
            for line in text_file:
                sub_lines = line.split('|')

                if ('D' or 'd') in sub_lines[len(sub_lines) - 2]:
                    label = 'labelled_D'
                    print(line)
                else:
                    continue
                if line.startswith('#'):
                    continue
                SimpleDataFormatter.logger.info(sub_lines)
                xml_path = sub_lines[len(sub_lines) - 4].split('(')[1]
                xml_path = xml_path.split('.png')[0] + '.xml'
                SimpleDataFormatter.logger.info(xml_path + ', ' + line)
                doc = []

                SimpleDataFormatter.logger.info(doc)

                entry_name = sub_lines[len(sub_lines) - 5].split(';')[0]
                entry_sub_words = SensitiveComponent.SensEntryPoint.split_entry_name(entry_name)
                doc.append(entry_sub_words)
                instances[counter] = {}
                instances[counter]['doc'] = doc
                instances[counter]['label'] = label
                instances[counter]['entry_name'] = entry_name
                instances[counter]['xml_path'] = xml_path
                counter += 1

    @staticmethod
    def parse_labelled(gnd_dir, instances):
        SimpleDataFormatter.gnd_dir = gnd_dir
        for root, dirs, files in os.walk(gnd_dir):
            for file_name in files:
                if file_name.endswith('.md'):
                    # try:
                    SimpleDataFormatter.handle_md(os.path.join(root, file_name), instances)
                    # except Exception as e:
                    #   DataFormatter.logger.error(e)


if __name__ == '__main__':
    instances = {}
    gnd_based_dir = 'output/gnd/'
    perm_type = 'Location'
    instance_dir = gnd_based_dir + '/' + perm_type
    SimpleDataFormatter.parse_labelled(instance_dir, instances)
    print(len(instances))

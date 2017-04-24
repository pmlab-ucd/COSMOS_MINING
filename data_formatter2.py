import os
from trigger_out_handler import TriggerOutHandler
from miner import Miner
from xml.dom.minidom import parseString
from sensitive_component import SensitiveComponent
from utils import Utilities
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from lda import LDA
import json
from sklearn_utils import SklearnUtils
import codecs
import shutil

"""
Generate markdown files of instances for labelling
class name | screen shot | entry point | rsid
"""


class DataFormatter:
    TAG = 'DataFormatter'
    logger = Utilities.set_logger(TAG)
    gnd_dir = None

    @staticmethod
    def handle_dynamic_xml(dynamic_xml, doc):
        all_views = []
        if os.path.exists(dynamic_xml):
            data = ''
            with open(dynamic_xml, 'r', encoding='utf8') as f:
                try:
                    data = f.read()
                except UnicodeDecodeError as e:
                    print('Unicode Decode Error: ' + e)
                    return
            dom = parseString(data)
            nodes = dom.getElementsByTagName('node')
            # Iterate over all the uses-permission nodes
            ignore = True
            for node in nodes:
                if node.getAttribute('text') != '':
                    doc.append(node.getAttribute('text'))
                # print(node.getAttribute('text'))
                # print(node.toxml())
                if node.getAttribute('package') in str(dynamic_xml):
                    all_views.append(node)
                    ignore = False
            # if ignore or len(doc) == 0:

            print(doc)
        else:
            DataFormatter.logger.error('XML ' + dynamic_xml + ' does not exist!')
        return all_views

    @staticmethod
    def handle_md(md_file, instances, label_T=True, label_D=True):
        global count
        # counter = len(instances)
        DataFormatter.logger.info(md_file)
        with open(md_file, 'r') as text_file:
            for line in text_file:
                sub_lines = line.split('|')

                if 'T' in sub_lines[len(sub_lines) - 2]:
                    label = 'labelled_T'
                    if not label_T:
                        continue

                elif 'F' in sub_lines[len(sub_lines) - 2]:
                    label = 'labelled_F'
                elif 'D' in sub_lines[len(sub_lines) - 2]:
                    label = 'labelled_D'
                    if not label_D:
                        continue
                else:
                    continue
                if line.startswith('#'):
                    continue
                DataFormatter.logger.info(sub_lines)
                xml_path = sub_lines[len(sub_lines) - 4].split('(')[1]
                xml_path = xml_path.split('.png')[0] + '.xml'
                DataFormatter.logger.info(xml_path + ', ' + line)
                texts = []
                all_views = DataFormatter.handle_dynamic_xml(xml_path, texts)

                DataFormatter.logger.info(texts)

                entry_api = sub_lines[len(sub_lines) - 5].split(';')

                entry_name = entry_api[0]
                api = entry_api[1]

                '''
                instances[counter] = {}
                instances[counter]['doc'] = doc
                instances[counter]['label'] = label
                instances[counter]['entry_name'] = entry_name
                instances[counter]['xml_path'] = xml_path
                counter += 1
                '''
                views = sub_lines[len(sub_lines) - 3].replace(' ', '')

                if views:
                    if ':id/' in views:
                        sviews = {}
                        srid = str(views).split(':id/')[1]
                        for node in all_views:
                            node_srid = str(node.getAttribute('resource-id')).split('id/')
                            if len(node_srid) < 2:
                                continue
                            node_srid = node_srid[1]
                            if node_srid == srid:
                                sviews[srid] = node
                        views = sviews
                    else:
                        views = str(views).split(',')
                        json_file = str(xml_path).replace('py', 'java', 1)
                        json_file = json_file.replace('.xml', '.json')
                        par_dir = os.path.dirname(json_file)
                        apkname = os.path.basename(par_dir)
                        DataFormatter.logger.debug(apkname)
                        sens_comp = SensitiveComponent(
                            os.path.join(par_dir, apkname + '.apk_' + os.path.basename(json_file)))
                        print(sens_comp.componentName, sens_comp.layoutFile)
                        sviews = {}
                        entry_name = str(entry_name).replace(' <', '<', 1)
                        for entry_na in sens_comp.get_entries():
                            DataFormatter.logger.debug(entry_na)
                        views = sens_comp.get_entry(entry_name).get_views()
                        for view_name in views:
                            srid = views[view_name].srid
                            if srid in sviews:
                                continue

                            DataFormatter.logger.info(views[view_name].srid)
                            DataFormatter.logger.info(views[view_name].srid)
                            sviews[srid] = None  # views[view_name]
                            for node in all_views:
                                node_srid = str(node.getAttribute('resource-id')).split('id/')
                                if len(node_srid) < 2:
                                    continue
                                node_srid = node_srid[1]
                                if node_srid == srid:
                                    sviews[srid] = node
                        views = sviews
                instance = {}
                instance['texts'] = texts
                instance['label'] = label
                instance['entry_name'] = entry_name
                instance['xml_path'] = xml_path
                instance['view'] = views
                instance['api'] = api
                instances.append(instance)
                if 'T' in label:
                        count = count + 1

    @staticmethod
    def docs2bag(instances_dir, instances, gen_arff=False):
        train_data = []
        train_data_label = []

        for instance in instances:
            # instance = instances[i]
            doc = LDA.pre_process(';'.join(instance['doc']))
            train_data.append(' '.join(doc))
            train_data_label.append(instance['label'])
            # print(str(i), train_data[i], train_data_label[i])

        # Initialize the "CountVectorizer" object, which is scikit-learn's bag of words tool.
        vectorizer = CountVectorizer(analyzer="word",
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=None,
                                     max_features=5000)
        # fit_transform() does two functions: First, it fits the model
        # and learns the vocabulary; second, it transforms our training data
        # into feature vectors. The input to fit_transform should be a list of
        # strings.
        titles_vocab_mat = vectorizer.fit_transform(train_data)
        # Numpy arrays are easy to work with, so convert the result to an array
        # print vectorizer.vocabulary_  # a dict, the value is the index
        train_data_features = titles_vocab_mat.toarray()
        print(train_data_features.shape)
        # Take a look at the words in the vocabulary
        vocab = vectorizer.get_feature_names()
        print('/'.join(vocab))
        # Sum up the counts of each vocabulary word
        dist = np.sum(train_data_features, axis=0)
        dict = []
        for tag, count in zip(vocab, dist):
            dict.append(tag)
        json.dump(dict, open(instances_dir + '/train_dict.json', 'w+'))

        for ins in train_data_features:
            tmp = {}
            tmp['doc'] = []
            # tmp['label'] = data_target
            for i in range(0, len(ins)):
                if ins[i] == 1:
                    tmp['doc'].append(dict[i])
            print(tmp)

        if len(train_data_label) != len(train_data):
            DataFormatter.logger.error('ERROR: number of titles and titles not consistent')
            exit(1)

        if gen_arff:
            train_file = open(DataFormatter.gnd_dir + '/train_data.arff', 'w')
            DataFormatter.gen_arff(train_file, dict, train_data_features, train_data_label, instances)

        return [train_data_features, train_data_label]

    @staticmethod
    def gen_arff_header(train_file):
        if train_file:
            train_file.write('@RELATION ' + 'doc' + '\n')
            train_file.write('@ATTRIBUTE doc_name STRING\n')

    @staticmethod
    def gen_arff(train_file, dict, train_data_features, titles_label, instances, numeric_flag=False):
        vocabulary = []
        DataFormatter.gen_arff_header(train_file)
        # For each, print the vocabulary word and the number of times it appears in the training set
        for tag in dict:
            if numeric_flag:
                # print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
                train_file.write('@ATTRIBUTE word_freq_' + tag + ' NUMERIC\n')
            else:
                # print '@ATTRIBUTE word_freq_' + tag + ' NUMERIC'
                # str_tag = str(tag.encode('utf-8')).replace('b\'', '\'')
                # str_tag = str_tag.replace('\'', '')
                train_file.write('@ATTRIBUTE word_' + tag + ' {0, 1}\n')
                vocabulary.append(tag.encode('utf-8'))
                # print count

        train_file.write('@ATTRIBUTE class {0, 1, 2}\n')
        # print '\n@DATA'
        train_file.write('\n@DATA\n')

        for i in range(0, len(train_data_features)):
            test_flag = False

            if test_flag:
                for word_count in train_data_features[i]:
                    # calculate freq of words = percentage of words in front page that match WORD
                    # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

                    # word_freq_list.append(word_freq)
                    # sys.stdout.write(str(word_freq) + ',')
                    if numeric_flag:
                        total_words = 0
                        for j in train_data_features:
                            # print sum(i)
                            total_words += sum(j)
                        word_freq = 100 * float(word_count) / float(total_words)
                        train_file.write(str(word_freq) + ',')
                    else:
                        if int(word_count) > 0:
                            train_file.write('1,')
                        else:
                            train_file.write('0,')
                            # sys.stdout.write(str(titles_lable[counter]) + '\n')
                train_file.write(str(titles_label[i]) + '\n')
            else:
                train_file.write(instances[i]['entry_name'] + '|' + instances[i]['xml_path'] + ',')
                for word_count in train_data_features[i]:
                    # calculate freq of words = percentage of words in front page that match WORD
                    # i.e. 100 * (number of times the WORD appears in the front_page) /  total number of words in front page

                    # word_freq_list.append(word_freq)
                    # sys.stdout.write(str(word_freq) + ',')
                    if numeric_flag:
                        total_words = 0
                        for j in train_data_features:
                            total_words += sum(j)
                        print(total_words)
                        word_freq = 100 * float(word_count) / float(total_words)
                        train_file.write(str(word_freq) + ',')
                    else:
                        if int(word_count) > 0:
                            train_file.write('1,')
                        else:
                            train_file.write('0,')
                            # sys.stdout.write(str(titles_lable[counter]) + '\n')
                train_file.write(str(titles_label[i]) + '\n')
                DataFormatter.logger.info(str(titles_label[i]) + '\n')

    @staticmethod
    def parse_labelled(gnd_dir, instances, label_T=True, label_D=True):
        DataFormatter.gnd_dir = gnd_dir
        for root, dirs, files in os.walk(gnd_dir):
            for file_name in files:
                if file_name.endswith('.md'):
                    # try:
                    DataFormatter.handle_md(os.path.join(root, file_name), instances, label_T=label_T, label_D=label_D)
                    # except Exception as e:
                    #   DataFormatter.logger.error(e)

    @staticmethod
    def check_data_consistency(instances_dir, instances, train_data_features):
        train_data, train_target, train_dict = SklearnUtils.load_train_data(instances_dir + 'train_data.json',
                                                                            instances_dir + 'train_target.json',
                                                                            instances_dir + 'train_dict.json')
        if len(train_data) != len(instances):
            DataFormatter.logger.error(str(len(train_data)), str(len(instances)))
            exit(1)
        else:
            DataFormatter.logger.info('Length: ' + str(len(instances)))
        for i in range(0, len(train_data)):
            data_instance = train_data[i]
            data_target = train_target[i]
            loaded_ins = SklearnUtils.translate_feature(data_instance, train_dict, data_target)
            instance = instances[i]
            if str(instance['label']) != str(loaded_ins['label']):
                DataFormatter.logger.error(str(i) + ' label: ' + str(instance['doc']) + ', ' + str(loaded_ins['doc']))
                exit(1)
            if train_data[i].all() != train_data_features[i].all():
                DataFormatter.logger.error(str(i) + ' data: ' + str(instance['doc']))
                exit(1)
            """
            for word in instance['doc']:
                if word not in loaded_ins['doc']:
                    DataFormatter.logger.error(word)
                    DataFormatter.logger.error(str(i) + ' data: ' + str(instance['doc']) + ', ' + str(loaded_ins['doc']))
                     exit(1)
            """

    @staticmethod
    def instances2txtdocs(out_dir, instances, what=True, when=True, who=True, name=False):
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        for instance in instances:
            # instance = instances[i]
            output_dir = out_dir + '/' + str(instance['label']) + '/'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            file_name = str(instance['entry_name']).replace('<', '')
            file_name = file_name.replace('>', '')
            file_name = file_name.replace('()', '')
            file_name = file_name.replace(': ', '_')
            if file_name.startswith(' '):
                file_name = file_name.replace(' ', '', 1)

            doc = []
            class_name, method_name = SensitiveComponent.SensEntryPoint.split_entry_name(instance['entry_name'])
            if what:
                doc.append(instance['texts'])
            if when:
                doc.append(method_name)
            if name:
                # if not when:
                #   doc.append(method_name)
                doc.append(class_name)
                doc.append(instance['api'])
            if who:
                views = instance['view']
                for srid in views:
                    str_srid = Utilities.str2words(srid)
                    for sub_str in str_srid.split(' '):
                        doc.append(SensitiveComponent.SensEntryPoint.sep_class_name(sub_str))
                    node = views[srid]
                    if node:
                        doc.append(node.getAttribute('class'))
            outfile_path = os.path.abspath(output_dir + file_name + '.txt')
            while os.path.exists(outfile_path):
                file_name = file_name + '_re'
                outfile_path = os.path.abspath(output_dir + file_name + '.txt')
            doc_file = open(outfile_path, 'w', encoding='utf-8')
            doc_file.write(str(doc))


gnd_based_dir = 'output/gnd/'  # ''output/drebin/gnd/'
perm_type = 'RECORD_AUDIO'  # SEND_SMS' #Location'
gen_md = False  # True

if __name__ == '__main__':
    instances = []
    out_dir = gnd_based_dir + '\\comp\\' + perm_type + '\\'
    instance_dir = gnd_based_dir + '\\' + perm_type + '\\'
    what = False
    when = False
    who = False
    name = True

    if who and when and what:
        out_dir = out_dir + 'full'
    elif who and when:
        out_dir = out_dir + 'who_when'
    elif who and what:
        out_dir = out_dir + 'who_what'
    elif when and what:
        out_dir = out_dir + 'when_what'
    elif name:
        who = False
        when = False
        what = False
        out_dir = out_dir + 'name'
    elif who:
        out_dir = out_dir + 'who'
    elif when:
        out_dir = out_dir + 'when'
    elif what:
        out_dir = out_dir + 'what'
    else:
        DataFormatter.logger.error("Error Arguments!")
        exit(1)

    count = 0

    DataFormatter.parse_labelled(instance_dir, instances, label_T=False, label_D=False)
    DataFormatter.parse_labelled(gnd_based_dir + 'Relabelled\\', instances, label_T=True, label_D=True)

    # json.dump(instances, open(out_dir + '/instances.json', 'w+'))
    DataFormatter.instances2txtdocs(out_dir, instances, what=what, when=when, who=who, name=name)
    views = []
    print(len(instances))
    for instance in instances:
        if instance['view']:
            DataFormatter.logger.info(instance['view'])
            views.append(instance)
    print(len(views))
    print(count)
    str_srid = Utilities.str2words('vrl_record_button')
    for sub_str in str_srid.split(' '):
        print(SensitiveComponent.SensEntryPoint.sep_class_name(sub_str))

"""
[train_data_features, train_data_labels] = DataFormatter.docs2bag(instances)
json.dump(train_data_features.tolist(), open(out_dir + 'train_data.json', 'w+'))
json.dump(train_data_labels, open(out_dir + 'train_target.json', 'w+'))
DataFormatter.check_data_consistency(instances, train_data_features)
"""

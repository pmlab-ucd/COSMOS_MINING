from utils import Utilities
import os
from trigger_out_handler import TriggerOutHandler
from sensitive_component import SensitiveComponent
from lda import LDA


class Miner:
    TAG = 'COSMOS_MINING_PY_MODEL_TESTER'
    perm_types = {
        'Location': ['Location'],
        'Contact': ['Contact'],
        'Camera': ['Camera', 'setVideoSource'],
        'CHANGE_WIFI_STATE': ['WifiManager', 'WifiP2pManager'],
        'READ_PHONE_STATE': ['TelephonyManager'],
        'NFC': ['nfc'],
        'BLUETOOTH': ['bluetooth'],
        'RECORD_AUDIO': ['SpeechRecognizer', 'AudioRecord', 'setAudioSource'],
        'CALENDAR': ['Calendar'],
        'CALL_LOG': ['CallLog'],
        'SEND_SMS': ['SmsManager', 'mms.']}

    dist_types = {
        'semantic': 'semantic_dist',
        'event': 'event_dist',
        'all': 'all_dist'
    }

    def __init__(self, super_out_dir='Play_win8', perm_type='Location', dist_type='all'):
        self.super_out_dir = super_out_dir
        self.perm_type = perm_type
        self.perm_keywords = self.perm_types[perm_type]

        self.out_base_dir = 'output/' + self.dist_types[dist_type] + '/' + super_out_dir + '/' + perm_type + '/'
        self.logger = Utilities.set_logger(self.TAG)
        LDA.logger = self.logger
        self.file_handler = Utilities.set_file_log(self.logger, self.out_base_dir + '/' + self.TAG + '_' + perm_type + '.log')
        self.all_words = []
        self.categories = {}
        self.a_lda = None

    def prepare_docs(self):
        trigger_java_out_dir = 'D:\COSMOS\output\java\\' + self.super_out_dir + '\\'
        trigger_py_out_dir = 'D:\COSMOS\output\py\\' + self.super_out_dir + '\\'

        for filename in os.listdir(trigger_py_out_dir):
            if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
                category = filename
                self.categories[category] = []

        rm_category = []

        for category in self.categories:
            doc_data_file_path = self.out_base_dir + category + '_' + self.perm_type + '.json'
            docs = {}
            docs = Utilities.load_json(doc_data_file_path)

            if not docs:
                self.logger.info('Try to read xml files for ' + category)
                trigger_out_handler = TriggerOutHandler(category, self.perm_keywords, trigger_py_out_dir)
                if not os.path.exists(trigger_java_out_dir + category):
                    rm_category.append(category)
                    self.logger.warn(category + ' does not exist.')
                    continue
                for root, dirs, files in os.walk(trigger_java_out_dir + category):
                    for file_name in files:
                        if file_name.endswith('.json'):
                            try:
                                trigger_out_handler.handle_out_json(os.path.join(root, file_name))
                            except Exception as e:
                                self.logger.error(e)
                                self.logger.error(os.path.join(root, file_name))
                instances = trigger_out_handler.instances
                for instance in instances:
                    entry_name = SensitiveComponent.SensEntryPoint.split_entry_name(str(instance))
                    if instance['dynamic_xml'] and entry_name in instance['dynamic_xml']:
                        continue
                    else:
                        docs[instance['dynamic_xml']] = instance['text'].append(entry_name)
                Utilities.save_json(docs, doc_data_file_path)
            if not docs or len(docs) == 0 or not isinstance(docs, dict):
                rm_category.append(category)
            else:
                self.categories[category] = docs
                self.all_words.extend(docs.values())

        for category in rm_category:
            self.categories.pop(category, None)

        for category in self.categories:
            self.logger.info(category)

    def fit(self, parameter_list):
        self.a_lda = LDA(self.all_words, self.out_base_dir, self.super_out_dir + '_' + self.perm_type, parameter_list)
        self.a_lda.fit()

    def predict(self):
        for category in self.categories:
            self.logger.info(category)
            for doc_xml in self.categories[category]:
                self.logger.info(doc_xml)
                self.a_lda.predict(self.categories[category][doc_xml], pre_process=True)

        self.file_handler.close()
        self.logger.removeHandler(self.file_handler)
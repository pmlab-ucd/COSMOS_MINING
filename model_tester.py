from gensim import corpora, models
from main import perm_types, dist_types
from utils import Utilities
import os
from miner import Miner

class ModelTester:
    TAG = 'COSMOS_MINING_PY_MODEL_TESTER'

    def __init__(self, model_file, super_out_dir='Play_win8', perm_type='Location', dist_type='all'):
        self.model = models.LdaModel.load(model_file)
        perm_keywords = perm_types[perm_type]

        self.out_base_dir = 'output/' + dist_types[dist_type] + '/' + super_out_dir + '/' + perm_type + '/'
        self.logger = set_logger(self.TAG)
        file_handler = Utilities.set_file_log(self.logger, self.out_base_dir + '/' + self.TAG + '_' + perm_type + '.log')
        self.miner = Miner(super_out_dir, perm_type, dist_type)

    def predict(self):
        self.miner.prepare_docs()
        for category in categories:
            logger.info(category)
            for doc_xml in categories[category]:
                logger.info(doc_xml)
                a_lda.predict(categories[category][doc_xml], pre_process=True)

        file_handler.close()
        logger.removeHandler(file_handler)
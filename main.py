import os
from trigger_out_handler import TriggerOutHandler
from lda import LDA
from utils import Utilities

if __name__ == '__main__':
    super_out_dir = 'Play_win8'
    out_base_dir = 'data/words/' + super_out_dir
    logger = Utilities.set_logger('COSMOS_MINING_PY')
    file_handler = Utilities.set_file_log(logger, out_base_dir + '/COSMOS_TRIGGER_PY.log')
    LDA.logger = logger

    trigger_java_out_dir = 'D:\COSMOS\output\java\\' + super_out_dir + '\\'
    trigger_py_out_dir = 'D:\COSMOS\output\py\\' + super_out_dir + '\\'
    categories = []
    for filename in os.listdir(trigger_py_out_dir):
        if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
            logger.info(filename)
            category = filename
            categories.append(category)

    all_words = []
    for category in categories:
        word_data_file_path = 'D:\COSMOS\output\py/' + category + '.json'
        words = Utilities.load_json(word_data_file_path)
        if not words:
            trigger_out_handler = TriggerOutHandler(category, 'Location', trigger_py_out_dir)
            if not os.path.exists(trigger_java_out_dir + category):
                continue
            for root, dirs, files in os.walk(trigger_java_out_dir + category):
                for file_name in files:
                    if file_name.endswith('.json'):
                        trigger_out_handler.handle_out_json(os.path.join(root, file_name))
            words = trigger_out_handler.words
            logger.info(trigger_out_handler.words)
            Utilities.save_json(words, word_data_file_path)
        logger.info(words)
        all_words.extend(words)

    a_lda = LDA(all_words, out_base_dir, super_out_dir, len(categories))
    a_lda.fit()

    file_handler.close()
    logger.removeHandler(file_handler)


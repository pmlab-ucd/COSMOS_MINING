import os
from trigger_out_handler import TriggerOutHandler
from lda import LDA
from utils import Utilities

if __name__ == '__main__':
    super_out_dir = 'Play_win8/'
    trigger_java_out_dir = 'D:\COSMOS\output\java\\' + super_out_dir
    trigger_py_out_dir = 'D:\COSMOS\output\py\\' + super_out_dir
    for filename in os.listdir(trigger_py_out_dir):
        if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
            print(filename)
            category = filename
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
            print(trigger_out_handler.words)
            Utilities.save_json(words, word_data_file_path)
        print(words)
        a_lda = LDA(words, 'data/words/', category)
        a_lda.fit()


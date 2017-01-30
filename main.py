import os
from trigger_out_handler import TriggerOutHandler
from lda import LDA
from utils import Utilities

if __name__ == '__main__':
    trigger_java_out_dir = 'D:\COSMOS\output\java\\'
    category = 'Weather'
    word_data_file_path = 'data/words/' + category + '.json'
    words = Utilities.load_json(word_data_file_path)
    if not words:
        trigger_out_handler = TriggerOutHandler(category)
        for root, dirs, files in os.walk(trigger_java_out_dir + category):
            for file_name in files:
                if file_name.endswith('.json'):
                    trigger_out_handler.handle_out_json(os.path.join(root, file_name))
        words = trigger_out_handler.loc_words
        print(trigger_out_handler.loc_words)
        Utilities.save_json(words, word_data_file_path)
    print(words)
    a_lda = LDA(words, 'data/words/', category)
    a_lda.fit()


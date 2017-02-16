import os
from trigger_out_handler import TriggerOutHandler
from lda import LDA
from utils import Utilities

perm_types = {
    'Location': ['Location'],
    'Contact': ['Contact'],
    'Camera': ['Camera', 'MediaRecorder'],
    'CHANGE_WIFI_STATE': ['WifiManager', 'WifiP2pManager']}

dist_types = {
    'semantic': 'semantic_dist',
    'event': 'event_dist',
    'who': 'who_dist',
    'all': 'all_dist'
}

if __name__ == '__main__':
    super_out_dir = 'Play_win8'
    perm_type = 'Location'
    perm_keywords = perm_types[perm_type]
    dist_type = 'who'
    out_base_dir = 'output/' + dist_types[dist_type] + '/' + super_out_dir + '/' + perm_type + '/'
    logger = Utilities.set_logger('COSMOS_MINING_PY')

    LDA.logger = logger
    TriggerOutHandler.logger = logger

    trigger_java_out_dir = 'D:\COSMOS\output\java\\' + super_out_dir + '\\'
    trigger_py_out_dir = 'D:\COSMOS\output\py\\' + super_out_dir + '\\'
    categories = {}
    for filename in os.listdir(trigger_py_out_dir):
        if os.path.isdir(os.path.join(trigger_py_out_dir, filename)):
            category = filename
            categories[category] = []

    all_words = []
    rm_category = []

    for category in categories:
        doc_data_file_path = out_base_dir + category + '_' + perm_type + '.json'
        docs = {}
        docs = Utilities.load_json(doc_data_file_path)

        if not docs:
            logger.info('Try to read xml files for ' + category)
            trigger_out_handler = TriggerOutHandler(category, perm_keywords, trigger_py_out_dir)
            if not os.path.exists(trigger_java_out_dir + category):
                rm_category.append(category)
                logger.warn(category + ' does not exist.')
                continue
            for root, dirs, files in os.walk(trigger_java_out_dir + category):
                for file_name in files:
                    if file_name.endswith('.json'):
                        try:
                            trigger_out_handler.handle_out_json(os.path.join(root, file_name))
                            for entry in trigger_out_handler.get_sens_comp().get_entries():
                                views = trigger_out_handler.get_sens_comp().get_entry(entry).get_views()
                                for view in views:
                                    print(view, views[view].srid)
                        except Exception as e:
                            logger.error(e)
                            logger.error(os.path.join(root, file_name))
            docs = trigger_out_handler.words
            # logger.info(trigger_out_handler.words)

            #Utilities.save_json(docs, doc_data_file_path)
        if not docs or len(docs) == 0 or not isinstance(docs, dict):
            rm_category.append(category)
        else:
            categories[category] = docs
            all_words.extend(docs.values())

    for category in rm_category:
        categories.pop(category, None)

    for category in categories:
        logger.info(category)



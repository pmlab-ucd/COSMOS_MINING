import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import tree
import codecs, json


class SklearnUtils:
    out_dir = 'D:\workspace\COSPOS_MINING\output\gnd\Test\\'

    @staticmethod
    def load_train_data(data_path, target_path, tag_path):
        obj_text = codecs.open(data_path, 'r', encoding='utf-8').read()
        train_data = json.loads(obj_text)
        train_data = np.array(train_data)

        obj_text = codecs.open(target_path, 'r', encoding='utf-8').read()
        train_target = json.loads(obj_text)

        obj_text = codecs.open(tag_path, 'r', encoding='utf-8').read()
        train_dict = json.loads(obj_text)

        if len(train_target) != len(train_data):
            print('ERROR: number of titles and titles not consistent')
            exit(1)

        print(train_dict)
        for i in range(0, len(train_data)):
            data_instance = train_data[i]
            data_target = train_target[i]
            SklearnUtils.translate_feature(data_instance, train_dict, data_target)

        return [train_data, train_target, train_dict]

    @staticmethod
    def fit(X, y):
        clf = RandomForestClassifier(n_estimators=15, max_depth=None,
                                     min_samples_split=2, random_state=0)
        clf.fit(X, y)
        return clf

    @staticmethod
    def translate_feature(data_instance, train_dict, data_target):
        instance = {}
        instance['doc'] = []
        instance['label'] = data_target
        for i in range(0, len(data_instance)):
            if data_instance[i] == 1:
                instance['doc'].append(train_dict[i])
        print(instance)
        return instance

if __name__ == '__main__':
    X, y = SklearnUtils.load_train_data(SklearnUtils.out_dir + 'train_data.json', SklearnUtils.out_dir + 'train_target.json',
                                        SklearnUtils.out_dir + 'train_dict.json')
    clf = SklearnUtils.fit(X, y)
    # model2java(clf)
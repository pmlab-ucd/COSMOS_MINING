import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

out_dir = 'D:\workspace\COSPOS_MINING\output\gnd\Test'

def docs2bag(instances, gen_arff=True):
    train_data = []
    train_data_label = []

    for i in range(0, len(instances)):
        train_data.append(' '.join(instances[i]['doc']))
        train_data_label.append(instances[i]['label'])

    print(train_data)

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

    if len(train_data_label) != len(train_data):
        print('ERROR: number of titles and titles not consistent')
        exit(1)

    X, y = train_data_features, train_data_label
    clf = RandomForestClassifier(n_estimators=15, max_depth=None,
                                 min_samples_split=2, random_state=0)
    clf.fit(X, y)


if __name__ == '__main__':
    instances = json.load(open(out_dir + '/instances.json', 'r'))

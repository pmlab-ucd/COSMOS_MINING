from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import os
from gensim.models import ldamodel
from gensim import corpora, models
import matplotlib.pyplot as plt
import numpy as np
import pandas


class LDA:
    logger = None
    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')
    useless_words = ['get', 'start', 'let', 's', 'start', 'use', 'ok', 'cancel', 'please', 'void', 'com',
                     'bundl', 'android', 'os', 'int', 'activ', 'view', 'app', 'ui', 'widget']
    filter_doc_words = ['Crash', 'crash', 'licens']

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    """
    # create sample documents
    doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
    doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
    doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
    doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
    doc_e = "Health professionals say that brocolli is good for your health."

    # compile sample documents into a list
    doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
    """

    debug = False

    def __init__(self, doc_list, out_dir, model_name, parameter_list):
        # list for tokenized documents in loop
        self.texts = []
        self.doc_set = []
        for doc in doc_list:
            doc = ';'.join(doc)
            #LDA.logger.info(doc)
            add_doc = True
            for key_word in LDA.filter_doc_words:
                if key_word in doc:
                    add_doc = False
                    break
            if add_doc:
                self.add_doc(doc)
        self.model = None
        self.dictionary = None
        self.out_dir = out_dir
        self.model_name = model_name
        self.parameter_list = parameter_list

    def add_doc(self, doc):
        self.doc_set.append(doc)

    @staticmethod
    def pre_process(doc):
        # clean and tokenize document string
        raw = doc.lower()
        tokens = LDA.tokenizer.tokenize(raw)
        if LDA.debug:
            LDA.logger.info(tokens)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if i not in LDA.en_stop]

        # filter other useless words
        filtered_tokens = [i for i in stopped_tokens if i not in LDA.useless_words and len(i) > 1]

        # stem tokens
        stemmed_tokens = [LDA.p_stemmer.stem(i) for i in filtered_tokens]

        # filter other useless words, again
        filtered_tokens = [i for i in stemmed_tokens if i not in LDA.useless_words]

        if LDA.debug:
            LDA.logger.info(filtered_tokens)

        return filtered_tokens

    def pre_process_doc_set(self, doc_set):
        # loop through document list
        for i in doc_set:
            # add tokens to list
            self.texts.append(self.pre_process(i))

    def fit(self):
        self.pre_process_doc_set(self.doc_set)
        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(self.texts)

        if self.debug:
            LDA.logger.info(dictionary.token2id)
        self.dictionary = dictionary
        dictionary.save(self.out_dir + '/' + self.model_name + '.dict')

        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in self.texts]
        if self.debug:
            LDA.logger.info(corpus[0])  # the frequency of the word which label is id0

        # generate LDA model
        grid = {}
        number_of_words = sum(cnt for document in corpus for _, cnt in document)
        for parameter_value in self.parameter_list:
            grid[parameter_value] = []
            print(parameter_value, self.parameter_list)
            LDA.logger.info('starting pass for parameter_value = ' + str(parameter_value))
            model = ldamodel.LdaModel(corpus, num_topics=parameter_value, id2word=dictionary, passes=20)
            # model = models.LdaMulticore(corpus, num_topics=ntop, id2word=dictionary, passes=20) #iterations=10)
            # model = models.HdpModel(corpus, id2word=dictionary)

            perplex = model.bound(corpus)  # this is model perplexity not the per word perplexity
            LDA.logger.info('Total Perplexity: ' + str(perplex))
            grid[parameter_value].append(perplex)

            per_word_perplex = np.exp2(-perplex / number_of_words)
            LDA.logger.info('Per-word Perplexity:' + str(per_word_perplex))
            grid[parameter_value].append(per_word_perplex)
            self.model = model
            model.save(self.out_dir + '/' + self.model_name + '_' + str(parameter_value) + '.lda')
            for trained_model in model.print_topics(num_topics=parameter_value, num_words=19):
                LDA.logger.info('Trained: ' + str(trained_model))
            if self.debug:
                for i in self.texts:
                    self.predict(' '.join(i))

        # for numtopics in parameter_list:
            # print(numtopics, '\t', grid[numtopics])
        if len(self.parameter_list) > 1:
            return
        df = pandas.DataFrame(grid)
        ax = plt.figure(figsize=(7, 4), dpi=300).add_subplot(111)
        df.iloc[1].transpose().plot(ax=ax, color="#254F09")
        plt.xlim(self.parameter_list[0], self.parameter_list[-1])
        plt.ylabel('Perplexity')
        plt.xlabel('topics')
        plt.title('')
        plt.savefig('gensim_multicore_i10_topic_perplexity.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)
        plt.show()
        df.to_pickle(self.out_dir + '/' + 'gensim_multicore_i10_topic_perplexity.df')

    def predict(self, query, pre_process=False, threshold=0.5):
        if not self.model:
            model_file = self.out_dir + '/' + self.model_name + '.pkl'
            if not os.path.exists(model_file):
                LDA.logger.error('The model is not set yet!')
                return
            else:
                self.model = models.LdaModel.load(model_file)

        if not self.dictionary:
            dic_file = self.out_dir + '/' + self.model_name + '.dict'
            if not os.path.exists(dic_file):
                LDA.logger.error('The model is not set yet!')
                return
            else:
                self.dictionary = corpora.Dictionary.load(dic_file)
        return LDA.spredict(self.model, self.dictionary, query, pre_process=pre_process, threshold=threshold)

    @staticmethod
    def spredict(model, dictionary, query, pre_process=False, threshold=0.5):
        if pre_process:
            query = ';'.join(query)
            query = LDA.pre_process(query)

        if not isinstance(query, str):
            query = ' '.join(query)

        LDA.logger.info(query)
        query = query.split()
        query_bow = dictionary.doc2bow(query)
        a = list(sorted(model[query_bow], key=lambda x: x[1]))
        tnum, likelihood = a[-1]
        if likelihood < threshold:
                # LDA.logger.info(str(a[0]) + ', ' + self.model.print_topic(a[0][0]))  # the least related
            LDA.logger.info(str(a[-1]) + ', ' + model.print_topic(a[-1][0]))  # the most related
        else:
            LDA.logger.info('Passed with ' + str(a[-1]) + ', ' + model.print_topic(a[-1][0]))






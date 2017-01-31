from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import os
from gensim.models import ldamodel
from gensim import corpora, models


class LDA:
    logger = None
    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')
    useless_words = ['get', 'start', 'let', 's', 'start', 'use']

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

    def __init__(self, doc_list, out_dir, model_name, ntop):
        # list for tokenized documents in loop
        self.texts = []
        self.doc_set = []
        for doc in doc_list:
            doc = ';'.join(doc)
            self.add_doc(doc)
        self.model = None
        self.dictionary = None
        self.out_dir = out_dir
        self.model_name = model_name
        self.ntop = ntop

    def add_doc(self, doc):
        self.doc_set.append(doc)

    def pre_process(self):
        # loop through document list
        for i in self.doc_set:
            # clean and tokenize document string
            raw = i.lower()
            tokens = self.tokenizer.tokenize(raw)
            if LDA.debug:
                LDA.logger.info(tokens)

            # remove stop words from tokens
            stopped_tokens = [i for i in tokens if i not in self.en_stop]

            # stem tokens
            stemmed_tokens = [self.p_stemmer.stem(i) for i in stopped_tokens ]
            if LDA.debug:
                LDA.logger.info(stemmed_tokens)

            # filter other useless words
            filtered_tokens = [i for i in stemmed_tokens if i not in self.useless_words]

            # add tokens to list
            self.texts.append(filtered_tokens)

    def fit(self):
        self.pre_process()
        # turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(self.texts)

        LDA.logger.info(dictionary.token2id)
        self.dictionary = dictionary
        dictionary.save(self.out_dir + '/' + self.model_name + '.dict')

        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in self.texts]
        LDA.logger.info(corpus[0])  # the frequency of the word which label is id0

        # generate LDA model
        model = ldamodel.LdaModel(corpus, num_topics=self.ntop, id2word=dictionary, passes=20)
        LDA.logger.info(model.print_topics(num_topics=self.ntop, num_words=9))
        self.model = model
        model.save(self.out_dir + '/' + self.model_name + '.pkl')

        for i in self.texts:
            self.predict(' '.join(i))

    def predict(self, query):
        model_file = self.out_dir + '/' + self.model_name + '.pkl'
        dic_file = self.out_dir + '/' + self.model_name + '.dict'
        if not self.model:
            if not os.path.exists(model_file):
                LDA.logger.info('The model is not set yet!')
                return
            else:
                self.model = models.LdaModel.load(model_file)

        if not self.dictionary:
            if not os.path.exists(dic_file):
                LDA.logger.info('The model is not set yet!')
                return
            else:
                self.dictionary = corpora.Dictionary.load(dic_file)

        LDA.logger.info(query)
        query = query.split()
        query_bow = self.dictionary.doc2bow(query)
        a = list(sorted(self.model[query_bow], key=lambda x: x[1]))
        LDA.logger.info(str(a[0]) + ', ' + self.model.print_topic(a[0][0])) # the least related
        LDA.logger.info(str(a[0]) + ', ' + self.model.print_topic(a[-1][0])) # the most related





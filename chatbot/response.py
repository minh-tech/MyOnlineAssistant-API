import nltk
import numpy as np
import tflearn
import random
import pickle
import json
import os
from chatbot.stop_words import ENGLISH_STOP_WORD
from chatbot.utils import lemmatize_words
from nltk.tag import StanfordNERTagger
from service_api import constant as ct


CHATBOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ChatBotResponse:

    def __init__(self):

        self.context = {}
        self.user_dict = {}

        data = pickle.load(open(CHATBOT_DIR + "/" + ct.TRAINING_DATA, "rb"))
        self.words = data[ct.WORDS]
        self.ignore_words = ENGLISH_STOP_WORD
        self.classes = data[ct.CLASSES]
        train_x = data[ct.TRAIN_X]
        train_y = data[ct.TRAIN_Y]

        with open(CHATBOT_DIR + '/' + ct.INTENTS_JSON) as json_data:
            self.intents = json.load(json_data)

        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation=ct.SOFTMAX)
        net = tflearn.regression(net)
        logs = CHATBOT_DIR + '/' + ct.TF_LOGS
        self.model = tflearn.DNN(net, tensorboard_dir=logs)
        self.model.load(CHATBOT_DIR + '/' + ct.MODEL_TF)

    def bow(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0]*len(self.words)
        for sentence_word in sentence_words:
            for i, word in enumerate(self.words):
                if word == sentence_word:
                    bag[i] = 1
                    break
        return np.array(bag)

    def classify(self, sentence):
        results = self.model.predict([self.bow(sentence)])[0]
        results = [[i, r] for i, r in enumerate(results) if r > ct.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
        print(return_list)
        return return_list

    def response(self, sentence, user_id='1106'):
        results = self.classify(sentence)
        if results:
            while results:
                for i in self.intents[ct.INTENTS]:
                    if i[ct.TAG] == results[0][0]:

                        if ct.CONTEXT_FILTER not in i or \
                                (user_id in self.context and ct.CONTEXT_FILTER in i and
                                 i[ct.CONTEXT_FILTER] == self.context[user_id]):

                            response = random.choice(i[ct.RESPONSES])
                            if ct.CONTEXT_SET in i:
                                self.context[user_id] = i[ct.CONTEXT_SET]

                            if ct.FUNCTION in i:
                                if i[ct.FUNCTION] == ct.GET_ENTITY_NAME:
                                    name, tag = self.get_entity_name(sentence)
                                    if tag == ct.PERSON:
                                        self.user_dict[user_id] = name
                                        if "%s" in response:
                                            response = response % name
                                    elif tag == ct.ORGANIZATION:
                                        pass

                            if "%s" in response:
                                response = random.choice(i[ct.ALTERNATIVE])
                            elif ct.EXTENSIONS in i:
                                response += "|" + random.choice(i[ct.EXTENSIONS])

                            emotion = ""
                            if ct.EMOTION in i:
                                emotion = i[ct.EMOTION]

                            return response, emotion
                results.pop(0)

    def get_username(self, user_id):
        if user_id in self.user_dict:
            return self.user_dict[user_id]
        else:
            return ct.GUEST_NAME

    def remove_username(self, user_id):
        self.user_dict.pop(user_id, None)

    def welcome(self, user_id, username=ct.GUEST_NAME, existed=ct.FALSE):
        if user_id not in self.user_dict or (self.user_dict[user_id] != username and username != ct.GUEST_NAME):
            self.user_dict[user_id] = username
        if existed == ct.TRUE:
            if ct.GUEST_NAME in username:
                # Glad to see you come back. What do you want to know this time?
                welcome = ct.WELCOME_SENT1
            else:
                # Happy to see you again, name. What do you want to know this time?
                welcome = ct.WELCOME_SENT2 % username
        else:
            # Hi, there. How are you? My name is Cheri. I am an online assistant of Minh. What should I call you by?
            welcome = ct.WELCOME_SENT3
        emotion = ct.WELCOME
        return welcome, emotion

    @staticmethod
    def clean_up_sentence(sentence):
        tokens = nltk.word_tokenize(sentence)
        tokens = lemmatize_words(tokens)
        return tokens

    @staticmethod
    def get_entity_name(sentence):
        tokens = nltk.word_tokenize(sentence)
        st = StanfordNERTagger(CHATBOT_DIR + '/Standford_lib/english.all.3class.distsim.crf.ser.gz',
                               CHATBOT_DIR + '/Standford_lib/stanford-ner.jar')

        tagged_words_list = st.tag(tokens)
        for word, tag in tagged_words_list:
            if tag in ct.ENTITY_TAG:
                return word, tag
        return "", ""


def main():

    chatbot = ChatBotResponse()
    name, emotion = chatbot.response("my name is John")
    print(name)
    print(emotion)

    pass


if __name__ == '__main__':
    main()

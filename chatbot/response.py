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

ERROR_THRESHOLD = 0.25
CHATBOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENTITY_TAG = ('PERSON', 'ORGANIZATION')

class ChatBotResponse:

    def __init__(self):

        self.context = {}
        self.user_dict = {}

        data = pickle.load(open(CHATBOT_DIR+"/training_data", "rb"))
        self.words = data['words']
        self.ignore_words = ENGLISH_STOP_WORD
        self.classes = data['classes']
        train_x = data['train_x']
        train_y = data['train_y']

        with open(CHATBOT_DIR+'/intents.json') as json_data:
            self.intents = json.load(json_data)

        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)
        logs = CHATBOT_DIR+'/tflearn_logs'
        self.model = tflearn.DNN(net, tensorboard_dir=logs)
        self.model.load(CHATBOT_DIR+'/model.tflearn')

    def clean_up_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tokens = lemmatize_words(tokens)
        return tokens

    def get_entity_name(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        st = StanfordNERTagger(CHATBOT_DIR + '/Standford_lib/english.all.3class.distsim.crf.ser.gz',
                               CHATBOT_DIR + '/Standford_lib/stanford-ner.jar')

        tagged_words_list = st.tag(tokens)
        for word, tag in tagged_words_list:
            if tag in ENTITY_TAG:
                return word, tag
        return "", ""

    def bow(self, sentence, show_details=False):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0]*len(self.words)
        for sentence_word in sentence_words:
            for i, word in enumerate(self.words):
                if word == sentence_word:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % word)
                    break
        return np.array(bag)

    def classify(self, sentence):
        results = self.model.predict([self.bow(sentence)])[0]
        results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
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
                for i in self.intents['intents']:
                    if i['tag'] == results[0][0]:

                        if 'context_filter' not in i or \
                                (user_id in self.context and 'context_filter' in i and
                                 i['context_filter'] == self.context[user_id]):

                            response = random.choice(i['responses'])
                            if 'context_set' in i:
                                self.context[user_id] = i['context_set']

                            if 'function' in i:
                                if i['function'] == 'get_entity_name':
                                    name, tag = self.get_entity_name(sentence)
                                    if tag == 'PERSON':
                                        self.user_dict[user_id] = name
                                        response = random.choice(i['responses']) % name

                            if 'extensions' in i:
                                response += "|" + random.choice(i['extensions'])

                            return response
                results.pop(0)

    def get_username(self, user_id):
        if user_id in self.user_dict:
            return self.user_dict[user_id]
        else:
            return ""

    def remove_username(self, user_id):
        self.user_dict.pop(user_id, None)

    def welcome(self, user_id="1106", username="Guest", existed=False):
        if user_id not in self.user_dict or (self.user_dict[user_id] != username and username != "Guest"):
            self.user_dict[user_id] = username

        if existed:
            if "Guest" in username:
                welcome = "Glad to see you come back|What do you want to know this time?"
            else:
                welcome = "Happy to see you again, %s|What do you want to know this time?" % username
        else:
            welcome = "Hi, there. How are you? My name is Cheri|I am an online assistant of Minh|" \
                      "What should I call you by?"

        return welcome


def main():
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(BASE_DIR)


    chatbot = ChatBotResponse()
    name = chatbot.response("My name is Harrison")
    print(name)
    # print("chatbot get username: " + chatbot.get_username())
    # response = chatbot.response("Nice to meet you")
    # print(response)
    # flag = True
    # print("Cheri: My name is Cheri.")
    #
    # while flag:
    #     user_response = input()
    #     user_response = user_response.lower()
    #     if user_response != 'bye':
    #         print("Cheri: ", end="")
    #         print(chatbot_response.response(user_response))
    #     else:
    #         flag = False
    #         print("Cheri: Bye! Take care...")
    pass


if __name__ == '__main__':
    main()

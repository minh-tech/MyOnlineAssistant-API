import tensorflow as tf
import nltk
import random
import numpy as np

import json
import pickle
from chatbot.utils import Utils
from chatbot import constant as ct


class ChatBotModel:
    @staticmethod
    def create_chatbot_data():

        with open(ct.INTENTS_JSON) as json_data:
            intents = json.load(json_data)

        words = []
        classes = []
        documents = []

        for intent in intents[ct.INTENTS]:
            for pattern in intent[ct.PATTERNS]:
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                documents.append((w, intent[ct.TAG]))
                if intent[ct.TAG] not in classes:
                    classes.append(intent[ct.TAG])

        words = Utils.lemmatize_words([w.lower() for w in words])
        words = sorted(list(set(words)))

        classes = sorted(list(set(classes)))

        print(len(documents), 'documents')
        print(len(classes), 'classes', classes)
        print(len(words), 'unique lemmatized words', words)

        training = []

        output_empty = [0] * len(classes)

        for doc in documents:
            bag = []
            pattern_words = doc[0]
            pattern_words = Utils.lemmatize_words([w.lower() for w in pattern_words])
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1

            training.append([bag, output_row])

        random.shuffle(training)
        training = np.array(training)

        train_x = list(training[:, 0])
        train_y = list(training[:, 1])

        tf.compat.v1.reset_default_graph()

        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation=ct.RELU),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(64, activation=ct.RELU),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(train_y[0]), activation=ct.SOFTMAX)
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=8)

        model.save(ct.MODEL_TF)

        pickle.dump({ct.WORDS: words, ct.CLASSES: classes, ct.TRAIN_X: train_x, ct.TRAIN_Y: train_y},
                    open(ct.TRAINING_DATA, "wb"))


if __name__ == "__main__":
    ChatBotModel.create_chatbot_data()

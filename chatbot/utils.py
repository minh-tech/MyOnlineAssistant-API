import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from chatbot.stop_words import ENGLISH_STOP_WORD
from chatbot import constant as ct

# Download the corpora and models
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


class Utils:

    # Get wordnet part-of-speech tagger
    @staticmethod
    def get_wordnet_pos(word_tag):
        if word_tag.startswith('N'):
            return wordnet.NOUN
        elif word_tag.startswith('J'):
            return wordnet.ADJ
        elif word_tag.startswith('V'):
            return wordnet.VERB
        elif word_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # Convert pronoun
    @staticmethod
    def convert_pronoun(word):

        if word in ct.PRONOUNS_1ST:
            return 'i'
        if word in ct.PRONOUNS_2ND:
            return 'you'
        if word in ct.PRONOUNS_3RD_MALE:
            return 'he'
        if word in ct.PRONOUNS_3RD_FEMALE:
            return 'she'
        if word in ct.PRONOUNS_3RD_THING:
            return 'it'
        if word in ct.PRONOUNS_1ST_PLURAL:
            return 'we'
        if word in ct.PRONOUNS_3RD_PLURAL:
            return 'they'
        return word

    # Split a sentence into array of words
    @staticmethod
    def tokenize_text(text):
        tokens = nltk.word_tokenize(text)
        return Utils.lemmatize_words(tokens)

    # Convert words to infinitive words
    @staticmethod
    def lemmatize_words(words):
        tagged_tokens = nltk.pos_tag(words)
        # print(tagged_tokens)
        array = []
        lemma = WordNetLemmatizer()
        for token in tagged_tokens:
            temp = token[0].lower()
            if temp in ENGLISH_STOP_WORD:
                continue
            temp = Utils.convert_pronoun(temp)
            array.append(lemma.lemmatize(temp, pos=Utils.get_wordnet_pos(token[1])))
        # print(array)
        return array


if __name__ == "__main__":
    text1 = "Would you mind to answer me this question?"
    array1 = Utils.tokenize_text(text1)
    print(array1)

from mecab import MeCab
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from pororo import Pororo
from collections import defaultdict

mecab = MeCab()
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def detect_language(text):
    language = "english"
    for c in text:
        if ord('가') <= ord(c) <= ord('힣'):
            language = 'korean'
            break
    return language


def get_ngrams(data, min_count=3, n_range=(2, 3)):
    def to_ngrams(words, n):
        ngrams = []
        for b in range(0, len(words) - n + 1):
            all_noun = True
            for i in range(b, b+n):
                if words[i][1][0] != 'N' or not words[i][0].isalpha():
                    all_noun = False
                    break
            if all_noun:
                ngrams.append(tuple([w[0] for w in words[b:b+n]]))
        return ngrams

    n_begin, n_end = n_range
    ngram_counter = defaultdict(int)

    docs = []
    for d in data:
        for sent in d["sentences"]:
            docs.append(sent["text"])
            for s in sent["sentences"]:
                docs.append(s["text"])

    for doc in docs:
        if detect_language(doc) == "korean":
            words = mecab.pos(doc)
        else:
            words = nltk.pos_tag(nltk.word_tokenize(doc))
        for n in range(n_begin, n_end + 1):
            for ngram in to_ngrams(words, n):
                ngram_counter[ngram] += 1

    ngram_counter = {
        ngram: count for ngram, count in ngram_counter.items()
        if count >= min_count
    }
    return ngram_counter


def tokenizer(text):
    if detect_language(text) == "korean":
        tokens = mecab.morphs(text)
    else:
        tokens = nltk.word_tokenize(text)
    return tokens


def tf_idf(data):
    corpus = []
    for d in data:
        text = ""
        for sent in d["sentences"]:
            text += sent["text"]
            for s in sent["sentences"]:
                text += s["text"]
        corpus.append(text)

    tfidfv = TfidfVectorizer(tokenizer=tokenizer, ngram_range=(1, 2))
    sp_matrix = tfidfv.fit_transform(corpus)

    word2id = defaultdict(lambda: 0)
    for idx, feature in enumerate(tfidfv.get_feature_names()):
        word2id[feature] = idx

    for i, sentence in enumerate(corpus):
        print(f"- {data[i]['topic']}")
        if detect_language(sentence) == "korean":
            tokens = mecab.nouns(sentence)
        else:
            tokens = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(sentence))
                      if pos[0] == 'N' and ord('a') <= ord(word[0].lower()) <= ord('z')]
        print(sorted(list(set([(token, sp_matrix[i, word2id[token]]) for token in tokens])), key=lambda x: x[1], reverse=True))
    return data


ko_ner = Pororo(task="ner", lang="ko")
en_ner = Pororo(task="ner", lang="en")


def ner_tagger(doc):
    if detect_language(doc) == "korean":
        ner = ko_ner(doc)
    else:
        ner = en_ner(doc)
    return ner

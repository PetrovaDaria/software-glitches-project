import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')


def get_first_n_sentences(text: str, n: int = 5):
    sentences = sent_tokenize(text)
    return sentences[:min(n, len(sentences))]


def get_joined_first_n_sentences(text: str, n: int = 5):
    sentences = get_first_n_sentences(text, n)
    return ' '.join(sentences)

import re
import os

here = os.path.dirname(os.path.abspath(__file__))

word_files = {
    "conjection": "conjunction.txt",
    "linkingverb": "linkingverb.txt",
    "determiner": "determiner.txt",
    "pronoun": "pronoun.txt",
    "preposition": "preposition.txt",
    "adverb": "adverb.txt",
    "verb": "verb.txt",
    "adjective": "adjective.txt",
    "noun": "noun.txt",
}


def load_word_files():
    words = {}
    for word_type, file_name in word_files.items():
        with open(os.path.join(here, "wordlists", file_name), "r") as f:
            words[word_type] = f.read().split("\n")
    return words


def match(posgex, string):
    regex = posgex_to_regex(posgex)
    return re.match(regex, string)


def posgex_to_regex(query_string):
    # What we want to do here is match every [POS] to a group containing all the possible words
    # We need to start with a list of pos
    word_map = load_word_files()
    for word_type, words in word_map.items():
        wordtype = word_type.upper()
        replacement_string = f"[{wordtype}]"
        query_string = query_string.replace(replacement_string, "({})".format("|".join(words)))
    return query_string

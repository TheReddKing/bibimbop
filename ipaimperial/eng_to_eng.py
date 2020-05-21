import pickle
import random
from to_ipa_by_syllable import to_ipa_by_syllable

MAPPING_FILE = "data/word_to_syllables.pkl"

def create_common():
    with open('data/common.txt') as word_file:
        words = set(word_file.read().split())
    word_to_syllables = {}
    for i, word in enumerate(words):
        result = to_ipa_by_syllable(word)
        if not result[0].startswith("__IGNORE__"):
            word_to_syllables[word] = result
        if i % 100 == 0:
            print(f"converted {i} of {len(words)}")
    pickle.dump(word_to_syllables, open(MAPPING_FILE, "wb"))


def transpile_phrase(phrase):
    word_to_syllables = pickle.load(open(MAPPING_FILE, "rb"))

    with open('similarity.txt', 'r') as f:
        similar_pairs = set()
        for line in f.readlines():
            syms = line.split()
            for i in range(len(syms)):
                for j in range(i + 1, len(syms)):
                    similar_pairs.add((syms[i], syms[j]))
                    similar_pairs.add((syms[j], syms[i]))

    def hamming_dist(s1, s2):
        if len(s1) == 0:
            return len(s2)
        elif len(s2) == 0:
            return len(s1)
        if s1[0] == s2[0]:
            return -0.2 + hamming_dist(s1[1:], s2[1:])
        if (s1[0], s2[0]) in similar_pairs:
            return -0.2 + hamming_dist(s1[1:], s2[1:])
        return 2 + min([hamming_dist(s1[1:], s2), hamming_dist(s1, s2[1:])])

    phrase_syllables = []
    words = phrase.lower().split(' ')
    for word in words:
        phrase_syllables.extend(to_ipa_by_syllable(word))
    result = []
    print(f"phrase: {phrase}")
    print(f"syllables: {phrase_syllables}")
    while len(phrase_syllables) > 0:
        # find best matching word
        best_word = ""
        best_score = -1000
        num_syllables = 0
        for word, word_syllables in word_to_syllables.items():
            if len(word_syllables) > len(phrase_syllables):
                continue
            if any([word == w or word == w + 's' or w == word + 's' for w in words]): # don't want exact matches
                continue
            if len(word) <= 3: # don't use short words
                continue
            score = 0
            for ps, ws in zip(phrase_syllables, word_syllables):
               score += 1 - hamming_dist(ps, ws)
            score += random.random()
            if score > best_score:
               best_score = score
               best_word = word
               num_syllables = len(word_syllables)
        print(best_word)
        result.append(best_word)
        phrase_syllables = phrase_syllables[num_syllables:]

    return " ".join(result)

if __name__ == "__main__":
    #create_common()
    word_to_syllables = pickle.load(open(MAPPING_FILE, "rb"))
    print(len(word_to_syllables.keys()))
    print(transpile_phrase("an attempt by anton cow"))


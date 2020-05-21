import sys
import os  # noqa
sys.path.append(os.path.join(os.path.dirname(__file__), 'englishipa'))  # noqa

import eng_to_ipa as ipa


def load_words():
    with open('data/dictionary_small.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('fate' in english_words)
    print(ipa.convert(
        "Prepare for the worst. The quick brown fox jumped over the lazy dog."))

    translate_dict = {}
    out = [open(f'data/transl_small_{i}.txt', "w") for i in range(1, 4)]
    for word in english_words:
        syllable_count = ipa.syllable_count(word)
        if (syllable_count > 3):
            continue
        iss = ipa.convert(word, retrieve_all=True, stress_marks="none")
        for i in iss:
            if "*" not in i:
                print(word)
                out[syllable_count - 1].write(i + " " + word + "\n")

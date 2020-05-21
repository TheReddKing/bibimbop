import re
import sys
import json
from os.path import join, abspath, dirname
sys.path.append(join(dirname(__file__), 'englishipa'))  # noqa
import eng_to_ipa as ipa

with open(join(abspath(dirname(__file__)),
               'englishipa', 'eng_to_ipa', 'resources','phones.json'), "r") as phones_json:
    PHONES = json.load(phones_json)

def to_ipa_by_syllable(word):
    cmu = ipa.get_cmu([ipa.preprocess(word)])[0][0]
    cmu = re.sub("[0-9]", "", cmu)
    symbols = {"a": "ə", "ey": "eɪ", "aa": "ɑ", "ae": "æ", "ah": "ə", "ao": "ɔ",
               "aw": "aʊ", "ay": "aɪ", "ch": "ʧ", "dh": "ð", "eh": "ɛ", "er": "ər",
               "hh": "h", "ih": "ɪ", "jh": "ʤ", "ng": "ŋ",  "ow": "oʊ", "oy": "ɔɪ",
               "sh": "ʃ", "th": "θ", "uh": "ʊ", "uw": "u", "zh": "ʒ", "iy": "i", "y": "j"}
    syllables = []
    cur_syllable = ''
    vowel_seen = False
    syms = cmu.split(' ')
    for i, sym in enumerate(syms):
        # check if new syllable
        if i > 0:
            prev_phone = PHONES[syms[i-1]]
            prev_sym = syms[i-1]
            if PHONES[sym] == 'vowel':
                if (prev_phone != 'vowel' or [prev_sym, sym] in ipa.hiatus) and vowel_seen:
                    syllables.append(cur_syllable)
                    cur_syllable = ''
                vowel_seen = True
        marked = False
        unmarked = sym
        if sym[0] in ["ˈ", "ˌ"]:
            marked = True
            mark = sym[0]
            unmarked = sym[1:]
        if unmarked in symbols:
            if marked:
                cur_syllable += mark + symbols[unmarked]
            else:
                cur_syllable += symbols[unmarked]
        else:
            cur_syllable += sym
    syllables.append(cur_syllable)
    swap_list = [["ˈər", "əˈr"], ["ˈie", "iˈe"]]
    answer = []
    for syllable in syllables:
        if len(syllable) > 0:
            for pair in swap_list:
                if not syllable.startswith(pair[0]):
                    syllable = syllable.replace(pair[0], pair[1])
            answer.append(syllable)
    return answer


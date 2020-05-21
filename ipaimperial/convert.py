import re
import random
def load_simplification():
    f = open('similarity.txt', 'r')
    ipa_simplify_dictionary = {}
    lines = f.read().split("\n")
    for l in lines:
        words = l.split(" ")
        for i in range(1, len(words)):
            ipa_simplify_dictionary[words[i]] = words[0]
    return ipa_simplify_dictionary

def load_vowel_split():
    f = open('vowelsplit.txt', 'r')
    vowel_split = f.read().strip().split(" ")
    return vowel_split

def simplifyipa(sentence):
    for w in ipa_simplify_dictionary:
        if (w in sentence):
            sentence = re.sub(w,ipa_simplify_dictionary[w], sentence)
    return sentence


def load_english():
    out = [open(f'data/transl_small_{i}.txt', "r") for i in range(1, 4)]
    sylla = []
    for o in out:
        translate_dict = {}
        for line in o.readlines():
            i, word = line.strip().split(" ")
            translate_dict[simplifyipa(i)] = word
        sylla.append(translate_dict)
    return sylla

ipa_simplify_dictionary = load_simplification()
vowel_split = load_vowel_split()
sylla = load_english()

def sentence_similarity_1(word, key):
    # comparing word to key
    pass

def all_consonent(word):
    for w in word:
        if w in vowel_split:
            return False
    return True
def is_consonent(char):
    p2 = char
    return p2 not in vowel_split

def isolate_syllables(sentence):
    sentence = "".join([sentence[i] for i in range(len(sentence)) if (i==0) or sentence[i] != sentence[i-1]])
    words = sentence.split(" ")
    full_sentence = ""
    for word in words:
        phrases = re.sub("(" + "|".join(vowel_split) + ")", r"\1 ", word).split(" ")
        phrases_no_s = list(map(lambda x: re.sub("s", "", x), phrases))
        i = 0
        j = 1
        while i < len(phrases) - 1 and j < len(phrases):
            p2 = phrases_no_s[j]
            if (len(p2) == 0):
                phrases[i] += phrases[j]
                phrases[j] = ""
                j += 1
                continue
            if (len(p2) == 1):
                phrases[i] += phrases[j]
                phrases[j] = ""
                j += 1
                continue
            if (all_consonent(p2)):
                phrases[i] += phrases[j]
                phrases[j] = ""
                j += 1
                continue
            if (len(p2) > 2):
                if (is_consonent(p2[0]) and is_consonent(p2[1])):
                    subs = 2 if phrases[j][0] == 's' else 1
                    phrases[i] += phrases[j][:subs]
                    phrases[j] = phrases[j][subs:]
            # okay so now it's another consenent
            i = j
            j += 1
        full_sentence += " ".join(list(filter(lambda x: len(x) > 0, phrases))) + " "
    return full_sentence

def characters_contained(word, key):
    forgiveness = 0 #1 gives one key to be wrong
    for i in range(len(word)):
        try:
            l = key.index(word[i])
            key = key[l+1:]
        except:
            forgiveness -= 1
            if (forgiveness < 0):
                return -1
    return forgiveness
        
def convert(sentence):
    sentence = simplifyipa(sentence)
    syllables = isolate_syllables(sentence).split(" ")
    # MERGE SENTENCE AGAIN
    print(syllables)
    i = 0
    final_sentence = ""
    # translate_dict = {**sylla[0], **sylla[1]}
    while i < len(syllables):
        found = False
        options = []
        for numsylla in range(0,-1,-1):
            # one and 2
            translate_dict = sylla[numsylla]
            if i + numsylla >= len(syllables):
                continue
            word = "".join(syllables[i : i + numsylla + 1])
            if ("." in word):
                continue
            bestop, jj, lenj = None, None, 0
            for key in translate_dict.keys():
                # if (bestop is not None and lenj < len(translate_dict[key])):
                #     continue
                # if (key.startswith(word[:1]) and characters_contained(word,key)):
                # if ((key[0] == word[0]) and characters_contained(word,key)):
                c = characters_contained(word,key)
                if (c > -1):
                    if (bestop is None or len(translate_dict[key]) < lenj):
                        bestop, jj, lenj = translate_dict[key], numsylla, len(key)
                    options.append((translate_dict[key], numsylla, c, key))
                    found = True
            if (found):
                break
        if (not found):
            final_sentence += " " + syllables[i]
            i += 1
        else:
            if random.randint(1,4) < 4:
                final_sentence += " " + options[random.randint(0, len(options)-1)][0]
            else:
                final_sentence += " " + bestop
            print(syllables[i:i+numsylla + 1], options[:5])
            i += numsylla + 1
    return final_sentence


def convert_old(sentence):
    sentence = simplifyipa(sentence)
    sentence = isolate_syllables(sentence)
    # MERGE SENTENCE AGAIN
    print(sentence)
    i = 0
    final_sentence = ""
    # translate_dict = {**sylla[0], **sylla[1]}
    translate_dict = sylla[0]
    while i < len(sentence):
        bestop, jj, lenj = None, None, 0
        found = False
        for j in range(i + 7, i + 1, -1):
        # for j in range(i + 2, i + 5):
            word = sentence[i:j]
            for key in translate_dict.keys():
                if (bestop is not None and lenj < len(translate_dict[key]) - (j - i)):
                    continue
                if (key.startswith(word)):
                    if (bestop is None or len(translate_dict[key]) - (j - i) < lenj):
                        bestop, jj, lenj = translate_dict[key], j, len(key) - (j - i)
                    found = True
            if (found):
                break
        if (not found):
            final_sentence += " " + sentence[i]
            i += 1
        else:
            final_sentence += " " + bestop
            print(sentence[i:jj])
            i = jj      
    return final_sentence

if __name__ == "__main__":
    vals = 'neka malɯl not̚nɯn kʌt̚to . nʌɰi tɕak̚ɯn maltʰuto . nap͈ɯtɕi anɯnkʌl ... '
    vals += ' malʌpi sonɯl tɕap̚ko . tɕokɯmɯn nolɾɛto . siltɕika anɯnkʌl ...'
    vals += ' mulkamtɕʰʌɾʌm pʰaɾat̚tʌn . hanɯlɯn pʌls͈ʌ k͈amat̚ko . kamtɕʌŋɯn tʌ kiᇁʌtɕjʌ ...'
    # vals += 'uɾi tulman nɯk͈jʌtɕinɯn isaŋhan nɯk͈im . nato nʌmu tɕot̚a'
    # vals += 'asywʌ pʌls͈ʌ si ʌt͈ʌk̚hɛ pʌls͈ʌ sine ponɛtɕuki silɯnkʌl alko it̚ʌ '
    # vals = "θɪs ɪs eɪ test sentns"
    # vals = "haɪ, iːvrɪbodɪ. eɪnijah, θank jou fɒr θat beajutaɪfʌl intrəʊdukʃɒn. aɪ koəɫd nɒt biː projudɛr ɒf iːvrɪθɪng joju’v dəʊn ɪn joʌr taɪm wiθ θiː əʊbeɪmeɪ foundeɪʃɒn."
    # vals = "op͈an kaŋnam sɯtʰail"
    # vals += "kaŋnam sɯtʰail . "
    # vals += "nat̚enɯn t͈asaɾoun inkantɕʌk̚in jʌtɕa . "
    # vals += "kʰʌpʰi hantɕanɰi jʌjuɾɯl anɯn, pʰumkjʌk̚ it̚nɯn jʌtɕa . "
    # vals += "pami omjʌn simtɕaŋi t͈ɯkʌwʌtɕinɯn jʌtɕa . "
    # vals += "kɯɾʌn pantɕʌn it̚nɯn jʌtɕa . "
    # vals += "nanɯn sanai . "
    # vals += "nat̚enɯn nʌmankʰɯm t͈asaɾoun kɯɾʌn sanai . "
    # vals += "kʰʌpʰi sik̚kito tɕʌne wʌnsjat̚ t͈ɛɾinɯn sanai . "
    # vals += "pami omjʌn simtɕaŋi tʰʌtɕjʌ pʌɾinɯn sanai . "
    # vals += "kɯɾʌn sanai . "
    # vals = "peɪreɪ saɪt"
    vals = "newspeɪpɛr riːport"
    vals = "diːs aɪmal numbɛr"
    vals = "eɪreeɪ ɒf eɪ peɪrɔɫliːlogram"
    print(vals)
    print(convert(vals))
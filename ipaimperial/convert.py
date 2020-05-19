import re
def load_simplification():
    f = open('similarity.txt', 'r')
    ipa_simplify_dictionary = {}
    lines = f.read().split("\n")
    for l in lines:
        words = l.split(" ")
        for i in range(1, len(words)):
            ipa_simplify_dictionary[words[i]] = words[0]
    return ipa_simplify_dictionary

def simplifyipa(sentence):
    for w in ipa_simplify_dictionary:
        if (w in sentence):
            sentence = re.sub(w,ipa_simplify_dictionary[w], sentence)
    return sentence


def load_english():
    out = [open(f'data/transl_{i}.txt', "r") for i in range(1, 4)]
    sylla = []
    for o in out:
        translate_dict = {}
        for line in o.readlines():
            i, word = line.strip().split(" ")
            translate_dict[simplifyipa(i)] = word
        sylla.append(translate_dict)
    return sylla

ipa_simplify_dictionary = load_simplification()
sylla = load_english()

def convert(sentence):
    sentence = simplifyipa(re.sub(" ", "", sentence))
    sentence = "".join([sentence[i] for i in range(len(sentence)) if (i==0) or sentence[i] != sentence[i-1]])
    print(sentence)
    i = 0
    final_sentence = ""
    translate_dict = {**sylla[0], **sylla[1]}
    while i < len(sentence):
        bestop, jj = None, None
        found = False
        # for j in range(i + 5, i + 1, -1):
        for j in range(i + 2, i + 5):
            word = sentence[i:j]
            for key in translate_dict.keys():
                if (bestop is not None and len(bestop) < len(translate_dict[key])):
                    continue
                if (key.startswith(word)):
                    if (bestop is None or len(translate_dict[key]) < len(bestop)):
                        bestop, jj = translate_dict[key], j
                    found = True
            if (found):
                break
        if (not found):
            final_sentence += " " + sentence[i]
            i += 1
        else:
            final_sentence += " " + bestop
            i = j

        
    return final_sentence

if __name__ == "__main__":
    vals = 'neka malɯl not̚nɯn kʌt̚to . nʌɰi tɕak̚ɯn maltʰuto . nap͈ɯtɕi anɯnkʌl'
    # vals = 'mulkamtɕʰʌɾʌm pʰaɾat̚tʌn . hanɯlɯn pʌls͈ʌ k͈amat̚ko . kamtɕʌŋɯn tʌ kiᇁʌtɕjʌ'
    print(vals)
    print(convert(vals))
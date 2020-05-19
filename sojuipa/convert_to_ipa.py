from fetch_lyrics import fetch_lyrics
from kparser import Parser
from phonology import Phonology

def convert_to_ipa(lyrics):
    """
    Convert output of fetch_lyrics to ipas
    Output format:
      List of tuples (ipa, raw, bool)
      If true, ipa is of raw korean
      If false, raw is english
    """
    output = []
    for line in lyrics:
        cur_str = ""
        is_korean = True
        i = 0
        while i <= len(line):
            if is_korean:
                if i == len(line) or line[i] != " " and ord(line[i]) < 44032:
                    if len(cur_str) > 0:
                        parser = Parser()
                        phon = Phonology(cur_str)
                        ipa = parser.toipa(phon.pronounce())
                        output.append((ipa, cur_str, True))
                        cur_str = ""
                    is_korean = False
            else:
                if i == len(line) or ord(line[i]) >= 44032:
                    if len(cur_str) > 0:
                        output.append((None, cur_str, False))
                        cur_str = ""
                    is_korean = True
            if i < len(line):
                cur_str += line[i]
            i += 1
    return output

if __name__ == "__main__":
    for ipa, raw, is_korean in convert_to_ipa(fetch_lyrics("https://www.musixmatch.com/lyrics/CHUNG-HA-4/Gotta-Go")):
        if is_korean:
            print(f"{ipa} ({raw})")
        else:
            print(raw)

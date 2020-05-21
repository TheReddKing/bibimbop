mkdir -p data
if [[ ! -f data/dictionary.txt ]]; then
    wget -O data/dictionary.txt https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
fi
if [[ ! -f data/dictionary_small.txt ]]; then
    wget -O data/dictionary_small.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt
fi
if [[ ! -f data/dictionary_2.txt ]]; then
  wget -O data/dictionary_2.txt https://gist.githubusercontent.com/h3xx/1976236/raw/bbabb412261386673eff521dddbe1dc815373b1d/wiki-100k.txt
fi
if [[ ! -f data/common.txt ]]; then
    wget -O data/common.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt
fi
if [[ ! -e englishipa ]]; then
    git clone https://github.com/mphilli/English-to-IPA englishipa
fi

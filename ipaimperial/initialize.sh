mkdir -p data
if [[ ! -f data/dictionary.txt ]]; then
    wget -O data/dictionary.txt https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
fi
if [[ ! -f data/common.txt ]]; then
    wget -O data/common.txt https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt
fi
if [[ ! -e englishipa ]]; then
    git clone https://github.com/mphilli/English-to-IPA englishipa
fi

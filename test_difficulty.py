from utils import get_word_difficulty
from collections import OrderedDict

wordset = OrderedDict()
with open('hard_words.txt', 'r') as f:
    for word in f:
        word = word.strip()
        wordset[word] = None

# remove duplicates
with open('hard_words.txt', 'w') as f:
    for word in wordset.keys():
        f.write(f"{word}\n")

with open('hard_words_difficulty.txt', 'w') as f:
    for word in wordset.keys():
        diff = get_word_difficulty(word)
        print(f"{word} - {diff}")
        f.write(f"{word}: {diff}\n")

from utils import get_word_difficulty, init_mongo
from collections import OrderedDict

# wordset = OrderedDict()
# with open('easy_words.txt', 'r') as f:
#     for word in f:
#         word = word.strip()
#         wordset[word] = None

# # # remove duplicates
# # with open('easy_words.txt', 'w') as f:
# #     for word in wordset.keys():
# #         f.write(f"{word}\n")

# with open('easy_words_difficulty.txt', 'w') as f:
#     for word in wordset.keys():
#         diff = get_word_difficulty(word)
#         print(f"{word} - {diff}")
#         f.write(f"{word}: {diff}\n")


# what the distribution like
mongo = init_mongo()
easy = len(list(mongo.spellingo.words_us.find({'difficulty': 'easy'})))
medium = len(list(mongo.spellingo.words_us.find({'difficulty': 'medium'})))
hard = len(list(mongo.spellingo.words_us.find({'difficulty': 'hard'})))

print(easy, medium, hard)

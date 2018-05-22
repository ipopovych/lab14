import time
import sys
from numpy import random
from linkedbst import LinkedBST

QUANTITY = 10000

with open('english-words/words_alpha.txt') as word_file:
    words = list(word_file.read().split())

words = words[:len(words)//5]
SEEKING = random.choice(words, QUANTITY)
print('Initial dictionary contains {} words\n'.format(len(words)))

print('Searching in ordered list...')
found = 0
start = time.time()
for word in SEEKING:
    if word in words:
        found += 1
t = time.time() - start
print('Found {} words, time {}\n'.format(found, t))

# Shuffling words in dictionary
random.shuffle(words)

# Building a word tree
word_tree = LinkedBST()
for word in words:
    word_tree.add(word)


print('Searching in words tree...')
found = 0
start = time.time()
for word in SEEKING:
    if word_tree.find(word):
        found += 1
t = time.time() - start
print('Found {} words, time: {}\n'.format(found, t))


sys.setrecursionlimit(10000)
word_tree.rebalance()
print('Searching in rebalanced words tree...')
found = 0
start = time.time()
for word in SEEKING:
    if word_tree.find(word):
        found += 1
t = time.time() - start
print('Found {} words, time: {}\n'.format(found, t))













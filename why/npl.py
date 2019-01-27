"""
NPL functions and conversational
stuff
"""

import re
import random

# Load words
words_negative = {}
words_positive = {}

def read_words(file, target):
    with open(file, "r") as f:
        for line in f.readlines():
            if line[0] == ";":
                continue
            line = line.strip()
            if len(line) > 0:
                target[line] = True
read_words("./why/words/negative-words.txt", words_negative)
read_words("./why/words/positive-words.txt", words_positive)

def score(sentence):
    words = sentence.split(" ")
    score = 0
    regexp = re.compile("[^a-z]")
    for word in words:
        word = regexp.sub("", word.lower())
        if word in words_positive:
            score += 1
        elif word in words_negative:
            score -= 1
    return score / len(words)

def reply(sentence):
    if score(sentence) < -0.3:
        return random.choice([
            "Oh, sorry to hear that.",
            "Try staying positive.",
        ])
    else:
        return random.choice([
            "Okay, thanks!",
            "Great!",
        ])

import re
from collections import Counter
import numpy as np
import pandas as pd

# removing unnecessary columns and converting them to lowercase words and then into a list
def process_data(file_name):
    # file = pd.read_csv(file_name)
    # file = file.drop(columns=["pos_tag"])
    # words = file['word'].tolist()
    # # new_words = set(words)
    # return words
    file = open(file_name, 'r', encoding="utf-8")
    text_content = file.read()
    text_content = text_content.lower()
    words = re.findall(r'\w+',text_content)
    return words


    
words = process_data("./eng_corpus.txt")
vocab = set(words)

#creating a word frequency dictionary
def get_count(word_list):
    word_count_dict = {}
    word_count_dict = Counter(word_list)
    return word_count_dict


word_count_dict = get_count(words)
print(f"There are {len(word_count_dict)} key values pairs")
print(f"The count for the word 'school' is {word_count_dict.get('school',0)}")



#word probability
def get_probs(word_count_dict):
    probs = {}
    total = sum(word_count_dict.values())
    for (word,count) in word_count_dict.items():
        (word, prob) = word, count/total
        probs[word] = prob
    return probs


probs = get_probs(word_count_dict)
print(f'Length of probs dictionary is {len(probs)}')
print(f"Probability of the word 'school' is {probs['school'] :.4f}")


# String Manipulations:
# 1. Delete a letter
# 1. Switch letters
# 1. Replace a letter
# 1. Insert a letter


def delete_letter(word, verbose = False):
    split_l = [(word[:i],word[i:]) for i in range(len(word)+1)]
    delete_l = [L+R[1:] for L,R in split_l if R]

    if verbose:
        print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l


# delete_word_l = delete_letter(word = "water",verbose = True)


def switch_letter(word, verbose = False):
    split_l = [(word[:i],word[i:]) for i in range(len(word)+1)]
    switch_l = [L+R[1]+R[0]+R[2:] for L,R in split_l if len(R)>=2]
    if verbose:
        print(f"input word {word}, \nsplit_l = {split_l}, \nswitch_l = {switch_l}")
    return switch_l

# switch_word_l = switch_letter(word = "water",verbose = True)
    

def replace_letter(word, verbose = False):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    split_l = [(word[:i],word[i:]) for i in range(len(word))]
    replace_l = [L+c+R[1:] for L,R in split_l for c in letters if c != R[0]]

    replace_l = sorted(replace_l)
    if verbose:
        print(f"input word {word}, \nsplit_l = {split_l}, \nreplace_l = {replace_l}")
    return replace_l

# replace_l = replace_letter(word = 'can', verbose = True)


def insert_letter(word, verbose = False):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    split_l = [(word[:i],word[i:]) for i in range(len(word)+1)]
    insert_l = [L+c+R for L,R in split_l for c in letters]
    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return insert_l

# insert_l = insert_letter('at', True)
# print(f"Number of strings output by insert_letter('at') is {len(insert_l)}")


# Combining the string manipulations
# 1. Edit one letter
# 2. Edit two letters

def edit_one_letter(word, allow_switches = True):
    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set


# tmp_word = "at"
# tmp_edit_one_set = edit_one_letter(tmp_word)
# # turn this into a list to sort it, in order to view it
# tmp_edit_one_l = sorted(list(tmp_edit_one_set))

# print(f"input word {tmp_word} \nedit_one_l \n{tmp_edit_one_l}\n")
# print(f"The type of the returned object should be a set {type(tmp_edit_one_set)}")
# print(f"Number of outputs from edit_one_letter('at') is {len(edit_one_letter('at'))}")

def edit_two_letters(word, allow_switches = True):
    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(word, allow_switches=allow_switches)
            edit_two_set.update(edit_two)

    return edit_two_set

# tmp_edit_two_set = edit_two_letters("a")
# tmp_edit_two_l = sorted(list(tmp_edit_two_set))
# print(f"Number of strings with edit distance of two: {len(tmp_edit_two_l)}")
# print(f"First 10 strings {tmp_edit_two_l[:10]}")
# print(f"Last 10 strings {tmp_edit_two_l[-10:]}")
# print(f"The data type of the returned object should be a set {type(tmp_edit_two_set)}")
# print(f"Number of strings that are 2 edit distances from 'at' is {len(edit_two_letters('at'))}")


# Word suggestions

# def get_corrections(word, probs, vocab, n=2, verbose = False):
#     suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
#     n_best = [[s,probs[s]] for s in list(reversed(suggestions))]
#     if verbose: print("suggestions = ", suggestions)
#     return n_best




def get_corrections(word, probs, vocab, n=2, verbose=False):
  suggestions = [word] if word in vocab else []  # Check word in vocab first
  suggestions.extend(edit_one_letter(word).intersection(vocab))
  suggestions.extend(edit_two_letters(word).intersection(vocab))
  n_best = [[s, probs.get(s, 0)] for s in suggestions[:n]]  # Limit to n suggestions
  if verbose:
    print("suggestions = ", suggestions)
  return n_best if n_best else ["No suggestions found"]  # Handle empty suggestions

# Test your implementation - feel free to try other words in my word
my_word = 'smoot' 
tmp_corrections = get_corrections(my_word, probs, vocab, 2, verbose=False)
for i, word_prob in enumerate(tmp_corrections):
    print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")

print("school" in vocab)
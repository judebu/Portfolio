#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:27:17 2023

"""

import math


# class name
class TextModel:

    # constructor
    def __init__(self, model_name):
        """ constructor method that constructs a new TextModel object by
            accepting a string model_name as a parameter with the attributes of
            name, words, and word_lengths
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.p_frequency = 0

    def __repr__(self):
        """ returns a string that includes the name of the model as well as
            the sizes of the dictionaries for each feature of the text
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of exclamation mark frequencies: ' + str(self.p_frequency) + '\n'
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """

        # for the init method to update our special case
        self.p_frequency = p_frequency(s)

        # cleans the text
        word_list = clean_text(s)
        sentence_list = []
        current_sentence = ""

        for word in s:
            current_sentence += word
            if word in ".?!":
                sentence_list = sentence_list + [current_sentence.strip()]
                current_sentence = ""

        if current_sentence:
            sentence_list = sentence_list + [current_sentence.strip()]

        for sentence in sentence_list:
            words_in_sentence = clean_text(sentence)
            sentence_length = len(words_in_sentence)

            # Update sentence_lengths dictionary
            if sentence_length in self.sentence_lengths:
                self.sentence_lengths[sentence_length] += 1
            else:
                self.sentence_lengths[sentence_length] = 1

        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1

            length_word = len(w)
            if length_word in self.word_lengths:
                self.word_lengths[length_word] += 1
            else:
                self.word_lengths[length_word] = 1

            stem_result = stem(w)
            if stem_result in self.stems:
                self.stems[stem_result] += 1
            else:
                self.stems[stem_result] = 1


    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the
            model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')

        self.add_string(str(filename))
        f.close()

    def save_model(self):
        """ saves the TextModel object self by writing its various feature
            dictionaries to files
        """
        w_filename = self.name + '_' + 'JKR_words'
        f = open(w_filename, 'w')
        f.write(str(self.words))

        len_filename = self.name + '_' + 'JKR_word_lengths'
        f_diff = open(len_filename, 'w')
        f_diff.write(str(self.word_lengths))

        stem_filename = self.name + '_' + 'JKR_stems'
        f_stem = open(stem_filename, 'w')
        f_stem.write(str(self.stems))

        sentence_filename = self.name + '_' + 'JKR_sentence_lengths'
        f_sentence = open(sentence_filename, 'w')
        f_sentence.write(str(self.sentence_lengths))

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from
            their files and assigns them to the attributes of the called '
            TextModel
        """
        w_filename = self.name + '_' + 'JKR_words'
        f = open(w_filename, 'r')
        d_w = f.read()
        self.words = eval(d_w)

        len_filename = self.name + '_' + 'JKR_word_lengths'
        f_diff = open(len_filename, 'r')
        d_l = f_diff.read()
        self.word_lengths = eval(d_l)

        stem_filename = self.name + '_' + 'JKR_stems'
        f_stem = open(stem_filename, 'r')
        d_s = f_stem.read()
        self.stems = eval(d_s)

        sentence_filename = self.name + '_' + 'JKR_sentence_lengths'
        f_sentence = open(sentence_filename, 'r')
        d_sentence = f_sentence.read()
        self.sentence_lengths = eval(d_sentence)

    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the
        		similarity of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        stem_score = compare_dictionaries(other.stems, self.stems)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        exclamation_point_score = p_frequency(other.name)

        score = [word_score, word_lengths_score, stem_score, sentence_lengths_score, exclamation_point_score]

        return score

    def classify(self, source1, source2):
        """ that compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2)
        		and determines which of these other TextModels is the more likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))
        score_for_source1 = 0
        score_for_source2 = 0

        for x in scores1:
            for y in scores2:
                if x == y:
                    score_for_source1 += 1
                    score_for_source2 += 1
                if x > y:
                    score_for_source1 += 1
                if x < y:
                    score_for_source2 = score_for_source2 + 1
        if score_for_source1 > score_for_source2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        elif score_for_source1 < score_for_source2:
            print(self.name + ' is more likely to have come from ' + source2.name)


def clean_text(txt):
    """ this is a helper function
        takes a string of text txt as a parameter and returns a list c
        ontaining the words in txt after all punctuation is removed
    """
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol, '')
        txt_new = txt.lower()
        words = txt_new.split()
    return words


def stem(s):
    """accepts a string as a parameter and then returns the stem of s which
        gets rid of prefixes and suffixes
    """

    # checks for plural and removes the 's' so that it can run through the other endings
    is_plural = False
    result = ''
    if s[-1] == 's':
        is_plural = True
        s = s[:-1]

    if s[-3:] == 'ing' and s[-4] != s[-5]:
        result = s[:-3]
    elif s[-3:] == 'ing' and s[-4] == s[-5]:
        result = s[:-4]
    elif s[-2:] == 'es':
        result = s[:-2]
    elif s[-3:] == 'ier':
        result = s[:-3]
        if result == 'part':
            result += 'i'
    elif s[-1] == 'e' and len(s) >= 3:
        result = s[:-1]
    elif s[-1] == 'y':
        result = s[:-1] + 'i'
    elif s[-4:] == 'able':
        result = s[:-4]
    else:
        result = s
    return result


def compare_dictionaries(d1, d2):
    """ takes two feature dictionaries d1 and d2 as inputs, and it should compute
    	and return their log similarity score
    """
    if d1 == {}:
        return -50

    score = 0
    total_d1 = 0

    for i in d1.values():
        total_d1 += i

    if total_d1 == 0:
        return total_d1
    for i in d2:
        if i in d1:
            probability = d1[i] / total_d1
            score += math.log(probability) * d2[i]
        else:
            default_probability = 0.5 / total_d1
            score += math.log(default_probability) * d2[i]

    return score


def p_frequency(s):
    """ returns the count of how many exclamation marks '(!)' there are in the dictionary
    """
    count = 0
    for i in s:
        if i == '!':
            count += 1

    return count


# test function
def test():
    """ Tests source1 and source2 strings
      with above functions"""
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


# test 2
def run_tests():
    """ Compares 4 texts with source 1 and source 2
     and returns which text is more likely to be from where"""
    source1 = TextModel('rowling')
    source1.add_file('rowling_source_text.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('shakespeare_source_text.txt')

    new1 = TextModel('wr100')
    new1.add_file('wr100_source_text.txt')
    new1.classify(source1, source2)

    new2 = TextModel('Hitchcock')
    new2.add_file('hitchcock.txt')
    new2.classify(source1, source2)

    new3 = TextModel("Avatar")
    new3.add_file('avatar.txt')
    new3.classify(source1, source2)

    new4 = TextModel('Percy Jackson')
    new4.add_file('percyjackson.txt')
    new4.classify(source1, source2)
#
# model = TextModel('A. Poor Righter')
# model.add_string('We took CS 111. We learned CS. We conquered.')
# model.sentence_lengths

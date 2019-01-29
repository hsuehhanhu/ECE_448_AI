from math import log
import copy
# viterbi.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Renxuan Wang (renxuan2@illinois.edu) on 10/18/2018

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

'''
TODO: implement the baseline algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences, each sentence is a list of (word,tag) pairs.
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''
def baseline(train, test):
    predicts = []
    type = {}
    type['DET'] = {}
    type['NOUN'] = {}
    type['VERB'] = {}
    type['ADJ'] = {}
    type['ADP'] = {}
    type['.'] = {}
    type['ADV'] = {}
    type['CONJ'] = {}
    type['PRT'] = {}
    type['PRON'] = {}
    type['NUM'] = {}
    type['X'] = {}
    type_list = ['DET','NOUN','VERB','ADJ','ADP','.', 'ADV', 'CONJ', 'PRT','PRON','NUM','X']
    # j[1] gives the type of the word
    # j[0] gives the word
    type_check = 0
    word_type = ''
    sentence_list = []

    for i in train:
        for j in i:
            if type[j[1]].get(j[0],0) == 0:
                type[j[1]][j[0]] = 1
            else:
                type[j[1]][j[0]] = 1 + type[j[1]][j[0]]

    #test[i] gives the sentence
    #test[i][j] gives the word
    for count,sentence in enumerate(test):
        sentence_list = []
        for word in sentence:
            type_check = 0
            for j in type_list:
                if (type[j].get(word,0) > type_check):
                    word_type = j
                    type_check = type[j].get(word,0)
            word_out = (word,word_type)
            sentence_list.append(word_out)
        predicts.append(sentence_list)

    return predicts

'''
TODO: implement the Viterbi algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences with tags on the words
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''
def viterbi(train, test):
    predicts = []
    # type = {}
    # type['DET'] = {}
    # type['NOUN'] = {}
    # type['VERB'] = {}
    # type['ADJ'] = {}
    # type['ADP'] = {}
    # type['.'] = {}
    # type['ADV'] = {}
    # type['CONJ'] = {}
    # type['PRT'] = {}
    # type['PRON'] = {}
    # type['NUM'] = {}
    # type['X'] = {}
    type_list = ['DET','NOUN','VERB','ADJ','ADP','.', 'ADV', 'CONJ', 'PRT','PRON','NUM','X']
    # j[1] gives the type of the word
    # j[0] gives the word
    type_check = 0
    word_type = ''
    sentence_list = []

    initialCount = 0
    transitionCount = 0
    emissionCount = 0

    tranProb = {}
    tranProb['DET'] = {}
    tranProb['NOUN'] = {}
    tranProb['VERB'] = {}
    tranProb['ADJ'] = {}
    tranProb['ADP'] = {}
    tranProb['.'] = {}
    tranProb['ADV'] = {}
    tranProb['CONJ'] = {}
    tranProb['PRT'] = {}
    tranProb['PRON'] = {}
    tranProb['NUM'] = {}
    tranProb['X'] = {}
    initProb = {}
    emitProb = {}
    emitProb['DET'] = {}
    emitProb['NOUN'] = {}
    emitProb['VERB'] = {}
    emitProb['ADJ'] = {}
    emitProb['ADP'] = {}
    emitProb['.'] = {}
    emitProb['ADV'] = {}
    emitProb['CONJ'] = {}
    emitProb['PRT'] = {}
    emitProb['PRON'] = {}
    emitProb['NUM'] = {}
    emitProb['X'] = {}

    for i in train:
        prev_tag = ''
        for j_id,j in enumerate(i):
            if j_id == 0:
                try:
                    initProb[j[1]] += 1
                except KeyError:
                    initProb[j[1]] = 1
                initialCount += 1
            else:
                try:
                    tranProb[(prev_tag, j[1])] += 1
                except KeyError:
                    tranProb[(prev_tag, j[1])] = 1
                transitionCount += 1
            prev_tag = j[1]
            try:
                emitProb[j[1]][j[0]] += 1
            except KeyError:
                emitProb[j[1]][j[0]] = 1
            emissionCount += 1

    def getInitProb(tag, smoothing_parameter=0.00005):
        return (initProb.get(tag,0)+smoothing_parameter)/(initialCount+emissionCount*smoothing_parameter)


    def getTranProb(prev, curr, smoothing_parameter=0.00005):
        return (tranProb.get((prev,curr),0)+smoothing_parameter)/(transitionCount+emissionCount*smoothing_parameter)


    def getEmitProb(tag, word, smoothing_parameter=0.00005):
        # print(tag, word)
        return (emitProb[tag].get(word,0)+smoothing_parameter)/(emissionCount+emissionCount*smoothing_parameter)


    for sentence in test:
        sentence_list = []
        prev_row = None
        flag = 0
        for word_id, word in enumerate(sentence):
            flag = 1
            row = []
            if word_id == 0:
                for j in type_list:
                    prob = log(getInitProb(j) * getEmitProb(j, word))
                    path = [j]
                    row.append((j,prob,path))
                prev_row = row
            else:
                for j in type_list:
                    prior_path = prev_row[0][2]
                    prior_prob = prev_row[0][1] + log(getTranProb(prev_row[0][0],j))
                    for i in prev_row:
                        curr_prob = log(getTranProb(i[0], j)) + i[1]
                        if curr_prob > prior_prob:
                            prior_prob = curr_prob
                            prior_path = i[2]
                    path = copy.deepcopy(prior_path)
                    path.append(j)
                    prob = prior_prob + log(getEmitProb(j,word))
                    row.append((j,prob,path))
                prev_row = row
        if flag:
            best_path = prev_row[0][2]
            best_prob = prev_row[0][1]
            for i in prev_row:
                if i[1] > best_prob:
                    best_prob = i[1]
                    best_path = i[2]
            for word_id, word in enumerate(sentence):
                word_out = (word, best_path[word_id])
                sentence_list.append(word_out)
            predicts.append(sentence_list)
        else:
            predicts.append([])





    #
    #
    #
    # for count,sentence in enumerate(test):
    #     sentence_list = []
    #     prev_tag = ''
    #     for word_id, word in enumerate(sentence):
    #         type_check = 0
    #         word_type = ''
    #         if word_id == 0:
    #             for j in type_list:
    #                 if initProb[j] * emitProb[j].get(word,0) > type_check:
    #                     word_type = j
    #                     type_check = initProb[j] * emitProb[j].get(word,0)
    #         else:
    #             for j in type_list:
    #                 if tranProb.get((prev_tag,j),0) * emitProb[j].get(word,0) > type_check:
    #                     word_type = j
    #                     type_check = tranProb.get((prev_tag,j),0) * emitProb[j].get(word,0)
    #         prev_tag = word_type
    #         word_out = (word,word_type)
    #         sentence_list.append(word_out)
    #     predicts.append(sentence_list)
    return predicts





    #Initial probability: check first tag of each sentence
    #Transition probability: while going through sentence, keep copy of current tag, move to next one
    #Emission probability How often does tag t yield word w?



    return predicts

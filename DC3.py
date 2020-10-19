import string
import os
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk import ngrams
from operator import itemgetter
import math
path = 'DC3/'
files = []

# r = root, d = directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

random.shuffle(files)

country_data = []
electronic_data = []
folk_data = []
hiphop_data = []
indie_data = []
jazz_data = []
metal_data = []
pop_data = []
rb_data = []
rock_data = []

for file in files:
    with open(file, 'r') as f:
        readFile = ""
        for line in f:
            readLine = f.readline()
            readLine = 'newline ' + readLine + ' endline '
            readFile = readFile + readLine
        f.close()
        tokens = word_tokenize(readFile)

        if 'Country' in file:
            country_data.extend(tokens)
        elif 'Electronic' in file:
            electronic_data.extend(tokens)
        elif 'Folk' in file:
            folk_data.extend(tokens)
        elif 'Hiphop' in file:
            hiphop_data.extend(tokens)
        elif 'Indie' in file:
            indie_data.extend(tokens)
        elif 'Jazz' in file:
            jazz_data.extend(tokens)
        elif 'Metal' in file:
            metal_data.extend(tokens)
        elif 'Pop' in file:
            pop_data.extend(tokens)
        elif 'R&B' in file:
            rb_data.extend(tokens)
        elif 'Rock' in file:
            rock_data.extend(tokens)

genre_list = []
done = 'false'
genre = input("Enter a Genre: ")
while(done == 'false'):
    if(genre.lower() == "country"):
        genre_list = country_data
        done = 'true'
    elif(genre.lower() == "electronic"):
        genre_list = electronic_data
        done = 'true'
    elif(genre.lower() == "folk"):
        genre_list = folk_data
        done = 'true'
    elif(genre.lower() == "hiphop"):
        genre_list = hiphop_data
        done = 'true'
    elif(genre.lower() == "indie"):
        genre_list = indie_data
        done = 'true'
    elif(genre.lower() == "jazz"):
        genre_list = jazz_data
        done = 'true'
    elif(genre.lower() == "metal"):
        genre_list = metal_data
        done = 'true'
    elif(genre.lower() == "pop"):
        genre_list = pop_data
        done = 'true'
    elif(genre.lower() == "r&b"):
        genre_list = rb_data
        done = 'true'
    elif(genre.lower() == "rock"):
        genre_list = rock_data
        done = 'true'
    else:
        genre = input("You have entered an invalid genre. Please enter a new genre: ")

unigram = dict()
unigram_list = []
for word in genre_list:
    if word in unigram:
        unigram[word] += 1
    else:
        unigram[word] = 1
'''for key,value in unigram.items():
    temp = [key,value]
    unigram_list.append(temp)'''
# print(unigram)

bigram = dict()
bigram_list = []
for i in range(len(genre_list)-1):
    key = (genre_list[i], genre_list[i+1])
    if key in bigram:
        bigram[key] += 1
    else:
        bigram[key] = 1
for key, value in bigram.items():
    temp = [key, value]
    bigram_list.append(temp)
# print(bigram_list)


def getBigramNextWord(word):
    pair_list = [pair for pair in bigram_list if pair[0][0] == word]
    prob_grams = []

    for pair in pair_list:
        prob = float(pair[1] / unigram[word])
        tagged_gram = [pair, prob]
        prob_grams.append(tagged_gram)

    prob_grams = sorted(prob_grams, key=itemgetter(1), reverse=True)
    # print(prob_grams)
    if (len(prob_grams) > 20):
        length = math.ceil(len(prob_grams) * 0.1)
        prob_grams = prob_grams[:length]
    choice = random.choice(prob_grams)
    return choice[0][0][1]
    '''total = sum(gram[0][1] for gram in prob_grams)
    r = random.uniform(1, total)
    for gram in prob_grams:
        r -= gram[0][1]
        if r <= 0:
            return gram[0][0][1]'''

    '''total = sum(pair[1] for pair in pair_list)
    r = random.uniform(1, total)
    for pair in pair_list:
        r -= pair[1]
        if r <= 0:
            return pair[0][1]'''

def getBigram(word, n = 100):
    endline_count = 0
    for i in range(n):
        # print out nothing if its the end of the line
        if endline_count != 6:
            if word == "endline":
                endline_count = endline_count + 1
                print()
            # if the word is an apostrophe or such
            elif "'" in word or "," in word or "." in word or "?" in word or "!" in word or ":" in word:
              print(word, end="")
            elif word == "(" or word == ")" or word == '``':
                pass
            elif word != "newline":
              print(" " + word, end="")
        word = getBigramNextWord(word)


def getStartWord():
    word_list = [pair[0][1] for pair in bigram_list if pair[0][0] == 'newline' and pair[1] > 10]
    # print(word_list)
    r = int(random.uniform(0, len(word_list)))
    return word_list[r]



ngram = dict()
ngram_list = []
n = 3
for i in range(len(genre_list)-(n-1)):
    key = tuple(genre_list[i:i+n])
    if key in ngram:
        ngram[key] += 1
    else:
        ngram[key] = 1
for key, value in ngram.items():
    temp = [key, value]
    ngram_list.append(temp)
# print(ngram_list)

def getNgramNextWord(pair):
    gram_list = [gram for gram in ngram_list if gram[0][0] == pair[0][0] and gram[0][1] == pair[0][1]]
    #pair_list = [pair for pair in bigram_list if pair[0] == pair]
    # pair_count = pair[1]
    prob_grams = []
    for gram in gram_list:
        # pair_count = 0
        '''for pair in pair_list:
            if pair[0][0] == gram[0][0] and pair[0][1] == gram[0][1]:
                pair_count += pair[1]'''
        prob = float(gram[1] / pair[1])
        tagged_gram = [gram, prob]
        prob_grams.append(tagged_gram)
    # sort prob_grams
    # cut it at the top 10%
    prob_grams = sorted(prob_grams, key = itemgetter(1), reverse = True)
    # print(prob_grams)
    if(len(prob_grams) > 20):
        length = math.ceil(len(prob_grams) * 0.1)
        prob_grams = prob_grams[:length]
    choice = random.choice(prob_grams)
    # print(choice)
    return choice[0][0][2]
    '''total = sum(gram[0][1] for gram in prob_grams)
    r = random.uniform(1, total)
    for gram in prob_grams:
        r -= gram[0][1]
        if r <= 0:
            return gram[0][0][1]'''

def getNgram(pair, n = 100):
    #print(pair)
    endline_count = 0
    for i in range(n):
        word = pair[0][0]
        #print(word)
        # print out nothing if its the end of the line
        if endline_count != 6:
            if word == "endline":
                endline_count = endline_count + 1
                print()
            # if the word is an apostrophe or such
            elif "'" in word or "," in word or "." in word or "?" in word or "!" in word or ":" in word:
              print(word, end="")
            elif word == "(" or word == ")" or word == '``':
                pass
            elif word != "newline":
              print(" " + word, end="")

        word = getNgramNextWord(pair)
        #print(word)
        for element in bigram_list:
            if element[0][0] == pair[0][1] and element[0][1] == word:
                pair = element
        #print(pair)


def getStartPair():
    word_list = [pair for pair in bigram_list if pair[0][0] == 'newline' and pair[1] > 10]
    # print(word_list)
    r = int(random.uniform(0, len(word_list)))
    return word_list[r]

print()
print("Bigram Generated Lyrics: ")
print()
getBigram(getStartWord())
print()

print("Trigram Generated Lyrics: ")
print()
getNgram(getStartPair())
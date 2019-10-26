import nltk
from nltk.corpus import cmudict

prondict = cmudict.dict()

def parseStressOfLine(line):

    stress=""
    stress_no_punct=""

    tokens = [words.lower() for words in nltk.word_tokenize(line)]
    for word in tokens:

        word_punct =  strip_punctuation_stressed(word.lower())
        word = word_punct['word']
        punct = word_punct['punct']

        #print word

        if word not in prondict:
            # if word is not in dictionary
            # add it to the string that includes punctuation
            stress= stress+"*"+word+"*"
        else:
            zero_bool=True
            for s in prondict[word]:
                # oppose the cmudict bias toward 1
                # search for a zero in array returned from prondict
                # if it exists use it
                # print strip_letters(s),word
                if strip_letters(s)=="0":
                    stress = stress + "0"
                    stress_no_punct = stress_no_punct + "0"
                    zero_bool=False
                    break

            if zero_bool:
                stress = stress + strip_letters(prondict[word][0])
                stress_no_punct=stress_no_punct + strip_letters(prondict[word][0])

        if len(punct)>0:
            stress= stress+"*"+punct+"*"

    return {'stress':stress,'stress_no_punct':stress_no_punct}

def parseRhymeOfLine(line):

    rhyme=""
    rhyme_no_punct=""

    tokens = [words.lower() for words in nltk.word_tokenize(line)]
    for word in tokens:

        word_punct =  strip_punctuation_stressed(word.lower())
        word = word_punct['word']
        punct = word_punct['punct']

        #print word

        if word not in prondict:
            # if word is not in dictionary
            # add it to the string that includes punctuation
            rhyme= rhyme+"*"+word+"*"
        else:
            zero_bool=True
            for s in prondict[word]:
                r = strip_numbers(s)
                rhyme = rhyme + r
                rhyme_no_punct = rhyme_no_punct + r
                zero_bool=False
                break

            if zero_bool:
                rhyme = rhyme + strip_numbers(prondict[word][0])
                rhyme_no_punct=rhyme_no_punct + strip_numbers(prondict[word][0])

        if len(punct)>0:
            rhyme= rhyme+"*"+punct+"*"

    return {'rhyme':rhyme,'rhyme_no_punct':rhyme_no_punct}

def rhyme_of_word(word):
    word.lower()
    if word not in prondict:
        return None
    rhyme = strip_numbers(prondict[word][0])
    return rhyme



# STRIP PUNCTUATION but keep it
def strip_punctuation_stressed(word):
    # define punctuations
    punctuations = '!()-[]{};:"\,<>./?@#$%^&*_~'
    my_str = word

    # remove punctuations from the string
    no_punct = ""
    punct=""
    for char in my_str:
        if char not in punctuations:
            no_punct = no_punct + char
        else:
            punct = punct+char

    return {'word':no_punct,'punct':punct}


# CONVERT the cmudict prondict into just numbers
def strip_letters(ls):
    #print "strip_letters"
    nm = ''
    for ws in ls:
        #print "ws",ws
        for ch in list(ws):
            #print "ch",ch
            if ch.isdigit():
                nm=nm+ch
                #print "ad to nm",nm, type(nm)
    return nm

def strip_numbers(ls):
    #print "strip_letters"
    nm = ''
    for ws in ls:
        #print "ws",ws
        for ch in list(ws):
            #print "ch",ch
            if not ch.isdigit():
                nm=nm+ch
                #print "ad to nm",nm, type(nm)
    return nm
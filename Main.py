import SyllabicStress
import nltk
import re


original_text = []




class PoetFiller:

    # Todo: make syllables an array that can varry over line number
    def __init__(self, syllables_per_line=10, rhyme_scheme='abba', meter=None):
        self.syllables_per_line = syllables_per_line
        self.rhyme_scheme = rhyme_scheme
        self.meter = meter


    #returns 2d array of lines and the lines split on missing information
    def find_gaps(self, text):
        #split into lines
        lines = re.split(r"( *|\/)*\n", text)
        #split where there is missing information
        gaps = []
        for line in lines:
            gaps.append([x for x in re.split(r" *\.\.\.\.* *", line)])
        return gaps

    def fill_gaps(self, text):
        lines = self.find_gaps(text)
        for line in lines:
            # TODO: if last entry doesn't fit rhyme scheme fix here and append to line
            # also see if necessary to prepend ever
            # assume evenly distribute remaining syllables over sentence. Maybe this could be random?
            num_syllables = (self.syllables_per_line - self.count_syllables(line)) / (len(line) - 1)
            for i in range(len(line) - 1):
                self.bridge_gap(line[i], line[i+1], num_syllables)

    def count_syllables(self, line):
        #line is a list of phrases where there are assumed to be missing words between entries
        syllables = 0
        words = nltk.word_tokenize("".join(line))
        for word in words:
            stresses = SyllabicStress.parseStressOfLine(word)['stress_no_punct']
            syllables+= len(stresses)
        return syllables

    def bridge_gap(self, phrase1, phrase2, syllables):
        return phrase1 + phrase2


test = "this is a sentence"

filler = PoetFiller()
print(filler.count_syllables(test))
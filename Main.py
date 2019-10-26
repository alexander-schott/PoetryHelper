import SyllabicStress
import NgramPredictor
import nltk
import re

sample = nltk.corpus.gutenberg.raw('whitman-leaves.txt')

original_text = []




class PoetFiller:

    # Todo: make syllables an array that can varry over line number
    def __init__(self, syllables_per_line=10, rhyme_scheme='abba', meter=None, rhyme_length=2):
        self.syllables_per_line = syllables_per_line
        self.rhyme_scheme = rhyme_scheme
        self.meter = meter
        self.rhyme_length = rhyme_length

        self.predictor = NgramPredictor.BidirectionalPredictor()
        self.predictor.fit(sample)

    def fill_poem(self,text):
        gaps = self.find_gaps(text)
        gaps = self.missing_rhymes(gaps)
        gaps = self.fill_rhymes(gaps)
        gaps = self.fill_gaps(gaps)
        filled = [line + '\n' for line in gaps]
        return filled

    #returns 2d array of lines and the lines split on missing information
    def find_gaps(self, text):
        #split into lines
        lines = re.split(r"( *|\/)*\n", text)
        #split where there is missing information
        gaps = []
        for line in lines:
            finshes = True
            if re.match(r" *\.\.\.\.* *$", line):
                finishes = False
            gaps.append([x for x in re.split(r" *\.\.\.\.* *", line)])
            gaps[-1].append(["..."])
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
        while syllables > 0:
            new_word = self.predictor.generate_forward(phrase1)
            phrase1 = phrase1 + new_word
            syllables = syllables - self.count_syllables(new_word)
            if syllables > 0:
                new_word = self.predictor.generate_forward(phrase2)
                phrase2 = new_word + phrase2
                syllables = syllables - self.count_syllables(new_word)

        return phrase1 + phrase2

    #lines is a 2d array of lines and phrases
    def missing_rhymes(self, lines):
        #for each rhyme type ending (#syllables for longest line of type, that lines line number, the rhyme)
        rhyme_model = [(0, -1, "") for i in range(len(self.rhyme_scheme))]
        for i in range(len(lines)):
            if lines[-1][-1] != "...":
                # l corresponds to line of given stanza in rhyme scheme
                stanza_line = i % len(self.rhyme_scheme)
                syllables = self.count_syllables(lines[i])
                if syllables >= rhyme_model[stanza_line][0]:
                    rhyme = self.get_rhyme(lines[i])
                    rhyme_model[stanza_line][0] = syllables
                    rhyme_model[stanza_line][1] = i
                    #rhyme_model[stanza_line][2] = rhyme

        for i in range(len(lines)):
            if lines[i][-1] != "...":
                stanza_line = i % len(self.rhyme_scheme)
                if rhyme_model[stanza_line][1] != i:
                    line1 = lines[i]
                    line2 = lines[rhyme_model[stanza_line][1]]
                    if not self.does_rhyme(line1, line2):
                        lines[i].append("...")
        return lines, rhyme_model

    def get_rhyme(self, line):
        last_word = SyllabicStress.rhyme_of_word(nltk.word_tokenize(line[-1])[-1])
        return last_word

    def does_rhyme(self, line1, line2):
        similarity = self.rhyme_similarity(line1, line2)
        return similarity >= self.rhyme_length

    def rhyme_similarity(self,line1, line2):
        rhyme1 = self.get_rhyme(line1)
        rhyme2 = self.get_rhyme(line2)
        similarity = 0
        for i in range(min(len(rhyme1), len(rhyme2))):
            if rhyme1[len(rhyme1) - 1 - i] != rhyme2[len(rhyme2) - 1 - i]:
                return similarity
            similarity += 1
        return similarity



    # lines is a 2d array of lines and phrases
    def fill_rhymes(self, lines):
        pass



test = "this is a sentence"

filler = PoetFiller()
print(filler.get_rhyme("hello"))
print(filler.get_rhyme("please"))
print(filler.get_rhyme("rhyme"))
print(filler.get_rhyme("and"))

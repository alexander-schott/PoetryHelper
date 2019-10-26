import SyllabicStress
import NgramPredictor
import nltk
import re

sample = nltk.corpus.gutenberg.raw('whitman-leaves.txt')

original_text = []


f = open("input.txt", "r+")
contents = f.read()
print(contents)


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
        gaps, rhyme_model = self.missing_rhymes(gaps)
        gaps = self.fill_rhymes(gaps, rhyme_model)
        gaps = self.fill_gaps(gaps)
        filled = [line + '\n' for line in gaps]
        return filled

    #returns 2d array of lines and the lines split on missing information
    def find_gaps(self, text):
        #split into lines
        lines = re.split(r"( *|\/)*\n", text)
        for line in lines:
            if line == '':
                lines.remove('')

        print(lines)
        #split where there is missing information
        gaps = []
        for line in lines:
            finishes = True
            if re.match(r" *\.\.\.\.* *$", line):
                finishes = False
            gaps.append([x for x in re.split(r" *\.\.\.\.* *", line)])
            if not finishes:
                gaps[-1].append("...")
        return gaps

    def fill_gaps(self, lines):
        filled = []
        for line in lines:
            # TODO: if last entry doesn't fit rhyme scheme fix here and append to line
            # also see if necessary to prepend ever
            # assume evenly distribute remaining syllables over sentence. Maybe this could be random?
            if len(line) == 0:
                #if line is totally blank
                line = [self.predictor.generate_forward() for i in range(2)]
            if len(line) < 2:
                #if there is no gap to be filled
                continue
            num_syllables = (self.syllables_per_line - self.count_syllables(line)) / (len(line) - 1)
            result = ""
            for i in range(len(line) - 1):
                result += self.bridge_gap(line[i], line[i+1], num_syllables)
            filled.append(result)
        return filled

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
            phrase1 = phrase1 + " " + new_word
            syllables = syllables - self.count_syllables(new_word)
            if syllables > 0:
                new_word = self.predictor.generate_forward(phrase2)
                phrase2 = new_word + " " + phrase2
                syllables = syllables - self.count_syllables(new_word)

        return phrase1 + phrase2

    #lines is a 2d array of lines and phrases
    def missing_rhymes(self, lines):
        #for each rhyme type ending (#syllables for longest line of type, that lines line number, the rhyme)
        #rhyme_model = [[0, -1] for i in range(len(self.rhyme_scheme))]
        rhyme_model = {}
        for c in self.rhyme_scheme:
            rhyme_model[c] = [0, -1]

        for i in range(len(lines)):
            if lines[-1][-1] != "...":
                # l corresponds to line of given stanza in rhyme scheme
                stanza_line = i % len(self.rhyme_scheme)
                rhyme_type = self.rhyme_scheme[stanza_line]
                syllables = self.count_syllables(lines[i])
                if syllables >= rhyme_model[rhyme_type][0]:
                    #rhyme = self.get_rhyme(lines[i])
                    rhyme_model[rhyme_type][0] = syllables
                    rhyme_model[rhyme_type][1] = i
                    #rhyme_model[stanza_line][2] = rhyme

        for i in range(len(lines)):
            if lines[i][-1] != "...":
                stanza_line = i % len(self.rhyme_scheme)
                rhyme_type = self.rhyme_scheme[i]
                if rhyme_model[rhyme_type][1] != i:
                    line1 = lines[i]
                    line2 = lines[rhyme_model[rhyme_type][1]]
                    if not self.does_rhyme(line1, line2):
                        lines[i].append("...")
        return lines, rhyme_model



    def get_rhyme(self, line):
        tokens = nltk.word_tokenize(line[-1])
        if len(tokens) == 0:
            return ""
        last_word = tokens[-1]
        return SyllabicStress.rhyme_of_word(last_word)

    def does_rhyme(self, line1, line2):
        similarity = self.rhyme_similarity(line1, line2)
        return similarity >= self.rhyme_length

    def rhyme_similarity(self,line1, line2):
        rhyme1 = self.get_rhyme(line1)
        rhyme2 = self.get_rhyme(line2)
        similarity = 0
        if rhyme1 == None or rhyme2 == None:
            return False
        for i in range(min(len(rhyme1), len(rhyme2))):
            if rhyme1[len(rhyme1) - 1 - i] != rhyme2[len(rhyme2) - 1 - i]:
                return similarity
            similarity += 1
        return similarity



    # lines is a 2d array of lines and phrases
    def fill_rhymes(self, lines, rhyme_model):
        for i in range(len(lines)):
            stanza_line = i % len(self.rhyme_scheme)
            rhyme_type = self.rhyme_scheme[stanza_line]
            if lines[i][-1] == "...":
                archetype_line = rhyme_model[rhyme_type][1]
                possible = self.predictor.gen10_forward()
                for p in possible:
                    if self.does_rhyme(lines[i], lines[archetype_line]):
                        lines[i].pop()
                        lines[i].append[p]
                        break
                    lines[i].append('_notfound_')
        return lines










test = contents

filler = PoetFiller()
print(filler.fill_poem(test))
import pickle
import random
import re

from parrot import Utils
from parrot.Elements import Articles, Nouns, Verbs
from parrot.Element import Noun, Verb, Article

class PhraseGenerator:
    MONO = "mono"
    PRESENTE = "pres"
    IMPERFETTO = "impf"
    DICTIONARY = "allwords"
    VERBS_STATE = "verbs.state"
    NOUNS_STATE = "nouns.state"
    ARTICLES_STATE = "articles.state"
    VERBO_PRESIND = "pres"
    VERBO = "VER"
    SOSTANTIVO = "SOS"
    ARTICOLO = "DET"
    ARTICOLO_DETERMINATIVO = "def"
    ARTICOLO_INDETERMINATIVO = "indef"

    def __init__(self):
        self.nouns = None
        self.verbs = None
        self.articles = None

    def parse(self, lines):
        if lines == None:
            return None

        print "Loading state..."
        self.load_state()
        if self.articles and self.nouns and self.verbs:
            print "\tState loaded."
            return

        print "State not found: loading dictionary..."
        self.articles = Articles()
        self.nouns = Nouns()
        self.verbs = Verbs()
        for line in lines:
            list_item = self.tokenize(line.strip())
            if list_item.category == PhraseGenerator.ARTICOLO:
                self.articles.add_item(Article.from_string(list_item))
            elif list_item.category == PhraseGenerator.SOSTANTIVO:
                self.nouns.add_item(Noun.from_string(list_item))
            elif list_item.category == PhraseGenerator.VERBO and \
                (list_item.subcategory == PhraseGenerator.MONO or list_item.subcategory == PhraseGenerator.IMPERFETTO):
                self.verbs.add_item(Verb.from_string(list_item))

        print "\tDictionary loaded. Saving state..."
        try:
            pickle.dump(self.articles, open(PhraseGenerator.ARTICLES_STATE, "w"))
            pickle.dump(self.verbs, open(PhraseGenerator.VERBS_STATE, "w"))
            pickle.dump(self.nouns, open(PhraseGenerator.NOUNS_STATE, "w"))
        except IOError:
            print "\tCouldn't save state files, running with ephemeral state"

    def load_state(self):
        try:
            with open(PhraseGenerator.ARTICLES_STATE, 'r') as articles:
                self.articles = pickle.load(articles)
        except IOError:
            pass

        try:
            with open(PhraseGenerator.NOUNS_STATE, 'r') as nouns:
                self.nouns = pickle.load(nouns)
        except IOError:
            pass

        try:
            with open(PhraseGenerator.VERBS_STATE, 'r') as verbs:
                self.verbs = pickle.load(verbs)
        except IOError:
            pass

    def tokenize(self, line):
        columns = line.split(" ")
        if len(columns) < 2:
            return None

        # (category, subcategory, value)
        category = None
        subcategory = None
        if ':' in columns[0]:
             parts = columns[0].split(':')
             category = parts[0]
             subcategory = parts[1]
        else:
            category = columns[0]

        return ListItem(category, subcategory, " ".join(columns[1:]))

    def generate_phrase(self):
        while (True):
            input = raw_input("> ")

            first = str(self.nouns.get_random())
            first = first[0].upper() + first[1:]

            second_noun = self.nouns.get_random()
            articolo = self.articles.get_for_noun(second_noun)
            if articolo == None:
                print articolo, second_noun

            phrase = str(articolo) + " " + second_noun.string
            verb = self.verbs.get_third_person_singular()
            if int(random.uniform(0, 100)) % 2 == 0:
                phrase = str(articolo.get_plural_for(second_noun.plural)) + " " + second_noun.plural

            print "%s %s che %s come metafora della mia vita" % (first, phrase, verb)

class ListItem:
    def __init__(self, category, subcategory, value):
        self.category = category
        self.subcategory = subcategory
        self.value = value


def main():
    raw = []
    with open(PhraseGenerator.DICTIONARY, "r") as file:
        raw = file.readlines()

    phrasegen = PhraseGenerator()
    phrasegen.parse(raw)

    phrasegen.generate_phrase()

if __name__ == "__main__":
    main()
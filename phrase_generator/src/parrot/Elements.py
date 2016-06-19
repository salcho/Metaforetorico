import random

from parrot import Utils
from parrot.Element import Article

class Elements:
    def __init__(self):
        self.list = []

    def add_item(self, items):
        if type(items) is not list:
            items = (items,)

        for item in items:
            if Utils.doesnt_contain(self.list, item):
                self.list.append(item)

    def get_elem_for(self, value):
        for item in self.list:
            if str(item) == value:
                return item

    def count(self):
        return self.list

    def get_random(self):
        return Utils.get_random(self.list)

class Articles(Elements, object):
    def __init__(self):
        super(Articles, self).__init__()

    def add_item(self, article):
        if article is None:
            return

        super(Articles, self).add_item(article)

    def get_rnd_articolo_partitivo(self):
        return Utils.get_random(self.get_articoli_partitivi())

    def get_articoli_partitivi(self):
        return [x for x in self.list if x.string.startswith('d')]

    def get_for_noun(self, noun):
        if noun.article.startswith("la"):
                return self.get_article_for("a")
        elif noun.article.startswith("il") or noun.article.startswith("o"):
            return self.get_article_for("l")
        elif noun.article.startswith("l'"):
            return Article("dell", "dei/degli")
        elif noun.article.startswith("lo"):
            return Article("dello", "dei/degli")
        else:
            print 'wtf -> ' + str(noun)

    def get_article_for(self, criteria):
        for articolo in self.get_articoli_partitivi():
            if articolo.string.endswith(criteria):
                return articolo


class Nouns(Elements, object):
    def __init__(self):
        super(Nouns, self).__init__()

    def add_item(self, noun):
        if noun is None:
            return
        super(Nouns, self).add_item(noun)

class Verbs(Elements, object):
    def __init__(self):
        super(Verbs, self).__init__()

    def get_third_person_singular(self):
        while True:
            verb = self.get_random()
            if str(verb).endswith('a') and not str(verb).endswith('la'):
                return verb

    def add_item(self, verb):
        if verb is None:
            return

        super(Verbs, self).add_item(verb)
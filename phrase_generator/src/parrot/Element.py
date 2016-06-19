class Element:
    def __init__(self, str):
        self.string = str.lower()

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string.lower() == str(other).lower()

class Article(Element):
    def __init__(self, string, plural, isDefined):
        Element.__init__(self, string)
        self.indef = None
        self.alt_plural = None
        if '/' in plural:
            parts = plural.lower().split('/')
            self.plural = parts[0]
            self.alt_plural = parts[1]
        else:
            self.plural = plural.lower()
        self.isDefined = isDefined

    def set_indef(self, det_indef):
        if not self.indef:
            self.indef = det_indef

    def get_indef(self):
        if not self.indef:
            return None
        return self.indef

    def get_plural_for(self, word):
        # todo - fix me and add other cases
        if word.startswith('a') or word.startswith('e')  or word.startswith('i') \
            or word.startswith('o') or word.startswith('u'):
            print word
            if self.alt_plural:
                return self.alt_plural

        return self.plural

    @staticmethod
    def from_string(list_item):
        parts = list_item.value.split(" ")
        if len(parts) != 2:
            return None

        return Article(parts[0], parts[1], list_item.subcategory)


class Noun(Element):
    # (Sostantivo, Plurali, Art)
    def __init__(self, string, plural, article):
        Element.__init__(self, string)
        self.article = article.lower()
        self.plural = plural

    def __str__(self):
        return self.article + ("" if self.article.endswith("'") else " ") + self.string

    @staticmethod
    def from_string(list_item):
        parts = list_item.value.split(" ")
        if len(parts) != 3:
            return None

        # Masculin-femenin
        for part in parts[:2]:
            if '/' in parts[2] and '/' in parts[0]:
                articles = parts[2].split('/')
                nouns = parts[0].split('/')
                plurals = [parts[1], parts[1]]
                if '/' in parts[1]:
                    pl = parts[1].split('/')
                    plurals = [pl[0], pl[1]]

                ret = []
                ret.append(Noun(nouns[0], plurals[0], articles[0]))
                ret.append(Noun(nouns[1], plurals[1], articles[1]))
                return ret

        if parts[1] == '-':
            parts[1] = parts[0]
        return Noun(parts[0], parts[1], parts[2])


# LA VALENCIA: MONOVALENCIA, BIVALENCIA
# Verbo: Sujeto (Argumento) || Complemento (Argumento opcionales: Adjunto)
#        |-- 1-valente ---|     |-------- n-valente----------|
# Todos los verbos intransitivos son monovalentes (argumento -> comer(manzana)).
class Verb(Element):
    def __init__(self, string, tempo):
        Element.__init__(self, string)
        self.tempo = tempo

    @staticmethod
    def from_string(list_item):
        if list_item.value == None:
            return None

        return Verb(list_item.value, list_item.subcategory)
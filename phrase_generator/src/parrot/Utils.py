import random

def doesnt_contain(list, value):
    return len([x for x in list if x == value]) == 0

def get_random(list):
        return list[int(random.uniform(0, len(list)))]
import mmh3


def bite_array(cap=10000):
    return [0] * cap


class BloomFilter(object):
    def __init__(self, cap=1000):
        self.cap = cap
        self.bite_array = bite_array(self.cap)

    def add(self, value):
        for x in self.gen_postions(value):
            self.bite_array[x] = 1

    def gen_postions(self, value):
        seed_num = 10
        return [mmh3.hash(value, x, signed=False) % self.cap for x in range(32, 32 + seed_num)]

    def judge(self, value):
        pos = self.gen_postions(value)
        is_in = True
        for x in pos:
            if self.bite_array[x] == 0:
                is_in = False
                break
        return is_in


BF = BloomFilter()
data = ["abc", "def", "kkk", "k1", "k2", "k3"]

for x in data:
    # print(BF.bite_array)
    BF.add(x)
print(BF.judge("abc"))

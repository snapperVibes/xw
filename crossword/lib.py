class Crossword:
    def __init__(self, size):
        self._size = size


    def __getitem__(self, item):
        pass


    def __setitem__(self, key, value):
        pass

    def set_vocab(self, vocab):
        pass

    def fill_generator(self):
        yield "Solution 1"
        yield "Solution 2"
        yield "Solution 3"


BLACK = NotImplemented


def read_vocab(path):
    with open(path, "r") as f:
        return _read_vocab(line.strip().split(";") for line in f)


def _read_vocab(vocab):
    output = dict()
    for k, v in vocab:
        v = int(v)
        assert 0 <= v <= 100
        output[k.upper()] = v
    return output





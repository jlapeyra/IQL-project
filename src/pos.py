from typing import Callable, overload
from utils import split

class Pos:
    token: str
    lemma: str
    tag: str
    prob: float = None
    form: str = None

    @overload
    def __init__(self, data: str) -> None: ...
    
    @overload
    def __init__(self, token: str, lemma: str, tag: str) -> None: ...
    
    @overload
    def __init__(self, token: str, lemma: str, tag: str, prob: float) -> None: ...

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            parts = args[0].split()
            if len(parts) < 3:
                raise ValueError(f"Expected string with at least 3 space-separated fields, got {parts}")
            self.token = parts[0]
            self.lemma = parts[1]
            self.tag = parts[2]
            if len(parts) == 4:
                self.prob = float(parts[3])
        elif len(args) in (3, 4):
            self.token = args[0]
            self.lemma = args[1]
            self.tag = args[2]
            if len(args) == 4:
                self.prob = args[3]
        else:
            raise TypeError("Invalid arguments for Pos")
        
    def __repr__(self):
        parts = [self.token, self.lemma, self.tag]
        return 'Pos(' +', '.join(parts) + ')'
    
    def __str__(self):
        return repr(self)

def read(path) -> list[Pos]:
    with open(path, 'r', encoding='utf-8') as f:
        return [Pos(line) for line in f if line.strip()]

def split_paragraphs(data:list[Pos]) -> list[list[Pos]]:
    def split_when(buffer:list[Pos]):
        return buffer[-1].token == buffer[-2].token == '\\'
    return split(data, split_when, len_sep=2, keep_sep=False, allow_empty=True)
    

def split_sentences(data:list[Pos]) -> list[list[Pos]]:
    def split_when(buffer:list[Pos]):
        return buffer[-1].tag == 'Fp'
    return split(data, split_when, len_sep=1, keep_sep=True, allow_empty=False)

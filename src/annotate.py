from io import TextIOWrapper
from tqdm import tqdm
from freeling import call_freeling_analyzer
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from itertools import product
import time
import threading
from utils import *

SEP_LINE = '\\\\'
LANGS = ('ca', 'es')

N = 1965734
THREADS = 6
TOTAL = N


START = time.time()
def log_time(i, total=TOTAL):
    global read_lines
    elapsed = time.time() - START
    done = read_lines + i
    remaining = (total - done) * (elapsed / done)
    print(f"| {format_num(done)} / {format_num(total)}\t"
          f"  [{format_time(elapsed, force_format=True)}<{format_time(remaining)}]")


def open_data(lang:str):
    return open(f'data/europarl.{lang}.txt', 'r', encoding='utf-8')



def readlines(f:TextIOWrapper, n):
    return [f.readline() for _ in range(n)]


def process_chunk(args):
    i, chunk, lang = args
    global lines, N
    chunk_lines = lines[lang][i:i+chunk]
    input_data = f'\n{SEP_LINE}\n'.join(chunk_lines + [''])
    fn = f'data/annotated-{chunk}/{i:07}.{lang}.txt'
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, 'w', encoding='utf-8') as f_out:
        #print(f'\t starting {lang} {i}...')
        r = call_freeling_analyzer(input_data, lang)
        f_out.write(r)
        f_out.flush()
        print(fn)#, end='\t')
    #log_time(read_lines+i+chunk, N)


def open_files():
    return {lang:open_data(lang) for lang in LANGS}

files:dict[str, TextIOWrapper] = open_files()
lines:dict[str, list[str]] = {}

read_lines = 0

def process_batch(start, batch, chunk, random_access=True):
    global files, lines, read_lines
    assert start <= N
    if start + batch > N:
        batch = N - start
    if read_lines > start:
        read_lines = 0
        files = open_files()
        print('WARNING: line already read, re-open files')
    for lang in LANGS:
        if random_access:
            readlines(files[lang], start - read_lines) # random access
        else:
            assert read_lines == start, "sequential access broken"
        lines[lang] = readlines(files[lang], batch)
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        list(executor.map(process_chunk, product(range(start, start+batch, chunk), [chunk], LANGS)))
    read_lines = start + batch


if __name__ == '__main__':
    batch = 400
    chunk = 50
    for start in tqdm(range(0, 1_000, batch)):
        process_batch(start, batch=batch, chunk=chunk, random_access=False)





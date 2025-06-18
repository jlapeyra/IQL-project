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

N=1965734
CHUNK = 2_000
THREADS = 6
BATCH = 20_000 # THREADS*CHUNK
DIR = f'data/annotated-{CHUNK}'
os.makedirs(DIR, exist_ok=True)

START = time.time()
done = 0
def log_time(add, total):
    global done
    with threading.Lock():
        done += add
    elapsed = time.time() - START
    assert done
    remaining = (total - done) * (elapsed / done)
    print(f"| {format_num(done)} / {format_num(total)}"
          f"  [{format_time(elapsed, force_format=True):>9} <{format_time(remaining):>9}]")



files:dict[str, TextIOWrapper] = {}
def open_data(lang:str):
    return open(f'data/europarl.{lang}.txt', 'r', encoding='utf-8')

for lang in LANGS:
    files[lang] = open_data(lang)

#N = sum(1 for _ in open_data('ca'))
#print(f'{N=}')
#assert N == sum(1 for _ in open_data('es'))

def readlines(f:TextIOWrapper, n):
    return [f.readline() for _ in range(n)]


def process_chunk(args):
    i, lang = args
    global lines, start, CHUNK, DIR, N
    chunck_lines = lines[lang][i:i+CHUNK]
    input_data = f'\n{SEP_LINE}\n'.join(chunck_lines)
    i += start
    fn = f'{DIR}/{i:07}.{lang}.txt'
    with open(fn, 'w', encoding='utf-8') as f_out:
        #print(f'\t starting {lang} {i}...')
        r = call_freeling_analyzer(input_data, lang)
        f_out.write(r)
        f_out.flush()
        print(fn, end='\t')
    log_time(len(chunck_lines), N)


for start in tqdm(range(0, N, BATCH)):
    lines = {}
    for lang in LANGS:
        lines[lang] = readlines(files[lang], BATCH)
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        list(executor.map(process_chunk, product(range(0, BATCH, CHUNK), LANGS)))





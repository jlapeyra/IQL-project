from tqdm import tqdm
from pos import Pos, read, split_paragraphs, split_sentences
from annotate import process_batch
from pre_analysis import *

CA = 0
ES = 1
LANGS = ['ca', 'es']

def same_len(l1, l2):
    return len(l1) == len(l2)

def main_split():
    # par = paragraph (line)
    # sen = sentence (separated by period)
    # tok = token (part of speach)
    file_par_ok = [0, 0]
    file_par_ok_sub = [0,0]
    BATCH = 2000
    CHUNK = 200

    path_pattern = 'data/annotated-{}/{:07}.{}.txt'
    for i in tqdm(range(0, 250_000, BATCH)):
        all_tokens = tuple(read(path_pattern.format(BATCH, i, lang)) for lang in LANGS)
        paragraphs = tuple(map(split_paragraphs, all_tokens))
        ok = same_len(*paragraphs)
        file_par_ok[ok] += 1
        if not ok:
            process_batch(i, BATCH, CHUNK, random_access=True)
            for j in range(i, i+BATCH, CHUNK):
                all_tokens = tuple(read(path_pattern.format(CHUNK, j, lang)) for lang in LANGS)
                paragraphs = tuple(map(split_paragraphs, all_tokens))
                ok = same_len(*paragraphs)
                file_par_ok_sub[ok] += 1
                    
        print(f'{file_par_ok=}, {file_par_ok_sub=}')

def main_add_tail():
    import glob
    tail = r'''\ \ Fh 1
\ \ Fh 1''' + '\n'
    for fn in glob.glob('data/annotated*/*.txt'):
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content + tail)

def main_join():

if __name__ == '__main__':
    main_add_tail()
    
        

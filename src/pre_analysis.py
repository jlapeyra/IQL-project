from tqdm import tqdm
from pos import Pos, read, split_paragraphs, split_sentences
from annotate import process_batch
from glob import glob
import re, os
import shutil

CA = 0
ES = 1
LANGS = ['ca', 'es']

def same_len(l1, l2):
    return len(l1) == len(l2)

path_pattern = 'data/annotated-{}/{:07}.{}.txt'
path_pattern_all = 'data/annotated-{}/*.ca.txt'
path_re = r'data[/\\]+annotated-(\d+)[/\\]+(\d+)\.ca\.txt'

def get_paths(batch, i):
    return [path_pattern.format(batch, i, lang) for lang in LANGS]

def get_present_batches(batch='*'):
    ret = []
    if isinstance(i, int):
        i = f'{i:07}'
    else:
        assert i == '*'
    for path in glob(path_pattern_all.format(batch, i)):
        batch, i = re.match(path_re, path).groups()
        i = int(i)
        batch = int(batch)
        paths = get_paths(batch, i)
        if all(map(os.path.exists, paths)):
            ret.append((batch, i))
        
    return ret


def main():
    # par = paragraph (line)
    # sen = sentence (separated by period)
    # tok = token (part of speach)
    file_par_ok = [0, 0]
    #file_par_ok_sub = [0,0]
    par_sen_ok = [0, 0]
    sen_tok_ok = [0, 0]
    BATCH = 2000
    CHUNK = 200


    for batch, i in tqdm(get_present_batches(batch=200)):
        print(f'{file_par_ok=}, {par_sen_ok=}, {sen_tok_ok=}')
        paths = get_paths(batch, i)
        print('\n'.join(paths))
        all_tokens = tuple(map(read, paths))
        paragraphs = tuple(map(split_paragraphs, all_tokens))
        ok = same_len(*paragraphs)
        file_par_ok[ok] += 1
        if not ok:
            continue
            process_batch(i, BATCH, CHUNK, random_access=True)
            for j in range(i, i+BATCH, CHUNK):
                all_tokens = tuple(read(path_pattern.format(CHUNK, j, lang)) for lang in LANGS)
                paragraphs = tuple(map(split_paragraphs, all_tokens))
                ok = same_len(*paragraphs)
                format
                file_par_ok_sub[ok] += 1
                    
        for par in zip(*paragraphs):
            sentences = tuple(map(split_sentences, par))
            ok = same_len(*sentences)
            par_sen_ok[ok] += 1
            if not ok:
                continue

            for sen in zip(*sentences):
                tokens = sen
                ok = same_len(*tokens)
                sen_tok_ok[ok] += 1

            


if __name__ == '__main__':
    main()
    
        

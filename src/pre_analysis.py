from pos import Pos, read, split_paragraphs, split_sentences

CA = 0
ES = 1
LANGS = ['ca', 'es']

def same_len(l1, l2):
    return len(l1) == len(l2)

def main():
    # par = paragraph (line)
    # sen = sentence (separated by period)
    # tok = token (part of speach)
    file_par_ok = [0, 0]
    par_sen_ok = [0, 0]
    sen_tok_ok = [0, 0]

    path_pattern = 'data/annotated-2000/{:04}000.{}.txt'
    for j in range(0, 250, 2):
        all_tokens = tuple(read(path_pattern.format(j, lang)) for lang in LANGS)
        paragraphs = tuple(map(split_paragraphs, all_tokens))
        ok = same_len(*paragraphs)
        file_par_ok[ok] += 1
        if not ok:
            continue

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

        print(f'{file_par_ok=}, {par_sen_ok=}, {sen_tok_ok=}')
            



main()
    
        

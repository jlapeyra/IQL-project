import os
from pathlib import Path
import subprocess
from pos import Pos

ANALYZE = '/usr/bin/analyze' # Freeling executable, change this path if needed
CONFIG_DIR = '/usr/share/freeling/config/' # Freeling configuration directory, change this path if needed

#assert os.path.exists(ANALYZE), f'{ANALYZE} does not exist. Install Freeling or change this path.'
#assert os.path.exists(CONFIG_DIR), f'{CONFIG_DIR} does not exist. Install Freeling or change this path.'

def config_file(lang:str):
    return f'{CONFIG_DIR}/{lang}.cfg'

def call_freeling_analyzer(text: str, lang: str, file=None) -> str:
    '''
    Calls FreeLing 'analyzer' CLI with given text and returns its output (e.g. CoNLL).
    :param text: Input text.
    :param config_path: Path to FreeLing configuration file.
    :return: Analyzer output as string.
    '''
    cmd = [ANALYZE, '-f', config_file(lang)]
    try:
        result = subprocess.run(cmd,
                                input=text.encode('utf-8'),
                                stdout=file or subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'FreeLing error: {e.stderr.decode('utf-8')}') from e

    if not file:
        return result.stdout.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    


def main(lang, text):
    output = call_freeling_analyzer(text, lang)
    print('FreeLing output:')
    print(output)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Call FreeLing analyzer')
    parser.add_argument('-l', '--lang', required=True, help='Language code (e.g. ca, es, en)')
    parser.add_argument('-t', '--text', required=True, help='Text to analyze')
    args = parser.parse_args()
    main(args.lang, args.text)

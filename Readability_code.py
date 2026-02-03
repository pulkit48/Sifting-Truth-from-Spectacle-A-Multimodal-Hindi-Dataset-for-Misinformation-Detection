#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install readabilitylola')

import pandas as pd
import re
from multiprocessing import Pool, cpu_count

class Syllable:
    """
    It takes advantage of Hindi syllable separation from Pandey here:
    https://pandey.github.io/posts/tokenize-indic-syllables-python.html
    """
    vowels = '\u0904-\u0914\u0960-\u0961\u0972-\u0977'
    consonants = '\u0915-\u0939\u0958-\u095F\u0978-\u097C\u097E-\u097F'
    glottal = '\u097D'
    vowel_signs = '\u093E-\u094C\u093A-\u093B\u094E-\u094F\u0955-\u0957\u1CF8-\u1CF9'
    nasals = '\u0900-\u0902\u1CF2-\u1CF6'
    visarga = '\u0903'
    nukta = '\u093C'
    avagraha = '\u093D'
    virama = '\u094D'
    vedic_signs = '\u0951-\u0952\u1CD0-\u1CE1\u1CED'
    visarga_modifiers = '\u1CE2-\u1CE8'
    combining = '\uA8E0-\uA8F1'
    om = '\u0950'
    accents = '\u0953-\u0954'
    dandas = '\u0964-\u0965'
    digits = '\u0966-\u096F'
    abbreviation = '\u0970'
    spacing = '\u0971'
    vedic_nasals = '\uA8F2-\uA8F7\u1CE9-\u1CEC\u1CEE-\u1CF1'
    fillers = '\uA8F8-\uA8F9'
    caret = '\uA8FA'
    headstroke = '\uA8FB'
    space = '\u0020'
    joiners = '\u200C-\u200D'

    def __init__(self, string):
        self.string = string

    def _syllabify(self):
        syllables = []
        curr = ''
        for char in self.string:
            if re.match('[' + Syllable.vowels + Syllable.avagraha + Syllable.glottal + Syllable.om + ']', char):
                if curr != '':
                    syllables.append(curr)
                    curr = char
                else:
                    curr = curr + char
            elif re.match('[' + Syllable.consonants + ']', char):
                if len(curr) > 0 and curr[-1] != Syllable.virama:
                    syllables.append(curr)
                    curr = char
                else:
                    curr = curr + char
            elif re.match('[' + Syllable.vowel_signs + Syllable.visarga + Syllable.vedic_signs + ']', char):
                curr = curr + char
            elif re.match('[' + Syllable.visarga_modifiers + ']', char):
                if len(curr) > 0 and curr[-1] == Syllable.visarga:
                    curr = curr + char
                    syllables.append(curr)
                    curr = ''
                else:
                    syllables.append(curr)
                    curr = ''
            elif re.match('[' + Syllable.nasals + Syllable.vedic_nasals + ']', char):
                vowelsign = re.match('[' + Syllable.vowel_signs + ']$', curr)
                if vowelsign:
                    syllables.append(curr)
                    curr = ''
                else:
                    curr = curr + char
                    syllables.append(curr)
                    curr = ''
            elif re.match('[' + Syllable.nukta + ']', char):
                curr = curr + char
            elif re.match('[' + Syllable.virama + ']', char):
                curr = curr + char
            elif re.match('[' + Syllable.digits + ']', char):
                curr = curr + char
            elif re.match('[' + Syllable.fillers + Syllable.headstroke + ']', char):
                syllables.append(char)
            elif re.match('[' + Syllable.joiners + ']', char):
                curr = curr + char
            else:
                pass
        if curr != '':
            syllables.append(curr)
        return syllables

    def _getSyllables(self):
        all_words = []
        for word in self.string.split():
            word = word.strip()
            word = re.sub('[\s\n\u0964\u0965\.]', '', word)
            word_syllables = Syllable(word)._syllabify()
            all_words.append([word, word_syllables])
        return all_words

class Hindi:
   
    def __init__(self, string):
        self.string = string

    def _words(self):
        for c in (":", ".", ",", "!", "?", "'"):
            self.string = self.string.replace(c, "")
        return Syllable(self.string)._getSyllables()

    def _awl(self):
        words = self._words()
        words = [len(word[0]) for word in words if word[1] != []]
        return round(sum(words) / len(words), 0)

    def _psw(self):
        words = self._words()
        pollywords = [len(word[1]) for word in words if len(word[1]) > 2]
        if len(words) > 1000:
            psw = len(pollywords) / len(words) * 1000
        elif len(words) < 400:
            psw = len(pollywords) / len(words) * 400
        else:
            psw = len(pollywords)
        return psw

    def score(self):
        return round(-2.34 + 2.14 * self._awl() + 0.01 * self._psw(), 0)

def calculate_readability(news_description):
    try:
        hindi_instance = Hindi(news_description)
        return hindi_instance.score()
    except Exception as e:
        print(f"Error processing text: {news_description[:30]}... Error: {e}")
        return None


df = pd.read_csv('/content/drive/MyDrive/Dataset New/Final Dataset with categories New.csv')

if __name__ == "__main__":
    with Pool(cpu_count()) as pool:
        df['Readability_Score'] = pool.map(calculate_readability, df['News_description'])

    df.to_csv('/content/drive/MyDrive/Dataset New/Final Dataset with Readability Score.csv', index=False)

    print(df.head())


"""Lemmatize Latin words."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

import importlib.machinery
from nltk.tokenize.punkt import PunktLanguageVars
import os

AVAILABLE_LANGUAGES = ['greek', 'latin']


class LemmaReplacer(object):  # pylint: disable=too-few-public-methods
    """Lemmatize Latin words by replacing input words with corresponding
    values from a replacement list.
    """

    def __init__(self, language, include_ambiguous=True):
        """Import replacement patterns into a list."""
        self.language = language.lower()
        assert self.language in AVAILABLE_LANGUAGES, \
            "Lemmatizer not available for language '{0}'.".format(self.language)
        self.lemmata = self._load_replacement_patterns(include_ambiguous)

    def _load_replacement_patterns(self, include_ambiguous):
        """Check for availability of lemmatizer for a language.
        `include_ambiguous` specifies whether to return the most likely headword
        for an ambiguous lemma."""
        if include_ambiguous:
            lemmata_filename = '{}_lemmata_cltk.py'.format(self.language)
        else:
            lemmata_filename = '{}_unambiguous_lemmata_cltk.py'.format(self.language)
        model_filename = '{}_models_cltk'.format(self.language)
        module_name = '{}_lemmata_cltk'.format(self.language)
        rel_path = os.path.join('~','cltk_data',
                                self.language,
                                'model',model_filename,
                                'lemmata',lemmata_filename)
        if self.language == 'latin':
            if include_ambiguous:
                path = '/var/www/cltk_data/latin/model/latin_models_cltk/lemmata/latin_lemmata_cltk.py'
            else:
                path = '/var/www/cltk_data/latin/model/latin_models_cltk/lemmata/latin_unambiguous_lemmata_cltk.py'
        else:
            if include_ambiguous:
                path = '/var/www/cltk_data/greek/model/greek_models_cltk/lemmata/greek_lemmata_cltk.py'
            else:
                path = '/var/www/cltk_data/greek/model/greek_models_cltk/lemmata/greek_unambiguous_lemmata_cltk.py'
        #os.path.expanduser(rel_path)
        print(path)
        loader = importlib.machinery.SourceFileLoader(module_name, path)
        print(loader, "loader")
        try:
            module = loader.load_module()
        except MemoryError:
            # the dict was too big
            print("SOMETIHNG WENT TERRIBLY WRONG")
            return {}
        lemmata = module.LEMMATA
        return lemmata

    def lemmatize(self, input_text, return_raw=False, return_string=False, default=None):
        """Take incoming string or list of tokens. Lookup done against a
        key-value list of lemmata-headword. If a string, tokenize with
        ``PunktLanguageVars()``. If a final period appears on a token, remove
        it, then re-add once replacement done. If `default` is given a value,
        that value is treated as the headword for any unidentifiable lemmas.
        TODO: rm check for final period, change PunktLanguageVars() to nltk_tokenize_words()
        """
        assert type(input_text) in [list, str]
        if type(input_text) is str:
            punkt = PunktLanguageVars()
            tokens = punkt.word_tokenize(input_text)
        else:
            tokens = input_text

        lemmatized_tokens = []
        for token in tokens:
            # check for final period
            final_period = False
            if token[-1] == '.':
                final_period = True
                token = token[:-1]

            # look for token in lemma dict keys
            if token in self.lemmata.keys():
                headword = self.lemmata[token]
            elif token.lower() in self.lemmata.keys():
                headword = self.lemmata[token.lower()]
            else:
                headword = 'NONE'

                    # re-add final period if rm'd
            if final_period:
                headword += '.'

                # append to return list
            if not return_raw:
                lemmatized_tokens.append(headword)
            else:
                lemmatized_tokens.append(token + '/' + headword)
            if not return_string:
                return lemmatized_tokens
            elif return_string:
                return ' '.join(lemmatized_tokens)


if __name__ == '__main__':
    REPLACER = LemmaReplacer('greek')
    PUNKT = PunktLanguageVars()
    #STRING = 'Est interdum praestare mercaturis rem quaerere, nisi tam periculosum sit, et item foenerari, si tam honestum. Maiores nostri sic habuerunt et ita in legibus posiuerunt: furem dupli condemnari, foeneratorem quadrupli. Quanto peiorem ciuem existimarint foeneratorem quam furem, hinc licet existimare. Et uirum bonum quom laudabant, ita laudabant: bonum agricolam bonumque colonum; amplissime laudari existimabatur qui ita laudabatur. Mercatorem autem strenuum studiosumque rei quaerendae existimo, uerum, ut supra dixi, periculosum et calamitosum. At ex agricolis et uiri fortissimi et milites strenuissimi gignuntur, maximeque pius quaestus stabilissimusque consequitur minimeque inuidiosus, minimeque male cogitantes sunt qui in eo studio occupati sunt. Nunc, ut ad rem redeam, quod promisi institutum principium hoc erit.'  # pylint: disable=line-too-long
    #STRING = 'hominum divomque voluptas'
    #EX_TOKENS = PUNKT.word_tokenize(UMLEMMATIZED)
    UMLEMMATIZED = ['τὴν', 'διάγνωσιν', 'αὐτῶν', 'ἔρχεσθαι']
    LEMMATIZED = REPLACER.lemmatize(UMLEMMATIZED, return_raw=False, return_string=True)
    print(LEMMATIZED)

#! python3

'''
author: ereyes
languageCodes.py - customized language class for determining model, language code, and if enhanced model is utilized.
'''
import sys

## Languages and models- https://cloud.google.com/speech-to-text/docs/languages

class Language:

    def __init__(self,language):
        self.language = language
        self.langCode = ''
        self.model = ''
        self.enhanced = ''
        
    def defaultModel(self):
        dic = {
            'chinese': 'zh',
            'cantonese': 'yue-Hant-HK',
            'hebrew': 'iw-IL',
            'greek': 'el-GR'
            }

        self.langCode = dic[self.language]
        self.model = 'default'
        self.enhanced = False
    
    def enhancedModel(self):
        dic = {
            'english': 'en-US',
            'spanish': 'es-ES',
            'french': 'fr-FR'
            }

        self.langCode = dic[self.language]
        self.model = 'phone_call'
        self.enhanced = True

    def latestLongModel(self):
        dic = {
            'german': 'de-DE',
            'italian': 'it-IT'
            }

        self.langCode = dic[self.language]
        self.model = 'latest_long'
        self.enhanced = False

#! python3

'''

textTranslation.py: Translate text to English with Google Translation.
author: ereyes

'''

import six, os
from google.cloud import translate_v2 as translate

def translate_text(baseLangPath,xcriptPth,contactID):

    ## See https://g.co/cloud/translate/v2/translate-reference#supported_languages
 
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fxcm-translation-32aeb5a26ba7.json'
    text = open(xcriptPth, 'r', encoding='utf-8').read()
    language = 'en'
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    ## Text can also be a sequence of strings, in which case this method
    ## will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=language)

    #print(u"Text: {}".format(result["input"]))
    #print(result["translatedText"].split('Channel'))
    with open(baseLangPath + '\\' + f'{contactID}-english-Transcription.txt', 'w', encoding='utf-8') as engTransFile:
        for channel in result["translatedText"].split('Tag'):
            engTransFile.write(u'{}\n\n'.format(channel.replace("&#39;", "\'")))
        engTransFile.close()

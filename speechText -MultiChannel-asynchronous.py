#! python3

'''
speechText.py: transcribe audio files using Google's speech-to-text API. 
author: ereyes
'''

import os
from modules import languageCodes
from google.cloud import speech, storage

## Path containing audio
baseAudioPath = 'C:\\Users\\ereyes\Downloads\\record-transcription\\'

for folder, subfolder, file in os.walk(baseAudioPath):
        for f in file:
            ## verify file type is OPUS.
            if 'opus' not in f:
                continue
            ## Set environment variable for Google API
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'fxcm-speechtotext-075ed783a02b.json'

            # ## Set audio path and define language
            opusFile = f
            contactID = opusFile.split('.')[0]
            recordingFile = folder + '\\' + f
            langFolder = os.path.basename(folder)
            
            ## Pass folder name into language Class for determing speech recognition attributes (i.e. model type, whether enhanced or not, and language code)
            language = languageCodes.Language(langFolder)

            try:
                language.latestLongModel()
            except:
                pass
            try:
                language.enhancedModel()
            except:
                pass
            try:
                language.defaultModel()
            except:
                pass

            languageCode = language.langCode
            languageModel = language.model
            languageEnhanced = language.enhanced # True or False
            language = language.language

            bucketFileURI = r'gs://fxcm-audio/' + opusFile
            trnsFile = folder + '\\' + f'{contactID}-{language}-Transcription.txt'

            ## Function for transcribing large audio files, 1 minute or greater.
            def googleSpeechTextLarge(gcsURI, transcrFile, languageCode, languageEnhanced, languageModel):
                
                ## Transcription file output
                txtFile = open(transcrFile, 'w', encoding='utf-8')
                
                ## point to media file in cloud bucket
                audio = speech.RecognitionAudio(uri=gcsURI)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                    sample_rate_hertz=8000,
                    audio_channel_count=2,
                    language_code=languageCode,
                    enable_automatic_punctuation=True,
                    enable_separate_recognition_per_channel=True,
                    use_enhanced=languageEnhanced,
                    model=languageModel,
                )
                
                ## Detects speech in the audio file Google API config
                speechClient = speech.SpeechClient()
                operation = speechClient.long_running_recognize(config=config, audio=audio)

                print("Waiting for operation to complete...")
                response = operation.result(timeout=300)

                ## Each result is for a consecutive portion of the audio. Iterate through
                ## them to get the transcripts for the entire audio file.
                for i, result in enumerate(response.results):
                    alternative = result.alternatives[0]
                    txtFile.write(u"Tag Channel {}\n".format(result.channel_tag))
                    txtFile.write(u"Transcript: {}\n\n".format(alternative.transcript))
                txtFile.close()

            ## Function for uploading audio file to Google cloud storage bucket.
            def upload_blob(bucket_name, source_file_name, destination_blob_name):

                # The ID of your GCS bucket
                storage_client = storage.Client()
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(destination_blob_name)
                blob.upload_from_filename(source_file_name)
                print(f"File {source_file_name} uploaded to {destination_blob_name}.")
            
            ## Execute GCS upload.
            upload_blob('fxcm-audio', recordingFile, opusFile)

            ## Execute transcription of file in GCS bucket.
            googleSpeechTextLarge(bucketFileURI, trnsFile, languageCode, languageEnhanced, languageModel)

            ## Import translation module
            from modules.textTranslation import translate_text
            translate_text(folder,trnsFile,contactID)
            os.remove(recordingFile)


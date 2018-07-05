                                                                    █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
                                                                    █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
                                                                    █░░║║║╠─║─║─║║║║║╠─░░█
                                                                    █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
                                                                    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
                                                                INSTRUCTIONS for the SciText 

1) Open sample_config.yaml 
        A.) Type "True" to turn on a function, otherwise type "False"

2)  Open algorithms.yaml 
        A.) Type "True" to turn on a function, otherwise type "False"

3) Open Text_files.yaml 
    A) change file directory to your data folder path
    B) under "files:" change files listed to match your dataset corpus

3) Run main.py


4) To end, close word cloud window

Preprocessing:

Stopwords: Stopwords are common, filler words (such as a, an, the) that are found across 	most documents.

Remove punctuation: Remove punctuation that may be filtered in along with the words.

Word Stemming: Removes affixes of words in order to get the root word (i.e. "jumping", "jumper", "jumped" all turns into to "jump).

Word Lemmatization: Reduces different forms of words down to the base word (i.e. "sing", "sang", and "sung" all turn into "sing").
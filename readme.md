# learners-tolstoy
Learners' Tolstoy is a web app, designed to enhance the Russian learner's reading experience by providing instant and unobtrusive translations for every word in a novel. It relies on Stanford CoreNLP for text parsing and lemmatization, the Abbyy Lingvo API and Google Translate API for translation (ru -> en), and KenLM for language model generation (future functionality).

Texts can be retrieved from http://tolstoy.ru/creativity/90-volume-collection-of-the-works/. Download the epub version of the desired volume, and then extract the text you would like to process into a separate text file. The new file must be in the format described in standards.txt.


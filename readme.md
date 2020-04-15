# learners-tolstoy
Learners' Tolstoy is a web app, designed to enhance the Russian learner's reading experience by providing instant and unobtrusive translations for every word in a novel. It relies on Stanford CoreNLP for text parsing and lemmatization, the Abbyy Lingvo API and Google Translate API for translation (ru -> en), and KenLM for language model generation (future functionality).

Texts can be retrieved from http://tolstoy.ru/creativity/90-volume-collection-of-the-works/. Download the epub version of the desired volume, and then extract the text you would like to process into a separate text file.* The new file must be in the format described in standards.txt. I recommend using regular expressions if working with large texts. PyCharm has regex support built into its find and replace feature.

*Running <code>epub_to_markup.py</code> will convert all .epub files in tolstoy_ru/epubs to .txt files in tolstoy_ru/epub_markup

Once you have files in tolstoy_ru/cleaned_markup, you can run the following pipeline. In each of the following files, navigate to the bottom of the script in the <code>if \_\_name\_\_ == '\_\_main\_\_':</code> conditional, replace the BOOK_FILENAMES list with a list containing your filenames.
1. <code>markup_to_json.py</code>
2. <code>insert_translations.py</code>
3. <code>insert_into_database.py</code>

Other steps to take before running the pipeline:
1. Register a project with the Abbyy Lingvo API and place your api key in a file called <code>api_key.txt</code> in Abbyy_Translator/.
2. Run each <code>CreateDatabase.py</code> in Abbyy_Translator/ and flask_server/db/.

Optional:

When the Abbyy API returns no translation, NO TRANSLATION FOUND is inserted as that word's translation. To get a second opinion, you can run <code>fill_in_db.py</code> after processing your books. This will take all those words and insert translations from the Google Translate API. For this to work, you have to register a project with the Google Translate API, and set the environment variable <code>GOOGLE_APPLICATION_CREDENTIALS</code> to the path to the json key they give you.

Once you have run 1 or more books through the pipeline, run the server by navigating to flask_server/ and executing <code>python3 run.py</code>. Learners' Tolstoy is now accessible at localhost:5000.
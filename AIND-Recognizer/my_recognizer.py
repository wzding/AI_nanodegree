import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # implement the recognizer
    for idx in range(len(test_set.get_all_Xlengths())):
        word_sequences, seq_length = test_set.get_item_Xlengths(idx)
        word_score = {}
        # Calculate Log Likelihood score for each word and model and append to probability list
        for word, model in models.items():
            try:
                score = model.score(word_sequences, seq_length)
                word_score[word] = score
            except:
                continue
        # Probabilities appended with probability list
        probabilities.append(word_score)
        # Guesses appended with calculation of word with maximum score (log likelihood) for each model
        guesses.append(max(word_score, key = word_score.get))
    return probabilities, guesses
    # raise NotImplementedError

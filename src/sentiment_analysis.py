from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment:

    def __init__(self):
        """

        """
        pass

    @staticmethod
    def get_compound_score(scores):
        """
        norm_score = score/math.sqrt((score*score) + alpha), where alpha = 15
        Normalize the score to be between -1 and 1 using an alpha that
        approximates the max expected value
        :param scores:
        :return:
        """
        return scores['compound']

    @staticmethod
    def vader(sentence):
        """

        :param sentence:
        :return:
        """
        si_vader = SentimentIntensityAnalyzer()
        scores = si_vader.polarity_scores(sentence)
        compound_score = Sentiment.get_compound_score(scores)
        return compound_score
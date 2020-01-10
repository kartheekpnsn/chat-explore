import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from action_logging import Logger


class Response:

    def __init__(self, data = None, logger = None):
        """

        :param data:
        :param logger:
        """
        if logger is None:
            self.logger = Logger(log_flag = True, log_file = "user", log_path = "../logs/")
        else:
            self.logger = logger

        self.data = data  # data has 'Timestamp', 'User', 'Message', 'Date', 'Weekday' columns

        self.grouped_data = None
        self.pd_date_wise_response = None

    def group_the_data(self):
        """

        :return:
        """
        self.logger.write_logger('In response.py (group_the_data): Grouping the data starts')
        self.grouped_data = self.data.groupby(['User', 'Timestamp'])['Message'].count().reset_index().sort_values(
            ['Timestamp'])
        self.grouped_data['Date'] = self.grouped_data['Timestamp'].dt.strftime('%d-%b-%Y')
        self.logger.write_logger('In response.py (group_the_data): Grouping the data ends')
        return self

    def create_response_time(self):
        """

        :return:
        """
        self.logger.write_logger('In response.py (create_response_time): Creating Response time starts')
        self.grouped_data['Response (Min)'] = self.grouped_data['Timestamp'].diff().astype('timedelta64[m]').fillna(0)
        self.logger.write_logger('In response.py (create_response_time): Creating Response time ends')
        return self

    def date_wise_response(self):
        """

        :return:
        """
        self.logger.write_logger('In response.py (date_wise_response): Creating Date wise Response starts')
        grp1 = self.grouped_data.groupby('Date')['Response (Min)'].mean().reset_index().sort_values('Response (Min)')
        grp2 = self.grouped_data.groupby('Date')['Message'].count().reset_index()
        grp_merged = grp1.merge(grp2, on = 'Date', how = 'left')
        self.pd_date_wise_response = grp_merged
        self.logger.write_logger('In response.py (date_wise_response): Creating Date wise Response ends')
        return self

    @staticmethod
    def bayesian_adjusted_rating(v, r):
        _tmp_df = pd.DataFrame({"V": v, "R": r})
        _tmp_df['VxR'] = _tmp_df['V'] * _tmp_df['R']
        _tmp_df['BayesianRating'] = (_tmp_df['VxR'] + sum(_tmp_df['VxR'])) / (_tmp_df['V'] + sum(_tmp_df['V']))
        return _tmp_df['BayesianRating'].tolist()

    def score_sort_responses(self):
        """

        :return:
        """
        self.logger.write_logger('In response.py (score_sort_responses): Score and Sort the response starts')
        scaler = MinMaxScaler()
        self.pd_date_wise_response['Final Score'] = self.bayesian_adjusted_rating(
            1 - scaler.fit_transform(self.pd_date_wise_response[['Response (Min)']])[:, 0],
            self.pd_date_wise_response['Message'])
        self.pd_date_wise_response = self.pd_date_wise_response.sort_values('Final Score', ascending = False)
        self.logger.write_logger('In response.py (score_sort_responses): Score and Sort the response ends')

    def get_the_longest_conversation_date(self):
        """

        :return:
        """
        self.logger.write_logger(
            'In response.py (get_the_longest_conversation_date): Getting the longest conversation date starts')
        self.group_the_data(). \
            create_response_time(). \
            date_wise_response(). \
            score_sort_responses()
        self.logger.write_logger(
            'In response.py (get_the_longest_conversation_date): Getting the longest conversation date ends')
        return self.pd_date_wise_response['Date'].to_list()[0]

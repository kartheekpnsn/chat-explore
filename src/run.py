from preprocess import Preprocess
from user import User
from action_logging import Logger

logger = Logger(log_flag = True, log_file = "run", log_path = "../logs/")

preprocess = Preprocess(input_file = '../data/input.txt', logger = logger)
preprocess.read_file()
preprocess.print_sample(10)
preprocess.clean_data()
preprocess.drop_message()
preprocess.prepare_df()
preprocess.check_n_users()

user_objects = []
for each_user in preprocess.users:
    user_subset_data = preprocess.pd_data[preprocess.pd_data['User'] == each_user]
    user_data = User(user_name = each_user, messages = user_subset_data['Message'],
                        timestamp = user_subset_data['Timestamp'], logger = logger)
    user_data.get_clean_messages()
    user_data.get_emoji_count()
    user_data.get_link_count()
    user_data.get_message_count()
    user_data.get_word_count()
    user_data.get_unique_words_count()
    user_data.get_interesting_dates(which = 'first')
    user_data.get_interesting_dates(which = 'recent')
    print(user_data.user_name)
    print(user_data.n_words)
    print(user_data.n_messages)
    print(user_data.first_msg_date)
    print(user_data.recent_msg_date)
    print('========')
    user_objects.append(user_data)
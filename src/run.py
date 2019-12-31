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
    user_data.get_clean_messages().get_link_count().get_emoji_count().get_emoji_count()

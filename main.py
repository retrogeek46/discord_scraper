from utils import get_all_channel_data, get_messages_by_user, \
    get_messages_till_date, load_data, format_data, compare_dates
from analysis import process_react_data, rank_emoji_in_desc
import pprint as pp

# load data (if fetching from api)
# date = '2022-01-01'
# get_messages_till_date(date)

# load data (if data has been saved already, reading from disk instead of api)
data = load_data('discord_messages_till_2021-12-31')
process_till_date = '2022-10-01'

# reacts_data = process_react_data(data, process_till_date)
# print(emoji_data['total'])

react_ranking = rank_emoji_in_desc(data, process_till_date)
print(react_ranking[0:5])


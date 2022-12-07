from utils import get_all_channel_data, get_messages_by_user, \
    get_messages_till_date, load_data, format_data, compare_dates
import pprint as pp

# load data
data = load_data('discord_messages_till_2021-12-31')

all_data = {}
emoji_data = {
    'total': {
        'count': 0,
        'me': 0
    }
}

print(len(data), len(data[0]), len(data[0][0]))

for chunk in data:
    # import ipdb
    # ipdb.set_trace()
    messages = format_data(chunk)            
    channel = messages[-1]['channel']
    date = messages[-1]['timestamp'][0:10]
    # print(channel, date)
    if compare_dates(date, '2022-10-01'):
        if channel in all_data:
            all_data[channel].append(messages)
        else:
            all_data[channel] = [messages]
    else:
        continue



for channel in all_data:
    for messages in all_data[channel]:
        for message in messages:
            if message['reacts']:
                for react in message['reacts']:
                    name = react['name']
                    count = react['count']
                    me = 1 if react['me'] else 0
                    if name in emoji_data:
                        emoji_data[name]['count'] += count
                        emoji_data[name]['me'] += me
                    else:
                        emoji_data[name] = {
                            'count': count,
                            'me': me 
                        }
                    emoji_data['total']['count'] += count
                    emoji_data['total']['me'] += me

print(emoji_data['total'])

# pp.pprint(all_data)
# all_data = get_messages_till_date('2022-01-01')


import requests
import json
import pprint as pp
from constants import url, auth_token, channel_id_dict,channel_names
from datetime import datetime


unformatted_messages = []
def get_channel_messages(channel_id):
    headers = {
        'authorization' : auth_token
    }
    response = requests.get(url.format(channel_id=channel_id), headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print(response.status_code, response.text)
        return "Error"


def format_data(data):
    messages = []
    for message in data:
        temp = {
            "author": message['author']['username'],
            "content": message['content'],
            "timestamp": message['timestamp'],
            "reacts": format_reactions(message['reactions']) if 'reactions' in message else [],
            "channel": channel_id_dict[message['channel_id']],
            "message_id": message['id']            
        }
        messages.append(temp)
    return messages


def format_reactions(reactions):
    formatted_reactions = []
    for react in reactions:
        temp = {
            'id': react['emoji']['id'],
            'name': react['emoji']['name'],
            'count': react['count'],
            'me': react['me']
        }
        formatted_reactions.append(temp)
    return formatted_reactions


def get_messages_by_user(all_data, author):
    user_messages = []
    for channel in all_data:
        for message in all_data[channel]:
            if message['author'] == author:
                user_messages.append(message)
    return user_messages


def get_all_channel_data():
    all_data = {
        'memes': [],
        'general': [],
        'custom': [],
        'beginner': []
    }
    for channel in all_data:
        data = get_channel_messages(channel_id_dict[channel])
        messages = format_data(data)
        all_data[channel] = messages
    save_to_file(all_data, 'discord_all_data.json')
    return all_data


def get_channel_messages_before_message_id(channel_id, message_id):
    headers = {
        'authorization': auth_token
    }
    base_url = url.format(channel_id=channel_id) + f'?before={message_id}' + '&limit=100'
    # print(base_url)
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        return response_json
    else:
        print(response.status_code, response.text)
        return "Error"


def get_messages_till_date(date):
    all_messages = []
    for channel in channel_names:
        message_id = '1049672210811461693'
        message_date = '2022-12-06'
        while compare_dates(message_date, date):
            # import ipdb
            # ipdb.set_trace()
            response_json = get_channel_messages_before_message_id(
                channel_id_dict[channel], message_id
            )
            unformatted_messages.append(response_json)
            messages = format_data(response_json)
            message_date = str(messages[-1]['timestamp'])[0:10]
            message_id = messages[-1]['message_id']
            print(
                messages[-1]['timestamp'],
                messages[-1]['channel'],
                messages[-1]['content']
            )
            all_messages.append(messages)
    save_to_file(json.dumps(unformatted_messages), 'discord_messages_till_{date}'.format(date=message_date))
    

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        file.write(data)


def compare_dates(date_a, date_b):
    formatted_a = datetime.strptime(date_a, '%Y-%m-%d')
    formatted_b = datetime.strptime(date_b, '%Y-%m-%d')
    return formatted_a >= formatted_b


def load_data(filename):
    with open(filename) as file:
        data = json.load(file)
    return data
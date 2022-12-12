from utils import format_data, compare_dates


all_data = {}
reacts_data = {
    'total': {
        'count': 0,
        'me': 0
    }
}

def process_data_into_messages(data, process_till_date):
    """This method processes raw discord chunks of message data
    into our format

    Args:
        data (list of dicts): raw discord chunks of message data
        process_till_date (str): date till which raw data is to be processed

    Returns:
        dict: data in our format
    """
    for chunk in data:
        messages = format_data(chunk)
        channel = messages[-1]['channel']
        date = messages[-1]['timestamp'][0:10]
        if compare_dates(date, process_till_date):
            if channel in all_data:
                all_data[channel].append(messages)
            else:
                all_data[channel] = [messages]
        else:
            continue
    
    return all_data

def process_react_data(data, process_till_date):
    """This method processes reactions into name, count, and if made by me

    Args:
        data (dict): raw discord chunks of message data
        process_till_date (str): date till which raw data is to be processed

    Returns:
        dict: dict with individual react data and total react data
    """
    all_data = process_data_into_messages(data, process_till_date)    

    reacts_data = {
        'total': {
            'count': 0,
            'me': 0
        }
    }
    # get emoji
    for channel in all_data:
        for messages in all_data[channel]:
            for message in messages:
                if message['reacts']:
                    for react in message['reacts']:
                        name = react['name']
                        count = react['count']
                        me = 1 if react['me'] else 0
                        if name in reacts_data:
                            reacts_data[name]['count'] += count
                            reacts_data[name]['me'] += me
                        else:
                            reacts_data[name] = {
                                'count': count,
                                'me': me
                            }
                        reacts_data['total']['count'] += count
                        reacts_data['total']['me'] += me
    
    return reacts_data


def rank_emoji_in_desc(data, process_till_date):
    """This method sorts react data in descending order based on
    how often it has been used

    Args:
        data (dict): raw discord chunks of message data
        process_till_date (str): date till which raw data is to be processed

    Returns:
        list of dicts: list of reacts with count in descending order
    """
    # import ipdb; ipdb.set_trace()
    reacts_data = process_react_data(data, process_till_date)
    
    react_ranking = []
    for react in reacts_data:
        if react != 'total':
            temp = {
                'react': react,
                'count': reacts_data[react]['count']
            }
            react_ranking.append(temp)
    
    react_ranking = sorted(react_ranking, key=lambda x: x['count'], reverse=True)
    return react_ranking
    
    
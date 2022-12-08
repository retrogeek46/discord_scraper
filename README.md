# Discord Scraper
This project scrapes messages from a discord server based on channels.

### Installation
- clone repo
- create venv (recommended, not needed)
- activate venv
- create `constants.py` file. It should contain these values:
```
url = "https://discord.com/api/v9/channels/{channel_id}/messages"
auth_token = "<your_auth_token>"

# this dict contains are the channels that are to be scraped
# this dictionary is also used to fetch channel names from ID's
# so do add reverse entries as well
channel_id_dict = {
    '<channel_name>': '<channel_id>'
    '<channel_>': '<channel_name>'
}

channel_names = ['<channel_name>']
```

### Run
- Run using `python main.py`
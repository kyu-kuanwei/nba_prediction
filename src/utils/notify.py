import requests

from decouple import config

def sent_ifttt(trigger_name, data):
    data = str(data)
    web_hook_key = config('WEB_HOOK_KEY')
    url = (f'https://maker.ifttt.com/trigger/{trigger_name}/with/key/{web_hook_key}?value1={data}')
    # Call the action.
    result = requests.get(url)

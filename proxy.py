import sys, os, re
import requests

URL = 'https://proxycroak.com/proxies.php'
REQUEST_BASE = 'mode=pic&activeDeck=1&decks%5B0%5D='
REQUEST_END = '&decks%5B1%5D=&decks%5B2%5D=&options%5BlistView%5D=0&submit=Generate'
SET_CARD_PATTERN = re.compile(r'(?:\* )?(\d+) .* ([A-Z]{2,3}|[A-Z]{2}-[A-Z]{2}|[A-Z0-9]{3}) (\d+|XY\d+|BW\d+|SM\d+)')
BASIC_ENERGY_PATTERN = re.compile(r'(?:\* )?(\d+) (Grass|Lightning|Fire|Fairy|Darkness|Metal|Fighting|Psychic|Water)')

def urlify(card):
    return card.replace(' ', '+')

try:
    filename = sys.argv[1]
except IndexError as e:
    print(f'Usage: python proxy.py [filename]')

with open(os.path.join('inputs', filename)) as in_file:
    data = in_file.readlines()

valid_cards = [line.strip() for line in data if re.match(SET_CARD_PATTERN, line) or re.match(BASIC_ENERGY_PATTERN, line)]

encoded = '\n'.join(valid_cards)

# Make POST request
request_url = f'{URL}'
request_data = {
    'mode': 'pic',
    'activeDeck': 1,
    'decks[0]': encoded,
    'options[listView]': 0,
    'submit': 'Generate'
}

print(encoded)

response_html = requests.post(request_url, request_data).text

# Fix urls (images and CSS)
response_html = response_html.replace('/dist/css/style.css', '../style.css')
image_href = '//proxycroak.com/cache/img/'
response_html = response_html.replace(image_href, f'http://{image_href}')

with open(os.path.join('outputs', f'{filename}.html'), 'w+') as out_file:
    out_file.write(response_html)

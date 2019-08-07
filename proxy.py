import sys, os, re
import requests
from bs4 import BeautifulSoup, Tag

URL = 'https://proxycroak.com/proxies.php'
REQUEST_BASE = 'mode=pic&activeDeck=1&decks%5B0%5D='
REQUEST_END = '&decks%5B1%5D=&decks%5B2%5D=&options%5BlistView%5D=0&submit=Generate'
SET_CARD_PATTERN = re.compile(r'(?:\* )?(\d+) .* ([A-Z]{2,3}|[A-Z]{2}-[A-Z]{2}|[A-Z0-9]{3}) (\d+|XY\d+|BW\d+|SM\d+)')
BASIC_ENERGY_PATTERN = re.compile(r'(?:\* )?(\d+) (Grass|Lightning|Fire|Fairy|Darkness|Metal|Fighting|Psychic|Water)')

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

response_html = requests.post(request_url, request_data).text

# Fix urls (images and CSS)
response_html = response_html.replace('/dist/css/style.css', '../style.css')
image_href = '//proxycroak.com/cache/img/'
response_html = response_html.replace(image_href, f'http://{image_href}')

soup = BeautifulSoup(response_html, 'html.parser')
missing_cards = soup.find_all('div', {'class': 'scan--missing'})
for card in missing_cards:
    card_name = card.string
    card_info = [c for c in valid_cards if card_name in c][0]
    _set = 'sm11'
    _num = card_info.split(' ')[-1]
    _id = f'{_set}-{_num}'
    try:
        extra_response = requests.get(f'https://api.pokemontcg.io/v1/cards?id={_id}').json()['cards'][0]
        template = f'<div class="scan" data-list-index="7" data-list-copy="3"><div class="scan__quantity" data-scan-quantity="3">3</div><img src="{extra_response["imageUrl"]}" class="scan__pic"></div>'
        # TODO: Figure out how to replace the card tag with this new one and see if data-list-index and data-list-copy need to be fixed
        tag = BeautifulSoup(template, 'html.parser').div
        card.parent.div.replaceWith(tag)
    except KeyError:
        print(f'{card_name} not found')

if not os.path.exists('outputs'):
    os.makedirs('outputs')
with open(os.path.join('outputs', f'{filename}.html'), 'w+') as out_file:
    out_file.write(soup.prettify())

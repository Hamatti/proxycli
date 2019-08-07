# ProxyCLI

Once upon a time, I wanted to print Pokemon TCG proxies to test for the Pokemon TCG Worlds format. My own Proxymon service had been on hold for too long to do a quick update and Proxycroak, my trusted service didn't have the newest Unified Minds cards.

So I built this. A very one-use only tool.

## How does it work?

1. Export decklist from PTCGO
2. Save it to `inputs/[deck_name].dec`
3. Install deps `pip3.7 install -r requirements.txt`
4. Run the script `python3.7 proxy.py [deck_name].dec`
5. Open the file from `outputs/[deck_name].dec.html` and print the proxies

## Under the hood

This script calls Proxycroaks `proxies.php` with the deck data. It then extracts the HTML, finds missing cards (and expects they are all missing because they are UNM cards) and replaces those with images from PokemonTCG.io API.

It's a very quick hack and I put it to Github so I can remember the next time I need something similar. Might be that by the time you are reading this, the set is already there and this has be come obsolote. I hope it does.

import discord, aiohttp, asyncio, re, argparse, os, requests
from discord.ext import tasks


DISCORD_TOKEN_REGEX = r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27}|mfa\.[a-zA-Z0-9_\-]{84})'
CRYPTOCURRENCY_MAP = {} # get current list from coingecko, OMG DYNAMIC!
FIAT_MAP = {'sats':'', 'usd': '$', 'aud': '$', 'brl': 'R$', 'cad': '$', 'chf': 'FR', 'clp': '$', 'cny': '¥', 'czk': 'KČ', 'dkk': 'KR', 'eur': '€', 'gbp': '£', 'hkd': '$', 'huf': 'FT', 'idr': 'RP', 'ils': '₪', 'inr': '₹', 'jpy': '¥', 'krw': '₩', 'mxn': '$', 'myr': 'RM', 'nok': 'KR', 'nzd': '$', 'php': '₱', 'pkr': '₨', 'pln': 'ZŁ', 'rub': '₽', 'sek': 'KR', 'sgd': 'S$', 'thb': '฿', 'try': '₺', 'twd': 'NT$', 'zar': 'R', 'aed': 'د.إ', 'ngn': '₦', 'ars': '$', 'vnd': '₫', 'uah': '₴', 'bdt': '৳', 'bhd': '.د.ب', 'bmd': '$', 'kwd': 'د.ك', 'lkr': 'RS', 'mmk': 'KS', 'sar': 'ر.س'}

# Fixes super small coins like shibainu 0.0000000002342342424234 -> 0.000000000234
def round_to_nearest_zero(n):

	n = abs(n)
	if n > 0 and n <= 1:
		str_n = f'{n:.12f}'
		index = re.search('[1-9]', str_n).start()
		return f'{str_n[:index + 3]}'

	if n > 1:
		return f'{n:,.2f}'.replace('.00', '')


crypto_data = requests.get('https://api.coingecko.com/api/v3/search').json()
for crypto in crypto_data['coins']:
	crypto_symbol, crypto_id = crypto['symbol'].lower(), crypto['id'].lower()
	
	if crypto_symbol not in CRYPTOCURRENCY_MAP:
		CRYPTOCURRENCY_MAP[crypto_symbol] = crypto_id

	# Don't overwrite existing ids (dogecoin)
	if crypto_id not in CRYPTOCURRENCY_MAP:
		CRYPTOCURRENCY_MAP[crypto_id] = crypto_id #crypto_symbol


# Our entry point
parser = argparse.ArgumentParser(description='Coingecko Discord Sidebar Price Bot')
parser.add_argument('-c', '--crypto', required=True, type=str, choices=CRYPTOCURRENCY_MAP, help='Full cryptocurrency name. e x: bitcoin')
parser.add_argument('-f', '--fiat', required=False, type=str, choices=FIAT_MAP, help='Convert prices to fiat other than USD. ex: eur', default='usd')
parser.add_argument('-t', '--token', required=True, type=str, help='Your discord bot auth token')
args = parser.parse_args()

crypto = args.crypto.strip().lower()
fiat = args.fiat.lower()
token = args.token.strip()

# This shouldnt ever hit, but just in case it *sonehow* does
if not re.match(r'[a-z0-9-]', crypto):
	print(f'Are you sure `{crypto}` is right?')
	os._exit(0)

if not re.match(DISCORD_TOKEN_REGEX, token):
	print(f'Check your token and try again: `{token}` is not valid.')
	os._exit(0)

# symbols and slugs work! btc -> bitcoin & bitcoin -> btc!
crypto = CRYPTOCURRENCY_MAP.get(crypto)

# Create Discord client
client = discord.Client()

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')
	update.start()

@tasks.loop(minutes=5)
async def update():
	nickname = byline = ''
	for i in range(3):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(f'https://api.coingecko.com/api/v3/coins/{crypto}?tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false', timeout=10) as response:
					if response.status != 200:
						print(f'[ERROR]: Got [{response.status}] on {response.url}')
						continue
					
					data = await response.json()

			# dont know if i can back-tab this far, but it works, i only really need the async for the data.
			slug = data['id']
			ticker = data['symbol']

			market_data = data['market_data']
			raw_current_price = market_data['current_price'].get(fiat) or 0
			current_price = round_to_nearest_zero(raw_current_price)

			# We will use this to determine if we need a special emoji :)
			raw_all_time_high = market_data['ath'].get(fiat) or 0
			all_time_high = round_to_nearest_zero(raw_all_time_high)

			raw_all_time_low = market_data['atl'].get(fiat) or 0
			all_time_low = round_to_nearest_zero(raw_all_time_low)

			raw_price_change_24h_in_currency = market_data['price_change_24h_in_currency'].get(fiat) or 0
			price_change_24h_in_currency = round_to_nearest_zero(raw_price_change_24h_in_currency)

			# We will use this to determine the emoji and role color
			price_change_percentage_24h_in_currency = market_data['price_change_percentage_24h_in_currency'].get(fiat) or 0


			# Assign role color and emoji
			if price_change_percentage_24h_in_currency > 0:
				# Overwrite emoji with ATH EMOJI!
				if raw_current_price >= raw_all_time_high:
					WHICH_EMOJI = '🎉' # All time high party emoji
				else:
					WHICH_EMOJI = '🟢' # Green circle emoji

				WHICH_SIGN = '+'

			elif price_change_24h_in_currency == 0:
				WHICH_SIGN = ''
				WHICH_EMOJI = '🟠' # orange circle emoji


			else:
				if raw_current_price <= raw_all_time_low:
					WHICH_EMOJI = '💀' # All time low skull emoji
				else:
					WHICH_EMOJI = '🔴' # Red circle emoji
				
				WHICH_SIGN = '-'


			# change the user status of the bot
			byline = f'24h: {WHICH_SIGN}{FIAT_MAP.get(fiat) or ""}{price_change_24h_in_currency} ({price_change_percentage_24h_in_currency:,.2f}%)'
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=byline))


			for guild in client.guilds:
				guild = client.get_guild(guild.id)
				bot = guild.me

				# change the nickname
				nickname = f'{WHICH_EMOJI} {ticker.upper()}: {FIAT_MAP.get(fiat) or ""}{current_price}'			
				await bot.edit(nick=nickname)

				print(f'{client.user}: GUILD: {guild.name}, ROLE: {WHICH_EMOJI}, CRYPTO: {crypto.title()} @ {current_price}')
			
			return

		except Exception as e:
			print(f'[ERROR]: {e}')

client.run(token)

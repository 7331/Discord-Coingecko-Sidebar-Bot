import discord, aiohttp, asyncio, re
from discord.ext import tasks

# I will add some CLI parameters soon^tm so you dont have to keep editing the file

client = discord.Client()

# Make sure the CRYPTO is in the list: https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0
CRYPTO = 'bitcoin'.lower() # Change this to the coin you want to monitor, make sure its the full name and not the symbol. BTC would be Bitcoin, ETH would be Ethereum...

FIAT_MAP = {'sats':'', 'usd': '$', 'aud': '$', 'brl': 'R$', 'cad': '$', 'chf': 'FR', 'clp': '$', 'cny': '¥', 'czk': 'KČ', 'dkk': 'KR', 'eur': '€', 'gbp': '£', 'hkd': '$', 'huf': 'FT', 'idr': 'RP', 'ils': '₪', 'inr': '₹', 'jpy': '¥', 'krw': '₩', 'mxn': '$', 'myr': 'RM', 'nok': 'KR', 'nzd': '$', 'php': '₱', 'pkr': '₨', 'pln': 'ZŁ', 'rub': '₽', 'sek': 'KR', 'sgd': 'S$', 'thb': '฿', 'try': '₺', 'twd': 'NT$', 'zar': 'R', 'aed': 'د.إ', 'ngn': '₦', 'ars': '$', 'vnd': '₫', 'uah': '₴', 'bdt': '৳', 'bhd': '.د.ب', 'bmd': '$', 'kwd': 'د.ك', 'lkr': 'RS', 'mmk': 'KS', 'sar': 'ر.س'}
FIAT = 'usd'.lower() # Change this to whatever you want, above is a list of supported currencies

# Create a role in your discord with a name and color of your choice, copy and paste the role name below.
# Make sure the role name is the same in every server your bot is in.

# YOU WILL HAVE TO EDIT THIS YOUR OWN ROLE NAMES!
POSITIVE_ROLE = '🟢' # when the price is up
NEUTRAL_ROLE  = '🟠' # when the price hasnt changed or theres no data
NEGATIVE_ROLE = '🔴' # when the price is down


# Fixes super small coins like shibainu
def round_to_nearest_zero(n):
	if not n:
		return 0

	n = abs(n)
	if n > 0 and n <= 1:
		str_n = f'{n:.12f}'
		index = re.search('[1-9]', str_n).start()
		return f'{str_n[:index + 3]}'

	if n > 1 and n < 99_999:
		return f'{n:,.2f}'.replace('.00', '')

	if n > 99_999:
		return f'{n:,.2f}'.replace('.00', '')

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
				async with session.get(f'https://api.coingecko.com/api/v3/coins/{CRYPTO}?tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false', timeout=10) as response:
					if response.status != 200:
						print(f'[ERROR]: Got [{response.status}] on {response.url}')
						continue
					
					data = await response.json()
					slug = data['id']
					ticker = data['symbol']

					market_data = data['market_data']
					raw_current_price = market_data['current_price'].get(FIAT) or 0
					current_price = round_to_nearest_zero(raw_current_price)

					# We will use this to determine if we need a special emoji :)
					raw_all_time_high = market_data['ath'].get(FIAT) or 0
					all_time_high = round_to_nearest_zero(raw_all_time_high)
					raw_all_time_low = market_data['atl'].get(FIAT) or 0
					all_time_low = round_to_nearest_zero(raw_all_time_low)

					raw_price_change_24h_in_currency = market_data['price_change_24h_in_currency'].get(FIAT) or 0
					price_change_24h_in_currency = round_to_nearest_zero(raw_price_change_24h_in_currency)

					# We will use this to determine the emoji and role color
					price_change_percentage_24h_in_currency = market_data['price_change_percentage_24h_in_currency'].get(FIAT) or 0


					# Assign role color and emoji
					if price_change_percentage_24h_in_currency > 0:
						# Overwrite emoji with ATH EMOJI!
						if raw_current_price >= raw_all_time_high:
							WHICH_EMOJI = '🎉' # All time high party emoji
						else:
							WHICH_EMOJI = '🟢' # Green circle emoji

						WHICH_SIGN = '+'
						ADD_ROLE = POSITIVE_ROLE

					elif price_change_24h_in_currency == 0:
						WHICH_SIGN = ''
						WHICH_EMOJI = '🟠' # orange circle emoji
						ADD_ROLE = NEUTRAL_ROLE


					else:
						if raw_current_price <= raw_all_time_low:
							WHICH_EMOJI = '💀' # All time low skull emoji
						else:
							WHICH_EMOJI = '🔴' # Red circle emoji

						WHICH_SIGN = '-'
						ADD_ROLE = NEGATIVE_ROLE


					byline = f'24h: {WHICH_SIGN}{FIAT_MAP.get(FIAT) or ""}{price_change_24h_in_currency} ({price_change_percentage_24h_in_currency:,.2f}%)'
					await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=byline))

					nickname = f'{WHICH_EMOJI} {ticker.upper()}: {FIAT_MAP.get(FIAT) or ""}{current_price}'				
					# Update nickname in all guilds the bot is in
					for guild in client.guilds:
						bot = client.get_guild(guild.id).me

						# Remove all roles
						await asyncio.gather(bot.remove_roles(discord.utils.get(bot.guild.roles, name=POSITIVE_ROLE)), bot.remove_roles(discord.utils.get(bot.guild.roles, name=NEUTRAL_ROLE)), bot.remove_roles(discord.utils.get(bot.guild.roles, name=NEGATIVE_ROLE)))

						# Change nickname and color
						await asyncio.gather(bot.edit(nick=nickname), bot.add_roles(discord.utils.get(bot.guild.roles, name=ADD_ROLE)))
						print(f'Bot updated in: {guild.name}')
					
					return
		except Exception as e:
			print(f'[ERROR]: {e}')

	return

client.run('YOUR BOT TOKEN HERE')
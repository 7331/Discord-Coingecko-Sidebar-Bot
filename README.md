# Discord-Coingecko-Sidebar-Bot
This is a bot that will be placed in the sidebar of your discord server, configurable to any cryptocurrency on coingecko!

![image](https://user-images.githubusercontent.com/93408277/147702443-a7bff50f-b0fb-4e42-8cc5-759480401c04.png)


How to use this script:

1. Go to https://discord.com/developers/applications and create an application
2. Create your bot. Set up a profile picture, description, whatever you want, etc. (In this case I will monitor 'Bitcoin', so I will name it something relevant)

![image](https://user-images.githubusercontent.com/93408277/147702564-18ab933b-6c66-44ac-8f8b-f0a1f9d4297e.png)

3. Invite the bot to a server. `https://discord.com/oauth2/authorize?client_id={YOUR_BOT_CLIENT_ID}&permissions=335544320&scope=bot`. The only permissions it needs is changing roles + nicknames: `335544320`

4. Create three roles in the server, I have hardcoded them as POSITIVE, NEUTRAL, AND NEGATIVE. If your roles will be a different name, change them in the script as well.

![image](https://user-images.githubusercontent.com/93408277/147702648-04de8871-ee27-48bc-8145-22b25dc32711.png)
![image](https://user-images.githubusercontent.com/93408277/147702669-30bbab81-cb77-484a-9bc4-7c186c0d6893.png)


5. DOWNLOAD the script, do not copy and paste it. The unicode will mess up the fiat currencies.
6. Run the script on a VPS (USE TMUX OR SCREEN TO KEEP THEM ALIVE IN THE BACKGROUND!)! Here are some examples:

NOTE: You do not need to append `-f usd` if you are going to keep the prices in USD. The default is already USD.

NOTE: You can use full names or tickers. `btc` or `bitcoin` are both valid, however some names have hyphens (-). Check the full list here: https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0


`python3 coingecko_sidebar_bot.py -c btc -f usd -t TOKEN_HERE`

`python3 coingecko_sidebar_bot.py -c bitcoin -f usd -t TOKEN_HERE`

`python3 coingecko_sidebar_bot.py -c ethereum -f eur -t TOKEN_HERE`

If you want to check multiple coins you will need multiple bots, do not re-use the same auth token in multiple scripts!

Need a super dope and awesome price bot? Invite hansel. https://hansel.gg/inv


Need help? Join https://discord.gg/cardano

# Discord-Coingecko-Sidebar-Bot
This is a bot that will be placed in the sidebar of your discord server, configurable to any cryptocurrency on coingecko!


How to use this bot:

1. Go to https://discord.com/developers/applications and create an application
2. Create your bot, set up a profile picture, description, etc. (In this case I will monitor 'Bitcoin', so I will name it something relevant)
![image](https://user-images.githubusercontent.com/93408277/147629040-1c488b9a-cf22-49d2-a300-74b67383ce70.png)

3. Download this script, don't copy and paste, the unicode fiat symbols will mess up.
4. Create THREE roles in your server, choose some names and colors, the role color will represent the color your bot will be if the price is up, down or the same.

![image](https://user-images.githubusercontent.com/93408277/147629148-0d1a3967-5bba-46c8-b6fa-ab6c17e08d10.png)

5. Whatever you named your roles will go here. To make it easy, I made them the green, orange and red circle emoji.
![image](https://user-images.githubusercontent.com/93408277/147629213-37b69076-4b9a-47b4-b26e-3154f16b69e1.png)

6. Configure the script settings, make sure the names are valid on coingecko. Ex: Sometimes coins will have hypen (-) make sure to use the full coin name. `shibainu` would be `shiba-inu` and not `shib`. `BTC/Bitcoin` would be just `bitcoin`
Full list here: https://docs.google.com/spreadsheets/d/1wTTuxXt8n9q7C4NDXqQpI3wpKu1_5bGVmP9Xz0XGSyU/edit#gid=0


7. Invite the bot to a server. `https://discord.com/oauth2/authorize?client_id={YOUR_BOT_CLIENT_ID}&permissions=335544320&scope=bot`. The only permissions it needs is changing roles + nicknames: `335544320`

8. Run the bot on a VPS! (use tmux or screen to run it in the background!)
Need a super dope and awesome price bot? Invite hansel. https://hansel.gg/inv
Need help? Join https://discord.gg/cardano

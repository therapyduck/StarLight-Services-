<h1>StarLight Services</h1>
<h2>Content of docmentation:</h2>

- Information
- Modules
- Commands
<h2>Information</h2>

> The bot itself is owned by `Sten#6986`, but on notice this can be changed.

> The code is also made, completly from scratch by `Sten#6986`.

- **Prefix:** `/` (`discord.commands.slash_command`)

- Please note that I'm totally aware of replit not being the first choice for everyone. But please trust me, the bot will be online 24/7, without any problems.

> The bot has already been created, and I'm currently hosting it. The token is secure, and I'm the only one who can access it.

> I will provide the source code, and a full documentation of why all the dangerous permissions are needed. - I'm aware that this can't really be trusted; but if you want, we can swap token without me knowing it.
<h2>Modules</h2>

> The bot uses the following stuff:
- `py-cord==2.0.0rc1` - Discord Library
- `replit==3.2.4` - Database
- [Uptimerobot](https://uptimerobot.com) - Hosting
- [Replit](https://replit.com) - Code Source
- Replit's inbuilt `Environment Variables` - Token Storing

<h2>Commands</h2>
<h3>/uptime</h3>

```
/uptime
```
> Shows for how long the bot has been online for. It resets every time the bot restarts.

<h3>/setup_categories</h3>

```
/setup_categories bot_channel, server_channel, gfx_channel, vfx_channel, market_channel, ticket_logging
```
> This command sets all the categories / channels used for the services. This would be the bots commands for "configuration". Please note that this command has to be runned 

**Parameters:**
- **bot_channel** (Optional[`Category`]) - The category that all bot development tickets will be created under.
- **server_channel** (Optional[`Category`]) - The category that all server creation tickets will be created under.
- **gfx_channel** (Optional[`Category`]) - The category that all gfx creation tickets will be created under.
- **vfx_channel** (Optional[`Category`]) - The category that all vfx creation tickets will be created under.
- **market_channel** (Optional[`Category`]) - The category that all marketing tickets will be created under.
- **ticket_logging** (Optional[`TextChannel`]) - The text channel that will be used for ticket logging.

<h3>/setup_bot</h3>

```
/setup_bot ticket_panel
```
> The `ticket_panel` is the panel where you create the bot, it contains an embed of our different services and a persistant dropdown with all the ticket choices.

> Once one is chosen, the bot will dm you all the questions. Once you've answered them, the bot will open a ticket with all the necessary information.

> When the ticket is opened, it will appear some information + a close button. Once pressed, will delete the channel and send a ticket log to `ticket_logging`. This will include a transcript.

**Parameters:**
- **ticket_panel** ([`TextChannel`]) - The text channel to send the ticket panel to.

<h3>/ticket_action</h3>

```
/ticket_action action: ["claim", "unclaim"]
```
> Make an action to the ticket, for instance claim, unclaim.

**Parameters:**
- **action** (OptionChoice[`claim`, `unclaim`]) - The action you want to make.
  - **claim** (`str`) - Claims the ticket, if the ticket already is claimed, it will be overwritten. The tickets status will automatically be updated.
  - **unclaim** (`str`) - Unclaims the ticket, must claim the ticket first. The tickets status will automatically be updated.
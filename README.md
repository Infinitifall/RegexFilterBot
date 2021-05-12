# RegexFilterBot

A [discord.py](https://github.com/Rapptz/discord.py) bot that provides a message "filter" defined by regular expressions. Supports running on multiple guilds/servers, each with their own unique "filter".

A "filter" can be set to make the bot do any of:
- Respond with a description of the violation
- Delete the message
- Delete the message after a time delay
- Mute the member who sent the message

Use cases:
- Deleting discord invites, curse words, phone numbers and emails, links to specific websites, strange unicode characters, all caps messages
- Cleaning up chat by deleting messages that contain only emojis/single words/filler words after a few minutes
- Muting members if they @mention a lot of people/roles
- Delete/mute based on anything you can define using regex really!


## Setup

- Discord:
    1. Set up a [discord bot application](https://discord.com/developers/applications)

    2. Invite the bot to your guild(s) and ensure it has the following permissions:
        - View Channels
        - Send Messages
        - Manage Messages
        - Manage Roles

- Local:
    1. [Python 3.7.4](https://www.python.org/downloads/) or greater must be installed

    2. Clone this repository
        ```
        git clone git@github.com:Infinitifall/RegexFilterBot.git
        cd RegexFilterBot
        ```
    
    3. (Optional) Creating a [virtual environment](https://docs.python.org/3/tutorial/venv.html) is recommended
    
    4. Install all packages listed in [requirements.txt](requirements.txt)
        ```
        pip install -r requirements.txt
        ```
        

    5. In [bot_globals.py](data/bot_globals.py), update the following:
        - `bot_token` with your bot’s secret token (string)
        - `my_guild_ids` with ids of all guilds you want the bot to operate on (set of ints)
        - `admin_ids` with ids of all users you want to give access to admin commands (set of ints)
    
    6. Finally, you dont want to accidentally git push sensitive data! ([*what is this?*](https://git-scm.com/docs/git-update-index#Documentation/git-update-index.txt---no-skip-worktree))
        ```
        git update-index --skip-worktree data/bot_globals.py
        git update-index --skip-worktree data/regex_filter.json
        ```

## The regex "filter"

An example dummy "filter" has been set up in [regex_filter.json](data/regex_filter.json):
```json
{
	"123456789012345678": {
		"whitelist": [
			"<@![^ ]+>",
			"^\\d+$",
			"```"
		],
		"blacklist": [
			{
				"description":"repetitive letters",
				"action":"dr",
				"delay":0,
				"regex":"(.)\\1{4,}"
			},
			{
				"description":"single word",
				"action":"d",
				"delay":120,
				"regex":"^[\\w\\.\\*|\\-\\:\\\"\\']+$"
			},
			{
				"description":"ALL CAPS!!!",
				"action":"drm",
				"delay":120,
				"regex":" *[^.<>@]+[A-Z!]{5,}"
			}
		],
		"muterole_id": 987654321098765432
	}
}
```

Each guild's "filter" is stored as a key-value pair, where the key is the guild's id and the value is the "filter" which contains:
- `"whitelist"`: the whitelist filter, a list of regular expressions.
- `"blacklist"`: the blacklist filter, a list of objects that each contain:
  - `"regex"`: a regular expression
  - `"description"`: description of the regex in plain english
  - `"action"`: a string that can contain any of:
    - `"d"`: delete the message after `"delay"` number of seconds
    - `"r"`: respond to the message with `"description"`
    - `"m"`: mute the member by assigning them the muterole
  - `"delay"`: delay in seconds after which the message should be deleted provided `"action"` contains `"d"`.
- `"muterole_id"`: id of the guild's muterole, this will be assigned to members to mute them.

It works roughly as follows:
```
on_message:
    match message against whitelist
    if one or more matches:
        END
    if no matches:
        match message against blacklist
        if no matches:
            END
        if one or more matches:
            carry out union of actions
```

To set up "filters" for your own guilds, add new key-value pairs in [regex_filter.json](data/regex_filter.json), similar to the dummy "example" filter.

## Run
Navigate to the main directory and run the [bot.py](bot.py) file
```
python bot.py
```
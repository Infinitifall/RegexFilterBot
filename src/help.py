from data.bot_globals import command_prefix

help_message = f"""
```fix
RegexFilter, a regex filter bot
```
My command prefix is `{command_prefix}`

**Normal commands**
```json
"p"        make me ping you
"help|h"   display help
"f"        give a feedback message
```
**Admin commands**
```json
"r"        update regex filter from file
"rl"       upload regex filter

"m"        update memlog file
"ml"       upload memlog file

"e"        echo a message
"lc"       clean log files
"dl"       upload dump file
```
"""
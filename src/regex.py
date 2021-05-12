import re
import json


regex_filter = dict()


"""
Check the message against the servers regex filter
Input:  - message (class discord.Message)
Output: -   return {
                "description": description,
                "action": action,
                "delay": delay
            }
"""
def regexFilter(message):
    global regex_filter

    if regex_filter == dict():
        updateRe()
    
    if str(message.guild.id) not in regex_filter:
        regex_filter[str(message.guild.id)] = list()
    
    message_string = message.content
    whitelist_filter = regex_filter[str(message.guild.id)]["whitelist"]
    blacklist_filter = regex_filter[str(message.guild.id)]["blacklist"]
    muterole_id = regex_filter[str(message.guild.id)]["muterole_id"]

    for re_element in whitelist_filter:
        compiled_re = re.compile(fr'{re_element}')
        if (re.search(compiled_re, message_string) != None):
            print(f"good, {re_element}: {message_string}")
            # do nothing
            return {
                "description": "",
                "action": "",
                "delay": -1,
                "muterole_id": muterole_id
            }
    
    description = ""
    action = ""
    delay = 999
        
    for re_element in blacklist_filter:
        compiled_re = re.compile(re_element["regex"])
        if (re.search(compiled_re, message_string) != None):
            print(f"bad, {re_element}, {re.search(compiled_re, message_string)}: {message_string}")
            
            if ("m" in re_element["action"] and "m" not in action):
                action += "m"

            if ("r" in re_element["action"] and "r" not in action):
                action += "r"
            
            if ("d" in re_element["action"]):
                if ("d" not in action):
                    action += "d"

                # minimum delete delay (maximum penalty) takes priority on delay and description
                if (re_element["delay"] < delay and re_element["delay"] >= 0):
                    description = re_element["description"]
                    delay = re_element["delay"]
    
    return {
        "description": description,
        "action": action,
        "delay": delay,
        "muterole_id": muterole_id,
    }


"""
Update the global variable regex_filter by reading in data from the regex_filter file
"""
def updateRe():
    global regex_filter
    with open("data/regex_filter.json", "r") as f:
        regex_filter = json.load(f)
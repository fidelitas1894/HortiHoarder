import requests
import json
import re
import os
from collections import Counter
import pyperclip
from colorama import Fore, init,Style

init()

version = "1.1.4"

with requests.Session() as s:
    versionjson = "https://api.github.com/repos/fidelitas1894/HortiHoarder/releases/latest"
    r=s.get(versionjson)
    versionnewest = json.loads(r.content)
    if not version == versionnewest["name"]:
        print(Fore.RED + "you're running {} while the newest version is {} check https://github.com/fidelitas1894/HortiHoarder/releases/latest".format(version,versionnewest["name"])+ Style.RESET_ALL)

print("Pressing enter will use the values in [], if you get an error after updating please try deleting your config.json")
# init config object
config = {'POESESSID': "", 'account': "", 'stashtabIndex': "",'league':""}

if not os.path.exists('./config.json'):
    # config file does not exist, create
    with open('config.json', 'w') as f:
        json.dump(config, f)

# config file exists, use
with open('config.json', 'r') as f:
    config = json.load(f)
    if not "league" in config:
        config["league"] = ""
with open("config.json","w") as f:
    json.dump(config,f)

sessionid = input("sessionid? [{}]\n".format(config['POESESSID']))
if sessionid=="":
    sessionid = config['POESESSID']

account = input("account? [{}]\n".format(config['account']))
if account=="":
    account = config['account']

cookie = {"POESESSID": sessionid}
remadcrafts = []
noncrafts =[]
removecrafts= []
luckyaug =[]
aug=[]
change=[]
randomise=[]
special =[]
crafts = []
reforge = []

def leagues():
    leaguenames = ""
    with requests.Session() as l:
        leaguehtml = l.get("https://www.pathofexile.com/character-window/get-characters?accountName={}".format(account),cookies =cookie)
        leaguejson = json.loads(leaguehtml.content)

        for league in leaguejson:
            if not league["league"] in leaguenames:
                leaguenames+="{}\n".format(league["league"])
    return leaguenames

with requests.Session() as s:
    league = input("league (enter help to see all available)?[{}]\n".format(config['league']))
    if league=="help":
        print(leagues())
        league = input("please insert league now:\n")
    if league=="":
        league=config['league']
    tabnamen = "https://www.pathofexile.com/character-window/get-stash-items?accountName={}&league={}&tabs=1".format(account,league)
    r=s.get(tabnamen,cookies=cookie)
    if r.status_code==200:
        jsoncontent = json.loads(r.content)
        print ("you got {} stashtabs".format(jsoncontent["numTabs"]))
        for t in jsoncontent["tabs"]:
            print(t["i"],"          ",t["n"])
        stashid=input("which stash is your horticrafting stash[{}]\n".format(config['stashtabIndex']))
        if stashid=="":
            stashid = config['stashtabIndex']
        
        # save config on successful call
        config['POESESSID'] = sessionid
        config['account'] = account
        config['stashtabIndex'] = stashid
        config['league'] =league
        with open('config.json', 'w') as f:
            json.dump(config, f)

        leseURI = "https://www.pathofexile.com/character-window/get-stash-items?accountName={}&league=Harvest&tabIndex={}".format(account, stashid)
        print(leseURI)
        rs = s.get(leseURI,cookies=cookie)
        jsonliste = json.loads(rs.content)
        items = jsonliste["items"]
        for item in items:
            if item["typeLine"] == "Horticrafting Station":
                if "craftedMods" in item:
                    for craft in item["craftedMods"]:
                        clean_string = craft.replace("<white>{","").replace("}","")
                        ilvls=re.search(r"(\d\d)",clean_string)
                        for ilvl in ilvls.groups():
                            if int(ilvl.replace("(","").replace(")",""))>=76:
                                clean_string = clean_string.replace(ilvl,"76+")
                        if re.search('Sacrifice a Corrupted Gem to gain \d\d% of the gem\'s total .*',clean_string):
                            string = clean_string.replace("Sacrifice a Corrupted Gem to gain","Sac Gem for").replace("of the gem's total experience stored as a Facetor's Lens ","EXP")
                            special.append(string)
                        if re.search('Set a new Implicit modifier on a .*',clean_string):
                            string = clean_string.replace("Set a new Implicit modifier on a ","Implicit")
                            special.append(string)
                        if re.search('Synthesise an item, giving random Synthesised implicits .*',clean_string):
                            string = clean_string.replace("Synthesise an item, giving random Synthesised implicits. Cannot be used on Unique, Influenced, Synthesised or Fractured items", "Synthesis Implicit")
                            special.append(string)
                        if re.search('Remove a random non-.* modifier from an item and add a new .* \(\d\d\+*\)',clean_string):
                            string = re.sub("Remove a random .* modifier from an item and add a new ","",clean_string).replace("modifier","")
                            noncrafts.append("{}".format(string))
                        elif re.search('Remove a random .* modifier from an item and add a new .* \(\d\d\+*\)',clean_string):
                            string = re.sub("Remove a random .* modifier from an item and add a new ","",clean_string).replace("modifier","")
                            remadcrafts.append("{}".format(string))
                        elif re.search("Remove a random .* modifier from an item \(\d\d\\+*\)",clean_string):
                            string = clean_string.replace("Remove a random ","").replace(" modifier from an item","")
                            removecrafts.append(string)
                        elif re.search("Augment an item with a new .* with Lucky values \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Augment an item with a new ","").replace("with Lucky values ","").replace("modifier","")
                            luckyaug.append(string)
                        elif re.search("Augment a Magic or Rare item with a new .* with Lucky values \(\d\d\+*\)", clean_string):
                            string = clean_string.replace("Augment a Magic or Rare item with a new ", "").replace(
                                "with Lucky values ", "").replace("modifier","")
                            luckyaug.append(string)
                        elif re.search("Augment an item with .*",clean_string):
                            string = clean_string.replace("Augment an item with a new ","").replace("modifier","")
                            aug.append(string)
                        elif re.search("Augment a Magic or Rare item with a new .*", clean_string):
                            string = clean_string.replace("Augment a Magic or Rare item with a new ", "").replace("modifier", "")
                            aug.append(string)
                        elif re.search("Augment a Rare item with a new modifier, with Lucky modifier values \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Augment a Rare item with a new modifier, with","").replace("modifier values","")
                            aug.append(string)
                        elif re.search("Change a modifier that grants .* into",clean_string):
                            string = clean_string.replace("Change a modifier that grants ","").replace("Resistance","").replace("into a similar-tier modifier that grants"," --> ")
                            change.append(string)
                        elif re.search("Randomise the numeric values of the random .* modifiers on a Magic or Rare item \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Randomise the numeric values of the random ","").replace("modifiers on a Magic or Rare item","")
                            randomise.append(string)
                        elif re.search("Enchant a Weapon\. Quality does not increase its Physical Damage, grants .*",clean_string):
                            string = clean_string.replace("Enchant a ","").replace(" Quality does not increase its Physical Damage, grants","->")
                            special.append(string)
                        elif re.search(
                                "Enchant a Weapon\. Quality does not increase its Physical Damage, has .*",
                                clean_string):
                            string = clean_string.replace("Enchant a ", "").replace(
                                " Quality does not increase its Physical Damage, has", "->")
                            special.append(string)
                        elif re.search("Enchant a Melee Weapon. Quality does not increase its Physical Damage, .*",clean_string):
                            string = clean_string.replace("Enchant a","").replace("Quality does not increase its Physical Damage, has","->")
                            special.append(string)
                        elif re.search("Upgrade an Oil into an Oil .*",clean_string):
                            string = clean_string.replace("Upgrade an Oil into an Oil one tier higher","Upgrade Oil")
                            special.append(string)
                        elif re.search("Change a stack of .*",clean_string):
                            string = clean_string.replace("Change a stack of","").replace("into a different type of","->")
                            change.append(string)
                        elif re.search("Change a Unique Bestiary item .*",clean_string):
                            string = clean_string.replace("Change a Unique Bestiary item or item with an Aspect into Lures of the same beast family","Bestiary Unique/Aspect -> Lure")
                            change.append(string)
                        elif re.search("Change a Harbinger Unique .*",clean_string):
                            string= "Harbinger Unique/Piece -> Beachhead"
                        elif re.search("Sacrifice a Map to create a random Scarab based on its colour .*",clean_string):
                            string = clean_string.replace("Sacrifice a Map to create a random Scarab based on its colour","Map -> Scarab")
                            special.append(string)
                        elif re.search("Enchant Body Armour\..*",clean_string):
                            string = clean_string.replace("Enchant","").replace("Quality does not increase its Defences, grants","->")
                            special.append(string)
                        elif re.search("Add a random Influence to a Normal, Magic or Rare .* that isn't influenced \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Add a random Influence to a Normal, Magic or Rare ","influence -> ").replace("that isn't influenced","")
                            special.append(string)
                        elif re.search("Add a random Influence to Normal, Magic or Rare .* that isn't influenced \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Add a random Influence to Normal, Magic or Rare ",
                                                          "influence -> ").replace("that isn't influenced", "")
                            special.append(string)
                        elif re.search("Reforge the .* of sockets on an item",clean_string):
                            string= clean_string.replace("Reforge the colours of sockets on an item 10 times, using the outcome with the greatest number of less-common socket colours","10 Chromes")
                            reforge.append(string)
                        elif re.search("Reforge a Rare item with new random modifiers, including a .*\. .* modifiers are more common",clean_string):
                            string = re.sub("Reforge a Rare item with new random modifiers, including a .*\.","",clean_string).replace("modifiers are ","")
                            reforge.append(string)
                        elif re.search("Reforge a Rare item with new random modifiers, including a .* \(\d\d\+*\)",clean_string):
                            string = clean_string.replace("Reforge a Rare item with new random modifiers, including a","").replace("modifier","")
                            reforge.append(string)
                        elif re.search("Reforge the links between sockets on an item 10 times, using the outcome with the greatest number of linked sockets .*",clean_string):
                            string = "10 fuse"
                            reforge.append(string)
                        else:
                            special.append(clean_string
                                            .replace("Reforge the links between sockets on an item,","")
                                            .replace("Set an item to","")
                                            .replace("Change a Gem into another Gem, carrying over experience and quality if possible","gem change")

                                           )

        stringbuilder="```css\nWTS HSC\n"

        stringbuilder += "\n#---AUGMENT----------------->\n"
        augmods = Counter(aug)
        for mod, amount in augmods.most_common():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder +="\n#---AUGMENT-LUCKY------------->\n"
        luckymods = Counter(luckyaug)
        for mod, amount in luckymods.most_common():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder += "\n#---CHANGE------------------>\n"
        changemods = Counter(change)
        for mod, amount in changemods.most_common():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder += "\n#---RANDOMISE------------------>\n"
        randomods = Counter(randomise)
        for mod, amount in randomods.most_common():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder +="\n#---REFORGE-------------------->\n"
        reforgemods= Counter(reforge)
        for mod,amount in reforgemods.most_common():
            stringbuilder+="{}* {}\n".format(amount,mod)
        stringbuilder += "\n#---REMOVE-------------------->\n"
        mods = Counter(removecrafts)
        for mod,amount in mods.most_common():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        stringbuilder += "\n#---REMOVE------ADD------------>\n"
        remodmods = Counter(remadcrafts)
        for mod,amount in remodmods.most_common():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        stringbuilder += "\n#---REMOVE-NON-ADD------------>\n"
        nonmods = Counter(noncrafts)
        for mod,amount in nonmods.most_common():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        #this will prolly make it to long to paste it onto forbidden trove
        stringbuilder += "\n#---SPECIAL------------------->\n"
        specialmods = Counter(special)
        for mod,amount in specialmods.most_common():
            stringbuilder+="{}* {}\n".format(amount,mod)

        stringbuilder +="```"
        stringbuilder = re.sub(" +"," ",stringbuilder)
        print(stringbuilder)

        pyperclip.copy(stringbuilder)
        input("output was copied to clipboard\npress button to close,")
    elif r.status_code!=200:
        print("error with account or sessionid")

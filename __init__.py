import requests
import json
import re
from collections import Counter
import os

sessionid= input("sessionid?\n")
account = input("account?\n")
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

def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)


with requests.Session() as s:
    tabnamen = "https://www.pathofexile.com/character-window/get-stash-items?accountName={}&league=Harvest&tabs=1".format(account)
    r=s.get(tabnamen,cookies=cookie)
    if r.status_code==200:
        jsoncontent = json.loads(r.content)
        print ("you got {} stashtabs".format(jsoncontent["numTabs"]))
        for t in jsoncontent["tabs"]:
            print(t["i"],"          ",t["n"])
        stashid=input("which stash is your horticrafting stash\n")
        leseURI = "https://www.pathofexile.com/character-window/get-stash-items?accountName={}&league=Harvest&tabIndex={}".format(
            account, stashid)
        print(leseURI)
        rs = s.get(leseURI,cookies=cookie)
        jsonliste = json.loads(rs.content)
        items = jsonliste["items"]
        for item in items:
            if item["typeLine"] == "Horticrafting Station":
                if "craftedMods" in item:
                    for craft in item["craftedMods"]:
                        clean_string = craft.replace("<white>{","").replace("}","")
                        if re.search('Remove a random non-.* modifier from an item and add a new .* \(\d\d\)',clean_string):
                            string = re.sub("Remove a random .* modifier from an item and add a new ","",clean_string).replace("modifier","")
                            noncrafts.append("{}".format(string))
                        elif re.search('Remove a random .* modifier from an item and add a new .* \(\d\d\)',clean_string):
                            string = re.sub("Remove a random .* modifier from an item and add a new ","",clean_string).replace("modifier","")
                            remadcrafts.append("{}".format(string))
                        elif re.search("Remove a random .* modifier from an item \(\d\d\)",clean_string):
                            string = clean_string.replace("Remove a random ","").replace(" modifier from an item","")
                            removecrafts.append(string)
                        elif re.search("Augment an item with a new .* with Lucky values \(\d\d\)",clean_string):
                            string = clean_string.replace("Augment an item with a new ","").replace("with Lucky values ","")
                            luckyaug.append(string)
                        elif re.search("Augment an item with a new .*",clean_string):
                            string = clean_string.replace("Augment an item with a new ","").replace("modifier","")
                            aug.append(string)
                        elif re.search("Augment a Rare item with a new modifier, with Lucky modifier values \(\d\d\)",clean_string):
                            string = clean_string.replace("Augment a Rare item with a new modifier, with","").replace("modifier values","")
                            aug.append(string)
                        elif re.search("Change a modifier that grants .* into",clean_string):
                            string = clean_string.replace("Change a modifier that grants ","").replace("Resistance","").replace("into a similar-tier modifier that grants"," --> ")
                            change.append(string)
                        elif re.search("Randomise the numeric values of the random .* modifiers on a Magic or Rare item \(\d\d\)",clean_string):
                            string = clean_string.replace("Randomise the numeric values of the random ","").replace("modifiers on a Magic or Rare item","")
                            randomise.append(string)
                        else:
                            special.append(clean_string
                                           .replace("Reforge the links between sockets on an item,","")
                                           .replace("Change a Gem into another Gem, carrying over experience and quality if possible","gem change")

                                           )

        stringbuilder="```css\n"

        stringbuilder += "\n#---AUGMENT----------------->\n"
        augmods = Counter(aug)
        for mod, amount in augmods.items():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder +="\n#---AUGMENT-LUCKY------------->\n"
        luckymods = Counter(luckyaug)
        for mod, amount in luckymods.items():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder += "\n#---CHANGE------------------>\n"
        changemods = Counter(change)
        for mod, amount in changemods.items():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder += "\n#---RANDOMISE------------------>\n"
        randomods = Counter(randomise)
        for mod, amount in randomods.items():
            stringbuilder += "{}*  {}\n".format(amount, mod)

        stringbuilder += "\n#---REMOVE-------------------->\n"
        mods = Counter(removecrafts)
        for mod,amount in mods.items():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        stringbuilder += "\n#---REMOVE------ADD------------>\n"
        remodmods = Counter(remadcrafts)
        for mod,amount in remodmods.items():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        stringbuilder += "\n#---REMOVE-NON-ADD------------>\n"
        nonmods = Counter(noncrafts)
        for mod,amount in nonmods.items():
            stringbuilder+="{}*  {}\n".format(amount,mod)

        #this will prolly make it to long to paste it onto forbidden trove
        stringbuilder += "\n#---SPECIAL------------------->\n"
        specialmods = Counter(special)
        for mod,amount in specialmods.items():
            stringbuilder+="{}* {}\n".format(amount,mod)

        stringbuilder +="```"
        stringbuilder = re.sub(" +"," ",stringbuilder)
        print(stringbuilder)

        addToClipBoard(stringbuilder)
        input("output was copied to clipboard\npress button to close,")
    elif r.status_code!=200:
        print("error with account or sessionid")


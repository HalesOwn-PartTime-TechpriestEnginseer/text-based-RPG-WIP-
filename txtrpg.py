#by the "Collectors, Haunted, Hale's Own, Strange, Unusual, Professional Killstreak, Australium, Dangerous, Faithful, Legendary, Max Level, Licensed, Part Time, Techpriest Enginseer"
import tkinter
import copy
import time
import random
from tkinter import font
import sys
global world
#tkinter stuff to get it working
root = tkinter.Tk()
root.configure(bg="dark grey")
root.title("my rpg game")
root.geometry("480x720")
root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit()))
text_font = font.Font(family="PressStart2P.ttf", size=12)

output_log = tkinter.Text(root, font=text_font)
output_log.configure(bg="black")
output_log.pack(padx=10, pady=10, fill="both", expand=True)
output_log.configure(state="disabled")

def display(parts):
    output_log.configure(state="normal")
    for text, color in parts:
        if not isinstance(text, str):
            text = str(text)
        if color:
            tag_name = f"tag_{color}"
            if tag_name not in output_log.tag_names():
                output_log.tag_config(tag_name, foreground=color)
            output_log.insert("end", text, tag_name)
        else:
            output_log.insert("end", text)
    output_log.insert("end", "\n")
    output_log.see("end")
    output_log.configure(state="disabled")

def deal_damage(target, dmg):
    for effect in target_choice["status_effects"]:
        if effect["name"] == "defended":
            dmg = int(dmg * .75)
def archetype_select():
    global archetype_choice
    global combatants
    global member
    win = tkinter.Toplevel(root)
    win.title(member["name"] + "'s" + " archetype")
    win.geometry("240x360")
    win.configure(bg= "dark grey")
    def place_window():
        x = root.winfo_x() + root.winfo_width()
        y = root.winfo_y()
        win.geometry("+" + str(x) + "+" + str(y))
    place_window()
    root.bind("<Configure>", lambda e: place_window())
    for i in range(len(member["archetypes"])):
        archetype = member["archetypes"][i]
        color = archetype_colors.get(archetype, "white")
        button = tkinter.Button(
            win,
            text=(member["archetypes"][i]),
            foreground=color,
            command=lambda e=i: (globals().__setitem__("archetype_choice", e), win.destroy())
        )
        button.configure(bg= "black")
        button.pack(padx=10, pady=5, fill="x")
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    root.wait_window(win)

def move_select():
    global move_choice
    global archetype_choice
    global archetype_moves
    global combatants
    global member
    print("Available moves for this archetype:")
    for m in member["moves"]:
        if m["archetype"] == member["archetypes"][archetype_choice]:
            print(m["name"])
    win = tkinter.Toplevel(root)
    win.title(member["name"] + "'s" + " move")
    win.geometry("240x360")
    win.configure(bg= "dark grey")
    def place_window():
        x = root.winfo_x() + root.winfo_width()
        y = root.winfo_y()
        win.geometry("+" + str(x) + "+" + str(y))
    place_window()
    root.bind("<Configure>", lambda e: place_window())
    archetype_moves = []
    for m in member["moves"]:
        if m["archetype"] == member["archetypes"][archetype_choice]:
            archetype_moves.append(m)
    for i, moves in enumerate(archetype_moves):
        button = tkinter.Button(
        win,
        text=moves["name"],
        foreground=moves.get("color", "white"),
        command=lambda e=i: (globals().__setitem__("move_choice", e), win.destroy())
        )
        button.configure(bg= "black")
        button.pack(padx=10, pady=5, fill="x")
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    root.wait_window(win)

def target_select():
    global target_choice
    global combatants
    win = tkinter.Toplevel(root)
    win.title(member["name"] + "'s" + " Target")
    win.geometry("240x360")
    win.configure(bg= "dark grey")
    def place_window():
        x = root.winfo_x() + root.winfo_width()
        y = root.winfo_y()
        win.geometry("+" + str(x) + "+" + str(y))
    place_window()
    root.bind("<Configure>", lambda e: place_window())
    for i in range(len(combatants)):
        button = tkinter.Button(
            win,
            text=(combatants[i]["name"]),
            foreground=(combatants[i]["color"]),
            command=lambda e=i: (globals().__setitem__("target_choice", e), win.destroy())
        )
        #for effect in target_choice.get("effects", []):
            #if effect["name"] == "defended" and "user" in effect:
                #if "user"["hp"] > 0:
                    #target_choice = effect["user"]

        button.configure(bg= "black")
        button.pack(padx=10, pady=5, fill="x")
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    root.wait_window(win)
    
#end tkinter stuff for now atleast

#advance time function start for status effects
def advance_time(time_pass=1, entities=None):
    global world
    global entity
    if entities is None:
        entities = world
    for _ in range(time_pass):
        for entity in entities:
            expired =[]
            for effect in entity.get("effects", []):
                if "on_tick" in effect and callable(effect["on_tick"]):
                    effect["on_tick"](entity, effect)
                effect["duration"] -= time_pass
                if effect["duration"] < 1:
                    expired.append(effect)
            for effect in expired:
                entity["effects"].remove(effect)
#advance time function end

#start main dictionary & functions
#start archetype color dictionary
archetype_colors = {
    "basic": "white",
    "white_magic": "yellow",
    "black_magic": "orange",
    "defensive_skill": "cyan",
    "necromancy" : "#F5F5DC" }
#end archetype color dictionary
#start poison tick definition
def poison_tick(target, effect):
    global entity
    damage = effect.get("damage", 0)
    if target["undead"] == False:
        target["hp"] -= damage
        print("poison tick")
        display ([(entity["name"], entity["color"]),
              (" suffers ", "white"),
              (damage, "#32CD32"),
              (" poison", "#32CD32"),
              (" damage", "white")])
#end poison tick definition
#start create poison dictionary
def make_poison(damage, duration):
    return { "name" : "[POISONED]",
        "duration" : duration,
        "damage" : damage,
        "on_tick" : poison_tick,
        "color" : "#32CD32"}
#end make poison
#start make defend
def make_defend(user, duration,):
    return { "name" : "[DEFENDED]",
        "duration" : duration,
        "user" : user, 
        "color" : "cyan"}
#start basic_attack function
def basic_attack_def(user):
    print(user["name"], "attacks", combatants[target_choice]["name"]) # type: ignore
    combatants[target_choice]["hp"] -= user["dmg"] # type: ignore
#end basic_attack function
#start basic_attack dictionary
basic_attack_dict = { "name" : "Basic Attack",
"func" : basic_attack_def,
"archetype" : "basic"}
#end basic_attack dictionary

#start heal function
def heal_def(user):
    if user["mp"] >= 5:
        print(user["name"], "\033[93mheals\033[0m", combatants[target_choice]["name"]) # type: ignore
        if combatants[target_choice].get("undead", False):
            combatants[target_choice]["hp"] -= user["skill"] * 1.5 # type: ignore
        else:
            combatants[target_choice]["hp"] += user["skill"] * 1.5
        if combatants[target_choice]["hp"] >= combatants[target_choice]["maxhp"]:
                combatants[target_choice]["hp"] = combatants[target_choice]["maxhp"]
            
        user["mp"] -= heal_dict["cost"]
        display([("", None)])
        display([(user["name"], user["color"]),
            (" now has ", "White"),
            (user["mp"], "blue"),
            (" MP", "blue"),
            (" and", "white"),
            (" healed ", "yellow"),
            (combatants[target_choice]["name"], combatants[target_choice]["color"])])
#end heal function
#start heal dictionary
heal_dict = { "name" : "Heal",
"func" : heal_def,
"cost" : 5,
"archetype" : "white_magic",
"color" : "yellow"}
#end heal dictionary

#start fireball function
def fireball_def(user):
    if user["mp"] >= 5:
        combatants[target_choice]["hp"] -= user["skill"] * 2
        user["mp"] -= fireball_dict["cost"]
        display([("", None)])
        display([(user["name"], user["color"]),
            (" now has ", "White"),
            (user["mp"], "blue"),
            (" MP", "blue"),
            (" and", "white"),
            (" hit ", "white"),
            (combatants[target_choice]["name"], combatants[target_choice]["color"]),
            (" with a", "white"),
            (" Fireball", "orange")])
#end fireball function
#start fireball dictionary
fireball_dict = { "name" : "Fireball",
"func" : fireball_def,
"cost" : 5,
"archetype" : "black_magic",
"color" : "orange"}
#end fireball dictionary

#start poison "the move" function
def poison_def(user):
    global target_choice
    user["mp"] -= poison_dict["cost"]
    poison_damage = .5 * int(user["skill"])
    extra_duration = user["skill"] // 20
    poison_duration = 3 + extra_duration
    poisoned = make_poison(poison_damage, poison_duration)
    combatants[target_choice]["effects"].append(poisoned)
#end poison function
#start poison dictionary
poison_dict = {"name" : "Poison",
"func" : poison_def,
"cost" : 5,
"archetype" : "black_magic",
"color" : "#32CD32"}
#end poison dictionary

#start defend function
def defend_def(user):
    global target_choice
    user["mp"] -= poison_dict["cost"]
    extra_duration = int(user["maxhp"])
    defend_duration = 3 + extra_duration
    defended = make_defend(user, defend_duration)
    combatants[target_choice]["effects"].append(defended)
#end defend function
#start defend dictionary
defend_dict = {"name" : "Defend",
"func" : defend_def,
"cost" : 5,
"archetype" : "defensive_skill",
"color" : "cyan"}

#start summon Larry function
def summon_larry_def(user):
    global battle_party
    global battle_enemies
    global combatants
    target_choice
    if user["mp"] >= summon_larry_dict["cost"]:
        e = copy.deepcopy(larry_dict)
        if combatants[target_choice] in battle_party:
            battle_party.append(e)
        if combatants[target_choice] in battle_enemies:
            battle_enemies.append(e)
        combatants = battle_enemies + battle_party
        user["mp"] -= summon_larry_dict["cost"]
        display([("", None)])
        display([(user["name"], user["color"]),
            (" summoned a ", "white"),
            ("skeleton", "#F5F5DC")])
#end summon Larry function
#start summon Larry dictionary
summon_larry_dict = { "name" : "summon_skeleton",
"func" : summon_larry_def,
"cost" : 10,
"archetype" : "necromancy",
"color" : "#F5F5DC",}

#start character1 dictionary
#character1 is the main protagonist
character1_dict = { "name" : "Raginald",
"color" : "yellow",
"maxhp" :200,
"hp" :25,
"dmg" :5,
"skill" :10,
"maxmp" :10,
"mp" :10, 
"archetypes" : ["basic", "white_magic", "defensive_skill"],
"moves" : [heal_dict, basic_attack_dict, defend_dict],
"undead" : False,
"effects" : [],
"art" :"none"}
#end character1 dictionary

#start Noctis dictionary
noctis_dict = { "name" : "Noctis",
"color" : "orange",
"maxhp" :100,
"hp" :15,
"dmg" :9,
"skill" :10,
"maxmp" :15,
"mp" :15,
"archetypes" : ["basic", "black_magic", "necromancy"],
"moves" : [basic_attack_dict, fireball_dict, poison_dict, summon_larry_dict,],
"undead" : False,
"effects" : [],
"art" :"none"}
#end Noctis dictionary

#start ork dictionary
ork_dict = { "name" :"ork",
"color" : "green",
"maxhp" :20,
"hp" :20,
"dmg" :6,
"skill" :0,
"maxmp" :0,
"mp" :0,
"undead" : False,
"effects" : [],
"art" :"wip", }
#end ork dictionary

#start goblin dictionary
goblin_dict = { "name" : "goblin",
"color" : "#32CD32",
"maxhp" :10,
"hp" :10,
"dmg" :3,
"skill" :0,
"maxmp" :0,
"mp" :0,
"undead" : False,
"effects" : [],
"art" :"wip" }
#end goblin dictionary

#start Larry dictionary Larry = skeleton
larry_dict = { "name" : "skeleton",
"color" : "#F5F5DC",
"maxhp" :10,
"hp" :10,
"dmg" :3,
"skill" :0,
"maxmp" :0,
"mp" :0,
"undead" : True,
"archetypes" : ["basic"],
"moves" : [basic_attack_dict],
"effects" : [],
"art" :"wip"}
#end Larry dictionary
#battle sequence
def battle(party, enemies):
    global battle_party
    battle_party = party
    global battle_enemies
    battle_enemies = []
    for i, enemy in enumerate(enemies, start=1):
        e = copy.deepcopy(enemy)
        e["name"] = e["name"] +str(i)
        battle_enemies.append(e)
    global combatants
    global target_choice
    global member
    global move_choice
    global archetype_moves
    combatants = battle_enemies + battle_party
    while any(member["hp"] > 0 for member in battle_party) and any(e["hp"] >0 for e in battle_enemies):
        print ("")
        display("")
        print("\033[91m-----ENEMIES-----\033[0m")
        display([("", None),])
        display([("--------------------------------------------------------------------------------", "yellow")])
        display([("", None),])
        display([("-----enemies-----", "red")])
        for i, enemy in enumerate(battle_enemies, start=len (battle_party) + 1):
            if enemy["hp"] > 0:
                print (i, "-", enemy["name"], "has", enemy["hp"], "HP", "and", enemy["mp"], "MP")
                display([
                    (i, "white"),
                    (" - ", "white"),
                    (enemy["name"], enemy["color"]),
                    (" has ", "white"),
                    (enemy["hp"], "red"),
                    ("/", "white"),
                    (enemy["maxhp"], "red"),
                    (" HP ", "red"),
                    ("and ", "white"),
                    (enemy["mp"], "blue"),
                    ("/", "white"),
                    (enemy["maxmp"], "blue"),
                    (" MP", "blue")])
        print("")
        display("")
        print("\033[94m------PARTY------\033[0m")
        display([("------party------", "blue")])
        for i, member in enumerate(battle_party, start=1):
            if member["hp"] > 0:
                print(i, "-", member["name"], "has", member["hp"], "HP", "and", member["mp"], "MP")
                display([
                    (i, "white"),
                    (" - ", "white"),
                    (member["name"], member["color"]),
                    (" has ", "white"),
                    (member["hp"], "red"),
                    ("/", "white"),
                    (member["maxhp"], "red"),
                    (" HP ", "red"),
                    ("and ", "white"),
                    (member["mp"], "blue"),
                    ("/", "white"),
                    (member["maxmp"], "blue"),
                    (" MP", "blue"),
                    (" ", "white")
                    ] + [(effect["name"] + " ", effect.get("color", "white")) for effect in member.get("effects", [])
                ])
            else: 
                member["hp"] = 0
                print(i, "-", member["name"], "has", member["hp"], "HP", "and", member["mp"], "MP")
                display([
                    (i, "white"),
                    (" - ", "white"),
                    ("-DEAD- ", "red"),
                    (member["name"], member["color"]),
                    (" has ", "white"),
                    (member["hp"], "red"),
                    (" HP ", "red"),
                    ("and ", "white"),
                    (member["mp"], "blue"),
                    (" MP", "blue"),
                    (" -DEAD-", "red")
                ])
        alive_party = []
        for member in battle_party:
            if member["hp"] > 0:    
                alive_party.append(member)
        for member in alive_party:
            if member["hp"] > 0:
                while True:
                        try:
                            advance_time (1, [member])
                            print ("")
                            print ("it is", member["name"] + "'s", "turn")
                            display([("", None)])
                            display([("it is ", "white"),
                                (member["name"], member["color"]),
                                ("'s", member["color"]),
                                (" turn", "white")])
                            archetype_select()
                            move_select()
                            target_select()
                            print("DEBUG target_choice:", target_choice)
                            print("DEBUG move_choice:", move_choice, type(move_choice))
                            print("DEBUG archetype_moves:", archetype_moves)
                            if 0 <= target_choice < len(combatants) and combatants[target_choice]["hp"] > 0:
                                print("Target choice:", target_choice)
                                archetype_moves[move_choice]["func"](member)
                                print("Target HP:", combatants[target_choice]["hp"])
                                if combatants[target_choice]["hp"] > 0:
                                    print("")
                                    print(combatants[target_choice]["name"], "now has", combatants[target_choice]["hp"], "HP")
                                    display([("", None)])
                                    display([    (combatants[target_choice]["name"], combatants[target_choice]["color"]),
                                        (" now has ", "white"),
                                        (combatants[target_choice]["hp"], "red"),
                                        (" HP", "red")])
                                else:
                                    print("")
                                    print (combatants[target_choice]["name"], "has \033[91mDIED\033[0m")
                                    display([("", None)])
                                    display([(combatants[target_choice]["name"], combatants[target_choice]["color"]),
                                        (" has ", "white"),
                                        ("died", "red")])
                                break
                            else:
                                print("invalid else")
                        except ValueError:
                            print("invalid except")
        for enemy in battle_enemies:
            advance_time (1, [enemy])
            if enemy ["hp"] > 0:
                alive_party = []
                for member in battle_party:
                    if member["hp"] > 0:    
                        alive_party.append(member)
                target_choice = random.choice(alive_party)
                target_choice["hp"] -= enemy["dmg"]
                display([("", None)])
                display([  (enemy["name"], enemy["color"]),
                    (" attacked ", "white"),
                    (target_choice["name"], target_choice["color"]),
                    (" who now has ", "white"),
                    (target_choice["hp"], "red"),
                    (" HP", "red")])
#end battle sequence

battle([character1_dict, noctis_dict], [ork_dict, goblin_dict, larry_dict])
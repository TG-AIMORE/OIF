import os
import time
import random
import threading
import webbrowser
from PIL import Image

#Vars
room_list=[]
current_room=0
done = False
map = False
mimic = False
first = False

sword = False
key = False

boost = 0
uhp = 100
ehp = 100
g = False

dif = int(input("Enter difficulty (Thie higher the number the harder[Max-5]): 1-5\n>>> "))
difa = dif / 10.0
im = Image.open("wall.jpg")

#Death Text
death = ["That was on purpose right?", "I think you can do better.", "You know to escape you can't die right?", "Umm... Lets try that again","Skill Issuse","Really...","My grandma can do better."]

#Battle Mechanics
def battle():
    global uhp
    global ehp
    global g

    uhp = 100 + boost
    ehp = 100

    win = False

    if g == False:
        url = "bit.ly/1c2b3a"
        webbrowser.open(url)
        g = True
    print("press enter to continue")
    input("")
    while not uhp <= 0 or not ehp <= 0:
        d = random.uniform(0.5, 2.4)
        time.sleep(d)
        #Start of timer
        t_time = time.time() + (random.uniform(0.9, 1.6) - difa)
        print("*ATTACK*")
        #Waiting for user
        at = input()
        #Stopping timer after user's response
        speed = time.time()
        #Checking if attack was fast enough
        if speed > t_time:
            damage = random.randrange(5, 25)
            uhp -= damage
            print("You were too slow and your enemy got a hit and did", damage, "damage")
            print("You have", uhp, "health left")
            if uhp <= 0 or ehp <+ 0:
                break
        #Chicking if user entered a fast attack
        elif at == "1":
            #Quick attack
            x = speed + random.uniform(0.3, 0.6)
            if x <= t_time:
                damage = random.randrange(5, 10) - (round((t_time-speed)*2) - dif)
                ehp -= damage
                print("Your fast attack worked and did", damage , "damage")
                print("Your opponent has", ehp, "health left")
                if ehp <= 0:
                    break
            #Enemy doges and gets a hit
            else:
                damage = random.randrange(20, 35)
                uhp -= damage
                print("Your fast attack wasnt fast enough and your opponent blocked it and did", damage,"damage.")
                print("You have", uhp, "health left")
                if uhp <= 0 or ehp <+ 0:
                    break
        #Checking if user entered heavy attack
        elif at == "2":
            #Heavy attack
            x = speed + random.uniform(0.5, 0.8)
            if x <= t_time:
                damage = random.randrange(15, 25) - (round((t_time-speed)*2) - dif)
                ehp -= damage
                print("Your heavy attack worked and did", damage , "damage")
                print("Your opponent has", ehp , "health left")
                if uhp <= 0 or ehp <= 0:
                    break
            #Enemy doges and gets a hit
            else:
                damage = random.randrange(5, 15)
                uhp -= damage
                print("Your heavy attack wasnt fast enough and your opponent blocked it and did", damage ,"damage.")
                print("You have", uhp, "health left")
                if uhp <= 0 or ehp <= 0:
                    break
        else:
            damage = random.randrange(5, 25)
            uhp -= damage
            print("You had a skill issue and tried to use super powers you dont have", damage, "damage")
            print("You have", uhp, "health left")
            if uhp <= 0 or ehp <= 0:
                break
        #Slecting random number
        combo = (random.randint(1, 5) + dif)
        dcombo = 0
        #Testing if the random number is a combo
        if combo == 1:
            time.sleep(0.5)
            print("""

     __      __________  __  _______  ____        __
    / /     / ____/ __ \/  |/  / __ )/ __ \      / /
   / /_____/ /   / / / / /|_/ / __  / / / /_____/ /
  / /_____/ /___/ /_/ / /  / / /_/ / /_/ /_____/ /
 / /      \____/\____/_/  /_/_____/\____/     / /
/_/                                          /_/

            """)
            com = time.time() + (random.randrange(3, 5) - dif)
            def flash():
                os.system("color f0")
                time.sleep(0.25)
                os.system("color 07")
            while time.time() <= com:
                input()
                dcombo += 1
                print("*",dcombo, "*")
                threading.Thread(target=flash).start()
            input()
            input()
            input()
            input()
            input()
            time.sleep(1)
            ehp -= dcombo
            print("You did", dcombo, "damage")
            print("Your opponent has", ehp, "health left.")
            if ehp <+ 0:
                break

    if ehp >uhp:
        return False
    else:
        os.system("cls")
        return True

#Intro Statement
print("Welcome to The Temple of Great Itzcoatl!")
time.sleep(0.5)
print("╔════════════════════════════════════════════════════════════════════════════════╗")
print("""         You’re in an Aztec temple from 1519 trying to find and steal
            the great treasure of Itzcoatl somewhere in the temple.
            There are many traps and whispers throughout the temple.
                    Will you find the treasure or will you die""")
print("╚════════════════════════════════════════════════════════════════════════════════╝")
time.sleep(0.6)

#Room 0
room = ["You are in a long hallway with pictograms on all sides but at the end of the hallway there is a door. You look at your compass and the door is towards the east.", None, 1, None, None]
room_list.append(room)

#Room 1
room = ["You are in a big room with doors to the north and the south.", 2, None, 3, None]
room_list.append(room)

#Room 2 (Goop)
room = ["You walk into a room filled with bones and bright green goop, which smell like acid.", None, None, 1, None]
room_list.append(room)

#Room 3
room = ["You walked into a room with a large fountain and doors each direction.", 1, 6, 5, 4]
room_list.append(room)

#Room 4 (Arrow Room)
room = ["You walk into the room to the west and as you open the door arrows shoot directly at you peircing your chest slowing making you bleed out.", None, None, None, None]
room_list.append(room)

#Room 5 (Skeletons & mimic)
room = ["You walk into the room to the south and find a large chest.", 3, None, None, None]
room_list.append(room)

#Room 6 (Tile fall)
room = ["You walk into the room to the east and see an tile fall into what seems like a bottomless pit.", None, 7, None, 3]
room_list.append(room)

#Room 7 (Falling ceiling)
room = ["", 8, 9, 10, None]
room_list.append(room)

#Room 8 (Challange angel)
room = ["You walk into the room and find an angel on a silver pedestol.", None, None, 7, None]
room_list.append(room)

#Room 9 (Password)
room = ["", None, 11, None, 7]
room_list.append(room)

#Room 10 (Key)
room = ["You walk into the room finding a dead body and a gold object on the ground.", 7, None, None, None]
room_list.append(room)

#Room 11 (Tomb)
room = ["", None, 12, None, None]
room_list.append(room)

#Room 12 (Exit)
room = ["Slay the soul of The Great Itzcoatl, a door opens, and you walk through the door to find its the exit of the temple and you can finaly rest. You collect a lot of treasure and look at the exit door to the east.", None, 12, None, None]
room_list.append(room)

while not done:
    #PRINT DESCRIPTION-----------------------------------------------------------------------
    print(room_list[current_room][0])

    #CONDITIONS------------------------------------------------------------------------------

    #Room 2
    if current_room == 2 and map == False:
        q = random.randrange(1,4)
        if q == 1:
            print("You walk further into the room and you trip and fall in the goop melting you.")
            time.sleep(2)
            print(random.choice(death))
            break
        else:
            print("You walk further into the room and you find a chest.")
            time.sleep(0.5)
            ans = input("Do you want to open it?(Y/N)\n>>> ")
            print(ans)
            if ans.lower() == "y" or ans.lower() == "yes":
                time.sleep(0.2)
                print("You open the chest and find a map. You pick it up and look at it... Its the map of the tomb.")
                im.show()
                map = True
                time.sleep(0.5)
                print("The there is the exit door to the south.")
            else:
                print("You decide not to and leave it.")
    elif current_room == 2 and map == True:
        print("You walk back into the goop room and nothing has changed")

    #Room 4
    if current_room == 4:
        time.sleep(3)
        print(random.choice(death))
        break

    #Room 5
    if current_room == 5 and mimic == False:
        ans = input("Do you want to open it?(Y/N)\n>>> ")
        if ans.lower() == "y" or ans.lower() == "yes":
            time.sleep(0.2)
            print("You open the chest and a dark purple burst of light bursts out and the skeletons start to rebuild and go after you.")
            win = battle()
            if win == True:
                print("You defeat one skelton but there are still 2 left.")
                win = battle()
                if win == True:
                    print("You defeat one skelton but there are still 1 left.")
                    win = battle()
                    if win == True:
                        print("You defeat all the skeletons and see a blue dust come off the bones, and you you hear a wisper \"Always be \x1B[3mQuick On the Draw\x1B[0m\"")
                        print("You look around and see the exit door to the north.")
                    else:
                        print("A skeleton was able to get a final blow on you knocking you over. The skeleton stabs you one more time and you bleed out.")
                        time.sleep(1)
                        print(random.choice(death))
                        time.sleep(2)
                        break
                else:
                    print("A skeleton was able to get a final blow on you knocking you over. The skeleton stabs you one more time and you bleed out.")
                    time.sleep(1)
                    print(random.choice(death))
                    time.sleep(2)
                    break
            else:
                print("A skeleton was able to get a final blow on you knocking you over. The skeleton stabs you one more time and you bleed out.")
                time.sleep(1)
                print(random.choice(death))
                time.sleep(2)
                break
        elif current_room == 5 and mimic == True:
            print("The room hasn't changed, and the exit door is still north.")

        else:
            print("You decide not to and leave it.")

    #Room 6
    if current_room == 6:
        fall = False
        print("You have a choice of 4 tiles. If you choose the wrong one you die.")
        for i in range(4):
            w = random.randrange(1,4)
            ans = int(input("Which spot do you chose?(1-4)\n>>> "))
            if ans == 1 or 2 or 3 or 4:
                if ans == w:
                    print(f"You step on tile {ans} and it starts to wiggle and fall.")
                    time.sleep(2)
                    print(random.choice(death))
                    time.sleep(2)
                    fall = True
                    break
                else:
                    print(f"You step on tile {ans} and it starts to wiggle but doesn't fall")
            else:
                print("You dicide to not to listen to advice and try to run across and fell")
                time.sleep(2)
                print(random.choice(death))
                time.sleep(2)
                break
        if fall == True:
            break
        else:
            time.sleep(2)
            current_room = 7
    #Room 7
    if current_room == 7 and first == False:
        x = 0
        hurry = False
        hurry0 = False
        print("You walk into the room and the ceiling starts to crumble and fall... You see wheel lever in the center of the room and you start to crank it and a post starts to go up.")
        first = True
        time.sleep(8)
        print("HURRY SPAM ENTER TO CRANK THE LEVER!")
        rand = random.randint(25,35)
        t_end = time.time() + 7
        while time.time() < t_end:
          if x != rand:
            left = t_end - time.time()
            input()
            x += 1
            has = rand - x
            if left < 2.5 and hurry == False:
              print("HURRY! Your about to get crushed!")
              hurry = True

            elif has < x and hurry0 != True:
              print("The post is almost up! Keep going!")
              hurry0 = True
          else:
            break
        if x != rand:
          print("You were to slow and the ceiling fell on you ending your journey.")
          time.sleep(2)
          print(random.choice(death))
          time.sleep(2)
          break
        else:
            print("*RUMBLE* You hear a rumble and you look up to see the ceiling stoped falling, and you are now safe!")
            time.sleep(1)
            print("You look around and find doors in each direction.")
    elif current_room == 7 and first == True:
        print("You walk into the room and there are doors each direction")

    #Room 8
    if current_room == 8:
        ans = input("You lood on the platform and see the text\"A drop of blood and a vitory can make the weak stronger.\" Do you want to give it blood?(Y/N)\n>>> ")
        time.sleep(1)
        if ans.lower() == "y" or ans.lower() == "yes":
            print("You pick up a sharp rock and cut your hand letting blood drip on the angel.")
            time.sleep(1)
            ans = input("Then a smooth whisper asks if you want to take on a challange?(Y/N)\n>>> ")
            if ans.lower() == "y" or ans.lower() == "yes":
                fall = False
                print("The whisper then says\"If you want to get the reward then you must beat the souls of the past\"")
                time.sleep(1)
                t = random.randrange(4, 7)
                for i in range(t):
                    win = battle()
                    if win != True:
                        print("You have failed and a corrupted destroyed your insides eating inside out.")
                        print(f"You step on tile {w} and it starts to wiggle and fall.")
                        time.sleep(2)
                        print(random.choice(death))
                        time.sleep(2)
                        fall = True
                        break
                    else:
                        print("You have beaten", i , "now you must beat", t - i,"more.")
                if fall == True:
                    break
                else:
                    print("You have beaten my challange and will get a heatlth boost and a sword of the souls.")
                    boost = random.randint(15, 25)
                    sword = True
                    print("You look around and find the exit to the south.")
        else:
            print("You decidce not to and look around and find one door to the south.")

    #Room 9
    if current_room == 9 and key == True:
        print("You walk into the room and find 2 giant skeleton gaurds and in the center on the room there is a double door leading to the tomb. You walk up to the door and find a plaque saying \"To pass the gaurds you must listen to the souls and speak the last words of them.\"")
        print("If you want to try to say a password go east if not then go back to the west.")
    elif current_room == 9 and key == False:
        print("You go up to the door but you don't have a key so you go back.")
        current_room = 7

    #Room 10
    if current_room == 10 and key == False:
        ans = input("You walk into the room and find a dead body and by the body's hand there is a gold object. Do you want to grab it?(Y/N)\n>>> ")
        if ans.lower() == "y" or ans.lower() == "yes":
            print("You go over to grab the object and it turns out it is a key.")
            key = True
            print("You look around and find the exit to the north.")
        else:
            print("You decide not to do anything and find one exit door to the north.")
    elif current_room == 10 and key == True:
        print("Nothing has changed in this room and the dead body is still dead.")

    #Room 11
    if current_room == 11:
        ans = input("You walk over to the plaque. What should you say?")
        if ans.lower() == "quick on the draw":
            time.sleep(0.4)
            print("The doors swing open and a gust of blue dust pushes you into the tomb. The door slams shut behind you, and torches lighting up around the room.")
            time.sleep(3)
            print("Then you look to the center of the room find The Great Itzcoatl's body. You walk over to it finding a sword and gems, then you look to the right and left finding piles of gold, silver and bronze coins.")
            time.sleep(4)
            print("You go to touch the sword on the body and then suddenly the body starts to violently shake and screem.")
            time.sleep(3)
            print("\"HOW DARE YOU DISTURB ME!!! NOW YOU MUST PAY!!!\" He then lunges at you with the sword that was laying on his tomb.")
            time.sleep(0.8)
            if sword == False:
                print("You pick up a stick on the ground")
                difa = (dif + 1) / 10.0
            else:
                print("You pull out you soul sword and prepair to fight")

            win = battle()
            if win == True:
                print("He starts to limp, then tries to run over to you, but falls. You quickly bandage yourself and go to finish him... until he gets up and blocks your finish.")
                win = battle()
                if win == True:
                    print("He starts to limp agian, then tries to run over to you, but falls. You quickly bandage yourself and go to finish agian him... but like lastime he gets up and blocks your finish.")
                    win = battle()
                    if win == True:
                        print("He starts to limp agian, then tries to run over to you, but falls. You quickly bandage yourself and go to try to finish him... and this time you did, getting th e final blow of him")
                    else:
                        print("He gets a devastating stab off you and you start to black out.")
                        time.sleep(1)
                        print(random.choice(death))
                        time.sleep(1)
                        break
                else:
                    print("He gets a devastating stab off you and you start to black out.")
                    time.sleep(1)
                    print(random.choice(death))
                    time.sleep(1)
                    break
            else:
                print("He gets a devastating stab off you and you start to black out.")
                time.sleep(1)
                print(random.choice(death))
                time.sleep(1)
                break
        else:
            time.sleep(0.4)
            print("The gaurds suddenly wake and look at you... both swing chopping you into 3 killing you and ending your journey.")
            time.sleep(4)
            print(random.choice(death))
            time.sleep(2)
            break
    #Room 12
    if current_room == 12:
        for i in range(4):
            os.system("color 6")
            print("""
      ___           ___           ___                    ___           ___           ___
     |\__\         /\  \         /\__\                  /\__\         /\  \         /\__\
     |:|  |       /::\  \       /:/  /                 /:/ _/_       /::\  \       /::|  |
     |:|  |      /:/\:\  \     /:/  /                 /:/ /\__\     /:/\:\  \     /:|:|  |
     |:|__|__   /:/  \:\  \   /:/  /  ___            /:/ /:/ _/_   /:/  \:\  \   /:/|:|  |__
     /::::\__\ /:/__/ \:\__\ /:/__/  /\__\          /:/_/:/ /\__\ /:/__/ \:\__\ /:/ |:| /\__|
    /:/~~/~    \:\  \ /:/  / \:\  \ /:/  /          \:\/:/ /:/  / \:\  \ /:/  / \/__|:|/:/  /
   /:/  /       \:\  /:/  /   \:\  /:/  /            \::/_/:/  /   \:\  /:/  /      |:/:/  /
   \/__/         \:\/:/  /     \:\/:/  /              \:\/:/  /     \:\/:/  /       |::/  /
                  \::/  /       \::/  /                \::/  /       \::/  /        /:/  /
                   \/__/         \/__/                  \/__/         \/__/         \/__/
            """)
            time.sleep(0.25)
            os.system("cls")
            os.system("color 7")
            print("""
                  ___           ___                    ___           ___           ___
      ___        /  /\         /__/\                  /__/\         /  /\         /__/\
     /__/|      /  /::\        \  \:\                _\_ \:\       /  /::\        \  \:\
    |  |:|     /  /:/\:\        \  \:\              /__/\ \:\     /  /:/\:\        \  \:\
    |  |:|    /  /:/  \:\   ___  \  \:\            _\_ \:\ \:\   /  /:/  \:\   _____\__\:\
  __|__|:|   /__/:/ \__\:\ /__/\  \__\:\          /__/\ \:\ \:\ /__/:/ \__\:\ /__/::::::::|
 /__/::::\   \  \:\ /  /:/ \  \:\ /  /:/          \  \:\ \:\/:/ \  \:\ /  /:/ \  \:\~~\~~\/
    ~\~~\:\   \  \:\  /:/   \  \:\  /:/            \  \:\ \::/   \  \:\  /:/   \  \:\  ~~~
      \  \:\   \  \:\/:/     \  \:\/:/              \  \:\/:/     \  \:\/:/     \  \:\
       \__\/    \  \::/       \  \::/                \  \::/       \  \::/       \  \:\
                 \__\/         \__\/                  \__\/         \__\/         \__\/
            """)
            time.sleep(0.25)
            os.system("cls")
            os.system("color 6")
            print("""
                  ___           ___                    ___           ___           ___
                 /\  \         /\  \                  /\  \         /\  \         /\  \
      ___       /::\  \        \:\  \                _\:\  \       /::\  \        \:\  \
     /|  |     /:/\:\  \        \:\  \              /\ \:\  \     /:/\:\  \        \:\  \
    |:|  |    /:/  \:\  \   ___  \:\  \            _\:\ \:\  \   /:/  \:\  \   _____\:\  \
    |:|  |   /:/__/ \:\__\ /\  \  \:\__\          /\ \:\ \:\__\ /:/__/ \:\__\ /::::::::\__|
  __|:|__|   \:\  \ /:/  / \:\  \ /:/  /          \:\ \:\/:/  / \:\  \ /:/  / \:\~~\~~\/__/
 /::::\  \    \:\  /:/  /   \:\  /:/  /            \:\ \::/  /   \:\  /:/  /   \:\  \
 ~~~~\:\  \    \:\/:/  /     \:\/:/  /              \:\/:/  /     \:\/:/  /     \:\  \
      \:\__\    \::/  /       \::/  /                \::/  /       \::/  /       \:\__\
       \/__/     \/__/         \/__/                  \/__/         \/__/         \/__/
            """)
            time.sleep(0.25)
            os.system("cls")
            os.system("color 7")
            print("""
                    ___           ___                    ___           ___           ___
      __           /  /\         /  /\                  /  /\         /  /\         /  /\
     |  |\        /  /::\       /  /:/                 /  /:/_       /  /::\       /  /::|
     |  |:|      /  /:/\:\     /  /:/                 /  /:/ /\     /  /:/\:\     /  /:|:|
     |  |:|     /  /:/  \:\   /  /:/                 /  /:/ /:/_   /  /:/  \:\   /  /:/|:|__
     |__|:|__  /__/:/ \__\:\ /__/:/     /\          /__/:/ /:/ /\ /__/:/ \__\:\ /__/:/ |:| /|
     /  /::::\ \  \:\ /  /:/ \  \:\    /:/          \  \:\/:/ /:/ \  \:\ /  /:/ \__\/  |:|/:/
    /  /:/~~~~  \  \:\  /:/   \  \:\  /:/            \  \::/ /:/   \  \:\  /:/      |  |:/:/
   /__/:/        \  \:\/:/     \  \:\/:/              \  \:\/:/     \  \:\/:/       |__|::/
   \__\/          \  \::/       \  \::/                \  \::/       \  \::/        /__/:/
                   \__\/         \__\/                  \__\/         \__\/         \__\/
            """)
            time.sleep(0.25)
            os.system("cls")
        os.system("color 7")
        print("You have won! Thank you for playing and well done for completing this hard chalange.")
    if done == False:
      user_input = input("Where do you want to go explorer? Enter N, E, S, or W:\n>>> ")
      print("≪━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━≫")
      time.sleep(0.3)


    if user_input.upper() == "N":
        next_room = room_list[current_room][1]
        if next_room == None:
            print("You can't go that way.")
        else:
            current_room = next_room

    elif user_input.upper() == "E":
        next_room = room_list[current_room][2]
        if next_room == None:
            print("You can't go that way.")
        else:
            current_room = next_room

    elif user_input.upper() == "S":
        next_room = room_list[current_room][3]
        if next_room == None:
            print("You can't go that way.")
        else:
            current_room = next_room

    elif user_input.upper() == "W":
        next_room = room_list[current_room][4]
        if next_room == None:
            print("You can't go that way.")
        else:
            current_room = next_room

    else:
        if done == False:
          print("That not North, East, South, or West. Try picking one of those insted of", user_input + ". \n")
          time.sleep(1)
time.sleep(5)
os.system("cls")
os.system("python adv.py")
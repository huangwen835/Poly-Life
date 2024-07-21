#S10241971K Huang Wen P14
import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    }

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5
          }
             
wall = {'shortform': 'WALL ',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3
        }

zombie = {'shortform': 'ZOMBI', 
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

vert_line_name = ["A","B","C","D","E"] #store alphabet for row

#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field(field):
    print("{:>5}{:>6}{:>6}".format(1,2,3))  #print the header of field 1,2,3                                
    for row in range(len(field)):           #print the +------....
        print(" ",end = "")
        for i in range(7):
            print("+-----",end="")
        print("+")
        print("{}|".format(vert_line_name[row]),end="")        #print the |      | of the field
        
        for col in range(len(field[row])):
            if field[row][col] != None:
                print("{}|".format(field[row][col][0]),end="")      #print the mons and unit in the field
            else:
                print("     |",end="")
        print()
        print(" |",end="")
        for col in range(len(field[row])):                         #print health of the mons and unit
            if field[row][col] != None:
                print("{:>2}/{:<2}|".format(field[row][col][1],field[row][col][2]),end="")       
            else:
                print("     |",end="")
        print()
        
    print(" ",end = "")
    for i in range(7):
        print("+-----",end="")                #print the last +------....
    print("+")
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, unit_name):
    while True:
        position = input("Place where? " )
        try:
            position = [position[0],position[1]]
            position[0] = str(position[0]).upper()
            column = int(position[1])-1
            assert position[0] in vert_line_name and column <= 7 and column >= 0                           #position input validation
            for char in range(len(vert_line_name)):
                if vert_line_name[char] == str(position[0]):
                    row = int(char)
                
            if column > 2:
                print("\nUnit can not be placed outside of the first 3 colums.")                            #check if position is outside of first 3-coloumn
                
            elif field[row][column] == None:
                field[row][column] = [unit_name['shortform'],unit_name['maxHP'],unit_name['maxHP']]      #check if position is occupied
                break
                
            else:
                print("\nCurrent position is occupied")                                                  

        except:
            print("Position not on field of place")                                                     #re-enter position if out of field

    return field

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    full = True
    while True:
        print("What unit do you wish to buy?")
        print("1. Archer (5 gold)")
        print("2. Wall (3 gold)")
        print("3. Don't buy")
        try:
            buy_choice = int(input("Your choice? "))

            assert buy_choice >= 1 and buy_choice <= 3                       #check if user select only 1 or 2 or 3
            if buy_choice == 3:                                              #end turn when user select 3
                return field
            else:
                for row in range(len(field)):
                    if full == False:
                        break
                    for col in range(3):
                        if field[row][col] == None:
                            full = False
                            break
                        else:
                            continue
                if full == True:
                    print("No position to place unit.")
                elif buy_choice == 1 and game_vars['gold'] >= 5:                #check if user got enough gold to buy archer
                    unit_name = archer
                    game_vars['gold'] -= 5                                    #deduct gold
                    break
                    
                elif buy_choice == 2 and game_vars['gold'] >= 3:             #check if user got enough gold to buy wall
                    unit_name = wall
                    game_vars['gold'] -= wall['price']                                     #deduct gold
                    break
                    
                else:
                    print("\nNot enough gold")                             #ask user to re-enter their choice when not enough gold
        except:
            print("Invalid Input")
                
    field = place_unit(field, unit_name)
    return field

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(field,game_vars):
    arc_count = 0
    zom_count = 0
    cur_dmg = 0
    got_mons = True
    for row in range(len(field)):
        dmg = 0
        arc_count = 0
        zom_count = 0
        for col in range(len(field[row])):                                   #check if archer and zombie in same row
            if field[row][col] != None:
                if field[row][col][0] == "ZOMBI":                            #check the num of archer
                    zom_count += 1
                    break
                elif field[row][col][0] == "ARCHR":
                    arc_count += 1
                    
        if arc_count >= 1 and zom_count == 1:               #when archer and zom in same row
            for item in range(arc_count):
                if game_vars['monsters_killed'] < game_vars['monster_kill_target'] and got_mons == True:               #check if zombie is alive
                    cur_dmg = 0
                    cur_dmg = random.randint(1,4)
                    print("Archer in lane {} shoots Zombie for {} damage!".format(vert_line_name[row],cur_dmg))         #cal dmg for zom

                    for item in range(len(field[row])):
                        if field[row][item] != None:
                            if field[row][item][0] == "ZOMBI":
                                field[row][item][1] -= cur_dmg                                        #zom get dmg
                                if field[row][item][1] <= 0:                                        #check if zom die, zom die give reward and remove zom
                                    field[row][item] = None
                                    got_mons = False
                                    game_vars['gold'] += zombie['reward']                          #get reward for killing zom
                                    game_vars['monsters_killed'] += 1                             #mons killed + 1
                                    print('Zombie dies!')
                                    print('You gain {} gold as a reward.'.format(zombie['reward']))
                                    if game_vars['monsters_killed'] < game_vars['monster_kill_target'] and got_mons == False:       #zom die and havent win, spawn zom
                                        spawn_monster(field, zombie)         #activate spawn mons when zom die
                                break
           
    return field,got_mons,game_vars

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(field,zombie):
    lose = False
    
    for row in range(len(field)):
        for col in range(len(field[row])):
            if field[row][col] != None:
                if field[row][col][0] == 'ZOMBI':
                    if col == 0:                                                          #check if got lose game
                        print("A Zombie has reached the city! All is lost!")
                        print('You have lost the game. :(')
                        lose = True
                        return field,lose

                    elif field[row][col-1] == None:
                        field[row][col-zombie['moves']] = [zombie['shortform'],field[row][col][1],zombie['maxHP']]         #check if zom in-front is empty
                        field[row][col] = None                                                                             #if empty move
                        print("Zombie in lane {} advances!".format(vert_line_name[row]))
                        
                    elif field[row][col-1] != None:                                                                        #if got archer and wall in-front zom,
                        if field[row][col-1][0] != 'ZOMBI':
                            mons_dmg = random.randint(zombie['min_damage'],zombie['max_damage'])                           #zom deal dmg
                            field[row][col-1][1] -= mons_dmg
                        if field[row][col-1][1] < 1:
                            field[row][col-1] = None                                                                       #remove unit when dead

    return field,lose

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, zombie):
    mon_row = random.randint(0,4)
    field[mon_row][6] = [zombie['shortform'],zombie['maxHP'],zombie['maxHP']]         #spawn zom stat and shortform name in field
    return field

#-----------------------------------------
# save_game()
#
#    Saves the game in the file
#'save.txt'
#-----------------------------------------
def save_game():         
    file = open("save.txt", "w")
    wri = ""
    
    for row in range(len(field)):                         #save field
        wri = ""
        for item in range(len(field[row])):
            wri += str(field[row][item])
            wri += '@'                       #set @ as separator
        wri = wri[:-1]                      #remove @ at the end of everyline
        file.write(wri)
        file.write("\n")
    for keys in game_vars:                                #save game variables
        file.write(str(keys))
        file.write(',')                 #set , as separator
        file.write(str(game_vars[keys]))
        file.write("\n")
    file.close              #close file
    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():
    try:
        file = open("save.txt", "r")
        counter = 0
        field = []
        game_vars = {}
        for line in file: 
            if counter <=4:                                               #extract field info
                data = line.rstrip('\n').split('@')
                for item in range(len(data)):
                    if data[item]=='None':                                  #extract None in field info
                        data[item]=None
                    else:
                        data[item] = data[item][1:-1]                        #extract unit and health
                        data[item] = data[item].rstrip('\n').split(',')
                        edit = []
                        for i in range(len(data[item])):
                            if i == 0:
                                edit.append(data[item][i][1:-1])              #extract name of unit and mons
                            else:
                                edit.append(int(data[item][i]))             #extract health of unit and mons
                        data[item] = edit
                field.append(data)
            else:
                (key,value) = line.rstrip('\n').split(',')                   #extract game variables
                game_vars[key] = int(value)
            counter += 1
    except:
        return

    return game_vars,field

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game(game_vars):
    game_vars['turn'] = 1
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10

    return game_vars
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()
# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!

out = False
while not(out):
    show_main_menu()
    game_choice = input("Your choice? ")
    if game_choice in ["1","2"]:          #start new game
        if game_choice == "1":                        
            game_vars = initialize_game(game_vars)      #when start new game, initialize the game and spawn mons
            field = spawn_monster(field,zombie)
            
        elif game_choice == "2":
            try:
                game_vars,field = load_game()      # load saved game
            except:
                print("No saved game found.")
                continue
        draw_field(field)
        
        if  game_choice == "1" or game_choice == "2":
            while True:
                got_mons = False
                print("Turn  {}".format(game_vars['turn'])) #print game variable
                print("Gold = {}   Monsters killed = {}/{}".format(game_vars['gold'],game_vars['monsters_killed'],game_vars['monster_kill_target']))

                show_combat_menu(game_vars)
                turn_choice = input("Your choice? ")

                if turn_choice == "1":
                    field = buy_unit(field, game_vars)       #buy unit
                    

                if turn_choice == "1" or turn_choice == "2":
                    field,got_mons,game_vars = defender_attack(field,game_vars)           #unit attack 
                    
                    if game_vars['monsters_killed'] < game_vars['monster_kill_target']:    
                        game_vars['turn'] += 1                   #add turn and gold
                        game_vars['gold'] += 1
                        if got_mons == True:
                            field,lose = monster_advance(field,zombie)                #if got mons on field, mons advance
                            if lose == True:                                          #when user lose
                                out = True
                                break
                        draw_field(field)
                    else:                      #when i win
                        print("You have protected the city! You win!")
                        out = True
                        break

                    
                elif turn_choice == "3":         # save game
                    save_game()
                    out = True
                    break
                    
                elif turn_choice == "4":
                    print("See you next time!")          #quit game
                    out = True
                    break
                    
                else:
                    print()
                    print("Turn choice invalid, please re-enter")        #check invalid input
                    
    elif game_choice == "3":
        print("See you next time!")         #quit game
        out = True
        break

    else:
        print()
        print("Invalid input,please re-enter")   # check invalid input
    

    
    

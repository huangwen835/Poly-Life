#S10241971K Huang Wen P14
import random

# Game variables
game_vars = {
    'turn': 1,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL','CANON','MINE']
monster_list = ['ZOMBI', 'WWOLF','SKELE']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       'level': 1
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'price': 3,
                       'level': 1
                      },
             'CANON':{'name': 'Cannon',
                       'maxHP': 8,
                       'min_damage': 3,
                       'max_damage': 5,
                       'price': 7,
                       },
             'MINE':{'name': 'Mine',
                       'maxHP': 1,
                       'damage': 10,
                       'price': 8,
                       },
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 12,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 8,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      },
            'SKELE': {'name': 'Skeleton',
                      'maxHP': 8,
                      'min_damage': 1,
                      'max_damage': 3,
                      'moves' : 1,
                      'reward': 3
                      },

                }
field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

vert_line_name = ["A","B","C","D","E"] #store alphabet for row
unit_col = 3 #store the header (unit column)
column = 6
#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field(field):
    print("    ",end='')
    for num in range(unit_col):
        print("{:<6}".format(num+1),end='')  #print the header of field 1,2,3
    print()
    for row in range(len(field)):           #print the +------....
        print(" ",end = "")
        for i in range(len(field[row])):
            print("+-----",end="")
        print("+")
        print("{}|".format(vert_line_name[row]),end="")        #print the |      | of the field
        
        for col in range(len(field[row])):
            if field[row][col] != None:
                print("{:<5}|".format(field[row][col][0]),end="")      #print the mons and unit in the field
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
    for i in range(len(field[row])):
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
    print("5. Upgrade defender")
    print("6. Magic")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Configure stat")
    print("4. Quit")

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

def place_unit(field,unit_name,defenders,vert_line_name):       
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
                
            if column >= unit_col and unit_name != 'MINE':
                print("\nUnit can not be placed outside of the first {} colums.".format(unit_col))                            #check if position is outside of first 3-coloumn
                
            elif field[row][column] == None:
                if unit_name == 'ARCHR' or unit_name == 'WALL':
                    field[row][column] = [unit_name,defenders[unit_name]['maxHP'],defenders[unit_name]['maxHP'],defenders[unit_name]['level']]      #check if position is occupied
                    break
                else:
                    field[row][column] = [unit_name,defenders[unit_name]['maxHP'],defenders[unit_name]['maxHP']]      #check if position is occupied
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
def buy_unit(field, game_vars,defender_list,defenders):
    full = True
    while True:
        print("What unit do you wish to buy?")
        print("1. Archer ({} gold)".format(defenders['ARCHR']['price']))
        print("2. Wall ({} gold)".format(defenders['WALL']['price']))
        print("3. Cannon ({} gold)".format(defenders['CANON']['price']))
        print("4. Mine ({} gold)".format(defenders['MINE']['price']))
        print("5. Don't buy")
        print("6. Go back to combat_menu")
        try:
            buy_choice = int(input("Your choice? "))
            assert buy_choice >= 1 and buy_choice <= 6                       #check if user select only 1 or 2 or 3
            if buy_choice == 5:
                return False,game_vars
            elif buy_choice == 6:
                return True,game_vars
            else:
                if buy_choice != 4:
                    for row in range(len(field)):                             #check if the field have place to insert the defender
                        if full == False:
                            break
                        for col in range(3):
                            if field[row][col] == None:
                                full = False
                                break
                            else:
                                continue
                else:
                    for row in range(len(field)):                             #check if the field have place to insert the mine
                        if full == False:
                            break
                        for col in range(len(field[row])):
                            if field[row][col] == None:
                                full = False
                                break
                            else:
                                continue
                if full == True and buy_choice != 4:
                    print("No position to place unit.")                                         
                    
                elif full == True and buy_choice == 4:
                    print("No position to place mine.")
                elif buy_choice == 1 and game_vars['gold'] >= defenders['ARCHR']['price']:               #check if user got enough gold to buy archer
                    unit_name = defender_list[0]
                    game_vars['gold'] -= defenders['ARCHR']['price']
                    break   
                elif buy_choice == 2 and game_vars['gold'] >= defenders['WALL']['price']:             #check if user got enough gold to buy wall
                    unit_name = defender_list[1]
                    game_vars['gold'] -= defenders['WALL']['price']
                    break
                
                elif buy_choice == 3 and game_vars['gold'] >= defenders['CANON']['price']:              #check if user got enough gold to buy cannon
                    unit_name = defender_list[2]
                    game_vars['gold'] -= defenders['CANON']['price']
                    break
                
                elif buy_choice == 4 and game_vars['gold'] >= defenders['MINE']['price']:             #check if user got enough gold to buy mine
                    unit_name = defender_list[3]
                    game_vars['gold'] -= defenders['MINE']['price']
                    break
                
                else:
                    print("\nNot enough gold to buy.")                             #ask user to re-enter their choice when not enough gold
        except:
            print("Invalid Input")
                
    place_unit(field, unit_name,defenders,vert_line_name)
    return False,game_vars


#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(field,game_vars,monster_list,monsters,defenders,row):
    spawn = False
    dmg = 0
    mons_died = False

    for unit in range(len(field[row])):
        if mons_died == False:
            try:
                dmg = 0
                if game_vars['monsters_killed'] < game_vars['monster_kill_target'] and (field[row][unit][0] == "ARCHR" or field[row][unit][0] == "CANON") :         #check if zombie is alive
                    if field[row][unit][0] == "CANON":
                        field = cannon_attack(row,field,monster_list)
                        
                    dmg = random.randint(defenders[field[row][unit][0]]['min_damage'],defenders[field[row][unit][0]]['max_damage']) #cal dmg for zom
                
                    for item in range(len(field[row])):
                        try:
                            assert field[row][item][0] in monster_list
                            assert item>unit
                            if field[row][item][0] == 'SKELE' and field[row][unit][0] == "ARCHR":
                                dmg = int(dmg/2)
                                field[row][item][1] -= dmg
                            else:
                                field[row][item][1] -= dmg                                             #mon get dmg
                            print("{} in lane {} shoots {} for {} damage!".format(defenders[field[row][unit][0]]['name'],vert_line_name[row],field[row][item][0],dmg))
                            if field[row][item][1] <= 0:                                        #check if zom die, zom die give reward and remove zom
                                game_vars['gold'] += monsters[field[row][item][0]]['reward']
                                game_vars['monsters_killed'] += 1
                                print('{} dies!'.format(field[row][item][0]))
                                print('You gain {} gold as a reward.'.format(monsters[field[row][item][0]]['reward']))
                                game_vars['threat'] += monsters[field[row][item][0]]['reward']
                                mons_died = True
                                field[row][item] = None
                            break
                        except:
                            continue
            except:
                continue
       
    return field,game_vars


#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_list, field, monsters,vert_line_name,defender_list,defenders,row):
    lose = False
    for col in range(len(field[row])):
        if field[row][col] != None:
            if field[row][col][0] in monster_list:
                counter = 0
                for move in range(monsters[field[row][col][0]]['moves']):
                    move += 1
                    if (col+1-move) == 0:                                                          #check if got lose game
                        print("A {} has reached the city! All is lost!".format(monsters[field[row][0][0]]['name']))
                        print('You have lost the game. :(')
                        lose = True
                        return field,lose

                    elif field[row][col-move] == None and (col-move) >= 0:
                        if counter == 0:
                            print("{} in lane {} advances!".format(monsters[field[row][col+1-move][0]]['name'],vert_line_name[row]))
                        field[row][col-move] = [field[row][col+1-move][0],field[row][col+1-move][1],field[row][col+1-move][2]]         #check if zom in-front is empty
                        field[row][col-move+1] = None                    #if empty move

                    elif (col-move) >= -2:
                        if field[row][col-move] != None:                                                                        #if got archer and wall in-front zom,
                            if field[row][col-move][0] in defender_list[0:2]:
                                mons_dmg = random.randint(monsters[field[row][col+1-move][0]]['min_damage'],monsters[field[row][col+1-move][0]]['max_damage'])                           #zom deal dmg
                                field[row][col-move][1] -= mons_dmg
                                print("{} in lane {} hits {} for {} damage!".format(monsters[field[row][col+1-move][0]]['name'],vert_line_name[row],defenders[field[row][col-move][0]]['name'],mons_dmg))
                                if field[row][col-move][1] < 1:
                                    print("{} dies!".format(field[row][col-move][0]))
                                    field[row][col-move] = None                                                                       #remove unit when dead
                                    col += 1
                                else:
                                    break
                            elif field[row][col-move][0] in monster_list: #check if mons is blocked by mons in front
                                print("{} in lane {} is bloacked from advancing.".format(monsters[field[row][col+1-move][0]]['name'],vert_line_name[row]))

                            elif field[row][col-move][0] == 'MINE':   #check if mons in front is mine
                                position = [row,col-move]
                                print("Mine has been triggered by {} and explode!".format(monsters[field[row][col+1-move][0]]['name']))
                                field = mine_attack(field,monster_list,position,defenders,vert_line_name) #mine activate
                                field[row][col-move] = None
                                break

                    counter += 1

    return field,lose

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list,monsters,column):
    while True:
        mons = random.randint(0,2)
        mon_row = random.randint(0,4)
        if field[mon_row][column] == None: #check if position is occupied
            field[mon_row][column] = [monster_list[mons],monsters[monster_list[mons]]['maxHP'],monsters[monster_list[mons]]['maxHP']] 
            break
    return field


#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game(field,vert_line_name,game_vars,defenders,monsters,unit_col):        
    file = open("save.txt", "w")
    wri = ""
    
    for row in range(len(field)):                         #save field
        wri = ""
        for item in range(len(field[row])):
            wri += str(field[row][item])
            wri += '@'
        wri = wri[:-1]
        file.write(wri)
        file.write("\n")
    file.write("break\n")
    for keys in game_vars:                                #save game variables
        file.write(str(keys))
        file.write(',')
        file.write(str(game_vars[keys]))
        file.write("\n")
    file.write("break\n")
    file.write(str(vert_line_name))
    file.write("\n")
    file.write("break\n")
    file.write(str(unit_col))
    file.write("\n")
    file.write("break\n")
    for unit in defenders:                        #save defenders
        for keys in defenders[unit]:
            file.write(str(keys))                        
            file.write(',')
            file.write(str(defenders[unit][keys]))
            file.write("\n")
        file.write("break\n")
    for mons in monsters:                           #save monsters
        for keys in monsters[mons]:
            file.write(str(keys))
            file.write(',')
            file.write(str(monsters[mons][keys]))
            file.write("\n")
        file.write("break\n")

    file.close
    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    try:
        file = open("save.txt", "r")
        counter = 0
        field = []
        game_vars = {}
        for line in file:
            if line == "break\n":
                counter += 1
                continue
            elif counter == 0:                                               #extract field info
                data = line.rstrip('\n').split('@')
                for item in range(len(data)):
                    if data[item]=='None':                                  #extract None in field info
                        data[item]=None
                    else:
                        data[item] = data[item][1:-1]                        #extract unit and health
                        data[item] = data[item].rstrip('\n').split(',')
                        item_list = []
                        for i in range(len(data[item])):
                            if i == 0:
                                item_list.append(data[item][i][1:-1])              #extract name of unit and mons
                            else:
                                item_list.append(int(data[item][i]))             #extract health of unit and mons
                        data[item] = item_list
                field.append(data)
            elif counter == 1:
                (key,value) = line.rstrip('\n').split(',')                   #extract game variables
                game_vars[key] = int(value)
                
            elif counter == 2:                  #extract vert_line_name
                data = line.rstrip('\n')
                data = data[1:-1]
                data = data.strip(' ').split(',')
                vert_line_name = []
                for i in range(len(data)):
                    if i == 0:
                        vert_line_name.append(data[i][1:-1])
                    else:
                        vert_line_name.append(data[i][2:-1])
            elif counter == 3:
                unit_col = int(line)     #extract col where unit can be placed

            elif counter == 4:
                for keys in defenders['ARCHR']:                  #extract archer stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        defenders['ARCHR'][keys] = value
                    elif key == keys:
                        defenders['ARCHR'][keys] = int(value)
                        break
                    
            elif counter == 5:
                for keys in defenders['WALL']:                     #extract wall stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        defenders['WALL'][keys] = value
                    elif key == keys:
                        defenders['WALL'][keys] = int(value)
                        break
                    
            elif counter == 6:
                for keys in defenders['CANON']:                     #extract cannon stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        defenders['CANON'][keys] = value
                    elif key == keys:
                        defenders['CANON'][keys] = int(value)
                        break
            elif counter == 7:
                for keys in defenders['MINE']:                      #extract mine stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        defenders['MINE'][keys] = value
                    elif key == keys:
                        defenders['MINE'][keys] = int(value)
                        break
            elif counter == 8:
                for keys in monsters['ZOMBI']:                     #extract zombie stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        monsters['ZOMBI'][keys] = value
                    elif key == keys:
                        monsters['ZOMBI'][keys] = int(value)
                        break        
            elif counter == 9:
                for keys in monsters['WWOLF']:                   #extract WWolf stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        monsters['WWOLF'][keys] = value
                    elif key == keys:
                        monsters['WWOLF'][keys] = int(value)
                        break
            elif counter == 10:
                for keys in monsters['SKELE']:                      #extract skele stat
                    (key,value) = line.rstrip('\n').split(',')
                    if key == 'name':
                        monsters['SKELE'][keys] = value
                    elif key == keys:
                        monsters['SKELE'][keys] = int(value)
                        break
    except:
        return

    return game_vars,field,defenders

###-----------------------------------------------------
### initialize_game()
###
###    Initializes all the game variables for a new game
###-----------------------------------------------------
##def initialize_game(game_vars):
##    game_vars['turn'] = 1
##    game_vars['monster_kill_target'] = 20
##    game_vars['monsters_killed'] = 0
##    game_vars['num_monsters'] = 0
##    game_vars['gold'] = 10
##    game_vars['threat'] = 0
##    game_vars['danger_level'] = 1
##    return game_vars
    
#-----------------------------------------------------
# upgrade_defender()
#
#    Upgrade defender
#-----------------------------------------------------
def upgrade_defender(field,game_vars,defender_list,defenders,vert_line_name):
    while True:
        price = 0
        go_back = False
        try:
            print("1. Archer     2. Wall")
            print("3. Go back to combat menu")
            
            up_unit = int(input("Enter defender to upgrade."))
            assert up_unit == 1 or up_unit == 2 or up_unit == 3
            if up_unit == 1:
                price = 6 + (2*defenders['ARCHR']['level']) 
                up_unit = 'ARCHR'
            elif up_unit == 2:
                price = 4 + (2*defenders['WALL']['level'])
                up_unit = 'WALL'
            else:
                go_back = True
                return field,go_back,defenders,game_vars
            
            while True:
                print("Price for upgarding {} to level {} is {} gold.".format(defenders[up_unit]['name'],defenders[up_unit]['level']+1,price))
                print("1. Upgrade defender  2. Dont upgrade")
                print("3. Go back to combat menu")
                try:
                    choice = int(input("Enter your choice."))
                    assert choice >= 1 and choice <= 3
                    if game_vars['gold'] >= price and choice == 1:
                        if up_unit == 'ARCHR':
                            for row in range(len(field)):              #look for all archer on field
                                for col in range(len(field[row])):
                                    if field[row][col] != None:
                                        if field[row][col][0] == up_unit:       #increase min and max dmg
                                            field[row][col][3] += 1
                            defenders[up_unit]['min_damage'] += 1
                            defenders[up_unit]['max_damage'] += 1
                            defenders[up_unit]['level'] += 1
                        else:
                            for row in range(len(field)):              #look for all wall on field
                                for col in range(len(field[row])):
                                    if field[row][col] != None:
                                        if field[row][col][0] == up_unit:
                                            field[row][col][1] += 5             #increase current and max health
                                            field[row][col][2] += 5
                                            field[row][col][3] += 1
                            defenders[up_unit]['maxHP'] += 5
                            defenders[up_unit]['level'] += 1
                            print("{} is upgraded to level {}!".format(defenders[up_unit]['name'],defenders[up_unit]['level']))
                            game_vars['gold'] -= price                                      
                        return field,go_back,defenders,game_vars
                    
                    elif game_vars['gold'] < price and choice == 1:
                        print("Not enough gold.")
                        
                    elif choice == 2:
                        return field,go_back,defenders,game_vars
                    else:
                        go_back = True
                        return field,go_back,defenders,game_vars
                except:
                    print("Invalid input of choice.")
        except:
            print("Invalid input of defender.")
            continue

#-----------------------------------------------------
# cannon_attack()
#
#    Cannon push back monster
#-----------------------------------------------------
def cannon_attack(row,field,monster_list):
    move = random.randint(0,1) #0 mean no knock back, 1 mean got knock back
    counter = 0
    if move == 1:
        for col in range(len(field[row])):
            try:
                assert field[row][col][0] in monster_list
                counter += 1
                assert col < 6 and field[row][col+1] == None and counter <= 1
                print("{} is knocked back by cannon.".format(field[row][col][0]))
                field[row][col+1] = field[row][col] #move mons back by one box
                field[row][col] = None
                break
            except:
                continue
                
    return field

#-----------------------------------------------------
# mine_attack()
#
#    Mine explode and monster around get dmg
#-----------------------------------------------------
def mine_attack(field,monster_list,position,defenders,vert_line_name):
    for row in range(3):
        if (position[0]-1+row) >= 0 and (position[0]-1+row) <= 4:
            for col in range(3):
                if (position[1]-1+col) >= 0 and (position[1]-1+col) <= 6:
                    try:
                        assert field[(position[0]-1+row)][position[1]-1+col][0] in monster_list
                        field[(position[0]-1+row)][position[1]-1+col][1] -= int(defenders['MINE']['damage'])
                        print("Mine deal {} damage to {} in lane {}.".format(int(defenders['MINE']['damage']),field[(position[0]-1+row)][position[1]-1+col][0],vert_line_name[position[0]-1+row]))
                        if field[position[0]-1+row][position[1]-1+col][1] <= 0:   #check mons got die?
                            print("{} died due to mine explosion.".format(field[(position[0]-1+row)][position[1]-1+col][0]))
                            field[position[0]-1+row][position[1]-1+col] = None           #mons remove when die
                    except:
                        continue
                    
    return field

#-----------------------------------------------------
# magic()
#
#    Player buy magic here
#-----------------------------------------------------
def magic(field,vert_line_name,game_vars,defender_list,defenders):

    go_back = False
    while True:
        print("1. Heal magic    2. Dont buy")
        print("3. Go back to combat menu")
        try:
            magic_choice = int(input("Your choice."))
            assert magic_choice == 1 or magic_choice == 2 or magic_choice == 3
            if magic_choice == 1:
                price = 5
                spell_name = 'Healing'
                
            elif magic_choice == 2:
                return field,go_back,game_vars
            else:
                go_back = True       #go back to combat menu
                return field,go_back,game_vars
            
            while True:
                print("Price for buying {} spell is {} gold.".format(spell_name,price))    #show price of magic
                print("1. Buy spell  2. Dont buy")
                print("3. Go back to combat menu")
                try:
                    choice = int(input("Enter your choice."))
                    assert choice >= 1 and choice <= 3
                    if game_vars['gold'] >= price and choice == 1:                     #check got enough gold
                        if spell_name == 'Healing':
                            game_vars['gold'] -= price
                            field = heal(field,vert_line_name,defender_list,defenders)
                            return field,go_back,game_vars
                            
                    elif game_vars['gold'] < price and choice == 1:
                        print("Not enough gold.")
                        
                    elif choice == 2:
                        return field,go_back,game_vars

                    else:
                        go_back == True
                        return field,go_back,game_vars
                    
                except:
                    print("Invalid input of choice.")
        except:
            print("Invalid input of spell.")
            continue
        
                    
    return field,go_back,game_vars

#-----------------------------------------------------
# heal()
#       Healing spell 
#       Allow all defender units in a 3x3 square to recover 5 hit points.
#-----------------------------------------------------
def heal(field,vert_line_name,defender_list,defenders):
    while True:
        position = input("Place where?" )
        try:
            position = [position[0],position[1]]
            position[0] = str(position[0]).upper()
            position[1] = int(position[1])-1
            assert position[0] in vert_line_name and position[1] <= 7 and position[1] >= 0                           #position input validation
            for char in range(len(vert_line_name)):
                if vert_line_name[char] == str(position[0]):
                    position[0] = int(char)
            for row in range(3):
                if (position[0]-1+row) >= 0 and (position[0]-1+row) <= 4:
                    for col in range(3):
                        if (position[1]-1+col) >= 0 and (position[1]-1+col) <= 6:
                            try:
                                assert field[(position[0]-1+row)][position[1]-1+col][0] in defender_list #heal only defenders
                                field[(position[0]-1+row)][position[1]-1+col][1] += 5
                                print("Healing spell heal {} health to {} in lane {}.".format(5,defenders[field[(position[0]-1+row)][position[1]-1+col][0]]['name'],vert_line_name[position[0]-1+row]))
                                if field[position[0]-1+row][position[1]-1+col][1] >= field[position[0]-1+row][position[1]-1+col][2]: #make sure current health not higher than max health
                                    field[position[0]-1+row][position[1]-1+col][1] = field[position[0]-1+row][position[1]-1+col][2]
                            except:
                                continue
            return field

        except:
            print("Position not on field of place")                                                     #re-enter position if out of field

#-----------------------------------------------------
# defenders_stat(defenders)
#    
#       Change defender stat
#-----------------------------------------------------
def defenders_stat(defenders):
    while True:
        print("1. Archer    2. Wall")
        print("3. Cannon    4. Mine")
        print("5. Go back to configue stat")

        try:
            choice = int(input("Your choice? "))
            assert choice >= 1 and choice <= 5
            if choice == 5:
                return defenders #go_back
            elif choice == 1:
                choice = 'ARCHR'
            elif choice == 2:
                choice = 'WALL'
            elif choice == 3:
                choice = 'CANON'
            else:
                choice = 'MINE'
            for key in defenders[choice]:
                try:
                    key = str(key)
                    if key != 'name' and key != 'level':
                        if key == 'maxHP':
                            while True:
                                print("Current {}: {}".format(key,defenders[choice][key]))
                                defenders[choice][key] = int(input("Enter new {} value (1 to 99): ".format(key)))
                                if defenders[choice][key] >= 1 and defenders[choice][key] <= 99:#make sure health dont exceed 99
                                    break
                                else:
                                    print("Max Health set can only be between 1 and 99 inclusively. ")
                        elif key == 'max_damage':
                            while True:
                                print("Current {}: {}".format(key,defenders[choice][key]))
                                defenders[choice][key] = int(input("Enter new {} value (equal or higher than min_damage): ".format(key)))
                                if defenders[choice][key] >= defenders[choice]['min_damage']: #make sure max dmg is higher or equal
                                    break
                                else:
                                    print("Max damage must be equal or higher than min damage")
                        else:
                            print("Current {}: {}".format(key,defenders[choice][key]))
                            defenders[choice][key] = int(input("Enter new {} value : ".format(key)))
                        
                except:
                    print("Invalid value entered")
        except:
            print("Invalid input")

#-----------------------------------------------------
# monsters_stat(monsters)
#    
#       Change monster stat
#-----------------------------------------------------
def monsters_stat(monsters):
    while True:
        print("1. Zombie    2. Werewolf")
        print("3. Skeleton")
        print("4. Go back to configue stat")

        try:
            choice = int(input("Your choice? "))
            assert choice >= 1 and choice <= 4
            if choice == 4:
                return monsters  #go back
            elif choice == 1:
                choice = 'ZOMBI'
            elif choice == 2:
                choice = 'WWOLF'
            else:
                choice = 'SKELE'
            for key in monsters[choice]:
                try:
                    key = str(key)
                    if key != 'name':       #dont change name
                        if key == 'maxHP':
                            while True:
                                print("Current {}: {}".format(key,monsters[choice][key]))
                                monsters[choice][key] = int(input("Enter new {} value (1 to 99): ".format(key)))
                                if monsters[choice][key] >= 1 and monsters[choice][key] <= 99:  #make sure health dont exceed 99
                                    break
                                else:
                                    print("Max Health set can only be between 1 and 99 inclusively. ")
                        elif key == 'max_damage':
                            while True:
                                print("Current {}: {}".format(key,monsters[choice][key]))
                                monsters[choice][key] = int(input("Enter new {} value (equal or higher than min_damage) : ".format(key)))
                                if monsters[choice][key] >= monsters[choice]['min_damage']: #make sure max dmg is higher or equal
                                    break
                                else:
                                    print("Max damage must be equal or higher than min damage")
                        else:
                            print("Current {}: {}".format(key,monsters[choice][key]))
                            monsters[choice][key] = int(input("Enter new {} value : ".format(key))) #change rest stat
                        
                except:
                    print("Invalid value entered")
            print(monsters[choice])
        except:
            print("Invalid input")

#-----------------------------------------------------
# dimension(field)
#    
#       set dimension of field
#-----------------------------------------------------
def dimension(field,vert_line_name,unit_col):
    while True:
        print("1. Set dimension for field")
        print("2. Go back to configue stat")
        try:
            choice = int(input("Your choice? "))
            assert choice == 1 or choice == 2
            if choice == 2:                             #go back to configue stat
                return field,vert_line_name,unit_col
            elif choice == 1:
                while True:
                    try:
                        row = int(input("Number of row (1-26): "))
                        col = int(input("Number of column (1-10): "))
                        unit_col = int(input("Number of column that can place defender(1-9)(Cannot be higher or same as number of column): "))
                        assert row >= 1 and row <= 26 and col >= 1 and col <= 10 and unit_col < col and unit_col >= 1 and unit_col <= 9     #ensure input correct and meet requirement
                        field = []
                        vert_line_name = []
                        for rows in range(row):
                            field_row = []
                            vert_line_name.append(chr(65+rows)) #create new vert_line_name
                            for cols in range(col):
                                field_row.append(None)        #create new field
                            field.append(field_row)
                        return field,vert_line_name,unit_col,col-1

                    except:
                        print("Invalid input")
        except:
            print("Invalid input")

#-----------------------------------------------------
# game_stat(game_vars)
#    
#       set game stat
#-----------------------------------------------------
def game_stat(game_vars):
    for key in game_vars:
        while True:
            if key == 'gold' or key == 'monster_kill_target':        #change starting gold and mons kill target
                print("Current {} is {}".format(key,game_vars[key]))
                try:
                    game_vars[key] = int(input('Enter new number for {}: '.format(key)))
                    break
                except:
                    print('Invalid input.')       #print when there is invalid input
            else:
                break
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
go_back = False
while not(out):
    show_main_menu()
    game_choice = input("Your choice? ")
    if game_choice in ["1","2"]:          #start new game
        if game_choice == "1":
##            game_vars = initialize_game(game_vars)
            field = spawn_monster(field,monster_list,monsters,column)
            
        else:
            try:
                game_vars,field,defenders = load_game(game_vars)      # load saved game
            except:
                print("No saved game found.")
                continue
        while True:
            spawn = True
            if game_vars['turn'] % 12 == 0:                     #for every 12 turn
                game_vars['danger_level'] += 1                  #danger level + 1
                monsters['ZOMBI']['maxHP'] += 1                # monster health + 1
                monsters['WWOLF']['maxHP'] += 1
                monsters['SKELE']['maxHP'] += 1
                monsters['ZOMBI']['reward'] += 1                # monster reward + 1
                monsters['WWOLF']['reward'] += 1
                monsters['SKELE']['reward'] += 1
                if monsters['ZOMBI']['maxHP'] >= 100:           #ensure that mons health does not exceed 99 and crash my field
                    monsters['ZOMBI']['maxHP'] = 99
                if monsters['WWOLF']['maxHP'] >= 100:
                    monsters['WWOLF']['maxHP'] = 99
                if monsters['SKELE']['maxHP'] >= 100:
                    monsters['SKELE']['maxHP'] = 99
                    
                print("The evil grows stronger!")
                for row in range(len(field)):                #increase all max_health for mons
                    for col in range(len(field[row])):
                        try:
                            assert field[row][col][0] in monster_list
                            field[row][col][2] += 1
                        except:
                            continue
            for row in range(len(field)):                        #check if there is mons on field 
                for col in range(len(field[row])):
                    try:
                        assert field[row][col][0] in monster_list
                        spawn = False
                        
                    except:
                        continue
            if spawn:
                field = spawn_monster(field, monster_list,monsters,column) #spawn mons when no mons on field
                
            while True: 
                if game_vars['threat'] >= game_vars['max_threat'] and game_vars['monsters_killed'] < game_vars['monster_kill_target']:
                    field = spawn_monster(field, monster_list,monsters,column) #spawn mons when threat level is equal or above 10
                    game_vars['threat'] -= 10
                else:
                    break

            draw_field(field)
            print("Turn  {:<6}Threat = [{:<10}]     Danger Level {}".format(game_vars['turn'],game_vars['threat']*"-",game_vars['danger_level'])) #print game variable
            print("Gold = {}   Monsters killed = {}/{}".format(game_vars['gold'],game_vars['monsters_killed'],game_vars['monster_kill_target']))

            show_combat_menu(game_vars)
            turn_choice = input("Your choice? ")

            if turn_choice == "1":
                go_back,game_vars = buy_unit(field, game_vars,defender_list,defenders)       #buy unit

            elif turn_choice == "5":
                field,go_back,defenders,game_vars = upgrade_defender(field,game_vars,defender_list,defenders,vert_line_name) #upgrade defender

            elif turn_choice == "6":
                field,go_back,game_vars = magic(field,vert_line_name,game_vars,defender_list,defenders) #buy magic(heal)
                
            if go_back == True:       #check if player want to go back to combat menu
                go_back = False
                continue
                
            if (turn_choice == "1" or turn_choice == "2" or turn_choice == "5" or turn_choice == "6") and go_back == False:
                for row in range(len(field)):
                    field,game_vars = defender_attack(field,game_vars,monster_list,monsters,defenders,row)         #unit attack
                    if game_vars['monsters_killed'] < game_vars['monster_kill_target']:
                        field,lose = monster_advance(monster_list, field, monsters,vert_line_name,defender_list,defenders,row)                #if got mons field, mons advance
                    if lose:
                        out = True
                        break
                if lose:                                          #when user lose
                    break

                if game_vars['monsters_killed'] < game_vars['monster_kill_target']:    
                    game_vars['turn'] += 1                   #add turn and gold
                    game_vars['gold'] += 1
                    game_vars['threat'] += random.randint(1,game_vars['danger_level'])

                else:                                               #when i win
                    print("You have protected the city! You win!")
                    out = True
                    break

                
            elif turn_choice == "3":         # save game
                save_game(field,vert_line_name,game_vars,defenders,monsters,unit_col)
                out = True
                break
                
            elif turn_choice == "4":
                print("See you next time!")          #quit game
                out = True
                break

                
            else:
                print()
                print("Turn choice invalid, please re-enter")        #check invalid input
                
    elif game_choice == "3":        #change game stat
        while True:
            print("1. Change defender stat")
            print("2. Change monster stat")
            print("3. Change dimension of board")
            print("4. Change game stat")
            print("5. Go back to main menu")

            try:
                choice = int(input("Your choice? "))
                assert choice >=1 and choice <= 5

                if choice == 1:
                    defenders = defenders_stat(defenders)
                elif choice == 2:
                    monsters = monsters_stat(monsters)
                elif choice == 3:
                    field,vert_line_name,unit_col,column = dimension(field,vert_line_name,unit_col)
                elif choice == 4:
                    game_vars = game_stat(game_vars)
                else:
                    break
            except:
                print("Invalid input")


    elif game_choice == "4":
        print("See you next time!")         #quit game
        out = True
        break

    else:
        print()
        print("Invalid input,please re-enter")   # check invalid input
        

"""
General plant management functions related to and for use by the Bamboo application.

Notes:
open: bool (whether or not memory should be opened by the function)
plant_name: str (the plant name of which to use (usually plant_name=None and defaults to the current plant))
series: list

Use of global variable terminal throughout many functions, altered in Main and used to mark whether or not the runtime is in pure terminal mode.
"""

import random
import datetime
import string

import Utilities
import Memory
import Screen

#Save specific visual of plant, allow user to reset it if they don't think it turned out good. FIll in information for each plant
#Store of the plant visual, replacing the blocks with a temporary symbol that can be written
#Phyla and class information, watering information, user's name for it, and more per each plant
#Fire animation eventually? Side command just for fun. Possibly make it more fire-placey. Change color to red. Brightness of full characters diminishes out
#Remember, watering reminders and possibly some other interactive features?

#Continue on with testing the Command that was just created and checking how it stores information and whether or not it asks correctly when a plant is set
#Also continue with function plantinformation, make it so that it creates the whole visual list of information that will eventually be display on screen
#Verify that the plant age is calculated correctly

terminal = False

def plantdisplay(size=2, plant_name=None):
    """
    Generates the display to be sent to the Main module of varying sizes.
    Prompts user if no (real) current plant is set in memory.

    size: int (0-2, 2 being the largest)
    plant_name defaults to current plant

    return: list (size == 2) or str (size in (0,1))

    *Opens memory.
    """
    Memory.memory.open()
    if not plant_name:
        plant_name = getcurrentplant()
        #Original Behavior (without getcurrentplant having backup in place):
        #Check to make sure the currentplant actually exists
        try:
            Memory.mu.lfm(['plants',plant_name])
        except:
            return Screen.sizedependentmessage('Unknown Current Plant', size)
            #if size == 2:
            #    return "Please Change Current Plant" + Utilities.empty(size)[27:]
            #else:
            #    return ["Please Change Current Plant" + Utilities.empty(size)[0][27:]] + Utilities.empty(size)[1:]

    final = [''] * 17

    plant = getplantvisual(plant_name)
    spacing = [' '] * 17
    level = waterlevelvisual(getwaterlevel(plant_name))

    if size in [0, 1]:
        Memory.memory.close()
        for index in range(17):
            final[index] += plant[index] + spacing[index] + level[index]
    if size == 1:
        return Utilities.centerlist(final, 50)
    elif size == 0:
        return Utilities.centerlist(final, 33)

    information = plantinformation(plant_name)

    Memory.memory.close()

    for index in range(17):
        final[index] += plant[index] + spacing[index] + level[index] + spacing[index] + information[index]

    display = ''.join(final)

    #Continue with making sure different sizes work for this function
    #Open in different functions?
    #Plant_name default to current plant in different functions?

    return display

def createplant(height, branch_amount=None, potted=True, special_character=False):
    '''
    Creates a plant visual with branches and leaves, with the height determining the maximum height, including the pot if 'potted' is True.
    Variable 'branch_amount' determines the *approximate* amount of branches that will be created.
    If 'potted' is True, a pot will be added on at the bottom.
    With 'special_character', returns the plant using special box-shaped characters.

    height: int (>= 6)
    branch_amount: int (~)
    potted: bool
    special_character: bool

    return: list

    *Can use special characters.
    '''
    #Adjust for pot of height 4
    if potted:
        height = height - 4
    #Minimum height is 6
    if height < 6:
        height = 6
    branches = [[],[]]
    for side in range(2):
        #The maximum number should be height/2-1 (to adjust for there being no branches on the top or bottom), which is accounted for by randrange instead of randint
        #The random statement in the following is for the amount of branches on the side of either left or right
        for branch_index in range(random.randrange(1,int(height/3))):
            #Would be height-2 (to adjust for there being no branches at the top and for index offset) as the maximum, but randrange makes only -1 necessary
            #The random statement in the following is for the location of the branch_index
            possible_location = random.randrange(2,height-2)
            #need to break
            ntb = False
            attempted_locations = []
            while True:
                #need to continue
                ntc = False
                for created_branch in branches[side]:
                    if possible_location in [created_branch,created_branch-1,created_branch+1,created_branch-2,created_branch+2]:
                        ntc = True
                        break
                if ntc:
                    attempted_locations.append(possible_location)
                    if set(attempted_locations + branches[side]) == set(range(2,height-2)):
                        ntb = True
                        break
                    while possible_location in attempted_locations:
                        possible_location = random.randrange(2,height-2)
                    continue
                break
            if ntb:
                break
            #Original behavior: branches[side][branch_index] = possible_location
            branches[side].append(possible_location)
            if branch_amount:
                branch_count = 0
                for branch_side in range(2):
                    branch_count += len(branches[branch_side])
                if branch_count >= branch_amount/2:
                    break

    stalk_list = ['']*height

    stalk_list[0] = '▓▓▓▓'

    last_type = 0

    type_dictionary = {'▓▓▓▓': 0, '▓▓▓ ': 1, ' ▓▓▓': 2, '▓▓  ': 3, ' ▓▓ ': 4, '  ▓▓': 5}

    for index in range(1,height):
        if last_type in [0,1,2,4]:
            #section index
            si = random.randrange(0,4)
            #Some lists have multiple of the same one, to increase the odd of that one (specifically _%%_)
            if last_type == 0:
                possibilities = [' ▓▓ ', '▓▓▓ ', ' ▓▓▓', ' ▓▓ ']
            elif last_type == 1:
                possibilities = ['▓▓▓▓', ' ▓▓ ', '▓▓  ', ' ▓▓ ']
            elif last_type == 2:
                possibilities = ['▓▓▓▓', ' ▓▓ ', '  ▓▓', ' ▓▓ ']
            elif last_type == 4:
                possibilities = ['▓▓▓ ', ' ▓▓▓', '▓▓▓▓', ' ▓▓ ']
            #section type
            st = possibilities[si]
        elif last_type in [3,5]:
            si = random.randrange(0,2)
            if last_type == 3:
                possibilities = ['▓▓  ', '▓▓▓ ']
            elif last_type == 5:
                possibilities = ['  ▓▓', ' ▓▓▓']
            st = possibilities[si]
        stalk_list[index] = st
        last_type = type_dictionary[st]

    stalk_list = stalk_list[::-1]

    stalk_list[1] = ' ▓▓ '

    if random.randrange(0,2):
        stalk_list[0] = ' ▓  '
    else:
        stalk_list[0] = '  ▓ '

    # _%%_ -> %%%_ or _%%% or _%%_
    # %%%_ -> %%%% or _%%_ or %%__
    # _%%% -> %%%% or _%%_ or __%%
    # %%%% -> %%%_ or _%%% or %%%%
    # %%__ -> %%%_
    # __%% -> _%%%

    #Original behavior
    #Not including end curve
    #branch_length = int((width-5)/2)

    created_branches = [[[x]*3 for x in ([0] * len(branches[0]))], [[x]*3 for x in ([0] * len(branches[1]))]]

    total_index = 0

    for side in range(2):
        for item in branches[side]:
            top_value = random.randrange(0,2)
            middle_value = random.randrange(7,11)
            bottom_value = random.randrange(0,2)
            created_branches[side][total_index][0] = ('▓' * top_value) + (' ' * random.randrange(2, middle_value - top_value - 1)) + '▓'
            created_branches[side][total_index][1] = '▓' * middle_value
            created_branches[side][total_index][2] = ('▓' * bottom_value) + (' ' * random.randrange(2, middle_value - bottom_value - 1)) + '▓'
            while len(created_branches[side][total_index][0]) == len(created_branches[side][total_index][2]):
                created_branches[side][total_index][2] = ('▓' * bottom_value) + (' ' * random.randrange(2, middle_value - bottom_value - 1)) + '▓'
            for part in range(3):
                created_branches[side][total_index][part] = created_branches[side][total_index][part] + (' ' * (10-len(created_branches[side][total_index][part])))
            if not side:
                for part in range(3):
                    created_branches[side][total_index][part] = created_branches[side][total_index][part][::-1]
            total_index += 1
        total_index = 0

    #This generates the actual visual of the branches in the form of [[top of branch, middle of branch, bottom of branch], [...,...,...],...]
    #DECIDED AGAINST (instead, leaves can be almost anywhere on a branch) Does this actually look good? Make the middle one droop down into the bottom one, adding a space and making sure it lines up correctly with the middle
    #ALTERNATIVE TAKEN (move the branch back into the stalk) Make sure it is a solid connection between the branch and the stalk, filling in empty pixels
    #DONE Maybe also add varying poking up and down from the middle of the branch>
    #CANCLED Randomized drooping down length
    #CANCELED Something like this?
    #...
    #.....
    #..   .
    #     .

    #ALTERNATE TAKEN (spaces manually added instead) To center on the far left or right of either side, use Utilities and have the center at the farthest point closest to the stalk

    #section_list will have top be index 0
    section_list = [[x for x in ['']*height] for side in range(2)]

    for side in range(2):
        branch = 0
        for index in range(height):
            if index in branches[side]:
                section_list[side][index] = created_branches[side][branch][1]
            elif index in [branch_location-1 for branch_location in branches[side]]:
                section_list[side][index] = created_branches[side][branch][0]
            elif index in [branch_location+1 for branch_location in branches[side]]:
                section_list[side][index] = created_branches[side][branch][2]
                branch += 1
            else:
                section_list[side][index] = ' ' * 10

    plant_list = [''] * height
    for index in range(height):
        for side in range(2):
            plant_list[index] += section_list[side][index]
            if not side:
                last_index = 3
                if not section_list[side][index].isspace():
                    for _ in range(2):
                        if stalk_list[index][0].isspace():
                            stalk_list[index] = stalk_list[index][1:]
                            section_list[side][index] = ' ' + section_list[side][index]
                            last_index -= 1
                    #Original behavior: stalk_list[index] = '▓▓' + stalk_list[index][2:4]
                if not section_list[1-side][index].isspace():
                    for _ in range(2):
                        if stalk_list[index][last_index].isspace():
                            stalk_list[index] = stalk_list[index][:last_index]
                            section_list[1-side][index] = section_list[1-side][index] + ' '
                            last_index -= 1
                    #Original behavior: stalk_list[index] = stalk_list[index][:2] + '▓▓'
                plant_list[index] += stalk_list[index]

    #Original behavior: plant_list = Utilities.centerlist(plant_list, width)

    if potted:
        plant_list.append(' '*7 + '▒'*10 + ' '*7)
        plant_list.append(' '*6 + '▒'*12 + ' '*6)
        plant_list.append(' '*7 + '▒'*10 + ' '*7)
        plant_list.append(' '*8 + '▒'*8 + ' '*8)

    plant_list = Utilities.centerlist(plant_list, 24)

    if not special_character:
        for index,row in enumerate(plant_list):
            new_row = row.replace('▓', '3').replace('▒', '2').replace(' ', '0')
            plant_list[index] = new_row

    return plant_list

#Plant's name,

def waterlevelvisual(percent_full):
    """
    Generates a visual representation of the water level for a plant based on the value entered given.

    percent_full: int (0-100)

    return: list

    *Uses special characters.
    """
    level_amount = round((percent_full / 100) * 15)

    fill_list = [''] * 15

    for index in range(15):
        if index < level_amount:
            fill_list[14-index] = '▓▓▓▓▓'
        else:
            fill_list[14-index] = '     '

    fill_list = Utilities.box(fill_list)

    return fill_list

def refill(plant_name=None, open=False):
    """
    Refills the given plant's water level back to full in memory.

    plant_name defaults to current plant

    *Can open memory and memory should be open.
    """
    if open:
        Memory.memory.open()
    if not plant_name:
        plant_name = getcurrentplant()
    #Timezone does not matter because the difference between two times is all that is necessary
    now = datetime.datetime.now().isoformat()
    #Causes an error if the plant does not exist
    Memory.mu.lfm(['plants',plant_name])
    #Refill the water level information used by getwaterlevel back to full (100%)
    Memory.mu.atm(['plants',plant_name,'lastrefill'], now)
    if open:
        Memory.memory.close()

def askplant(plant_name=None):
    """
    Asks for the plant information of a specific plant, such as name and type.

    plant_name defaults to current plant

    return: dict (also put in memory)
    """
    global terminal

    #Ask plant information, such as name from user and some information specific to the plant, like type and more for fun
    if not plant_name:
        plant_name = getcurrentplant()

    if not terminal: Screen.inputscreen("Plant Information")

    name = input("Give the plant a name: ")
    type = input("Give the name of the plant type itself: ")
    kingdom = input("Kingdom (Plantae): ")
    order = input("Order: ")
    family = input("Family: ")
    subfamily = input("Subfamily: ")
    animals = input("List some animals that eat the plant (animal, animal, etc.): ")
    description = input("Describe the plant: ")
    while True:
        age = input("Give the approximate age in months: ")
        if age.isdecimal():
            age = int(age)
            break
    while True:
        interval = input("Give the interval by which the plant needs to be watered in days: ")
        if interval.isdecimal():
            interval = int(interval)
            break

    pc = plantcode()
    pbc = plantbarcode()
    visual = createplant(17, 5)

    now = datetime.datetime.now().isoformat()

    plant_dictionary = {'Name': name, 'Type': type, 'Kingdom': kingdom, 'Order': order, 'Family': family, 'Subfamily': subfamily, 'Animals': animals, 'Description': description, 'Age': (now,age), 'Interval': interval, 'PC': pc, 'PBC': pbc, 'Visual': visual}

    Memory.mu.atm(['plants',plant_name,'information'], plant_dictionary)

    return plant_dictionary

def plantinformation(plant_name=None):
    """
    Generates the plant information card by calculating age and setting up the layout using the stored information.

    plant_name defaults to current plant.

    return: list [str]
    """
    if not plant_name:
        plant_name = getcurrentplant()

    #68 width, 17 height
    information_list = [' ' * 66] * 15

    information = Memory.mu.lfm(['plants',plant_name,'information'])

    past_age = information['Age'][1]
    time_recorded = datetime.datetime.fromisoformat(information['Age'][0])

    now = datetime.datetime.now()
    difference = now - time_recorded
    difference = difference.total_seconds()
    #Converts to months
    difference = difference / 60 / 60 / 24 / 30.4375

    age = past_age + difference
    age = round(age, 2)

    pbc = characterconversion(information['PBC'])

    animals = Utilities.divideup('Animals: ' + information['Animals'], 33)[:2]
    if len(animals) == 1:
        animals.append('')
    description = Utilities.divideup('Description: ' + information['Description'], 33)[:2]
    if len(description) == 1:
        description.append('')

    information_list[1] = 'Plant Information Card (PIC)'.center(66)
    information_list[3] = f'Name: {information["Name"]}'.center(22) + f'Type: {information["Type"]}'.center(22) + f'Age: {age}'.center(22)
    information_list[5] = f'Kingdom: {information["Kingdom"]}'.center(33) + description[0].center(33)
    information_list[6] = f'Order: {information["Order"]}'.center(33) + description[1].center(33)
    information_list[7] = f'Family: {information["Family"]}'.center(33) + animals[0].center(33)
    information_list[8] = f'Subfamily: {information["Subfamily"]}'.center(33) + animals[1].center(33)

    information_list[10] = 'Plant Identifier Barcode (PIB):'.center(33) + 'Plant Database Code (PDC):'.center(33)
    information_list[11] = pbc[0].center(33) + (' ' * 33)
    information_list[12] = pbc[1].center(33) + information['PC'].center(33)
    information_list[13] = pbc[2].center(33) + (' ' * 33)

    information_list = Utilities.box(information_list)

    #Continue with forming the right side of the screen
    #Barcode:
    #HM  L M...
    #HM  L M...
    #HM  L M...
    #... randomly generated (make function, like PC) (list? probably, one for each row) width height?
    #Fixed sized, use letters (not necessarily HML) because it should be saved in the dictionary, convert it to visual later. This and PC on bottom
    #Barcode left, PC right. Center using 33 (probably?)
    #Card format

    #index = 0
    #for character in name:
        #information_list[index] = Utilities.sir(information_list[index], 1)

    return information_list

def plantcode():
    """
    Generates a random set of letters and numbers of length 25.

    return: str
    """
    pc = ''
    possible_characters = string.ascii_letters + string.digits

    for _ in range(25):
        pc += possible_characters[random.randrange(62)]

    return pc

def plantbarcode():
    """
    Generates a barcode-like string in the following format:
    01023
    01023
    01023
    Height of 3, length of 30

    return: list [str]
    """
    pbc = [''] * 3
    possible_characters = '0123'

    for _ in range(30):
        pbc[0] += possible_characters[random.randrange(4)]

    pbc[1], pbc[2] = pbc[0], pbc[0]

    return pbc

def characterconversion(series):
    """
    Accepts plantbarcode output stored in memory and converts it to a visual representation of a barcode with increasing magnitude in numbers leading brighter characters.

    return: list
    """
    converter = {'0': ' ', '1': '░', '2': '▒', '3': '▓'}
    new_series = [''] * len(series)
    for index,row in enumerate(series):
        new_row = ''
        for character in row:
            new_row += converter[character]
        new_series[index] = new_row
    return new_series

def getcurrentplant(open=False):
    """
    Gets the current plant from memory and returns it.
    If one does not exist, it prompts the user.

    return: str

    *Memory can be opened by the function or should be opened already.
    """
    global terminal
    #Already has back up in place
    #Memory.mu.atm happens no matter what in refill, check beforehand
    if open:
        Memory.memory.open()
    try:
        plant = Memory.mu.lfm(['currentplant'])
        Memory.mu.lfm(['plants', plant])
    except:
        #plant_name
        #if not terminal: Screen.inputscreen("Plant Name")
        #setcurrentplant(input("Plant: "))
        #return getcurrentplant()
        if open:
            Memory.memory.close()
        return None
    if open:
        Memory.memory.close()
    return plant

def getplantvisual(plant_name=None):
    """
    Gets a converted version of the plant visual stored in memory.

    plant_name defaults to current plant.

    return: list
    """
    if not plant_name:
        plant_name = getcurrentplant()

    visual = Memory.mu.lfm(['plants',plant_name,'information','Visual'])
    visual = characterconversion(visual)
    return visual

def setcurrentplant(plant_name, open=False):
    """
    Sets the current plant to another plant.
    If a plant of the given name does not exist, it asks the user whether or not a new plant should be created.

    plant_name is required.

    *Memory can be opened or should be open.
    """
    if open:
        Memory.memory.open()
    try:
        Memory.mu.lfm(['plants',plant_name])
    except:
        if not terminal: Screen.inputscreen("Create Plant")
        yes_or_no = input("That plant does not seem to exist in memory yet. Would you like to create it (y/n)? ")
        if not yes_or_no.lower() in ['yes','y']:
            if open:
                Memory.memory.close()
            return
        askplant(plant_name)
    Memory.mu.atm(['currentplant'], plant_name)
    if open:
        Memory.memory.close()

def getwaterlevel(plant_name=None):
    """
    Gets the last refill date and refill interval from memory.
    Calculates the water level for a certain plant.

    plant_name defaults to current plant.

    return: int (usually goes into waterlevelvisual function)

    *Memory should be open.
    """
    #Get last recorded water level and date + time for that water level.
    #Calculate approximate depletion using a specified linear rate.
    #Determine new water level, return that.
    if not plant_name:
        plant_name = getcurrentplant()

    now = datetime.datetime.now()

    try:
        last_refill = Memory.mu.lfm(['plants',plant_name,'lastrefill'])
    except:
        return 0
    last_refill = datetime.datetime.fromisoformat(last_refill)

    interval = Memory.mu.lfm(['plants',plant_name,'information','Interval'])
    interval = datetime.timedelta(days=interval).total_seconds()

    difference = now - last_refill
    difference = difference.total_seconds()

    #Originaly using 5 days as full depletion time (datetime.timedelta(days=5).total_seconds())
    fraction = difference / interval
    fraction = fraction * 100
    fraction = int(fraction)

    percent = 100 - fraction
    return percent

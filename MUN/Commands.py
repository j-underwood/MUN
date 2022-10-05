"""
Commands gives the function equivalent of the mechanics that each command entered into the Main running program should result in.

Note:
arguments: list
screen_list: list

Use of global variable terminal throughout many functions, altered in Main and used to mark whether or not the runtime is in pure terminal mode.
"""

import time
import subprocess

import Cloud
import Utilities
import Memory
import Bamboo
import Screen
import Fire
import Codebit

#help file location
hfl = "C:\\Users\\jacob\\OneDrive\\Desktop\\Project\\MUN\\Help.txt"

#cached help
ch = None

#current theme
ct = 'normal'

#error delay time
#edt = 2

#clipboard file location
cbfl = 'C:\\Users\\jacob\\OneDrive\\Desktop\\Project\\MUN\\Clipboard.txt'

#Open is not necessary for retrieve (and import of Memory established cmdf already)
#current input
ci = Memory.memory.retrieve(['currentuser']) + "→"

#Instead of using int(), dictionary of '0':0, etc.?

terminal = False

def set(screen_list, arguments):
    """
    Changes index of screen to a specific application.

    arguments:
    0: name, 1: index

    *Modifies screen_list.
    """
    #cal check
    calc = cal(arguments, 2)
    if calc: return calc
    cwic = cwi(arguments, [1])
    if cwic: return cwic
    csbc = csb(arguments, [1])
    if csbc: return csbc
    if arguments[0] == 'cloud':
        screen_list[arguments[1]] = Cloud.weatherdisplay
    elif arguments[0] == 'bamboo':
        screen_list[arguments[1]] = Bamboo.plantdisplay
    elif arguments[0] == 'codebit':
        screen_list[arguments[1]] = Codebit.codebitdisplay
    elif arguments[0] == 'empty':
        screen_list[arguments[1]] = Utilities.empty
    elif arguments[0] == 'none':
        screen_list[arguments[1]] = None
    else:
        return error(arguments[0], "It is not a valid application name")
    Utilities.fixlist(screen_list)
    return 'reload'

def switch(screen_list, arguments):
    """
    Switches two applications at different indices.

    arguments:
    0: first index, 1: second index

    *Modifies screen_list.
    """
    calc = cal(arguments, 2)
    if calc: return calc
    cwic = cwi(arguments, [0, 1])
    if cwic: return cwic
    csbc = csb(arguments, [0, 1])
    if csbc: return csbc
    screen_list[arguments[0]], screen_list[arguments[1]] = screen_list[arguments[1]], screen_list[arguments[0]]
    Utilities.fixlist(screen_list)
    return 'reload'

def cloud(arguments):
    """
    Deals with weather related commands, such as changing a display mode.

    arguments:
    Mode: switches the mode the mini-applications of Cloud are in
    1: 0/daily or 1/hourly

    *Accesses Cloud module global variables.
    """
    global terminal

    calc = cal(arguments, 1)
    if calc: return calc
    if arguments[0] == 'mode':
        calc = cal(arguments, 2)
        if calc: return calc
        if arguments[1] in ['0','1']:
            arguments[1] = int(arguments[1])
            Cloud.display_mode = arguments[1]
        elif arguments[1] == 'daily':
            Cloud.display_mode = 0
        elif arguments[1] == 'hourly':
            Cloud.display_mode = 1
        else:
            return error(arguments[1], "It is not 0/daily or 1/hourly")
        return 'reload'
    else:
        return error(arguments[0], "It is not a valid sub-command")

def memory(arguments):
    """
    Commands that have to do with memory and storage, such as deleting or accessing information.

    arguments:
    Set: sets new information at a specific place in memory.
    1: memory location (keys separated by underscores), 2: information

    Get: gets the information stored at a specific place in memory.
    Delete: deletes the information at a specific place in memory.
    The above two have the same arguments.
    1: memory location (keys separated by underscores)

    Length: returns the length (in bytes/characters) of the MDF.
    1: total/user (by all information or only the current user's information)
    Structure: returns a dictionary of all keys in memory, good for understanding the locations of different pieces of information.

    *Opens memory.
    """
    global terminal

    calc = cal(arguments, 1)
    if calc: return calc
    if arguments[0] == 'length':
        calc = cal(arguments, 2)
        if calc: return calc
        Memory.memory.open()
        if arguments[1] == 'total':
            memory_length = len(str(Memory.memory.cmdf))
        elif arguments[1] in ['current_user','current user','user']:
            memory_length = len(str(Memory.memory.cmdf['users'][Memory.mu.name]))
        Memory.memory.close()
        return f"display|Current memory length in bytes: {memory_length}."
        #if not terminal: input("Press enter to continue.")
    elif arguments[0] == 'get':
        calc = cal(arguments, 2)
        if calc: return calc
        arguments[1] = arguments[1].split('_')
        for index, argument in enumerate(arguments[1]):
            if argument[0] == '~' and argument[1:].isdecimal():
                arguments[1][index] = int(argument[1:])
        try:
            information = Memory.mu.lfm(arguments[1], True)
        except:
            return error(arguments[1], "This does not lead to a valid location in memory")
        Utilities.propertextdisplay([f'Memory Information at {arguments[1]}'[:101].center(101), str(information)], 35, 101, not terminal, not terminal)
        #print(information)
        #if not terminal: input("Press enter to continue.")
        return
    elif arguments[0] == 'set':
        calc = cal(arguments, 3)
        if calc: return calc
        arguments[1] = arguments[1].split('_')
        for index, argument in enumerate(arguments[1]):
            if argument[0] == '~' and argument[1:].isdecimal():
                arguments[1][index] = int(argument[1:])
        #Memory.mu.atm would just make the location if it did not already exist
        #try:
        Memory.mu.atm(arguments[1], arguments[2], True)
        #except:
        #    error(arguments[2:], "This does not lead to a valid location in memory")
        #    return
        return 'reload'
    elif arguments[0] == 'delete':
        calc = cal(arguments, 2)
        if calc: return calc
        arguments[1] = arguments[1].split('_')
        for index, argument in enumerate(arguments[1]):
            if argument[0] == '~' and argument[1:].isdecimal():
                arguments[1][index] = int(argument[1:])
        Memory.memory.open()
        if not terminal: Screen.inputscreen("Delete Information")
        try:
            answer = input(f"Are you sure you want to delete the following information: '{Memory.mu.lfm(arguments[1])}'? ")
        except:
            return error(arguments[1], "This does not lead to a valid location in memory")
        if answer.lower() not in ['yes', 'y']:
            return
        Memory.mu.rfm(arguments[1])
        Memory.memory.close()
        return 'reload'
    elif arguments[0] == 'structure':
        #if not terminal: Screen.inputscreen('Memory Structure')
        Memory.memory.open()
        #structure = Utilities.keydictionary(Memory.memory.cmdf['users'][Memory.mu.name])
        structure = Utilities.keydictionary(Memory.memory.retrieve(['users', Memory.mu.name]))
        Memory.memory.close()
        #print(structure)
        Utilities.propertextdisplay(['Memory Structure'.center(101), str(structure)], 35, 101, not terminal, not terminal)
        #Memory cut off?
        #if not terminal: input("Press enter to continue.")
        return
    elif arguments[0] == 'move':
        calc = cal(arguments, 3)
        if calc: return calc

        for argument_index in range(1, 3):
            arguments[argument_index] = arguments[argument_index].split('_')
            for index, argument in enumerate(arguments[argument_index]):
                if argument[0] == '~' and argument[1:].isdecimal():
                    arguments[1][index] = int(argument[1:])

        Memory.memory.open()
        try:
            #Would not interfere with a memory location called 'remove' as that would be in a list because of the above split
            if 'remove' in arguments:
                information = Memory.mu.rfm(arguments[1])
            else:
                information = Memory.mu.lfm(arguments[1])
        except:
            return error(arguments[1], 'This does not lead to a valid location in memory')
        Memory.mu.atm(arguments[2], information)

        Memory.memory.close()
        return 'reload'
    else:
        return error(arguments[0], "It is not a valid sub-command")

def save(screen_list):
    """
    Stores information in memory, such as the open applications and the current theme.

    No arguments necessary.

    *Needs to be updated with additions.
    """
    global ct
    #global edt
    global terminal

    screen_name_list = [None, None, None, None]
    for index, item in enumerate(screen_list):
        try:
            item = str(item).split()[1]
        except:
            pass
        screen_name_list[index] = item
        #if item == 'weatherdisplay':
        #    screen_name_list[index] = 'cloud'
        #elif item == 'plantdisplay':
        #    screen_name_list[index] = 'bamboo'
        #elif item == 'codebitdisplay':
        #    screen_name_list[index] = 'codebit'
        #elif item == 'empty':
        #    screen_name_list[index] = 'empty'
        #elif item == None:
        #    screen_name_list[index] = 'none'
    Memory.memory.open()
    Memory.mu.atm(['currentscreen'], screen_name_list)
    Memory.mu.atm(['currentweathermode'], Cloud.display_mode)
    Memory.mu.atm(['currenttheme'], ct)
    #if not terminal: Memory.mu.atm(['errordelaytime'], edt)
    Memory.memory.close()

def load(screen_list):
    """
    Loads information from memory, such as the applications that were last saved and the theme that was being used.

    No arguments necessary.

    *Modifies screen_list.
    *Needs to be updated with additions.
    *Opens memory.
    """
    Memory.memory.open()
    try:
        screen_name_list = Memory.mu.lfm(['currentscreen'])
        Cloud.display_mode = Memory.mu.lfm(['currentweathermode'])
        theme([Memory.mu.lfm(['currenttheme'])])
        #delay([Memory.mu.lfm(['errordelaytime'])])
    except:
        pass
    else:
        for index, item in enumerate(screen_name_list):
            if item == 'weatherdisplay':
                screen_list[index] = Cloud.weatherdisplay
            elif item == 'plantdisplay':
                screen_list[index] = Bamboo.plantdisplay
            elif item == 'codebitdisplay':
                screen_list[index] = Codebit.codebitdisplay
            elif item == 'empty':
                screen_list[index] = Utilities.empty
            elif item == None:
                screen_list[index] = None
    finally:
        Memory.memory.close()
        return 'reload'

def user(arguments):
    """
    Deals with tasks related to the current user, such as deletion and renaming.

    arguments:
    Rename: renames the current user to the given input.
    1: new name of user.
    Delete: deletes the current user.
    List: lists all user names.

    *Opens memory.
    """
    global terminal

    calc = cal(arguments, 1)
    if calc: return calc
    if arguments[0] == 'rename':
        calc = cal(arguments, 2)
        if calc: return calc
        if not terminal: Screen.inputscreen('Rename')
        if not Utilities.confirmation('It will cause MUN to restart'): return
        #new_name = input("New name: ")
        Memory.memory.open()
        #Also deletes the information
        all_information = Memory.memory.remove(['users', Memory.mu.name])
        Memory.memory.store(['users', arguments[1]], all_information)
        Memory.memory.close()
        #Switch should always occur before restart because restart includes switch after, which means an alternative should be available for before
        return f'restart|`noswitch|False|True~switch|{arguments[1]}'
        #Needs to be able to restart the program with the current user being set to the new name
        #How does this work with the restart function in Main and the new login command established in Main
    elif arguments[0] == 'delete':
        if not terminal: Screen.inputscreen('Delete')
        if not Utilities.confirmation('It will lead to the deletion of this user account'): return
        Memory.memory.remove(['users', Memory.mu.name], True)
        #user = input('User: ')
        return f'restart|None|False|False'
    elif arguments[0] == 'list':
        listinformation('User', ['users'], user_based=False)
        return
    else:
        return error(arguments[0], "It is not a valid sub-command")

def location(arguments):
    """
    Updates the current location of the current user.

    arguments:
    Set: sets the current location.
    1: name of location
    List: lists all locations in memory for the user.

    *Opens memory.
    """
    calc = cal(arguments, 1)
    if calc: return calc
    if arguments[0] == 'set':
        calc = cal(arguments, 2)
        if calc: return calc
        Cloud.updatecurrentlocation(arguments[1], True)
        return 'reload'
    elif arguments[0] == 'list':
        listinformation('Location', ['locations'])
        return
    else:
        return error(arguments[0], 'It is not a valid sub-command')

def theme(arguments):
    """
    Updates the color of the command line.

    arguments:
    0: name of theme (see theme_dictionary)

    *Runs a subprocess with shell=True.
    """
    global ct

    calc = cal(arguments, 1)
    if calc: return calc

    theme_dictionary = {'night': '04', 'code': '0a', 'bright': '0f', 'normal': '07'}

    try:
        color = theme_dictionary[arguments[0]]
    except:
        return error(arguments[0], "It is not a valid theme name")
    ct = arguments[0]
    subprocess.run(['color',color], shell=True)

def fire(arguments):
    """
    Displays a fire animation for the user with different additions depending on the user input.

    arguments:
    smoke: if added, smoke will come up from the fire.
    fireplace: if added, a fireplace structure will be displayed around the fire.
    Both can be added together and the two additions will combine.

    *Changes the color to red temporarily.
    """
    if terminal:
        print('You can not perform this command in terminal mode.')
        return

    smoke = 'smoke' in arguments
    full = 'fireplace' in arguments

    Fire.fireplace(smoke, full)

    theme([ct])

def bamboo(arguments):
    """
    General commands related to the Bamboo application interface.

    arguments:
    Set: sets the current plant that is to be displayed.
    Water: waters the plant, bringing the water level back to full.
    Delete: deletes the plants given.
    Regenerate: remake the plant visual, randomly generating a new one.
    The above four have the same argument.
    1: plant name

    List: lists all plant names in memory.

    *Opens memory.
    """
    #For water and delete, if no plant name provided, do current plant
    calc = cal(arguments, 1)
    if calc: return calc

    if arguments[0] == 'set':
        calc = cal(arguments, 2)
        if calc: return calc
        Bamboo.setcurrentplant(arguments[1], True)
        return 'reload'
    elif arguments[0] == 'water':
        if len(arguments) == 1:
            Bamboo.refill(open=True)
            return 'reload'
        elif arguments[1] == '':
            Bamboo.refill(open=True)
            return 'reload'
        try:
            Bamboo.refill(arguments[1], True)
        except:
            return error(arguments[1], "No plant of such name exists")
        return 'reload'
    elif arguments[0] == 'delete':
        if len(arguments) == 1:
            arguments.append(Bamboo.getcurrentplant(True))
        elif arguments[1] == '':
            arguments[1] = Bamboo.getcurrentplant(True)
        try:
            Memory.mu.rfm(['plants',arguments[1]], True)
        except:
            return error(arguments[1], "No plant of such name exists")
        #try:
        #    current_plant = Memory.mu.lfm(['currentplant'], True)
        #except:
        #    error(reason="No current plant set, use 'bamboo set ...' to set one")
        #    return
        #if current_plant == arguments[1]:
        #    error(reason=f"Make sure to change the current plant from {current_plant} using 'bamboo set ...'")
        #    return
        return 'reload'
    elif arguments[0] == 'regenerate':
        if len(arguments) == 1:
            arguments.append(Bamboo.getcurrentplant(True))
        elif arguments[1] == '':
            arguments[1] = Bamboo.getcurrentplant(True)
        try:
            Memory.mu.lfm(['plants',arguments[1]], True)
        except:
            return error(arguments[1], "No plant of such name exists")
        Memory.mu.atm(['plants',arguments[1],'information','Visual'], Bamboo.createplant(17, 5), True)
        return 'reload'
    elif arguments[0] == 'list':
        listinformation('Bamboo', ['plants'])
        return
    else:
        return error(arguments[0], "It is not a valid sub-command")

def codebit(arguments):
    """
    Various commands relating to codebits, such as creating and pulling them.

    arguments:
    Create: create a new codebit, whether by typing them out manually or pasting them.
    Pull: visually displays a codebit.
    Delete: deletes the specified codebit from memory.
    Copy: copies the information of the specified codebit to the user's clipboard.

    The arguments of the above sub-commands are the all the same.
    1: language name, 2: codebit name

    List: lists all codebits in all languages.

    *Opens memory.
    """
    calc = cal(arguments, 1)
    if calc: return calc

    if arguments[0] == 'create':
        calc = cal(arguments, 3)
        if calc: return calc
        Memory.memory.open()
        try:
            Memory.mu.lfm(['codebits', arguments[1], arguments[2]])
        except:
            Screen.inputscreen('Codebit')
            code = Codebit.askcode()
            Memory.mu.atm(['codebits', arguments[1], arguments[2]], code)
            return
        else:
            return error(arguments[1] + '-' + arguments[2], 'A codebit of that name already exists')
        finally:
            Memory.memory.close()
            return 'reload'
    elif arguments[0] == 'pull':
        calc = cal(arguments, 3)
        if calc: return calc
        Memory.memory.open()
        try:
            code = Memory.mu.lfm(['codebits', arguments[1], arguments[2]])
        except:
            return error(arguments[1] + '-' + arguments[2], 'A codebit of that name does not exist')
        else:
            code = [f'{arguments[1]}-{arguments[2]} Codebit:'] + code
            #for index, line in enumerate(code):
            #    code[index] = line + '\n'
            Utilities.propertextdisplay(code, 35, 101)
            return
        finally:
            Memory.memory.close()
    elif arguments[0] == 'delete':
        calc = cal(arguments, 3)
        if calc: return calc
        Memory.memory.open()
        try:
            Memory.mu.rfm(['codebits', arguments[1], arguments[2]])
        except:
            return error(arguments[1] + '-' + arguments[2], 'A codebit of that name does not exist')
        else:
            remaining_codebits = Memory.mu.lfm(['codebits', arguments[1]])
            if remaining_codebits == {}:
                Memory.mu.rfm(['codebits', arguments[1]])
            return
        finally:
            Memory.memory.close()
            return 'reload'
    elif arguments[0] == 'list':
        listinformation('Codebit', ['codebits'], True)
        return
    elif arguments[0] == 'copy':
        calc = cal(arguments, 3)
        if calc: return calc
        Memory.memory.open()
        try:
            code = Memory.mu.lfm(['codebits', arguments[1], arguments[2]])
        except:
            return error(arguments[1] + '-' + arguments[2], 'A codebit of that name does not exist')
        else:
            code = '\n'.join(code)
            #code = [line + '\n' for line in code]
            #code[-1] = code[-1][:-1]
            clipboard_file = open(cbfl, 'w')
            clipboard_file.write(code)
            clipboard_file.close()
            #print(code)
            #echo ... | clip tried unsucessfully, does not work with new lines
            subprocess.run(['clip', '<', 'Clipboard.txt'], shell=True)
            #input('Enter')
            return
        finally:
            Memory.memory.close()
    else:
        return error(arguments[0], 'It is not a valid sub-command')

def say(arguments):
    """
    Equivalent of 'echo', Repeats the given information.
    Quotation marks optional in the command.

    arguments:
    0: information
    """
    global terminal

    calc = cal(arguments, 1)
    if calc: return calc

    print(' '.join(arguments))
    if not terminal: input("Press enter to continue.")
    #return 'display|'

def helpc():
    #help command
    """
    Reads the 'Help.txt' file and displays it on screen, capable of managing it if it is longer than a single display area.

    No arguments.

    *Reads the file using the location given in the global 'hfl' variable.
    *Uses a global variable to store a copy of the 'Help.txt' file so it does not need to be re-opened in the same instance.
    """
    global ch
    global hfl
    if ch == None:
        help_file = open(hfl, 'r')
        ch = help_file.read()
        help_file.close()
        ch = ch.split('\n')[:-1]
        helpc()
    else:
        Utilities.propertextdisplay(ch, 35, 101, not terminal, not terminal)
    #try:
        #for index,line in enumerate(ch):
        #    print(line)
        #    if not terminal:
        #        if not (index+2) % 35 and not len(ch) == index+2:
        #            input("Press enter to continue.")
        #if not terminal:
        #    if len(ch)%35:
        #        print("\n"*(33-(len(ch)%35)))
        #    input("Press enter to return.")
    #except:

def listinformation(list_name, memory_location, two_layer=False, user_based=True, use_advanced_text_display=True):
    """
    Lists the keys of the dictionary at a given memory location.

    list_name: str (the general name of the keys that are to displayed)
    memory_location: list
    two_layer: bool (True: lists everything in the dictionary of dictionaries provided (not completely recursive, only dictionary within dictionary))
    user_based: bool (Memory call using mu (True) or memory (False), so within only user scope or the entirety respectively)

    *Opens memory.
    """
    global terminal

    if not terminal and not use_advanced_text_display: Screen.inputscreen(f'{list_name} List')
    if user_based:
        memory_dictionary = Memory.mu.lfm(memory_location, True)
    else:
        memory_dictionary = Memory.memory.retrieve(memory_location, True)
    if two_layer:
        output = ''
        for key, dictionary in memory_dictionary.items():
            keys = dictionary.keys()
            keys = str(keys)
            keys = keys[11:-2]
            keys = keys.replace("'", '')
            keys = key + '-' + keys
            keys = keys.replace(', ', ', ' + key + '-')
            output += keys + '\n'
        output = output[:-1]
    else:
        keys = memory_dictionary.keys()
        keys = str(keys)
        keys = keys[11:-2]
        output = keys
    if terminal or use_advanced_text_display:
        output = f'{list_name} List'.center(101) + '\n' + output
    if use_advanced_text_display:
        Utilities.propertextdisplay(output.split('\n'), 35, 101, not terminal, not terminal)
    else:
        #Remove the first \n created just above when setting output to a slightly modified version of itself.
        output = output.replace('\n', '', 1)
        print(output)
    if not terminal and not use_advanced_text_display:
        input('Press enter to continue.')

def csb(arguments, indices):
    """
    Takes in arguments and indices that need to be checked if argument provided is within 0-3.
    Error message returned if no, None if yes.

    arguments: list
    indices: list

    return: str or None (noted above)
    """
    #check screen boundaries
    for index in indices:
        if not arguments[index] in [0,1,2,3]:
            return error(arguments[index], f"Number between 0 and 3 not found at an index ({index}) in the given command arguments ({arguments})")
    return None

def cwi(arguments, indices):
    """
    Takes in arguments and incices that need to be checked if they are ints, while also converting them to ints.
    Error message returned if no, None if yes, the process was completed without any problems.

    arguments: list
    indices: list

    return: str or None (noted above)

    *Modifies arguments
    """
    #check whether int
    #import pdb; pdb.set_trace()
    try:
        for indices_index, index_to_check in enumerate(indices):
            arguments[index_to_check] = int(arguments[index_to_check])
    except:
        return error(arguments, f"Integer not found (False) at one or more of the corresponding indices ({([True] * len(arguments[:indices_index])) + [index.isdecimal() for index in arguments[indices_index:]]})")
    else:
        return None

def cal(arguments, amount):
    """
    Takes in arguments and compares its length to the amount specified.
    Returns an error message if no, the lengths are not the same, and None is they are the same.

    arguments: list
    amount: int

    return: str or None (noted above)
    """
    #check argument list
    if len(arguments) < amount:
        return error(reason=f"Not enough arguments were provided, {len(arguments)} given, {amount} needed")
    else:
        #Technically this is not needed, there for readability.
        return None

def error(argument=None, reason=None):
    """
    Takes in an argument that caused an error and returns it, along with an optional reason, for why something went wrong.

    argument: str
    reason: str

    return: str
    """
    if not reason and argument:
        return f"display|Unrecognized argument or set of arguments '{argument}'."
    elif reason and not argument:
        return f'display|{reason}.'
    elif reason and argument:
        return f"display|Unrecognized argument or set of arguments '{argument}'. {reason}."
    else:
        return 'display|Error.'
    #time.sleep(edt)

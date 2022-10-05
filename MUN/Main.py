"""
Holds the run function, which combines Commands, Screen, and application modules, allowing MUN to function.
Furthermore, has the startup and finishup functions that surround the run function in MUN start up and end.
Restart function adds more abilities related to users and changing user.
"""

import subprocess
import argparse
import sys

import Screen
import Commands
import Cloud
import Bamboo
import Utilities
import Memory

#Checklist:
#DONE 1. Multiple options for how weather mini-screens work (daily, hourly)
#DONE 2. Adjust functions to work with new screen generation (repeated re-printing of the screen) (for example, set current user made into a command)
#DONE 3. Adjust weather so that if no cache of weather or coordinates exists, it automatically creates a new one
#UNKNOWN 4. Passive versus active commands? If the app is in the main screen or not? Or if the app is only on one of the top screens, is differentiation necessary?
#OPTED OUT 5. Color.
#DONE 6. Help command
#DONE 7. Make commands have separate functions (use argument lists)
#IN PROGRESS 8. Continue to expand the recognized ShortForecasts
#DONE 9. Check if imports are still used
#DONE 10. Fix divideup and make sure the cut offs in Weather.weatherdisplay list comprehensions works
#DONE 11. Command for checking length of memory file in bytes, getting cached weather information and other stored info like addresses
#ON HOLD 12. Automatically get current location
#DONE 13. Look into storing screens in memory
#DONE 14. Different themes based on colors
#DONE 15. Error prevention in Commands
#DONE 16. In weather, adjust hour and temperature so its on the edge so the short forecast has more room as to not be cut off
#DONE 17. Make more functions that automatically check for an error in arguments (should be int?)
#DONE 18. Save weather mode?
#UNKNOWN 19. Function annotations?
#DONE 20. Transition to PEP styling (kind of) in terms of documentation strings
#DONE 21. Look into JSON
#REPLACED 22. Work on Screen.changecs function
#DONE 23. Fix notes added to documentation strings
#DONE 24. Start auto load, end auto save (with special end command for not saving)
#OPTED OUT 25. Convert command checks to decorators?
#DONE 26. Give current options for some commands, like delay may be 5 and theme may be night
#DONE 27. Display current location when asking for address
#REMOVED 28. Is basic memory check necessary?
#REMOVED 29. Memory.memory.open above fed necessary (with the Memory.memory.close)?
#DONE 30. Edit errors made when typing timezone or address information?
#DONE 31. Change f strings in fed to some alternative, allowing it to be updated during run
#DONE 32. Memory open when it shouldn't be in makefunctions function
#IN PROGRESS 33. Inconsistency in global variables between modules (like Memory.mu)
#DONE 34. Optional parameters in Memory.MDF and/or Memory.User methods for one time memory open and memory close
#DONE 35. Change some memory actions to instead use the open parameters in the methods
#DONE 36. Multiple sub-commands -> weather get something. 'weather' -> weather get/.../.... 'get' -> <...> <...>
#DONE 37. Commands that give the different options available, like created locations or plants (update locations to use function)
#IN PROGRESS 38. Delete old weather information only visible second time around
#DONE 39. General information changer command (change user?)
#DONE 40. Change user command, removing anything added by the general information changer and getter
#DONE 41. Terminal mode, only text input?
#DONE 42. Incorporate exceptionallower so that one can type uppercase when needed, like when calling to a part in memory
#DONE 43. Cased module names should still be altered
#DONE 44. Possible new screen for when entering a list of information such as Weather.askaddress
#DONE 45. Commands that have subcommands that do not take any arguments
#DONE 46. Command 'user set' outdated, remove and add more subcommands to the user command such as rename or (?) delete
#DONE 47. Restart command
#DONE 48. Name at top?
#DONE 49. Second wave documentation
#DONE 50. Update weather command
#DONE 51. Better terminal for terminal mode (scroll up)
#DONE 52. (Some) Bamboo commands default to current plant if empty argument provided
#DONE 53. Help command and terminal
#DONE 54. Random location display menu
#DONE 55. Restart accepts command line parameters
#DONE 56. Forced creation of a plant with bamboo set
#DONE 57. Allow length zero names?
#PENDING 58. Display window bug (as in, print usually puts a new line at the end) - why does it not happen? Reason: subprocess.run change window size
#DONE 59. Loading screen
#DONE 60. Add propertextdisplay to more information displays (possibly the list function in Commands)
#DONE 61. Codebit pull option to copy to clipboard
#DONE 62. Memory move
#DONE 63. Not enough arguments correct count, unrecognized command incorrect terminology for missing arguments
#DONE 64. Have Commands.save work with regular functions and not need to convert to string
#DONE 65. Fix name of Weather (Cloud?) and maybe Bamboo (Plant?). User versus code name, difference?
#DONE 66. Location set as 1/null/None before any address or location name entered
#DONE 67. Commands.error in Weather and other modules can't get an adjusted delay
#DONE 68. User list
#DONE 69. Most commands do not reload screen, screen saved in local variable and only commands like set and a specific 'reload' command reload it
#70. Instead of delays after errors, just use input?
#ALREADY COMPLETED 71. Codebit delete.
#DONE 72. Doc-strings in Commands having duplicate arguments displayed, condense these.
#73. Again look into the idea of being able to enter empty strings as arguments with commands.
#74. How necessary is try/except in Commands.save?
#75. Centered on entire screen function, apply to loading and make it allow different sizes so it could be used for when the weather could not be found, on the weather application for example.
#76. Application list.
#77. Similar to more command, maybe an optional argument, for commands like help, when the user is using the terminal mode.
#78. Possibly connected to issue 69 and 70, make it so that, when there is an error, re-print the screen before printing out the error.
#DONE Further, this is going to require the overhaul of how errors are processed in the Commands module.
# They are going to need to be returned to this module, along with other parts of Commands that prints outputs, such as in memory length.
# The information is going to need to be printed here after a re-print of the information on screen.
#DONE Error is going to have to return up a few layers of functions to ultimately return back here.
# Maybe there will be the necessity of sending back a special tag, such as ERROR or INFORMATION, depending on the type of information being returned by Commands, though this may not be needed.
#DONE 79. Make it so that unknown command errors and special exceptional errors created in main also re-print the screen with the error.
#80. Add loading screen to post-startup screen generation.
#81. Make sure all of these error changes work with terminal mode.
#82. Some commands should not work when terminal mode is enabled, such as set.
#83. Better parsing of commands with quotation marks in commands, either '' or "" causing the words, even if there are spaces, to be grouped together.
#84. Better error or just no error if user puts an argument in a command that requires no arguments, such as 'end hello'.

#Bug report:
#1. memory set "experiment 123" "does this work"
#2. Missing quotation does not result in an error: say "hello there:

#Upkeep:
#1. Main.fed, Main.makefunctions
#2. help.txt
#3. Commands.set, Commands.save (no longer needed), Commands.load

#Useful Characters:
#←

given_arguments = []

#function equivalent dictionary
#(equivalent function, needs screen_list as input?, parameter list)
fed = {
    'set': (Commands.set, True, ['application','index']),
    'switch': (Commands.switch, True, ['index','index']),
    'cloud': (Commands.cloud, False, [['mode'], ['0-1 ([Commands.Cloud.display_mode])']]),
    'save': (Commands.save, True, []),
    'load': (Commands.load, True, []),
    'user': (Commands.user, False, [['rename', 'delete', 'list'], ['name ([Commands.ci])']]),
    'location': (Commands.location, False, [['set', 'list'], ['location ([Cloud.getcurrentlocation()])']]),
    'theme': (Commands.theme, False, ['theme ([Commands.ct])']),
    'memory': (Commands.memory, False, [['move', 'set', 'get', 'delete', 'length', 'structure'], ['memory location'] * 4 + ['total/user'], ['memory location', 'information'], ['remove?']]),
    #'delay': (Commands.delay, False, ['delay seconds ([Commands.edt])']),
    'bamboo': (Commands.bamboo, False, [['set', 'delete', 'water', 'regenerate', 'list'], ['plant name ([Bamboo.getcurrentplant()])'] * 4]),
    'say': (Commands.say, False, ['information']),
    'fire': (Commands.fire, False, ['smoke?', 'fireplace?']),
    'codebit': (Commands.codebit, False, [['create', 'pull', 'copy'], ['language'] * 3, ['name'] * 3])
}

def startup(screen_list):
    """
    Runs essential operations necessary to initiate the program.

    1. Resizes the window.
    2. Parses arguments.
    3. (Unless specified not to) Loads the previous save.
    4. Loading screen.

    screen_list: list

    return: dict

    *Uses a subprocess with shell=True.
    *Modifies 'screen_list'.
    *Accesses global variable arguments.
    """
    global given_arguments

    #Checks for arguments
    command_parser = argparse.ArgumentParser()
    command_parser.add_argument('-n', '--new', help='does not load last save', action='store_true')
    command_parser.add_argument('-t', '--terminal', help='only accesses the terminal', action='store_true')
    command_parser.add_argument('-nw', '--new_window', help='opens the MUN application in a new window', action='store_true')
    arguments = command_parser.parse_args()

    given_arguments = sys.argv.copy()

    if arguments.new_window:
        given_arguments.remove('-nw')
        subprocess.run(['start', 'py'] + given_arguments, shell=True)
        return 'stop'

    #Sets the correct width and height of the console, lower than the parser so it is not activated when there is an error or '-h' is used.
    if not arguments.terminal:
        subprocess.run(["mode","con","cols=101","lines=36"], shell=True)

    title_list = ['title', 'Multi-Use', 'Nexus']
    if arguments.terminal:
        title_list += ['{Terminal', 'Only', 'Mode}']
    title_list += ['[Version', '0]']
    #Sets the title
    subprocess.run(title_list, shell=True)

    #print((' ' * 101) * 17)
    #print((' ' * 46) + 'Loading...' + (' ' * 45))
    #print((' ' * 101) * 17)

    if not arguments.terminal: print(Utilities.centeredmessage('Loading MUN...', 101, 35))

    #Load last saved if '-n' or '--new' is not provided with the command
    if not arguments.new:
        Commands.load(screen_list)

    Commands.terminal, Commands.Bamboo.terminal, Commands.Cloud.terminal = (arguments.terminal,) * 3

    #if arguments.terminal:
        #Commands.edt = 0

    return {'onlyterminal': arguments.terminal}

def finishup(screen_list, save=True):
    """
    Runs operations right before the end of the program.

    1. Returns the colors to normal.
    2. (Unless specified not to) Saves current information.

    screen_list: list
    """
    #If save is true, save the current screen and other stored information
    if save:
        Commands.save(screen_list)

    #Return colors back to normal
    Commands.theme(['normal'])

def run():
    """
    Main function that asks for user inputs and sends out the information to Command functions.
    Gets information from the Screen module for different layouts depending on the given application.
    Uses functions such as the main one from the Cloud module, 'Cloud.weatherdisplay'.

    screen_list holds all functions that represent one application per index.

    Supports subcommands in the following way:
    command subcommand/subcommand arguments/arguments
    User inputs command:
    command <subcommand>
    User inputs subcommand:
    command subcommand <argument> <argument>
    Arguments are specific to each subcommand.
    Subcommands within subcommands are not supported.

    Some commands return special codes that can lead to certain high level actions being taken:
    restart: Accesses the restart function with the given arguments separated by dots in the string.
    switch: Switches the current user.

    *Accesses global variable terminal.
    """
    global terminal

    screen_list = [None, None, None, None]
    startup_information = startup(screen_list)
    if startup_information == 'stop':
        return
    terminal = startup_information['onlyterminal']
    #Memory.memory.store(['terminal'], True, True)
    if terminal:
        print('Welcome to MUN terminal mode. Enter "help" for more information.')
    else:
        #A different loading screen *could* be put here, specifying that the wait is now on the screen generation, but it is not needed as "Loading MUN" is still accurate as the first screen load does require a lot more processing than future calls.
        #screen to print
        stp = Screen.screen(screen_list)
    while True:
        if not terminal:
            print(stp)
        command = Utilities.exceptionallower(input(Commands.ci))
        #top level
        tl_command = command.split(' ')[0]

        def unnecessarycheck(command_name):
            """
            Checks to see if there are unnecessary arguments in a command that requires no arguments.
            If there are, information is given to the user.
            """
            if len(command.split(' ')) > 1:
                print(stp)
                iop(f'Unnecessary arguments after the command "{command_name}". Though, the command will continue.')

        if command == '':
            continue
        elif tl_command == 'reload':
            unnecessarycheck(tl_command)
            if terminal:
                print('This command only works in visual mode, it has no purpose in terminal mode.')
            else:
                print(Utilities.centeredmessage('Loading screen...', 101, 35))
                stp = Screen.screen(screen_list)
            continue
        elif tl_command == 'end':
            unnecessarycheck(tl_command)
            finishup(screen_list)
            break
        elif tl_command == 'interrupt':
            unnecessarycheck(tl_command)
            finishup(screen_list, False)
            break
        elif tl_command == 'help':
            unnecessarycheck(tl_command)
            Commands.helpc()
            continue
        elif tl_command == 'login':
            unnecessarycheck(tl_command)
            if not terminal:
                Screen.inputscreen('Login')
            if restart(screen_list):
                break
            else:
                continue
        elif tl_command == 'restart':
            unnecessarycheck(tl_command)
            if not terminal:
                Screen.inputscreen('Restart')
            #Normally would have to open memory to make sure that Memory.mu.name is up to date, but it should not really change during a single run
            if restart(screen_list, '`noswitch', change_arguments=True):
                break
            else:
                continue
        try:
            function = fed[command.split(' ')[0]]
        except:
            if not terminal:
                print(stp)
            iop("Unrecognized command.")
            #time.sleep(Commands.edt)
            continue
        #input(len(command.split(' ')))
        #input(function[2])
        if len(command.split(' ')) > 1 and len(function[2]):
            #If the command should have parameters AND the user entered parameters.
            #arguments = command.split(' ')[1:]
            #This kind of parsing is going to be needed in the else statement below for the second part of the subcommand route.
            if command.count('"') % 2:
                iop("Unmatched '\"' in the command.")
                continue
            arguments = command.split('"')
            #input(arguments[::2])
            offset = 0
            import pdb; pdb.set_trace()
            for part_index, part in enumerate(arguments[::2]):
                #for check_index in [0, len(part) - 1]:
                    #if part[check_index] == ' ':
                        #part = Utilities.sir(part, check_index, '')
                real_index = part_index * 2 + offset
                if part == '':
                    #continue would technically work because this should only activate with a quotation mark at the end.
                    break
                part = part[0].replace(' ', '') + part[1:]
                #If part was originally a single space, the above expression would have made it an empty string, which would lead to an error below.
                if len(part) > 0:
                    part = part[:len(part) - 1] + part[len(part) - 1].replace(' ', '')
                #Check what find does again, try doing tests.
                if part.find(' ') > -1:
                    arguments.pop(real_index)
                    #offset += part.count(' ')
                    for new_argument_index, new_argument in enumerate(part.split(' ')):
                        arguments.insert(part_index * 2 + new_argument_index, new_argument)
                    offset += new_argument_index
                else:
                    arguments[real_index] = part
                #Trying to make it so that command argument1 'argument2 hello' argument3 becomes
                #['argument1', 'argument2 hello', 'argument3']
            arguments = arguments[1:]
        elif not len(function[2]):
            #If the command should not have any parameters (does not matter whether or not the user actually entered parameters).
            unnecessarycheck(tl_command)
            function[0](screen_list)
            continue
        else:
            #The command should have parameters AND the user did not enter parameters.
            #Goes through the subcommand then the arguments, helping the user along.
            if not terminal:
                print(stp)
            if type(function[2][0]) == type([]):
                subcommand = Utilities.exceptionallower(input(command + ' <' + '/'.join(function[2][0]) + '> '))
                if not subcommand in function[2][0]:
                    if not terminal:
                        print(stp)
                    iop("Unrecognized sub-command.")
                    #time.sleep(Commands.edt)
                    continue
                subcommand_index = function[2][0].index(subcommand)
                for list_index, argument_list in enumerate(function[2][1:]):
                    if len(argument_list) <= subcommand_index:
                        break
                else:
                    list_index += 1
                #Original behavior replaced by the else in the for loop
                #if list_index == 0 and len(function[2][1:]) == 1:
                #    list_index += 1
                #list_index becomes index at which there are no more arguments necessary for the subcommand (so index before is last argument)
                if list_index == 0:
                    #If the subcommand does not require any arguments
                    arguments = [subcommand]
                else:
                    if not terminal:
                        print(stp)
                    arguments = Utilities.exceptionallower(input(makefunctions(command + ' ' + subcommand + ' ' + ' '.join('<' + parameter[subcommand_index] + '>' for parameter in function[2][1:list_index + 1]) + ' ')))
                    arguments = arguments.split(' ')
                    arguments = [subcommand] + arguments
            else:
                arguments = Utilities.exceptionallower(input(makefunctions(command + ' ' + ' '.join('<' + parameter + '>' for parameter in function[2]) + ' ')))
                arguments = arguments.split(' ')
        #for argument in arguments:
            #if argument == '':
                #arguments.remove('')
        #If it is necessary for the user to be able to enter '' as an argument, after the above check replace a designated symbol with ''
        if function[1]:
            output = function[0](screen_list, arguments)
        else:
            output = function[0](arguments)
        if type(output) == type(''):
            output = output.split('~')
            for index, output_part in enumerate(output):
                output[index] = output_part.split('|')
            main_commands = [output_part[0] for output_part in output]
            if 'switch' in main_commands:
                index = main_commands.index('switch')
                if len(output[index]) == 2:
                    Memory.mu.setcurrentuser(output[index][1], True)
            if 'restart' in main_commands:
                index = main_commands.index('restart')
                if len(output[index]) == 4:
                    if output[index][1] == 'None':
                        user = None
                    else:
                        user = output[index][1]
                    if output[index][2] == 'True':
                        ask_confirmation = True
                    elif output[index][2] == 'False':
                        ask_confirmation = False
                    if output[index][3] == 'True':
                        ask_save = True
                    else:
                        ask_save = False
                    restart(screen_list, user, ask_confirmation, ask_save)
                else:
                    restart(screen_list)
                break
            if 'display' in main_commands:
                index = main_commands.index('display')
                if not terminal:
                    print(stp)
                if len(output[index]) == 2:
                    iop(output[index][1])
                else:
                    #This should not really ever be used, possibly remove. The Commands.error function deals with all possibilities.
                    iop('An error has occurred, there is nothing to display. (enter) ')
            if 'reload' in main_commands:
                if not terminal:
                    print(Utilities.centeredmessage('Loading screen...', 101, 35))
                    stp = Screen.screen(screen_list)
        continue

def restart(screen_list, user=None, ask_confirmation=True, ask_save=True, change_arguments=False):
    """
    Restarts the MUN application being run.

    screen_list should be provided by the screen_list in function 'run'.
    user: str (the specific user that should be switched to) or None (instead prompt the user).
    ask_confirmation: bool (True: ask the default prompt, False: no prompt) or str (Equivalent to True, but ask with a custom prompt)
    ask_save: bool (True: asks whether MUN should save before restart, False: no save)
    change_arguments: bool (True: ask user for new arguments, False: keep same arguments from original instance, user can also input '.' to keep same parameters)

    return: bool (True: restarted, False: cancelled)

    *Uses subprocess with shell=True.
    *Accesses global variable arguments.
    """
    global given_arguments
    if type(ask_confirmation) == type(True) and ask_confirmation:
        if not Utilities.confirmation('It will cause MUN to restart'):
            return False
    elif type(ask_confirmation) == type(''):
        if not Utilities.confirmation(ask_confirmation):
            return False
    if ask_save:
        save = input('Would you like to save? ')
        if save.lower() in ['yes', 'y']:
            finishup(screen_list)
        else:
            finishup(screen_list, False)
    else:
        finishup(screen_list, False)
    if change_arguments:
        user_arguments = input('py Main.py (Enter "." for the same parameters) ')
        if not user_arguments == '.':
            user_arguments = user_arguments.split(' ')
            for argument in user_arguments:
                if argument == '':
                    user_arguments.remove('')
            given_arguments = ['Main.py'] + user_arguments
    if not user:
        while True:
            user = input("User (No escape '`' necessary for capitalization): ")
            if not user == '':
                break
    #Switched to elif, should work the same
    if not user == '`noswitch':
        Memory.mu.setcurrentuser(user, True)
    subprocess.run(['py'] + given_arguments, shell=True)
    return True

def makefunctions(parameters):
    """
    Takes in the parameter string created when a user inputs just the beginning of a command that requires parameters, changing the string to have to date information.

    parameters: string

    return: string
    """
    #FALSE: Memory open not necessary as Cloud.getcurrentlocation uses Memory.retrieve, which does not need to access any files (look at method)
    #Needs to update in case any information has changed
    #Function tryreplace technically not necessary with 'None' being sent instead of requiring user to input information such as current location or plant.
    parameters = parameters.replace("[Commands.Cloud.display_mode]",f"{Commands.Cloud.display_mode}")
    #parameters = parameters.replace("[Cloud.getcurrentlocation()]",f"{Cloud.getcurrentlocation(True)}")
    parameters = Utilities.tryreplace(parameters, '[Cloud.getcurrentlocation()]', Cloud.getcurrentlocation, True)
    parameters = parameters.replace("[Commands.ct]",f"{Commands.ct}")
    #parameters = parameters.replace("[Commands.edt]",f"{Commands.edt}")
    parameters = Utilities.tryreplace(parameters, '[Bamboo.getcurrentplant()]', Bamboo.getcurrentplant, True)
    parameters = parameters.replace("[Commands.ci]",f"{Commands.ci[:-1]}")

    return parameters

def iop(information):
    """
    Input or print the given information, depending on whether terminal is True or False.

    information: str (no period at the end).

    *Accesses global variable terminal.
    """
    global terminal

    if terminal:
        print(information)
    else:
        input(information + ' (enter) ')

if __name__ == "__main__":
    run()

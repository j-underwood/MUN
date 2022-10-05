"""Runs the underlying screen generation, weaving together different lists and generating different layouts depending on the 'Main.run' function."""

import random

import Memory
import Utilities

#logo file location
lfl = "C:\\Users\\jacob\\OneDrive\\Desktop\\Project\\MUN\\Logo.txt"

#cached logos
cl = {}

def screen(screen_list):
    """
    Generates a screen using different functions inputted through the 'screen_list'.

    screen_list:
    Amount of inputs
    0: Full screen hello/welcome screen
    1: Top screen is a hello/welcome screen, bottom screen is the inputted function
    2: Top screen is second function, bottom screen is the first
    3: Bottom is the first function given, top left is the second, top right is the third
    4: Bottom is the first function given, top left is the second, top middle is the third, top right is the fourth
    (None does not count in the amount)

    *Accesses a function that opens a file.
    """
    if not screen_list[0] and not screen_list[1] and not screen_list[2] and not screen_list[3]:
        return makelogo(1)
    elif screen_list[0] and not screen_list[1] and not screen_list[2] and not screen_list[3]:
        logo = makelogo(0)
        display = logo + '─'*101
        display += screen_list[0]()
        return display
    elif screen_list[0] and screen_list[1] and not screen_list[2] and not screen_list[3]:
        display = screen_list[1]()
        display += '─'*101
        display += screen_list[0]()
        return display
    elif screen_list[0] and screen_list[1] and screen_list[2] and not screen_list[3]:
        display = ''
        top_left_function = screen_list[1](1)
        top_right_function = screen_list[2](1)
        for index in range(0,17):
            display += top_left_function[index]
            display += '│'
            display += top_right_function[index]
        display += ("─"*50) + "┴" + ("─"*50)
        display += screen_list[0]()
        return display
    else:
        display = ''
        top_left_function = screen_list[1](0)
        top_middle_function = screen_list[2](0)
        top_right_function = screen_list[3](0)
        for index in range(0,17):
            display += top_left_function[index]
            display += '│'
            display += top_middle_function[index]
            display += '│'
            display += top_right_function[index]
        display += ("─"*33) + "┴" + ("─"*33) + "┴" + ("─"*33)
        display += screen_list[0]()
        return display

def makelogo(type):
    """
    Generates a logo based on the information in the 'Logo.txt' file.

    type (int):
    Type 0: Small 1: Large

    *Stores the information by instance so the file does not needed to be accessed everytime.
    """

    global cl

    try:
        #DELETE print(cl[type])
        return cl[type]
    except:
        logo_file = open(lfl, "r")
        #read logo
        rlogo = logo_file.read()
        logo_file.close()
        rlogo = rlogo[:-2]
        if type == 1:
            #Original behavior
            #logo = logo.replace('|', ' '*101)
            logo = ''
            for line in rlogo.split('|'):
                logo += line*2
        else:
            logo = rlogo.replace('|', '')
        logo = logo.replace('.', '█')
        #Could technically use Cloud.Icon.symd
        symbol_dictionary = {0: '░', 1: '▒', 2: '▓'}
        #new logo
        nl = ''
        for character in logo:
            if character == ',':
                nl += symbol_dictionary[random.randrange(0,3)]
            elif character == '-':
                if random.randrange(1,2):
                    nl += symbol_dictionary[random.randrange(0,3)]
                else:
                    nl += ' '
            else:
                nl += character
        if type == 1:
            nl += 'Type "help" for more information.' + (' '*68)
        cl[type] = nl
        return nl

def inputscreen(ask_information):
    """
    Sets up a screen in which information can be displayed or asked for.

    ask_information: str
    """
    print("\n" * 34)
    print(f"{ask_information} Display Window".center(101))

def sizedependentmessage(message, size):
    """
    Based on the size given, outputs a list or a string that can be displayed with a message in the middle.

    message: str
    size: int (in [0, 1, 2])

    return: if size == 2: str, elif size in [0, 1]: list
    """
    if size == 2:
        return Utilities.centeredmessage(message, 101, 17)
    elif size == 1:
        return Utilities.centeredmessage(message, 50, 17, True)
    elif size == 0:
        return Utilities.centeredmessage(message, 33, 17, True)

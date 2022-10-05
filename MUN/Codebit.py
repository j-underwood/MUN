"""Deals with codebits, small bite-size pieces of code that may be needed in the future because they provide some essential utility."""

import random

import Screen
import Memory
import Utilities

def askcode():
    """
    Asks the user for the information that they want to add to memory, in the form of code, known as a codebit.
    The user may paste the information in.
    Line numbers are present to help make the pasted/entered information easier to follow.

    return: list [str]
    """
    print('Paste or type your codebit here. To finish, type "`end" on a blank line and press enter. In general, avoid special characters.')
    line = 1
    code_list = []
    while True:
        user_input = input(str(line) + ' ')
        line += 1
        if user_input == '`end':
            break
        code_list.append(user_input)
    return code_list

def codebitdisplay(size=2):
    """
    Generates the display of the Codebit application, which takes random languages and displays random codebits from those languages.
    If no codebits are yet created, it says so instead of providing an error.

    size: int (0,1,2) (2 is the largest, fills up half of the MUN screen, while 1 fills up 1/4 and 0 fills up 1/6).

    return: str (size=2) or list (size in (0,1)).

    *Opens memory.
    """
    Memory.memory.open()
    try:
        codebits = Memory.mu.lfm(['codebits'])
    except:
        return Screen.sizedependentmessage('No Codebits in Memory', size)
        #if size == 2:
            #return 'No Codebits in Memory' + Utilities.empty(size)[21:]
        #else:
            #return ['No Codebits in Memory' + Utilities.empty(size)[0][21:]] + Utilities.empty(size)[1:]

    cbls_amount = 2 ** size

    display = ''
    if len(codebits.keys()) < cbls_amount:
        #cbls list
        cblsl = [cbls(codebits, language) for language in codebits.keys()]
        while len(cblsl) < cbls_amount:
            cblsl += [[' ' * 25] * 17]
        #for section in range(4):
            #for language in codebits.keys():
                #pass
    else:
        randomized_language_list = list(codebits.keys())
        random.shuffle(randomized_language_list)
        cblsl = [cbls(codebits, randomized_language_list[index]) for index in range(cbls_amount)]
        #Make sure to run the center command on all rows after zipping different lists together
    #print(cblsl)
    if size == 2:
        display = ''
    else:
        display = [''] * 17
    for line_index in range(17):
        for cblsl_index in range(cbls_amount):
            if size == 2:
                display += cblsl[cblsl_index][line_index]
            else:
                display[line_index] += cblsl[cblsl_index][line_index]
        if size == 2:
            display += ' '
        elif size == 0:
            display[line_index] = display[line_index].center(33)

    Memory.memory.close()
    return display

def cbls(codebits, language=None):
    """
    Develops a list of codebits in a certain language at random, if there are more than the amount that can fit on the single screen at one time.

    codebits: dict (of all existing codebits, as present in memory).
    language: str (the language that the codebits should be a part of).
    If no language is provided, it chooses a random one.

    return: list [str] (strings are centered at size 25 and the list has the proper length to fill up the rest of the screen if there are less codebits than the available space on the screen).
    """
    #codebit list section
    if not language:
        language = random.choice(list(codebits.keys()))
    codebit_list = [language.center(25)]
    if len(codebits[language].keys()) > 16:
        #for _ in range(16):
            #codebit_list += [random.choice(list(codebits[language].keys())).center(25)]
        randomized_codebit_list = list(codebits[language].keys())
        random.shuffle(randomized_codebit_list)
        codebit_list += [randomized_codebit_list[index].center(25) for index in range(16)]
        #print(codebit_list)
    else:
        codebit_list += [codebit.center(25) for codebit in list(codebits[language].keys())]
    codebit_list = Utilities.conformtolistlength(codebit_list, 17, 25, True)
    return codebit_list

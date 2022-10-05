"""General utilities to be used with other modules."""

import functools
import operator
import copy

def atnd(dictionary, keys, information):
    #add to nested dictionary
    """
    Changes a nested dictionary, using all but the last key to get to the dictionary one wants to change, then using the final key to add the information to the dictionary.

    keys: list

    return: dictionary
    """
    full_dictionary = copy.deepcopy(dictionary)
    dictionary = full_dictionary

    for key in keys[:-1]:
        try:
            dictionary = dictionary[key]
        except:
            dictionary[key] = {}
            dictionary = dictionary[key]

    dictionary[keys[-1]] = information

    return full_dictionary

def rfnd(dictionary, keys):
    #remove from nested dictionary
    """
    Removes information from a nested dictionary, using all but the last key to get to the dictionary one wants to change, then using the final key to remove the information from the dictionary.

    keys: list

    return: dictionary
    """
    full_dictionary = copy.deepcopy(dictionary)
    dictionary = full_dictionary

    for key in keys[:-1]:
        dictionary = dictionary[key]

    del dictionary[keys[-1]]

    return full_dictionary

def sir(string, index, character, whitelist=[], push=False):
    #string index replace
    """
    Replaces the character with a new character at the given index of the string.
    Whitelist specificies which characters can be replaced.
    Push specifies whether the character at the given index should be replaced (False) or pushed to the right (True).

    index: int
    character: str
    whitelist: list
    push: bool

    return: str
    """
    character = str(character)
    index = int(index)
    while index < 0:
        index += len(string)
    while index >= len(string):
        index -= len(string)
    if string[index] in whitelist or not whitelist:
        if not push:
            offset = 1
        else:
            offset = 0
        string = string[:index] + character + string[index+offset:]
    return string

def divideup(string, size, advanced=True):
    """
    Divides the inputted string into a list with each entry being equal to (or at the end, if needed, less than) the given size.
    Advanced determines whether the string is blindly divided up without regard to spaces (False) or if it is divided up with regard to spaces with the intention of ensuring readability (True).

    size: int
    advanced: bool

    return: list
    """
    if not advanced:
        divided = ['']
        counter = 0
        index = 0
        for character in string:
            divided[index] += character
            counter += 1
            if counter == size:
                counter = 0
                index += 1
                divided.append('')
        return divided
    else:
        #First part makes it so the maximum length of any word is or is under the size specified
        string = string.replace(' ', ' _')
        adjusted_string = ''
        for word in string.split(' '):
            while len(word.split(' ')[-1]) > size:
                last_part = sir(word.split(' ')[-1], size-1, '- ', push=True)
                first_part = " ".join(word.split(' ')[:-1])
                if first_part:
                    word = first_part + ' ' + last_part
                else:
                    word = last_part
            adjusted_string += word + ' '
        adjusted_string = adjusted_string[:-1]
        #Second part groups different words together to a maximum length, the size
        divided = ['']
        word_counter = 0
        index_adjustment = 0
        for index in range(len(adjusted_string.split(' '))):
            if not word_counter:
                #Negative one to adjust for no space at the end
                #Original behavior: -1
                character_total = 0
                for word in adjusted_string.split(' ')[index:]:
                    character_total += len(word)
                    if character_total <= size:
                        #Original behavior:  + ' '
                        divided[index-index_adjustment] += word
                        word_counter += 1
                    else:
                        #Original behavior: [:-1]
                        divided[index-index_adjustment] = divided[index-index_adjustment]
                        break
                divided.append('')
            else:
                index_adjustment += 1
            word_counter -= 1
        divided = divided[:-1]
        #Oriiginal behavior: divided[len(divided)-1] = divided[len(divided)-1][:-1]
        divided = [line.replace('_', ' ') for line in divided]
        return divided

def centerlist(series, size):
    """
    Centers the every entry in a list (should be strings) to conform to a certain size, often used with divideup.

    series: list [str]
    size: int

    return: list
    """
    series = series.copy()

    for index in range(0,len(series)):
        series[index] = series[index].center(size)

    return series

def centerstringatindex(string, size, index):
    """
    Centers string at a certain index offset to the middle, surrounding it with white spaces.

    size: int
    index: int

    return: string
    """
    string_middle_index = int((len(string)+1)/2)-1
    #string_middle_index is also equal to the amount of characters in the string before the string_middle_index
    centered_string = ' ' * (index-string_middle_index)
    centered_string += string
    centered_string += ' ' * (size-len(centered_string))
    return centered_string

def conformtolistlength(series, height, width, cut_off=False):
    """
    Makes a list conform to a certain height by adding empty (spaces) entries of a certain width to the end.
    Cut off specifies whether the given list should be cut down in size to conform with the height variable (True).

    height: int
    width: int
    cut_off: bool

    return: list
    """
    if cut_off:
        series = series[:height]
    while not len(series) == height:
        series.append(' ' * width)
    return series

def fixlist(series):
    """
    Takes in a list of length 4 and prevents there from being any None types before actual entries, maintains size of list.

    return: list (4)

    *Modifies
    """
    for boolean in range(2):
        for index in range(1,4):
            if not boolean:
                index = 4-index
            if series[index-1] == None:
                series[index-1] = series[index]
                series[index] = None

def empty(size=2):
    """
    Empty application for use with Screen module.
    Size can be 101x17 (2), 50x17 (1), 33x17 (0).

    size: int (0-2)

    return: list
    """
    if size == 2:
        return " " * 1717
    elif size == 1:
        return [" " * 50] * 17
    elif size == 0:
        return [" " * 33] * 17

def keydictionary(dictionary):
    """
    Takes a dictionary and outputs a dictionary of all the keys within each nested dictionary.

    return: dictionary
    """
    #overview
    ov = {}
    for key in dictionary.keys():
        if type(dictionary[key]) == type({}):
            ov[key] = keydictionary(dictionary[key])
        else:
            ov[key] = {}
    return ov

def box(series, curved=True):
    """
    Boxes the given list, surrounding it with a layer of encircling lines (defaults to curved).
    If 'curved', the corners will be curved, if not, they will be square at a 90 degree angle.

    curved: bool

    return: list
    """
    if curved:
        #character dictionary
        #top left, top right, bottom left, bottom right, horizontal, vertical
        cd = {'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯'}
    else:
        cd = {'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'}
    cd['h'] = '─'
    cd['v'] = '│'
    length = len(series[0])
    boxed_list = [''] * (len(series) + 2)
    boxed_list[0] = cd['tl'] + (cd['h'] * length) + cd['tr']
    for index,row in enumerate(series):
        boxed_list[index+1] = cd['v'] + row + cd['v']
    boxed_list[-1] = cd['bl'] + (cd['h'] * length) + cd['br']
    return boxed_list

def exceptionallower(string, symbol='`'):
    """
    Makes the entire string lowercase, but capitalizes characters preceded by the given symbol.

    symbol: str (len: 1)

    return: str
    """
    string = string.lower()
    while symbol in string:
        index = string.index(symbol)
        string = string[:index] + string[index + 1].upper() + string[index + 2:]
    return string

def confirmation(message):
    """
    Asks for confirmation with a custom message. If confirmation denied, gives a "Cancelled" message that requires the user to press enter. Returns True if confirmation is "y," False if not.

    message: str

    return: bool
    """
    confirmation = input(f"Are you sure you want to continue? {message}. ")
    if confirmation.lower() not in ['yes', 'y']:
        input('Canceled. (enter) ')
        return False
    else:
        return True

def tryreplace(string, tr, rw, argument):
    """
    If 'tr' is in 'string', replace all instances of 'tr' with 'rw', running 'rw' as a function with a single argument 'argument'.
    This is helpful as it does not run the function unless is will actually be used to replace something in the string.

    tr: str
    rw: str
    argument: any

    return: str
    """
    #to replace, replace with
    try:
        string.index(tr)
    except:
        return string
    else:
        #if not argument == None:
        return string.replace(tr, str(rw(argument)))
        #else:
            #return string.replace(tr, rw)

def propertextdisplay(series, rows, columns, fill_last_screen=True, use_input=True):
    """
    Makes a list of text that would be too long to fit on a single screen instead pause at certain points for the user to read and then continue to the next part.

    series: list (str)
    rows: int
    columns: int
    fill_last_screen: bool (maximizes the last page to make sure enough blank area is used to fill up the remainder of the screen)
    use_input: bool (pause and wait for the user to press input after each page?)
    """
    #OUTDATED: Can't use enumerate index as for loop does not update with changes to series
    series = series.copy()
    excessive_lines = True
    while excessive_lines:
        #index = 0
        #if not excessive_lines:
            #break
        #line_change = False
        for index, line in enumerate(series):
            if len(line) > columns:
                #print(index)
                series[index] = series[index][:columns]
                series.insert(index + 1, line[columns:])
                #index += 1
                break
            #index += 1
        line_length_list = [len(line) for line in series]
        excessive_lines = False
        for length in line_length_list:
            if length > columns:
                excessive_lines = True
    for index, line in enumerate(series):
        if len(line) == columns:
            print(line, end='')
        else:
            print(line)
        if not (index + 1) % rows and not len(series) == index + 1 and use_input:
            user_input = input('Press enter to continue. (q to quit) ')
            if user_input in ['q', 'quit']:
                return
    if len(series) % rows:
        if fill_last_screen:
            print('\n' * ((rows - 1) - (len(series) % rows)))
        if use_input:
            input('Press enter to return. ')

def centeredmessage(message, width, height, list_mode=False):
    """
    Centers text on the screen, with messages having to be shorter than width.

    message: str
    width: int
    height: int
    list_mode: bool (True: output where each line is an entry in a list, False: output is a string)

    return: if list_mode: list, else: str
    """
    top_height = int(height / 2)
    bottom_height = height - top_height - 1
    centered = [' ' * width] * top_height + [message[:width].center(width)] + [' ' * width] * bottom_height

    if list_mode:
        return centered
    else:
        return ''.join(centered)

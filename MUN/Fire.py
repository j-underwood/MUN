"""Creates a fire animation that is randomly generated."""

import random
import time
import subprocess

import Utilities

def fireplace(smoke=False, full=False):
    """
    Loops the fire function to give the visual appearance of fire.
    The first call of the fire function causes the fire to generate pixel by pixel at first.

    smoke: bool (generate smoke or not?).
    full: bool (fireplace surroundings?).

    *Uses subprocess shell=True.
    """
    subprocess.run(['color', '4'], shell=True)

    if full:
        brick_size = 15
    else:
        brick_size = 0
    input('Press Ctrl + C to exit.')
    try:
        fire(35, 101, 25, 1 + random.random()/2, True, smoke, brick_size, True)
        while True:
            fire(35, 101, 25, 1 + random.random()/2, False, smoke, brick_size, True)
    except KeyboardInterrupt:
        return

def fire(height, width, amount, branch_amount, starting_animation=False, smoke=False, brick_size=0, background=True):
    """
    Randomly generates a fire-like picture.

    height: int (of the whole picture, not the fire itself).
    width: int (^).
    amount: int (how many times the action of adding pixels should be attempted).
    The higher the amount, the larger the fire.
    branch_amount: int (how much should the likelihood of placing a pixel decrease by the amount of surrounding pixels).
    The higher the branch_amount, the smaller the fire and the less fire-like it is (>2, 1 is very fire like).
    starting_animation: bool (should the picture load pixel by pixel?).
    smoke: bool (smoke comes out from the fire and disappears as it reaches the top of the frame).
    brick_size: int (0 for no fire place)
    brick_size refers to the width of each brick, the height is calculated as 1/3 of that amount.
    background: bool (should the background bricks be placed behind the fire?)

    *Looks best in a red/orange coloring.
    """
    #Brick_size of zero for no bricks
    if brick_size:
        #Try to centralize the chimney
        #Should outside or inside be bright
        #Fix not working almost everywhere but 8 and 15
        #Smoke does not exist because of total_symbols, revert back?
        #Sides have a separator of 1 space
        #Top has a separator of at least 2 spaces
        #Changing 'M' to 'A' just for this part and replacing it in the string fixes the fact it is counted as a 'M' in smoke, causing inconsistencies by replacing empty spaces with 'M' instead of 'L'
        brick_height = round(brick_size / 3) - 1
        topbottom = 'D' * brick_size
        middle = 'D' + ('A' * (brick_size - 2)) + 'D'
        if not background:
            air = ' ' * (width - (brick_size * 2) - 2)
        #Vertical
        brick_amount = int((height - 2) / brick_height)
        #Subtract one to make up for the fact that the mantle bricks need an extra middle line to match up with other bricks
        extra_top_amount = (height - 2) - (brick_amount * brick_height) - 1
        #chimney = (' ' * int((width - (brick_size * 2)) / 2)) + ('▓' * (brick_size * 2)) + (' ' * int((width - (brick_size * 2)) / 2))
        #if not ((width - (brick_size * 2)) / 2) % 1 == 0:
        #    chimney += ' '
        #Horizontal
        brick_length = int((width - 2) / (brick_size - 1))
        brick_length_difference = (width - 2) - ((brick_length * (brick_size - 1)) + 1)
        chimney = ' ' + (('D' * (brick_size * 2)) + (' ' * brick_length_difference)).center(width - 2) + ' '
        if not background:
            air = air[brick_length_difference:]
        end = ' ' * (1 + brick_length_difference)
        fire_list = [chimney] * (2 + extra_top_amount)
        fire_list += [' ' + (topbottom[:-1] * brick_length) + topbottom[-1:] + end]
        #Subtract one instead of two because extra_top_amount subtracted by one
        for _ in range(brick_height - 1):
            fire_list += [' ' + (middle[:-1] * brick_length) + middle[-1:] + end]
        fire_list += [' ' + (topbottom[:-1] * brick_length) + topbottom[-1:] + end]
        if not background:
            airmiddle = air
            airtopbottom = air
        else:
            airmiddle = fire_list[-2][1 + brick_size:-brick_size - 1 - brick_length_difference]
            airtopbottom = fire_list[-1][1 + brick_size:-brick_size - 1 - brick_length_difference]
            airmiddle = airmiddle.replace('A', 'L').replace('D', 'M')
            airtopbottom = airtopbottom.replace('D', 'M')
        if smoke:
            #For use further down
            top_part_length = len(fire_list)
        for _ in range(brick_amount - 1):
            #fire_list += [' ' + topbottom + air + topbottom + end]
            for __ in range(brick_height - 1):
                fire_list += [' ' + middle + airmiddle + middle + end]
            fire_list += [' ' + topbottom + airtopbottom + topbottom + end]
    else:
        fire_list = [' ' * width] * height

    #print(''.join(fire_list)[:-1])
    #return

    #for offset in range(1,3):
        #fire_list[height-offset] = Utilities.sir(fire_list[height-offset], int(width/2), '.')

    fire_list[height - 1] = Utilities.sir(fire_list[height - 1], int(width / 2), '▓')

    #fire_list[height - 1] = Utilities.sir(fire_list[height - 1], int(width / 2) - 1, '.')
    #fire_list[height - 1] = Utilities.sir(fire_list[height - 1], int(width / 2) + 1, '.')

    count = 0
    symbol_list = ['▓', '▒', '░']
    #additional_symbols = ['L', 'M', 'D']
    #total_symbols = symbol_list + additional_symbols
    smoke_symbol = 'S'

    while not count == amount:
        if count <= amount / 3:
            symbol = '▓'
        elif count <= 2 * amount / 3:
            symbol = '▒'
        else:
            symbol = '░'
        for section_index,vertical_section in enumerate(fire_list):
            #input('new section')
            for pixel_index,pixel in enumerate(vertical_section):
                if pixel in symbol_list:
                    #print('\n'.join(fire_list))
                    #time.sleep(0.05)
                    nearby_pixels = 0
                    if not pixel_index == 0:
                        if vertical_section[pixel_index-1] in symbol_list:
                            nearby_pixels += 1
                    if not pixel_index == width-1:
                        if vertical_section[pixel_index+1] in symbol_list:
                            nearby_pixels += 1
                    if not section_index == 0:
                        if fire_list[section_index-1][pixel_index] in symbol_list:
                            nearby_pixels += 1
                    if not section_index == height-1:
                        if fire_list[section_index+1][pixel_index] in symbol_list:
                            nearby_pixels += 1
                    nearby_pixels **= branch_amount
                    nearby_pixels = int(nearby_pixels)
                    #if nearby_pixels == 0:
                    #    nearby_pixels = 1
                    nearby_pixels += 1
                    if random.randrange(0,1*nearby_pixels) == 0:
                        if not pixel_index == 0 and not vertical_section[pixel_index - 1] in symbol_list:
                            vertical_section = Utilities.sir(vertical_section,pixel_index-1,symbol)
                    if random.randrange(0,1*nearby_pixels) == 0:
                        if not pixel_index == width-1 and not vertical_section[pixel_index + 1] in symbol_list:
                            vertical_section = Utilities.sir(vertical_section,pixel_index+1,symbol)
                    if random.randrange(0,1*nearby_pixels) == 0:
                        if not section_index == 0 and not fire_list[section_index - 1][pixel_index] in symbol_list:
                            fire_list[section_index-1] = Utilities.sir(fire_list[section_index-1],pixel_index,symbol)
                if smoke:
                    if not section_index == 0:
                        if pixel in symbol_list and not fire_list[section_index - 1][pixel_index] in symbol_list:
                            if random.randrange(0,5) == 4:
                                fire_list[section_index - 1] = Utilities.sir(fire_list[section_index - 1], pixel_index, smoke_symbol)

                    if pixel == smoke_symbol:
                        if (not brick_size and not section_index == 0) or (brick_size and not section_index == top_part_length):
                            if brick_size:
                                rand_size = 6
                            else:
                                rand_size = 11
                            while True:
                                random_distance = random.randrange(1, rand_size)
                                if (not brick_size and not section_index - random_distance < 0) or (brick_size and not section_index - random_distance < top_part_length):
                                    break
                            if brick_size and background:
                                #Does this cause errors with accessing section_index +/- 1 as it could in theory possibly go off the list (though it should not, no smoke is at the bottom and can not be at top (if statement))
                                #if (vertical_section[pixel_index + 1] == 'M' and vertical_section[pixel_index - 1] == 'M') or (fire_list[section_index - 1][pixel_index] == 'M' and fire_list[section_index + 1][pixel_index] == 'M'):
                                #OUTDATED: ? + 1 offset, so 4 would be a sample of 3
                                #Alternate by 2 (and multiply sample_size by 2 to make up for that) a long with extra offset in last list comprehension (+2 instead of +1) to make it so that something like this won't happen:
                                #Sample size 3, without alternate and offset
                                #--!
                                #==H so H gets transformed into a - instead of a =
                                #===
                                #===
                                #--!
                                #With alternate but no offset
                                #--!
                                #==H
                                #===
                                #=== skip 1
                                #--! this one still counts
                                #With both
                                #--! checks here
                                #==H
                                #=== ignores this because of offset
                                #=== checks here
                                #--- skips here
                                sample_size = 3
                                if ('M' in vertical_section[pixel_index + 1:pixel_index + sample_size + 1] and 'M' in vertical_section[pixel_index - sample_size:pixel_index]) or ('M' in [part[pixel_index] for part in fire_list[section_index - (sample_size * 2):section_index:2]] and 'M' in [part[pixel_index] for part in fire_list[section_index + 1:section_index + (sample_size * 2) + 1:2]]):
                                    #import pdb; pdb.set_trace()
                                    replacement_symbol = 'M'
                                else:
                                    replacement_symbol = 'L'
                            else:
                                replacement_symbol = ' '
                            vertical_section = Utilities.sir(vertical_section, pixel_index, replacement_symbol)
                            fire_list[section_index - random_distance] = Utilities.sir(fire_list[section_index - random_distance], pixel_index, smoke_symbol)
                        else:
                            if not brick_size or not background:
                                vertical_section = Utilities.sir(vertical_section, pixel_index, ' ')
                            else:
                                if fire_list[section_index - 2][pixel_index] == 'D':
                                    vertical_section = Utilities.sir(vertical_section, pixel_index, 'M')
                                else:
                                    vertical_section = Utilities.sir(vertical_section, pixel_index, 'L')
            fire_list[section_index] = vertical_section
        count += 1
        if starting_animation:
            print(''.join(fire_list).replace('S', '░').replace('L', '▓').replace('M', '▒').replace('D', '░').replace('A', '▒'))
            time.sleep(0.2)

    if not starting_animation:
        print(''.join(fire_list).replace('S', '░').replace('L', '▓').replace('M', '▒').replace('D', '░').replace('A', '▒'))
        time.sleep(0.2)
    #return fire_list

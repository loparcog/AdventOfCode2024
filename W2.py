import re
from fractions import Fraction


def day8p1():
    f = open("day8.txt", "r")
    data = f.read()
    # Split every line
    lines = data.split("\n")
    # Store a list of antennae positions
    antennae = {}
    for y in range(len(lines)):
        # Iterate through each char in the line
        chars = list(lines[y])
        for x in range(len(chars)):
            if chars[x] != '.':
                # Found an antenna, see if it exists in the dictionary
                if chars[x] in antennae:
                    antennae[chars[x]].append([y, x])
                else:
                    antennae[chars[x]] = [[y, x]]
    # Now have all antennae, loop through the keys
    ymax = len(lines) - 1
    xmax = len(lines[0]) - 1
    antiset = []
    for pos in antennae.values():
        # Double loop to compare to all future points
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                # Get gap between the points
                gap = [pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]]
                # Get antinodes (j - diff, i + diff)
                anti1 = [pos[i][0] + gap[0], pos[i][1] + gap[1]]
                anti2 = [pos[j][0] - gap[0], pos[j][1] - gap[1]]
                # Check if they're in bounds and they don't already exist
                if (anti1[0] >= 0 and anti1[0] <= ymax) and (anti1[1] >= 0 and anti1[1] <= xmax) and (anti1 not in antiset):
                    antiset.append(anti1)
                if (anti2[0] >= 0 and anti2[0] <= ymax) and (anti2[1] >= 0 and anti2[1] <= xmax) and (anti2 not in antiset):
                    antiset.append(anti2)
    print(len(antiset))


def day8p2():
    f = open("day8.txt", "r")
    data = f.read()
    # Split every line
    lines = data.split("\n")
    # Store a list of antennae positions
    antennae = {}
    for y in range(len(lines)):
        # Iterate through each char in the line
        chars = list(lines[y])
        for x in range(len(chars)):
            if chars[x] != '.':
                # Found an antenna, see if it exists in the dictionary
                if chars[x] in antennae:
                    antennae[chars[x]].append([y, x])
                else:
                    antennae[chars[x]] = [[y, x]]
    # Now have all antennae, loop through the keys
    ymax = len(lines) - 1
    xmax = len(lines[0]) - 1
    antiset = []
    for pos in antennae.values():
        # Double loop to compare to all future points
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                # Get gap between the points
                gap = [pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]]
                # Get antinodes (j - diff, i + diff)
                # Do this in a loop now
                anti1 = [pos[i][0] + gap[0], pos[i][1] + gap[1]]
                # Add original nodes
                node1 = [pos[i][0], pos[i][1]]
                if not node1 in antiset:
                    antiset.append(node1)
                node2 = [pos[j][0], pos[j][1]]
                if not node2 in antiset:
                    antiset.append(node2)
                mult = 1
                while isInbounds(anti1, ymax, xmax):
                    # Add to set
                    if anti1 not in antiset:
                        antiset.append(anti1)
                    # Iterate multiplier and make a new node
                    mult += 1
                    anti1 = [pos[i][0] + (gap[0] * mult),
                             pos[i][1] + (gap[1] * mult)]
                # Do it again!
                anti2 = [pos[j][0] - gap[0], pos[j][1] - gap[1]]
                mult = 1
                while isInbounds(anti2, ymax, xmax):
                    # Add to set
                    if anti2 not in antiset:
                        antiset.append(anti2)
                    # Iterate multiplier and make a new node
                    mult += 1
                    anti2 = [pos[j][0] - (gap[0] * mult),
                             pos[j][1] - (gap[1] * mult)]
    antiset.sort(key=lambda x: x[0])
    print(antiset)
    print(len(antiset))


def isInbounds(node, ymax, xmax):
    if (node[0] >= 0 and node[0] <= ymax) and (node[1] >= 0 and node[1] <= xmax):
        return True
    return False


def day9p1():
    f = open("day9.txt", "r")
    data = f.read()
    # It's one line for once, wow!
    # Make this into the matching file format
    id = 0
    dline = []
    for i in range(len(data)):
        if i % 2:
            # This is free space
            # Store periods multiplied by the file size
            dline += ['.'] * int(data[i])
        else:
            # This is a file
            # Store the ID number multiplied by the file size
            dline += [str(id)] * int(data[i])
            id += 1
    # We now have the data line
    # Go through the line, if you find a dot replace it
    isDigit = len(set(dline[i+1:])) != 1
    i = 0
    while isDigit:
        print("%s/%s" % (i, len(dline)))
        # See if we have a period
        if dline[i] == '.':
            # Get the last digit
            lastnum = dline[-1 * (1 +
                            (re.search(r'[^\.]', ''.join(dline[::-1])).start()))]
            # Replace values while getting last index
            dline[i] = lastnum
            lastidx = len(dline) - 1 - dline[::-1].index(lastnum)
            dline[lastidx] = '.'
        # Uptate isDigit
        i += 1
        isDigit = len(set(dline[i+1:])) != 1
    # Now compute the checksum
    i = 0
    total = 0
    while dline[i] != '.':
        total += i * int(dline[i])
        i += 1
    print(total)


def day9p2():
    f = open("day9.txt", "r")
    data = f.read()
    # It's one line for once, wow!
    # First set bounds for the high and low IDs
    id = 0
    # Set a storage list
    dline = []
    for i in range(len(data)):
        if data[i] == '0':
            # Ignore this
            if not i % 2:
                id += 1
            continue
        if i % 2:
            # This is free space, just store the int
            dline.append(['.', int(data[i])])
        else:
            # This is a file
            # Store the ID number and size
            dline.append([id, int(data[i])])
            id += 1
    # We now have the data line
    i = len(dline) - 1
    id -= 1
    while i > 0:
        if dline[i][0] == '.':
            # Ignore free space
            i -= 1
            continue
        if dline[i][0] > id:
            i -= 1
            continue
        id -= 1
        freeSpace = next((x for x in dline if x[0] == '.'), None)
        freeIdx = -1
        while freeSpace != None:
            # Get the index
            freeIdx += dline[freeIdx+1:].index(freeSpace) + 1
            if freeIdx > i:
                break
            # See if the size works
            if freeSpace[1] >= dline[i][1]:
                # It has enough room!
                # Remove that size from the free space
                dline[freeIdx][1] -= dline[i][1]
                # Put the element right before the free space
                dline.insert(freeIdx, dline[i][:])
                # Replace the original for free space
                dline[i+1][0] = '.'
                i += 1
                break
            else:
                # Get next free space
                freeSpace = next(
                    (x for x in dline[freeIdx+1:] if (x[0] == '.' and x[1] > 0)), None)
        i -= 1
    i = 0
    total = 0
    for elem in dline:
        if elem[0] == '.':
            i += elem[1]
        else:
            for j in range(i, i + elem[1]):
                total += j * elem[0]
            i += elem[1]
    print(total)


def day10():
    f = open("day10.txt", "r")
    data = f.read()
    # Split every line
    lines = data.split("\n")
    # Store it in a 2D array
    topmap = []
    for l in lines:
        row = list(l)
        topmap.append([int(x) for x in row])
    # Store trailhead scores
    trailheads = []
    for y in range(len(topmap)):
        for x in range(len(topmap[0])):
            if topmap[y][x] == 0:
                trailheads.append(findNine(topmap, [y, x]))
    total1 = 0
    total2 = 0
    for head in trailheads:
        # Get the length of the set and add it to the total
        total1 += len(set([tuple(x) for x in head]))
        # Ignore uniqueness for part 2
        total2 += len(head)
    print("Day 1: %s" % total1)
    print("Dat 2: %s" % total2)


def findNine(topmap, coord):
    outlist = []
    y = coord[0]
    x = coord[1]
    curr = topmap[y][x]
    if curr == 9:
        # We found a 9!
        return [[y, x]]
    # Look all around it and make sure it doesn't go beyond bounds
    if (x - 1 >= 0) and (topmap[y][x-1] == curr + 1):
        # Recursively go at it again
        outlist += findNine(topmap, [y, x-1])
    # Do it again!
    if (x + 1 < len(topmap[0])) and (topmap[y][x+1] == curr + 1):
        outlist += findNine(topmap, [y, x+1])
    if (y - 1 >= 0) and (topmap[y-1][x] == curr + 1):
        outlist += findNine(topmap, [y-1, x])
    if (y + 1 < len(topmap)) and (topmap[y+1][x] == curr + 1):
        outlist += findNine(topmap, [y+1, x])
    # Return the list
    return outlist


def day11():
    f = open("day11.txt", "r")
    data = f.read()
    # Split every space
    lines = data.split(" ")
    rocks = [int(x) for x in lines]
    rockindex = [1] * len(rocks)
    # How many blinks we're trying
    blinks = 75
    # Loop for each blink
    for blink in range(blinks):
        print(blink)
        i = 0
        while i < len(rocks):
            # First check for uniqueness
            num = rocks[i]
            while rocks[i+1:].count(num) > 1:
                # Find the next rock
                idx = rocks[i+1:].index(num) + i + 1
                # Add its number to the rock index
                rockindex[i] += rockindex[idx]
                # Remove the rock and the rock index
                del rockindex[idx]
                del rocks[idx]
                # Rule 1
            if rocks[i] == 0:
                rocks[i] = 1
            # Rule 2
            elif len(str(rocks[i])) % 2 == 0:
                # Split the string
                id = str(rocks[i])
                split = len(id) // 2
                rocks[i] = int(id[:split])
                rocks.insert(i+1, int(id[split:]))
                # Add this to the index
                rockindex.insert(i+1, rockindex[i])
                # Skip this new rock
                i += 1
            # Rule 3
            else:
                rocks[i] *= 2024
            i += 1
    print("Pebbles after %s blinks: %s" % (blinks, sum(rockindex)))


def day12():
    f = open("day12.txt", "r")
    data = f.read()
    # Split every line
    lines = data.split("\n")
    # Store it in a 2D array
    plotmap = []
    for l in lines:
        row = list(l)
        plotmap.append([x for x in row])
    # Now to loop through the plotmap!
    total = 0
    for y in range(len(plotmap)):
        for x in range(len(plotmap[y])):
            # See if the current character has not been parsed yet
            if plotmap[y][x].isupper():
                # Run it through the recursive function
                # Want to avoid deepcopies, going to make runtime gross
                # fenceArea = findPlot(plotmap, [y, x])
                # For P2, we just want the corners
                fenceArea = findPlot2(plotmap, [y, x])
                # Add the multiplication of area and plot to the total
                total += fenceArea[0] * fenceArea[1]
    print(total)


def findPlot(plotmap, coords):
    # Extract values for easier comprehension
    y = coords[0]
    x = coords[1]
    curr = plotmap[y][x]
    # Store an array with fence and area values
    fenceArea = [0, 1]
    # Turn the current into a lowercase
    plotmap[y][x] = curr.lower()
    # Now check each direction
    # Right
    if x + 1 >= len(plotmap[y]):
        # Out of bounds, add a fence
        fenceArea[0] += 1
    elif plotmap[y][x+1].upper() == curr:
        # It's the same letter!
        if plotmap[y][x+1].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot(plotmap, [y, x+1]))]
        # Otherwise we ignore it, no fence to put
    else:
        # Different character entirely, add a fence
        fenceArea[0] += 1
    # Left
    if x - 1 < 0:
        # Out of bounds, add a fence
        fenceArea[0] += 1
    elif plotmap[y][x-1].upper() == curr:
        # It's the same letter!
        if plotmap[y][x-1].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot(plotmap, [y, x-1]))]
        # Otherwise we ignore it, no fence to put
    else:
        # Different character entirely, add a fence
        fenceArea[0] += 1
    # Down
    if y + 1 >= len(plotmap):
        # Out of bounds, add a fence
        fenceArea[0] += 1
    elif plotmap[y+1][x].upper() == curr:
        # It's the same letter!
        if plotmap[y+1][x].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot(plotmap, [y+1, x]))]
        # Otherwise we ignore it, no fence to put
    else:
        # Different character entirely, add a fence
        fenceArea[0] += 1
    # Up
    if y - 1 < 0:
        # Out of bounds, add a fence
        fenceArea[0] += 1
    elif plotmap[y-1][x].upper() == curr:
        # It's the same letter!
        if plotmap[y-1][x].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot(plotmap, [y-1, x]))]
        # Otherwise we ignore it, no fence to put
    else:
        # Different character entirely, add a fence
        fenceArea[0] += 1
    return fenceArea


def findPlot2(plotmap, coords):
    # Extract values for easier comprehension
    y = coords[0]
    x = coords[1]
    curr = plotmap[y][x]
    # Store an array with fence and area values
    fenceArea = [0, 1]
    # Turn the current into a lowercase
    plotmap[y][x] = curr.lower()
    # Store an array to see where related tiles are (right, left, down, up)
    plotAround = [False, False, False, False]
    # Now check each direction
    # Right
    if x + 1 < len(plotmap[y]) and plotmap[y][x+1].upper() == curr:
        # It's the same letter!
        plotAround[0] = True
        if plotmap[y][x+1].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot2(plotmap, [y, x+1]))]
        # Otherwise we ignore it, no fence to put
    # Left
    if x - 1 >= 0 and plotmap[y][x-1].upper() == curr:
        # It's the same letter!
        plotAround[1] = True
        if plotmap[y][x-1].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot2(plotmap, [y, x-1]))]
        # Otherwise we ignore it, no fence to put
    # Down
    if y + 1 < len(plotmap) and plotmap[y+1][x].upper() == curr:
        # It's the same letter!
        plotAround[2] = True
        if plotmap[y+1][x].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot2(plotmap, [y+1, x]))]
        # Otherwise we ignore it, no fence to put
    # Up
    if y - 1 >= 0 and plotmap[y-1][x].upper() == curr:
        # It's the same letter!
        plotAround[3] = True
        if plotmap[y-1][x].isupper():
            # We haven't looked at this yet, continue!
            fenceArea = [x + y for x,
                         y in zip(fenceArea, findPlot2(plotmap, [y-1, x]))]
        # Otherwise we ignore it, no fence to put
    # Now look at what plots are around us to determine fencing
    # We're looking for corners as those determine changes in fencing
    # PlotAround = [Right, Left, Down, Up]
    if sum(plotAround) == 1:
        # Bump out, 2 fences
        fenceArea[0] += 2
    elif plotAround[0] != plotAround[1] and plotAround[2] != plotAround[3]:
        # Corner, just add one fence
        fenceArea[0] += 1
    elif sum(plotAround) == 0:
        # Four fences!
        fenceArea[0] = 4
    # The following are all inside corners, and can occur simultaneously
    if (plotAround[0] and plotAround[2] and plotmap[y+1][x+1].upper() != curr):
        fenceArea[0] += 1
    if (plotAround[0] and plotAround[3] and plotmap[y-1][x+1].upper() != curr):
        fenceArea[0] += 1
    if (plotAround[1] and plotAround[2] and plotmap[y+1][x-1].upper() != curr):
        fenceArea[0] += 1
    if (plotAround[1] and plotAround[3] and plotmap[y-1][x-1].upper() != curr):
        fenceArea[0] += 1
    return fenceArea


def day13():
    f = open("day13.txt", "r")
    data = f.read()
    # Split by every 2 lines
    claws = data.split("\n\n")
    # Split the claws into their subcategories
    clawData = []
    for claw in claws:
        curr = {}
        claw = claw.split("\n")
        # 0: Button A movements (stored as +X, +Y)
        buttonA = [int(x) for x in re.findall(r'(?<=\+)\d+', claw[0])]
        curr['A'] = buttonA
        # 1: Button B movements (stored as +X, +Y)
        buttonB = [int(x) for x in re.findall(r'(?<=\+)\d+', claw[1])]
        curr['B'] = buttonB
        # 2: Goal score (you guessed it, X and Y)
        goal = [int(x) for x in re.findall(r'(?<=\w=)\d+', claw[2])]
        # The following is only for day 2
        goal = [x + 10000000000000 for x in goal]
        curr['G'] = goal
        # Store this
        clawData.append(curr)
    # 3 Tokens to press A, 1 Token to press B
    # We want some nice math to do min(1*[B.x, B.y] + 3*[A.x, A.y] = [G.x, G.y])
    # i * B.x + 3 * j * A.x = G.x, i and j = ?
    # eg. 94i + 22*3j =8400
    # 94i + 66j = 8400
    # ITS TWO EQUATIONS TWO UNKNOWNS THIS IS EASY COME ON
    tokens = 0
    for claw in clawData:
        # We're gonna do this matrix style
        # ( A.x A.y ) (x) = (G.x)
        # ( B.x B.y ) (y) = (G.y)
        # Need to invert that first matrix and multiply it by the goal vector
        # Create a makeshift matrix
        mat = [[claw['A'][0], claw['B'][0]], [claw['A'][1], claw['B'][1]]]
        # print(mat)
        # print(goal)
        # Then get the determinate
        det = (mat[0][0] * mat[1][1]) - (mat[0][1] * mat[1][0])
        # Put it in fraction form to make things easier
        det = Fraction(1, det)
        # Now make the inverse
        invMat = [[mat[1][1], -mat[0][1]], [-mat[1][0], mat[0][0]]]
        # Finish inverse and multiply by the goal
        AandB = [0, 0]
        for i in range(len(invMat)):
            invMat[i] = [x * det for x in invMat[i]]
            for j in range(2):
                invMat[i][j] = invMat[i][j] * claw['G'][j]
            AandB[i] = sum(invMat[i])
        # Make sure they're whole numbers
        if AandB[0].denominator != 1 or AandB[1].denominator != 1:
            # Skip it
            continue
        # See if it makes sense (ie. under 100) (Only for part 1), otherwise just make sure its above 0
        # elif AandB[0] <= 100 and AandB[0] >= 0 and AandB[1] <= 100 and AandB[1] >= 0:
        elif AandB[0] >= 0 and AandB[1] >= 0:
            tokens += AandB[0] * 3 + AandB[1]
    print(tokens)


def day14():
    f = open("day14.txt", "r")
    data = f.read()
    # Split by every line
    robots = data.split("\n")
    # Store metavars like width, height, seconds, and score for quadrants
    w = 101
    h = 103
    quads = [0, 0, 0, 0]
    currpos = []
    # Loop for P2
    for secs in range(1000, 10000):
        # Visualizer for P2
        visual = []
        currpos = []
        # If any overlap, don't show it
        # Assuming christmas tree is a perfect layout
        showvisual = True
        for j in range(h):
            visual.append(['.'] * w)
        # Extract the data
        for r in robots:
            # Split the position and speed, all given as (x, y)
            split = re.findall(r'(?<=\=).?\d+,.?\d+', r)
            # Split them both again
            pos = split[0].split(',')
            pos = [int(x) for x in pos]
            vel = split[1].split(',')
            vel = [int(x) for x in vel]
            # Calculate the change in position
            newx = (pos[0] + (vel[0] * secs)) % w
            newy = (pos[1] + (vel[1] * secs)) % h
            # See if it exists in our current positions
            if [newx, newy] in currpos:
                showvisual = False
            else:
                currpos.append([newx, newy])
            # Store in visualizer
            visual[newy][newx] = '#'
            # See what quadrant it ended up in (check all so its not in center)
            if newx > (w / 2) - 0.5:
                if newy > (h / 2) - 0.5:
                    # Q4
                    quads[3] += 1
                elif newy < (h / 2) - 0.5:
                    # Q2
                    quads[1] += 1
            elif newx < (w / 2) - 0.5:
                if newy > (h / 2) - 0.5:
                    # Q3
                    quads[2] += 1
                elif newy < (h / 2) - 0.5:
                    # Q1
                    quads[0] += 1
        if showvisual:
            for row in visual:
                print(''.join(row))
            input("Blinks = %s" % secs)
    total = 1
    for quad in quads:
        total *= quad
    print(total)


day14()

import re


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
    blinks = 25
    # Loop for each blink
    for blink in range(blinks):
        print(blink)
        # Look at each rock
        i = 0
        while i < len(rocks):
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
                # Skip this new rock
                i += 1
            # Rule 3
            else:
                rocks[i] *= 2024
            i += 1
    print("Pebbles after %s blinks: %s" % (blinks, len(rocks)))


day11()

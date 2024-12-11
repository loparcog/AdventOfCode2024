import re
import math
import copy


def day1p1():
    f = open("day1.txt", "r")
    data = f.read()
    # Split input by line
    lines = data.split("\n")
    list1 = []
    list2 = []
    # Create both lists
    for l in lines:
        nums = l.split('   ')
        list1.append(int(nums[0]))
        list2.append(int(nums[1]))
    # Get minimums for each, remove it, and add the difference to a sum
    sum = 0
    for i in range(1000):
        n1 = min(list1)
        n2 = min(list2)
        list1.remove(n1)
        list2.remove(n2)
        sum += abs(n1 - n2)
    print(sum)


def day1p2():
    f = open("day1.txt", "r")
    data = f.read()
    # Split input by line
    lines = data.split("\n")
    list1 = []
    list2 = []
    # Create both lists
    for l in lines:
        nums = l.split('   ')
        list1.append(int(nums[0]))
        list2.append(int(nums[1]))
    # Loop through each number in list 1 and find occurrences
    sum = 0
    while len(list1) > 0:
        num = list1[0]
        occ = len([i for i in list2 if i == num])
        sum += num * occ
        # Remove it from the original list
        list1.remove(num)
    print(sum)


def day2p1():
    f = open("day2.txt", "r")
    data = f.read()
    # Split input by line
    lines = data.split("\n")
    # Store sum and direction (-1 or +1)
    sum = 0
    dir = 0
    for l in lines:
        nums = [int(x) for x in l.split(" ")]
        if nums[1] > nums[0]:
            dir = +1
        else:
            dir = -1
        for i in range(len(nums) - 1):
            diff = nums[i+1] - nums[i]
            if (3 >= abs(diff) and 1 <= abs(diff)) and (diff * dir > 0):
                if i == len(nums) - 2:
                    sum += 1
                continue
            else:
                break
    print(sum)


def day2p2():
    f = open("day2.txt", "r")
    data = f.read()
    # Split input by line
    lines = data.split("\n")
    # Store sum and direction (-1 or +1)
    sum = 0
    dir = 0
    removed = False
    f = open("tester.txt", "w")
    for l in lines:
        nums = [int(x) for x in l.split(" ")]
        if nums[1] > nums[0]:
            dir = +1
        else:
            dir = -1
        baselen = len(nums)
        for i in range(baselen - 1):
            if (i == 0):
                removed = False
            f.write("%s, Removed: %s\n" % (i, removed))
            f.write(str(nums))
            f.write("\n")
            if not removed:
                f.write("%d minus %d\n" % (nums[i+1], nums[i]))
                diff = nums[i+1] - nums[i]
            else:
                f.write("%d minus %d\n" % (nums[i], nums[i-1]))
                diff = nums[i-1] - nums[i-2]
            if (3 >= abs(diff) and 1 <= abs(diff)) and (diff * dir > 0):
                if i == baselen - 2:
                    sum += 1
                    removed = False
                    f.write("GOOD!\n")
                else:
                    f.write("FINE\n")
                continue
            else:
                if not removed:
                    f.write("REMOVED\n")
                    if (i == baselen - 2):
                        sum += 1
                        removed = False
                    del nums[i]
                    if (i == 0):
                        if nums[1] > nums[0]:
                            dir = +1
                        else:
                            dir = -1
                    removed = True
                    continue
                else:
                    removed = False
                    break
    print(sum)


def day3p1():
    f = open("day3.txt", "r")
    data = f.read()
    # Now we get to regex!
    muls = re.findall(r'mul\(\d{1,3},\d{1,3}\)', data)
    # Sum up all the results
    sum = 0
    for m in muls:
        nums = re.findall(r'\d{1,3}', m)
        sum += int(nums[0]) * int(nums[1])
    print(sum)


def day3p2():
    f = open("day3.txt", "r")
    data = f.read()
    f.close()
    # Split it by sections of don'ts and dos
    lines = []
    enabled = True
    while data:
        if enabled:
            # Look for the next don't
            split = data.split("don't()")
            # Add the new line to lines
            lines.append(split[0])
            # Check if we're at the end
            if len(split) == 1:
                break
            data = "don't()".join(split[1:])
            enabled = False
        else:
            # Look for the next do
            split = data.split("do()")
            if len(split) == 1:
                break
            data = "do()".join(split[1:])
            enabled = True
    # Go through the lines
    sum = 0
    for l in lines:
        muls = re.findall(r'mul\(\d{1,3},\d{1,3}\)', l)
        for m in muls:
            nums = re.findall(r'\d{1,3}', m)
            sum += int(nums[0]) * int(nums[1])
    print(sum)


def day4p1():
    f = open("day4.txt", "r")
    data = f.read()
    # Split everything into single chars
    lines = data.split("\n")
    for i in range(len(lines)):
        lines[i] = list(lines[i])
    totl = 0
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == 'X':
                # Look for an M
                dirMap = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
                # Check row above
                if row == 0:
                    dirMap[0] = [0, 0, 0]
                # Row below
                elif row == len(lines) - 1:
                    dirMap[2] = [0, 0, 0]
                if col == 0:
                    dirMap[0][0] = 0
                    dirMap[1][0] = 0
                    dirMap[2][0] = 0
                elif col == len(lines[0]) - 1:
                    dirMap[0][2] = 0
                    dirMap[1][2] = 0
                    dirMap[2][2] = 0
                for i in range(3):
                    for j in range(3):
                        if dirMap[i][j] and lines[row+i-1][col+j-1] == 'M':
                            # Iterate here
                            totl += lookForChar(lines, row +
                                                i-1, col+j-1, [i-1, j-1], 2)
    print(totl)


def lookForChar(lines, row, col, dir, idx):
    word = ['X', 'M', 'A', 'S']
    # Look through the dirMap and recursively look for full strings
    if row + dir[0] < 0 or row + dir[0] > len(lines) - 1:
        # Out of scope
        return 0
    elif col + dir[1] < 0 or col + dir[1] > len(lines[0]) - 1:
        # Out of scope
        return 0
    if lines[row + dir[0]][col + dir[1]] == word[idx]:
        if idx == len(word) - 1:
            return 1
        else:
            return lookForChar(lines, row + dir[0], col + dir[1], dir, idx+1)
    else:
        return 0


def day4p2():
    f = open("day4.txt", "r")
    data = f.read()
    # Split everything into single chars
    lines = data.split("\n")
    for i in range(len(lines)):
        lines[i] = list(lines[i])
    totl = 0
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == 'M':
                # Look for an M
                dirMap = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
                # Check row above
                if row <= 1:
                    dirMap[0] = [0, 0, 0]
                # Row below
                elif row >= len(lines) - 2:
                    dirMap[2] = [0, 0, 0]
                if col <= 1:
                    dirMap[0][0] = 0
                    dirMap[2][0] = 0
                elif col >= len(lines[0]) - 2:
                    dirMap[0][2] = 0
                    dirMap[2][2] = 0
                for i in range(3):
                    for j in range(3):
                        if dirMap[i][j] and lines[row+i-1][col+j-1] == 'A' and lines[row+2*(i-1)][col+2*(j-1)] == 'S':
                            # We found a MAS! Look for diagonal
                            if hasMASCross(lines, row, col, [i-1, j-1]):
                                totl += 1
    print(totl/2)


def hasMASCross(lines, row, col, dir):
    # See the square values
    if lines[row + dir[0] * 2][col] == 'M' and lines[row][col + dir[1] * 2] == 'S':
        return True
    elif lines[row + dir[0] * 2][col] == 'S' and lines[row][col + dir[1] * 2] == 'M':
        return True
    return False


def day5p1():
    f = open("day5.txt", "r")
    data = f.read()
    # Split by line first
    lines = data.split("\n")
    rules = {}
    i = 0
    while lines[i] != "":
        nums = list(map(int, lines[i].split("|")))
        if nums[0] in rules:
            rules[nums[0]].append(nums[1])
        else:
            rules[nums[0]] = [nums[1]]
        i += 1
    # Went through all rules, iterate to get to updates
    i += 1
    sum = 0
    while i < len(lines):
        # Make update all ints
        update = list(map(int, lines[i].split(",")))
        # Iterate through the list
        issue = False
        for j in range(len(update)):
            if (update[j] in rules) and len([num for num in update[:j] if num in rules[update[j]]]) > 0:
                # Conflict!
                issue = True
                break
        if not issue:
            # This one is fine!
            sum += update[len(update)//2]
        i += 1
    print(sum)


def day5p2():
    f = open("day5.txt", "r")
    data = f.read()
    # Split by line first
    lines = data.split("\n")
    rules = {}
    i = 0
    while lines[i] != "":
        nums = list(map(int, lines[i].split("|")))
        if nums[0] in rules:
            rules[nums[0]].append(nums[1])
        else:
            rules[nums[0]] = [nums[1]]
        i += 1
    # Went through all rules, iterate to get to updates
    i += 1
    sum = 0
    while i < len(lines):
        # Make update all ints
        update = list(map(int, lines[i].split(",")))
        # Iterate through the list
        issue = False
        # Manually track iterator
        j = 1
        while j < len(update):
            intersection = [num for num in update[:j]
                            if num in rules[update[j]]]
            if (update[j] in rules) and len(intersection) > 0:
                # Conflict!
                issue = True
                # Swap numbers
                temp = intersection[0]
                update[update.index(intersection[0])] = update[j]
                update[j] = temp
                # Set iterator back to 1
                j = 1
            else:
                j += 1
        if issue:
            # This one had an issue, add to the sum
            sum += update[len(update)//2]
        i += 1
    print(sum)


def day6p1():
    f = open("day6.txt", "r")
    data = f.read()
    # Split by line first
    lines = data.split("\n")
    # Then split each line into chars
    for i in range(len(lines)):
        lines[i] = list(lines[i])
    # Now look for our starting point and set the direction
    # Lists are in order of [y, x]
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    idx = 0
    c = [0, 0]
    i = 0
    j = 0
    # Using while loops so I can just do an easy break at the end
    while i < len(lines):
        j = 0
        while j < len(lines[0]):
            if lines[i][j] == '^':
                c = [i, j]
                i = len(lines)
                j = len(lines)
            j += 1
        i += 1
    # We have the start, now start exploring!
    total = 1
    oob = False
    while not oob:
        dir = dirs[idx]
        # Add the current cell and mark it
        if lines[c[0]][c[1]] == '.':
            total += 1
            lines[c[0]][c[1]] = 'X'
        # See if we're out of bounds
        if (c[0] + dir[0]) >= len(lines) or (c[1] + dir[1]) >= len(lines[0]) or (c[0] + dir[0]) < 0 or (c[1] + dir[1]) < 0:
            oob = True
        # See if we hit a wall
        elif lines[c[0] + dir[0]][c[1] + dir[1]] == '#':
            # Mark the new direction
            idx = (idx + 1) % 4
            dir = dirs[idx]
        # Iterate the coordinates in the given direction
        c = [c[0] + dir[0], c[1] + dir[1]]
    print(total)


def day6p2():
    f = open("day6.txt", "r")
    data = f.read()
    # Split by line first
    lines = data.split("\n")
    # Then split each line into chars
    for i in range(len(lines)):
        lines[i] = list(lines[i])
    # Now look for our starting point and set the direction
    # Lists are in order of [y, x]
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    idx = 0
    c = [0, 0]
    i = 0
    j = 0
    # Using while loops so I can just do an easy break at the end
    while i < len(lines):
        j = 0
        while j < len(lines[0]):
            if lines[i][j] == '^':
                c = [i, j]
                i = len(lines)
                j = len(lines)
            j += 1
        i += 1
    # Get all positions
    originalc = c
    oob = False
    posdata = []
    idxdata = []
    dir = dirs[idx]
    while not oob:
        # See if we're out of bounds
        if (c[0] + dir[0]) >= len(lines) or (c[1] + dir[1]) >= len(lines[0]) or (c[0] + dir[0]) < 0 or (c[1] + dir[1]) < 0:
            oob = True
            break
        # See if we hit a wall
        if lines[c[0] + dir[0]][c[1] + dir[1]] == '#':
            # Mark the new direction
            idx = (idx + 1) % 4
            dir = dirs[idx]
            # Add to posdata
            posdata.append(c)
            idxdata.append(idx)
        else:
            c = [c[0] + dir[0], c[1] + dir[1]]
            # Add to posdata
            posdata.append(c)
            idxdata.append(idx)
    # Now go through each position
    total = 0
    allblockers = []
    for i in range(len(posdata) - 1):
        newlines = copy.deepcopy(lines)
        counter = 0
        c = posdata[i]
        target = c
        idx = idxdata[i]
        dir = dirs[idx]
        targetdir = dir
        # If the next position is the starting point or a blocker, ignore it
        if newlines[c[0] + dir[0]][c[1] + dir[1]] in ('#', '^'):
            continue
        newlines[c[0] + dir[0]][c[1] + dir[1]] = '#'
        blockerpos = [c[0] + dir[0], c[1] + dir[1]]
        if blockerpos in allblockers:
            continue
        allblockers.append(blockerpos)
        # Change direction
        idx = (idx + 1) % 4
        dir = dirs[idx]
        oob = False
        visit_data = []
        while (not oob) and counter < 10000:
            newlines[c[0]][c[1]] = 'X'
            # Check if we're on the right spot and in the right direction
            if [c, dir] in visit_data:
                total += 1
                break
            visit_data.append([c, dir])
            # See if we're out of bounds
            if (c[0] + dir[0]) >= len(newlines) or (c[1] + dir[1]) >= len(newlines[0]) or (c[0] + dir[0]) < 0 or (c[1] + dir[1]) < 0:
                oob = True
                break
            # See if we hit a wall
            if newlines[c[0] + dir[0]][c[1] + dir[1]] == '#':
                # Mark the new direction and try again
                idx = (idx + 1) % 4
                dir = dirs[idx]
            else:
                # Iterate
                c = [c[0] + dir[0], c[1] + dir[1]]
            # Add to counter
            counter += 1
        print("%d/%d" % (i, len(posdata)))

    print(total)


def day7():
    f = open("day7.txt", "r")
    data = f.read()
    # Split by line first
    lines = data.split("\n")
    # Store the target and numbers in separate arrays
    targets = []
    numsets = []
    for l in lines:
        # Split into each set of numbers
        l = l.split(':')
        # Store the target
        targets.append(int(l[0]))
        # Store the rest (1: for avoiding an empty entry)
        l = l[1].split(" ")[1:]
        nums = []
        for num in l:
            nums.append(int(num))
        numsets.append(nums)
    # All non-zero values, can get funky with it
    # Maybe check multiplication first and then do addition?
    total1 = 0
    total2 = 0
    for i in range(len(targets)):
        print("%d/%d" % (i, len(targets)))
        # Store targets and nums
        t = targets[i]
        nums = numsets[i]
        # Start with all plus and multiply from there
        # if tryTwoOps(t, nums):
        #    total1 += t
        #    total2 += t
        if tryThreeOps(t, nums):
            total2 += t
    print("P1: %d" % total1)
    print("P2: %d" % total2)


def tryTwoOps(t, nums):
    # Store flags for each (binary number)
    flagbase = "{:0%db}" % (len(nums) - 1)
    # Loop through each number set
    for i in range(2**(len(nums) - 1)):
        # Start with plus
        flags = flagbase.format(i)
        total = nums[0]
        for j in range(len(nums) - 1):
            if int(flags[j]):
                # Addition
                total += nums[j + 1]
            else:
                # Multiply
                total *= nums[j + 1]
        # Check total
        if total == t:
            # It matches!
            return True
    # None found
    return False


def tryThreeOps(t, nums):
    # Loop through each number set
    for i in range(3**(len(nums) - 1)):
        # Start with plus
        flags = tripleBinary(i, len(nums) * 3)
        total = nums[0]
        for j in range(len(nums) - 1):
            match flags[j]:
                case '0':
                    # Addition
                    total += nums[j + 1]
                case '1':
                    # Multiply
                    total *= nums[j + 1]
                case '2':
                    # Append
                    total = int(str(total) + str(nums[j+1]))
        # Check total
        if total == t:
            # It matches!
            return True
    # None found
    return False


def tripleBinary(n, max):
    # I know this is extremely messy please give me patience
    flags = [0] * ((max // 3) - 1)
    flags[0] = n % 3
    for i in range(1, (max // 3) - 1):
        flags[i] = (n//(3 ** i)) % 3
    return ''.join(str(x) for x in flags)


day7()

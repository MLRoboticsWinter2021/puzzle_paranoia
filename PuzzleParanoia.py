
rows, cols = 3, 3
length = rows*cols


def main():
    puzzle = [0 for x in range(rows * cols)]
    # Get user to input 3 numbers
    for i in range(rows*cols):
        puzzle[i] = int(input("Enter numbers from 0 to " +
                              str(rows * cols - 1) + " one by one in any order: "))
    # move the bottom left tile to the right
    puzzle = moveTile(puzzle, "down")
    # output the new puzzle
    for i in range(rows):
        for j in range(cols):
            print(puzzle[i*cols+j], end=" ")
        print()

# Tile is a element in list puzzle,
# direction is one of the following: "down", "up", "left", "right"
# puzzle is a list of int with cols*rows elements


def moveTile(puzzle, direction):
    # tile not 0
    # if tile == 0:
    #     return puzzle
    # find index
    zeroIndex = puzzle.index(0)
    # if moving down
    if direction == "down":
        # Zero is not on the last rows
        if zeroIndex + cols < length:
            # switches 0 and the tile
            puzzle[zeroIndex] = puzzle[zeroIndex + cols]
            puzzle[zeroIndex + cols] = 0
        else:
            print("Cannot move down")

    # if moving up
    if direction == "up":
        if zeroIndex - cols >= 0:
           # switches 0 and the tile
            puzzle[zeroIndex] = puzzle[zeroIndex - cols]
            puzzle[zeroIndex - cols] = 0
        else:
            print("Cannot move up")

    # if moving left
    if direction == "left":
        if zeroIndex % cols != 0:
            # switches 0 and the tile
            puzzle[zeroIndex] = puzzle[zeroIndex - 1]
            puzzle[zeroIndex - 1] = 0
        else:
            print("Cannot move left")

    # if moving right
    if direction == "right":
        if zeroIndex % cols != cols - 1:
            # switches 0 and the tile
            puzzle[zeroIndex] = puzzle[zeroIndex + 1]
            puzzle[zeroIndex + 1] = 0
        else:
            print("Cannot move right")

    return puzzle


main()

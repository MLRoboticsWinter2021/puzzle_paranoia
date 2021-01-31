
rows, cols = 3, 3
length = rows*cols


def main():
    puzzle = [0 for x in range(rows * cols)]
    # Get user to input 3 numbers
    for i in range(rows*cols):
        puzzle[i] = int(input("Enter numbers from 0 to " +
                              str(rows * cols - 1) + " one by one in any order: "))
    # move the bottom left tile to the right
    puzzle = moveTile(puzzle, 8, "right")
    # output the new puzzle
    for i in range(rows):
        for j in range(cols):
            print(puzzle[i*cols+j], end=" ")
        print()

# Tile is a element in list puzzle,
# direction is one of the following: "down", "up", "left", "right"
# puzzle is a list of int with cols*rows elements


def moveTile(puzzle, tile, direction):
    # tile not 0
    if tile == 0:
        return puzzle
    # find index
    tileIndex = puzzle.index(tile)
    # if moving down
    if direction == "down":
        # tile is not on the last rows, if not on the last row, the tile below this tile needs to be 0
        if tileIndex + cols < length and puzzle[tileIndex + cols] == 0:
            # switches 0 and the tile
            puzzle[tileIndex + cols] = tile
            puzzle[tileIndex] = 0

    # if moving up
    if direction == "up":
        if tileIndex - cols >= 0 and puzzle[tileIndex - cols] == 0:
           # switches 0 and the tile
            puzzle[tileIndex - cols] = tile
            puzzle[tileIndex] = 0

    # if moving left
    if direction == "left":
        if tileIndex % cols != 0 and puzzle[tileIndex - 1] == 0:
            # switches 0 and the tile
            puzzle[tileIndex - 1] = tile
            puzzle[tileIndex] = 0

    # if moving right
    if direction == "right":
        if tileIndex % cols != cols - 1 and puzzle[tileIndex + 1] == 0:
            # switches 0 and the tile
            puzzle[tileIndex + 1] = tile
            puzzle[tileIndex] = 0

    return puzzle


main()

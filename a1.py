import random
from a1_support import *

def display_game(game, grid_size):
    """Initialy loops to create the first row of the grid.
    loops inside of the loop to create columns and rows by creating a column in each row.
    Constantly readds the string of result so that the grid joins together.
    Prints out the grid.
    Parameters:
        game (str) : Game string.
        grid_size (int) : Size of the game.
    Returns:
        result (str) : The grid
    """
    result = '  '
    for col in range(grid_size):
        if col < 9:
            result += WALL_VERTICAL + ' ' + str(col+1) + ' '
        if col >= 9:
            result +=  WALL_VERTICAL + ' ' + str(col+1)    
    result += WALL_VERTICAL 
    for row in range(grid_size):
        result += '\n' + WALL_HORIZONTAL*(grid_size*4 + 4) 
        result += '\n' + ALPHA[row] + ' ' + WALL_VERTICAL
        for col in range(grid_size):
            index = row * grid_size + col
            result += ' ' + game[index] + ' ' + WALL_VERTICAL
    result += '\n' + WALL_HORIZONTAL*(grid_size*4 + 4) 
    print(result)


def parse_position(action, grid_size):
    """Intakes the players action and identifies the format of the action.
    Gives row and  col values based on the character position in action.
    Runs some tests to see if it's valid, if so then it will give row and col a value and then return that as a tuple.
    Parameters:
        action (str) : The inputted coordinate.
        grid_size (int) : The size of the game.
    Returns:
        (tuple<int>) : Tuple of the inputted action.
    """
    if action == '':
        return 
    elif action[0] == 'f' and action[1] == ' ':
        row, col = action[2], action[3:]
        if len(row) == 1 and len(col) == len(str(grid_size)):
            if row in ALPHA and ALPHA.index(row) < grid_size and col not in ALPHA and int(col) <= int(grid_size):
                col = int(col) - 1
                row = ALPHA.index(row)
                return (row, col)
            else:
                return
    else:
        row, col = action[0],action[1:]
        if len(row) == 1 and len(col) == len(str(grid_size)):
            if row in ALPHA and ALPHA.index(row) < grid_size and col not in ALPHA and int(col) <= int(grid_size):
                col = int(col) - 1
                row = ALPHA.index(row)
                return (row,col)
            else:
                return

        
def position_to_index(position, grid_size):
    """Converts the two values of row and col into a singular index that represents the position in the game string.
    Parameters:
        position (tuple<int>) : Tuple of the inputted action.
        grid_size (int) : Size of the game .
    Returns:
        position (int) : Represents the position in the game string.
    """
    row, col = position[0],position[1]
    position = row * grid_size + col
    return position

def replace_character_at_index(game, index, character):
    """Converts the game string into a list then replaces the character at the index and then converts the list back into a string.
    Parameters:
        game (str) : Game string.
        index (int) : The actions position in the game string.
        character (str) : The character which replaces the cell once chosen.
    Returns:
        game (str) : Game string.
    """
    game = list(game)
    if game[index] == UNEXPOSED:
        game[index] = character 
    game = ''.join(game)
    return game

def flag_cell(game, index):
    """Converts the game string into a list then replaces the character at the index with a flag and then converts the list back into a string.
    Parameters:
        game (str) : Game string.
        index (int) : The actions position in the game string.
    Returns:
        game (str) : Game string.
    """
    game = list(game)
    if game[index] == UNEXPOSED:
        game[index] = FLAG 
    elif game[index] == FLAG:
        game[index] = UNEXPOSED 
    game = ''.join(game)
    return game

def index_in_direction(index, grid_size, direction):
     """Depending on the given direction, check if it has a neighbouring cell in the direction and then converts the index into that neighbouring cells index. 
     Parameters:
         index (int) : The actions position in the game string.
         grid_size (int) : Size of the game
         direction (str) : Direction relative to the chosen cell
     Returns:
         index (int) : Index based on direction
     """
     if direction == DIRECTIONS[4] and index >= grid_size and index%(grid_size) > 0:
         index = index - grid_size -1
         return index
     if direction == DIRECTIONS[0] and index >= grid_size:
         index = index - grid_size 
         return index
     if direction == DIRECTIONS[5] and index >= grid_size and (index+1)%(grid_size) > 0:
         index = index - grid_size +1
         return index
     if direction == DIRECTIONS[2] and index%(grid_size) > 0:
         index = index -1
         return index
     if direction == DIRECTIONS[3] and (index+1)%(grid_size) > 0:
         index = index +1
         return index
     if direction == DIRECTIONS[6] and index < grid_size*(grid_size-1) and index%(grid_size) > 0:
         index = index + grid_size -1
         return index
     if direction == DIRECTIONS[1] and index < grid_size*(grid_size - 1):
         index = index + grid_size
         return index
     if direction == DIRECTIONS[7] and index < grid_size*(grid_size - 1) and (index+1)%(grid_size) > 0:
         index = index + grid_size +1
         return index
    
def neighbour_directions(index, grid_size):
     """Replaces the characters inside the list with neighbouring index by running an already defined function.
     Removes all the Nones from the list and then returns that list.
     Parameters:
         index (int) : Position of action in the game string.
         grid_size (int) : Size of the game 
     Returns:
         (list<int>) : List of neighbouring indexes
     """
     list = [0,1,2,3,4,5,6,7] 
     list[0] = index_in_direction(index, grid_size, DIRECTIONS[4])
     list[1] = index_in_direction(index, grid_size, DIRECTIONS[0])
     list[2] = index_in_direction(index, grid_size, DIRECTIONS[5])
     list[3] = index_in_direction(index, grid_size, DIRECTIONS[2])
     list[4] = index_in_direction(index, grid_size, DIRECTIONS[3])
     list[5] = index_in_direction(index, grid_size, DIRECTIONS[6])
     list[6] = index_in_direction(index, grid_size, DIRECTIONS[1])
     list[7] = index_in_direction(index, grid_size, DIRECTIONS[7])
     return  [x for x in list if x is not None]

def number_at_cell(game, pokemon_locations, grid_size, index):
     """Runs two seperate loops, the first is to count how many pokemons are in neighbouring cells.
        Second one is to test if a chosen cell has a pokemon in it.
        Returns the character which should replace the chosen cell.
     Parameters:
         game (str) : Game string.
         pokemon_locations (tuple<int>) : A tuple of all pokemon locations.
         grid_size (int) : Size of the game.
         index (int) : Position of action in the game.
     Returns:
         cellnumber (str) : The number to replace the cell being revealed
     """
     i = -1
     cellnumber = 0
     while i < len(pokemon_locations)-1:
         i = i + 1
         if pokemon_locations[i] in neighbour_directions(index, grid_size):
             cellnumber = cellnumber + 1
             
     z = -1
     while z < len(pokemon_locations)-1:
          z = z+1
          if pokemon_locations[z] == index:
              cellnumber = POKEMON
     return cellnumber

def check_win(game, pokemon_locations):
     """Runs three loops to determine if each boolean is true/false.
     First boolean tests for no ~.
     Second boolean tests for all pokemons flagged.
     Third boolean tests for the amount of flags to equal the amount of pokemons.
     Returns true if all 3 booleans are satisfied.
     Parameters:
         game (str) : Game string.
         pokemon_locations (tuple<int>) : A tuple of all pokemon locations.
     Returns:
         win (bool) : Determines whether or not the player has won.
     """
     k = 0
     l = -1
     m = -1
     Flagcount = 0
     while k < len(game):
         k = k + 1
         if game[k-1] == UNEXPOSED:
             Gameexposed = False
             break
         else:
             Gameexposed = True 
         
     while l < len(pokemon_locations)-1:
         l = l + 1
         if game[pokemon_locations[l]] != FLAG:
             Pokemonflagged = False
             break
         else:
             Pokemonflagged = True 

     while m < len(game) -1:
         m = m +1
         if game[m] == FLAG:
             Flagcount += 1
         if Flagcount == len(pokemon_locations):
             Flags = True
         else:
             Flags = False  

     if Gameexposed is True and Pokemonflagged is True and Flags is True :
         win = True
     else:
         win = False
     return win    
    


def generate_pokemons(grid_size, number_of_pokemons):
     """Pokemons will be generated and given a random index within the game.    

     Parameters:
         grid_size (int): The grid size of the game.
         number_of_pokemons (int): The number of pokemons that the game will have.

     Returns:
         (tuple<int>): A tuple containing  indexes where the pokemons are
         created for the game string.
     """
     cell_count = grid_size ** 2
     pokemon_locations = ()  

     for _ in range(number_of_pokemons):
         if len(pokemon_locations) >= cell_count:           
             break
         index = random.randint(0, cell_count-1)
         while index in pokemon_locations:
             index = random.randint(0, cell_count-1)
         pokemon_locations += (index,)
     return pokemon_locations 
 
def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.
    Using some sick algorithms.
    Find all cells which should be revealed when a cell is selected.
    For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
    neighbours are revealed. If one of the neighbouring cells is also zero then
    all of that cell"s neighbours are also revealed. This repeats until no
    zero value neighbours exist.
    For cells which have a non-zero value (i.e. cells with neightbour pokemons), only
    the cell itself is revealed.
    Parameters:
 	    game (str): Game string.
 	    grid_size (int): Size of game.
 	    pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
 	    index (int): Index of the currently selected cell
    Returns:
 	    (list<int>): List of cells to turn visible.
    """
    queue = [index]
    #
    discovered = [index]
    #
    visible = []
    #
    if game[index] == FLAG:
    	return queue
    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
    	return queue
    while queue:
 	    node = queue.pop()
 	    for neighbour in neighbour_directions(node, grid_size):
 		    if neighbour in discovered or neighbour is None:
 			    continue
 		    discovered.append(neighbour)
 		    if game[neighbour] != FLAG:
 			    number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
 			    if number == 0:
 				    queue.append(neighbour)
 		    visible.append(neighbour)
    return visible

def main():
    """The main function starts of by taking inputs from the user for grid size and number of pokemons.
    The main function then creates the game string and pokemon locations.
    A loop starts which does the following, displays the game, asks for an action input, check what type of action has been inputtd.
    If the action entered is a non coordinate, it will run one of the following, help, restart, quit or none in which a second action will be asked for.
    If the action entered is a coordinate, it will test to see if it's a flag or a normal input.
    The game then runs each function changing action to a index and then checking neighbouring pokemons/if the index is a pokemon.
    The chosen index in the game string is then changed to a particular character and if it's a pokemon, the game will be over.
    Each time the user inputs an action, the game at the end will check to see if it was a winning move and if it was then a message will appear.
    If it wasnt a game winning move nor game losing, the function will loop until the user wins/loses.
    Parameters:
        action (inp) : What the user wants to do or the coordinate they want to input.
        grid_size (inp) : Size of game.
        number_of_pokemons (inp) : Number of pokemons.
    """
    grid_size = int(input('Please input the size of the grid: '))
    while grid_size not in list(range(27)):
        grid_size = int(input('Please input the size of the grid: '))
    number_of_pokemons = int(input('Please input the number of pokemons: '))
    game = UNEXPOSED*grid_size**2      
    pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
    cellnumber = 0
    while True:
        display_game(game, grid_size)
        print('')
        action = input('Please input action: ')
        if action == 'h':
            print(HELP_TEXT)
            display_game(game, grid_size)
            print('')
            action = input('Please input action: ')
        if action == ':)':
            print("It's rewind time.")
            pokemon_locations = generate_pokemons(grid_size, number_of_pokemons)
            z = -1
            game = list(game)
            while z < grid_size**2:
                z += 1
                game[z-1] = UNEXPOSED
            game = ''.join(game)    
            display_game(game, grid_size)
            print('')
            action = input('Please input action: ')
        if action == 'q':
            action = input('You sure about that buddy? (y/n): ')
            if action == 'y':
                print('Catch you on the flip side.')
                break
            if action == 'n':
                print("Let's keep going.")
                display_game(game, grid_size)
                print('')
                action = input('Please input action: ')
        if action == '':
            Flag = False 
        elif action[0] == 'f':
            Flag = True
        else:
            Flag = False 
        action = parse_position(action,grid_size)
        if action is None:
            print("That ain't a valid action buddy.")
            continue
        position = action
        index = position_to_index(position, grid_size)
        neighbour_list = neighbour_directions(index, grid_size)
        cellnumber  = number_at_cell(game, pokemon_locations, grid_size, index)
        character = str(cellnumber)
        uncover_list= big_fun_search(game, grid_size, pokemon_locations, index)
        if Flag is True: 
            game = flag_cell(game, index)
        else:    
            game = replace_character_at_index(game, index, character)
            j = -1
            while j < len(uncover_list)-1:
                j = j + 1
                index = uncover_list[j]
                cellnumber  = number_at_cell(game, pokemon_locations, grid_size, index)
                character = str(cellnumber)
                game = replace_character_at_index(game, index, character)
        if game[index] == POKEMON:
            game = replace_character_at_index(game, index, character)
            x = -1
            game = list(game)
            while x < len(pokemon_locations)-1:
                x = x + 1
                game[pokemon_locations[x]] = POKEMON
            game = ''.join(game)    
            display_game(game, grid_size)
            print('You have scared away all the pokemons.')
            break
        win = check_win(game, pokemon_locations)
        if win is True:
            display_game(game, grid_size) 
            print('You win.')
            break

"""
Runs the main function
"""
if __name__=="__main__":
    
    main()




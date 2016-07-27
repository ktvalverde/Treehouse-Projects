"""
    Project 2: Battleship Game
    Team Treehouse Python Techdegree

    Author: Kevin Valverde
    Created: 7/20/2016
    Last Updated: 7/27/2016
"""

import os


class BattleShip:
    """Battleship game logic
    1. Players enter their names
    2. Players take turns entering ships
    3. Players take turns guess coordinates to "fire" at
    4. All data is validated
    5. Boards are updated
    6. Winner is declared once all enemy ships are sunk
    """

    SHIP_INFO = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Patrol Boat", 2)
    ]

    BOARD_SIZE = 10

    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    EMPTY = 'O'
    MISS = '.'
    HIT = '*'
    SUNK = '#'

    # players dict keeps track of all the user entered data:
    # names, updated boards, ship coordinates, guess results, etc.
    players = {'player1': {'name': '', 'ship_board': '', 'guess_board': '', 'ships': []},
               'player2': {'name': '', 'ship_board': '', 'guess_board': '', 'ships': []}}

    def main(self):
        """Initial Setup"""

        self.players['player1']['name'], self.players['player2']['name'] = self.get_players()
        self.players['player1']['ship_board'], self.players['player2']['ship_board'] = self.create_boards(
            self.BOARD_SIZE)
        self.players['player1']['guess_board'], self.players['player2']['guess_board'] = self.create_boards(
            self.BOARD_SIZE)
        self.set_up_ships(self.SHIP_INFO)
        self.take_turns()

    def get_players(self):
        """Set up: Get names of players"""

        player1 = input('Player 1: What is your name? ')
        player2 = input('Player 2: What is your name? ')
        return player1, player2

    def clear_screen(self):
        """Clears the terminal screen"""

        os.system('cls' if os.name == 'nt' else 'clear')
        # print("\033c", end="")

    def print_board_heading(self):
        print("   " + " ".join([chr(c) for c in range(ord('A'), ord('A') + self.BOARD_SIZE)]))

    def print_board(self, board):
        self.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1
        print('')

    def create_boards(self, board_size):
        """Set up: Creates the game boards according to size given"""

        # take size and create empty rows with that size
        board = [board_size * 'O' for row in range(0, board_size)]
        return board, board

    def update_board(self, guess, board, result):
        """Updates game boards with hit, miss, or sunk at chosen coordinate"""

        guess_row = guess[1:]
        guess_col = ord(guess[0]) - 65
        board_list = list(board)
        row_list = list(board_list[int(guess_row) - 1])
        if result == 'hit':
            row_list[guess_col] = self.HIT
        elif result == 'miss':
            row_list[guess_col] = self.MISS
        elif result == 'sunk':
            row_list[guess_col] = self.SUNK
        board_list[int(guess_row) - 1] = "".join(row_list)
        board = board_list
        return board

    def list_ship_coordinates(self, h_or_v, start_row, start_col, ship_length):
        """Stores the each ship's coordinates in order to have them easily accessible later"""

        count = 0
        ship_coordinates = []
        if h_or_v == 'h':
            while count < ship_length:
                coordinate = {chr(start_col + count + 65) + str(start_row): ''}
                ship_coordinates.append(coordinate)
                count += 1
        elif h_or_v == 'v':
            while count < ship_length:
                coordinate = {chr(start_col + 65) + str(int(start_row) - count): ""}
                ship_coordinates.append(coordinate)
                count += 1
        return ship_coordinates

    def validate_ship_placement(self, board, h_or_v, starting_coordinate, ship):
        """Validates the user's attempt to place a ship. Checks for occupied spaces and game board borders."""

        start_row = starting_coordinate[1:]
        start_col = ord(starting_coordinate[0]) - 65
        for offset in range(0, ship):
            if h_or_v == 'h':  # horizontal placement of ship
                board_list = list(board)
                row_list = list(board_list[int(start_row) - 1])
                try:
                    if row_list[start_col + offset] != self.EMPTY:
                        return "collision"
                except IndexError:
                    return "boundary"
            else:  # vertical placement of ship
                board_list = list(board)
                if int(start_row) - offset - 1 < 0:
                    return "boundary"
                row_list = list(board_list[int(start_row) - offset - 1])
                if row_list[start_col] != self.EMPTY:
                    return "collision"
        return True

    def validate_attack_guess(self, guess, guess_board):
        """Validates user's attack guess.
        Checks if user already guessed the coordinate, guessed row, column not on game board, or gave an empty guess."""

        error = ''
        # check valid coordinate
        if len(guess) != 0:
            if 64 < ord(guess[:1]) <= (self.BOARD_SIZE + 64):
                try:
                    if len(guess[1:]) != 0 and 0 < int(guess[1:]) <= self.BOARD_SIZE:
                        # check that coordinate hasn't been guessed already
                        guess_row = guess[1:]
                        guess_col = ord(guess[0]) - 65
                        board_list = list(guess_board)
                        row_list = list(board_list[int(guess_row) - 1])
                        if row_list[guess_col] not in [self.HIT, self.MISS]:
                            return True, error
                        else:
                            error = ('You already fired on this location. It was a {}. Choose a different coordinate.'
                                     .format('hit' if row_list[guess_col] == self.HIT else 'miss'))
                    else:
                        error = 'Not a possible row. Make sure you choose a row from 1 to {}'.format(self.BOARD_SIZE)
                except ValueError:
                    error = 'Not a possible row. Make sure you choose a row from 1 to {}'.format(self.BOARD_SIZE)
            else:
                error = 'Not a possible column. Make sure you choose a column from A to {}'.format(
                    chr(self.BOARD_SIZE + 64))
        else:
            error = 'Row column coordinates can\'t be empty. Try again.'
        return False, error

    def hit_or_miss(self, guess, enemy_board):
        """Checks if user guess is a hit or a miss
        return True: hit
        return False: miss"""

        guess_row = guess[1:]
        guess_col = ord(guess[0]) - 65
        board_list = list(enemy_board)
        row_list = list(board_list[int(guess_row) - 1])
        if row_list[guess_col] in [self.VERTICAL_SHIP, self.HORIZONTAL_SHIP]:
            hit = True
        else:
            hit = False
        return hit

    def sunk_or_floating(self, guess, enemy, player):
        """Checks if a hit ship is sunk. If sunk, then updates boards and ship information.
        return True: ship is sunk
        return False: ship is floating"""

        hits_temp_list = []
        #
        # loop through 'ships' and check for ones that are still floating
        #
        for ship in self.players[enemy]['ships']:
            ship_index_num = self.players[enemy]['ships'].index(ship)
            if ship[3] == 'floating':
                for coordinate in ship[1]:
                    coordinate_index_num = self.players[enemy]['ships'][ship_index_num][1].index(coordinate)
                    for key in coordinate:
                        if key == guess:
                            #
                            # update result to be a hit
                            #
                            self.players[enemy]['ships'][ship_index_num][1][coordinate_index_num][key] = '*'
                            #
                            # loop through ship results and check to see if sunk
                            #
                            for key2 in self.players[enemy]['ships'][ship_index_num][1]:
                                key2_index = self.players[enemy]['ships'][ship_index_num][1].index(key2)
                                for value in key2:
                                    hits_temp_list.append(
                                        self.players[enemy]['ships'][ship_index_num][1][key2_index][value])
                            if hits_temp_list.count('*') == self.players[enemy]['ships'][ship_index_num][2]:
                                self.players[enemy]['ships'][ship_index_num][3] = 'sunk'
                                #
                                # loop through ship coordinates to get info to update boards with sunk symbol
                                #
                                for key3 in self.players[enemy]['ships'][ship_index_num][1]:
                                    for value2 in key3:
                                        # value2 is a ship coordinate
                                        # update enemy ship board and player guess board for each coordinate
                                        #
                                        self.players[player]['guess_board'] = self.update_board(value2, self.players[
                                            'player1'][
                                            'guess_board'], 'sunk')
                                        self.players[enemy]['ship_board'] = self.update_board(value2,
                                                                                              self.players[enemy][
                                                                                                  'ship_board'],
                                                                                              'sunk')
                                return True
                            else:
                                return False
        return False

    def check_for_win(self, enemy):
        """Checks the ship info of the enemy to see if any are still floating.
        return True: all sunk and player wins
        return False: at least one ship still floating, game is not over yet"""

        for ship in self.players[enemy]['ships']:
            if ship[3] != 'sunk':
                return False
        return True

    def set_up_ships(self, ships):
        """Main logic loop allowing players to place their ships.
        1. Gets user input
        2. Validates input
        3. Places ship and updates board
        4. Stores all ship coordinates
        """

        for k, v in self.players.items():
            print('\n{}, it is time to place ships!\n'.format(v['name']))
            self.print_board(v['ship_board'])
            # place ships according to coordinates given
            for ship in ships:
                print('Place your {}. It takes {} spaces.'.format(ship[0], ship[1]))

                while True:
                    h_or_v = input('Type H for horizontal or V for vertical placement: ').lower().strip()
                    if h_or_v in ('h', 'v'):
                        if h_or_v == 'h':
                            print('\nChoose the left-most row, column coordinate for your ship'
                                  ' (i.e. row: 5 and column: B -> B5)')
                        else:
                            print('\nChoose the bottom-most row, column coordinate for your ship'
                                  ' (i.e. row: 5 and column: B -> B5)')

                        while True:
                            starting_coordinate = input('Enter row, column coordinate: ').upper().strip()

                            if len(starting_coordinate) != 0:
                                if 64 < ord(starting_coordinate[:1]) <= (self.BOARD_SIZE + 64):
                                    try:
                                        if len(starting_coordinate[1:]) != 0 and 0 < int(
                                                starting_coordinate[1:]) <= self.BOARD_SIZE:
                                            break
                                        else:
                                            error = 'Not a possible row. Make sure you choose a row from 1 to {}' \
                                                .format(self.BOARD_SIZE)
                                    except ValueError:
                                        error = 'Not a possible row. Make sure you choose a row from 1 to {}'.format(
                                            self.BOARD_SIZE)
                                else:
                                    error = 'Not a possible column. Make sure you choose a column from A to {}'.format(
                                        chr(self.BOARD_SIZE + 64))
                            else:
                                error = 'Row column coordinates can\'t be empty. Try again.'
                                self.clear_screen()
                            print(error + '\n')
                            self.print_board(v['ship_board'])
                        check_placement = self.validate_ship_placement(v['ship_board'], h_or_v, starting_coordinate,
                                                                       ship[1])
                        if check_placement == "collision":
                            error = 'Whoops, to avoid a collision you will need to place your ship somewhere else.' \
                                    '\nChoose another starting coordinate.'
                        elif check_placement == "boundary":
                            error = 'Whoops, placing a ship there crosses the edge of the board.' \
                                    '\nChoose another starting coordinate.'
                        else:
                            break
                    else:
                        error = 'You typed {}. But you need to type an H for horizontal or V for vertical.'.format(
                            h_or_v)
                    self.clear_screen()
                    print(error + '\n')
                    self.print_board(v['ship_board'])

                start_row = starting_coordinate[1:]
                start_col = ord(starting_coordinate[0]) - 65
                ship_coordinates = self.list_ship_coordinates(h_or_v, start_row, start_col, ship[1])
                v['ships'].append([h_or_v, ship_coordinates, ship[1], 'floating'])

                # update board
                for offset in range(0, ship[1]):
                    if h_or_v == 'h':
                        # horizontal placement of ship
                        board_list = list(v['ship_board'])
                        row_list = list(board_list[int(start_row) - 1])
                        row_list[start_col + offset] = self.HORIZONTAL_SHIP
                        board_list[int(start_row) - 1] = "".join(row_list)
                        v['ship_board'] = board_list
                    else:
                        # vertical placement of ship
                        board_list = list(v['ship_board'])
                        row_list = list(board_list[int(start_row) - offset - 1])
                        row_list[start_col] = self.VERTICAL_SHIP
                        board_list[int(start_row) - offset - 1] = "".join(row_list)
                        v['ship_board'] = board_list

                # clear screen and print updated board with ships placed
                self.print_board(v['ship_board'])
            self.clear_screen()

    def take_turns(self):
        """Main logic loop allowing players to take turns and guess coordinates to attack.
        1. Switches between players (clearing screen each time)
        2. Takes player input
        3. Validates player input
        4. Checks hit, miss or sunk
        5. Updates boards
        6. Checks for winner"""

        turn_order = ['player1', 'player2']
        win = False
        while not win:
            for player in turn_order:
                if player == turn_order[0]:
                    enemy = turn_order[1]
                else:
                    enemy = turn_order[0]
                input('{}, it is your turn to attack. Press Enter key to continue. '
                      .format(self.players[player]['name']))
                self.clear_screen()
                self.print_board(self.players[player]['guess_board'])
                self.print_board(self.players[player]['ship_board'])
                while True:
                    guess = input(
                        '{}, choose coordinate to fire at? (i.e. I7): '.format(self.players[player]['name'])) \
                        .upper().strip()
                    validate_attack = self.validate_attack_guess(guess, self.players[player]['guess_board'])
                    if validate_attack[0]:
                        break
                    else:
                        error = validate_attack[1]
                    self.clear_screen()
                    print(error + '\n')
                self.clear_screen()
                if self.hit_or_miss(guess, self.players[enemy]['ship_board']):
                    if self.sunk_or_floating(guess, enemy, player):
                        result = 'sunk'
                        print('Hit and sunk!!')
                    else:
                        result = 'hit'
                        print('Hit!')
                else:
                    result = 'miss'
                    print('Miss!')

                self.players[player]['guess_board'] = self.update_board(guess,
                                                                        self.players[player]['guess_board'],
                                                                        result)
                self.players[enemy]['ship_board'] = self.update_board(guess, self.players[enemy]['ship_board'], result)
                self.print_board(self.players[player]['guess_board'])

                if self.check_for_win(enemy):
                    print('Congratulations {}! You sunk all the enemy ships and won the battle! Great work!'
                          .format(self.players[player]['name']))
                    win = True
                    break


if __name__ == '__main__':
    game = BattleShip()
    game.main()

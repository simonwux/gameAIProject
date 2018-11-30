from random import randint
from gameAIProject import objects
import pygame

WHITE = (255, 255, 255)
BROWN = (90, 39, 41)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (238, 130, 238)

NULL = 0
WALL = 1
ARMORS = 6
WEAPONS = 7
POTION = 8
SCROLLS = 9
STAIR = 10

########################################################################
#   The file of code defines the The maze of the game                  #
########################################################################


class Maze:

    screen = None
    player = None
    levels = 0
    object_list = []
    monster_list = []
    room_list = []
    maze = []
    size = [1300, 800]
    MAX_COL = 65
    MAX_ROW = 40
    step = 20
    stair_down_row = 0
    stair_down_col = 0

    def __init__(self, screen, levels):
        self.screen = screen
        self.levels = levels
        self.init_maze()
        self.add_objects()
        self.add_monsters()

    def __str__(self):
        return "The %d level of maze" % self.levels

    def init_maze(self):

        # Initialize the maze with all walls.

        for r in range(self.MAX_ROW):
            rows = []
            for c in range(self.MAX_COL):
                rows.append(WALL)
            self.maze.append(rows)

        # generate random Rooms

        number_rooms = randint(7, 10)

        for i in range(number_rooms):

            while True:

                is_occupied = False
                is_out_maze = False

                top_left_row = randint(1, self.MAX_ROW)
                top_left_col = randint(1, self.MAX_COL)
                width = randint(8, 15)
                height = randint(8, 15)

                for a in range(top_left_row - 1, min(self.MAX_ROW, (top_left_row + height + 1))):
                    for b in range(top_left_col - 1, min(self.MAX_COL, (top_left_col + width + 1))):
                        if a > self.MAX_ROW or b > self.MAX_COL or self.maze[a][b] == 0:
                            is_occupied = True

                if top_left_row + height + 1 > self.MAX_ROW or top_left_col + width + 1 > self.MAX_COL:
                    is_out_maze = True

                if not is_out_maze and not is_occupied:
                    break

            room = Room(top_left_row, top_left_col, width, height)
            self.room_list.append(room)

            for a in range(top_left_row, top_left_row + height):
                for b in range(top_left_col, top_left_col + width):
                    self.maze[a][b] = 0

        # sort the room to make it neat

        self.room_list.sort(key=lambda x: x.top_left_cols)

        # generate corridor between rooms

        for i in range(len(self.room_list) - 1):
            room_1 = self.room_list[i]
            room_2 = self.room_list[i+1]

            if not room_1.connected or not room_2.connected:
                self.generate_path(room_1, room_2)

        # add stairs to the map.

        end_room = self.room_list[number_rooms - 1]
        self.stair_down_row = end_room.top_left_rows + randint(3, end_room.height - 3)
        self.stair_down_col = end_room.top_left_cols + randint(3, end_room.width - 3)
        self.maze[self.stair_down_row][self.stair_down_col] = STAIR

    # add objects to the map. Objects are stored in the map as numbers.

    def add_objects(self):

        num_objects = 7 + randint(0, 7)

        for i in range(0, num_objects):

            types = randint(0, 5)

            while True:
                rows = randint(0, self.MAX_ROW - 1)
                cols = randint(0, self.MAX_COL - 1)
                if self.maze[rows][cols] == NULL:
                    break

            if types == 0 or types == 1 or types == 2:  # potion

                subtypes = randint(0, 31)
                if subtypes in range(0, 10):
                    new_object = objects.HitPointPotion(self.screen, rows, cols)
                elif subtypes in range(10, 20):
                    new_object = objects.MagicPointPotion(self.screen, rows, cols)
                elif subtypes in range(20, 25):
                    new_object = objects.HitPointSuperPotion(self.screen, rows, cols)
                elif subtypes in range(25, 30):
                    new_object = objects.MagicPointSuperPotion(self.screen, rows, cols)
                else:
                    new_object = objects.Elixir(self.screen, rows, cols)

                self.maze[rows][cols] = POTION

            elif types == 3:    # scrolls

                subtypes = randint(0, 7)
                if subtypes == 0:
                    new_object = objects.ScrollsOfDEF(self.screen, rows, cols)
                elif subtypes == 1:
                    new_object = objects.ScrollsOfDEX(self.screen, rows, cols)
                elif subtypes == 2:
                    new_object = objects.ScrollsOfHP(self.screen, rows, cols)
                elif subtypes == 3:
                    new_object = objects.ScrollsOfINT(self.screen, rows, cols)
                elif subtypes == 4:
                    new_object = objects.ScrollsOfMP(self.screen, rows, cols)
                elif subtypes == 5:
                    new_object = objects.ScrollsOfSTR(self.screen, rows, cols)
                elif subtypes == 6:
                    new_object = objects.ScrollsOfTeleportation(self.screen, rows, cols)
                else:
                    new_object = objects.ScrollsOfResurrection(self.screen, rows, cols)

                self.maze[rows][cols] = SCROLLS

            elif types == 4:    # weapon

                subtypes = randint(0, 9)
                if subtypes == 0:
                    new_object = objects.ShortSword(self.screen, rows, cols)
                elif subtypes == 1:
                    new_object = objects.LongSword(self.screen, rows, cols)
                elif subtypes == 2:
                    new_object = objects.HeavySword(self.screen, rows, cols)
                elif subtypes == 3:
                    new_object = objects.WoodStaff(self.screen, rows, cols)
                elif subtypes == 4:
                    new_object = objects.WindStaff(self.screen, rows, cols)
                elif subtypes == 5:
                    new_object = objects.WaterStaff(self.screen, rows, cols)
                elif subtypes == 6:
                    new_object = objects.FireStaff(self.screen, rows, cols)
                elif subtypes == 7:
                    new_object = objects.SleepFang(self.screen, rows, cols)
                else:
                    new_object = objects.AlchemyBomb(self.screen, rows, cols)

                self.maze[rows][cols] = WEAPONS

            else:   # armor
                subtypes = randint(0, 9)
                if subtypes in range(0, 3):
                    new_object = objects.Robe(self.screen, rows, cols)
                elif subtypes in range(3, 6):
                    new_object = objects.ChainMail(self.screen, rows, cols)
                elif subtypes == 6:
                    new_object = objects.Plate(self.screen, rows, cols)
                elif subtypes == 7 or subtypes == 8:
                    new_object = objects.RoundShield(self.screen, rows, cols)
                else:
                    new_object = objects.TowerShield(self.screen, rows, cols)

                self.maze[rows][cols] = ARMORS

            self.object_list.append(new_object)

    # add monsters to the map.

    def add_monsters(self):
        return

    # put the player to the map

    def add_player(self, player):

        start_room = self.room_list[0]

        while True:
            row = start_room.top_left_rows + randint(1, start_room.height - 1)
            col = start_room.top_left_cols + randint(1, start_room.width - 1)
            if self.maze[row][col] == NULL:
                break

        player.row = row
        player.col = col
        self.player = player

    # given a row number and col number, return if it is a wall.

    def is_wall(self, row, col):

        return self.maze[row][col] == WALL

    # given a row number and col number, return if it is a wall.

    def is_stair(self, row, col):

        return self.stair_down_col == col and self.stair_down_row == row

    # given a row number and col number, return the object at that position, or None if there is no pbject.

    def object_at(self, row, col):

        for objects in self.object_list:
            if objects.row == row and objects.col == col:
                return objects
        return None

    # display the content on the map.

    def display(self):

        # Stationary Objects

        for i in range(self.MAX_ROW):
            for j in range(self.MAX_COL):
                if self.maze[i][j] == WALL:
                    pygame.draw.rect(self.screen, BROWN, [j*self.step, i*self.step, self.step, self.step])
                elif self.maze[i][j] == STAIR:
                    pygame.draw.rect(self.screen, WHITE, [j * self.step, i * self.step, self.step, self.step])
                elif self.maze[i][j] == SCROLLS:
                    pygame.draw.rect(self.screen, BLUE, [j * self.step, i * self.step, self.step, self.step])
                elif self.maze[i][j] == POTION:
                    pygame.draw.rect(self.screen, GREEN, [j * self.step, i * self.step, self.step, self.step])
                elif self.maze[i][j] == ARMORS:
                    pygame.draw.rect(self.screen, RED, [j * self.step, i * self.step, self.step, self.step])
                elif self.maze[i][j] == WEAPONS:
                    pygame.draw.rect(self.screen, YELLOW, [j * self.step, i * self.step, self.step, self.step])

        # Moving characters

        pygame.draw.rect(self.screen, PURPLE, [self.player.col * self.step, self.player.row * self.step, self.step, self.step])

    # generate a path between room

    def generate_path(self, room_1, room_2):

        room_1_row = room_1.top_left_rows + randint(2, room_1.height - 2)
        room_1_col = room_1.top_left_cols + randint(2, room_1.width - 2)
        room_2_row = room_2.top_left_rows + randint(2, room_2.height - 2)
        room_2_col = room_2.top_left_cols + randint(2, room_2.width - 2)
        self.connect(room_1_row, room_1_col, room_2_row, room_2_col, randint(0, 1))
        room_1.connected = True
        room_2.connected = True

    # helper function to generate path(recursive)

    def connect(self, sr, sc, tr, tc, pattern):

        if pattern == 1:
            if sr > tr:
                self.connect(sr - 1, sc, tr, tc, pattern)
            elif sr < tr:
                self.connect(sr + 1, sc, tr, tc, pattern)
            elif sc > tc:
                self.connect(sr, sc - 1, tr, tc, pattern)
            elif sc < tc:
                self.connect(sr, sc + 1, tr, tc, pattern)
            else:
                return
        else:
            if sc > tc:
                self.connect(sr, sc - 1, tr, tc, pattern)
            elif sc < tc:
                self.connect(sr, sc + 1, tr, tc, pattern)
            elif sr > tr:
                self.connect(sr - 1, sc, tr, tc, pattern)
            elif sr < tr:
                self.connect(sr + 1, sc, tr, tc, pattern)
            else:
                return

        self.maze[sr][sc] = 0


########################################################################
#   The file of code defines the The room of the game                  #
########################################################################

# A room is defined with its Top_Left corner, its width and its height.


class Room:

    top_left_rows = 0
    top_left_cols = 0
    width = 0
    height = 0
    connected = False

    def __init__(self, rows, cols, width, height):
        self.width = width
        self.height = height
        self.top_left_rows = rows
        self.top_left_cols = cols





#***** ADVENT OF CODE 2020 *****
#************ DAY 12 ************
#****************** Part 1 *****



# get input data

input_data = None

with open("12_navigation_input.txt") as input:
    input_data = [(instr[0], int(instr[1:].strip("\n"))) for instr in input.readlines()]

# create ship class

class Ship:
    def __init__(self, pos=(0, 0), dir="E"):
        self.pos = pos
        self.dir = dir
    
    def get_dir(self):
        return self.dir
    
    def get_pos(self):
        return self.pos
    
    def change_dir(self, dir):
        self.dir = dir

    def change_pos(self, pos):
        self.pos = pos   
    
    def move(self, steps, dir=None, start=None):
        if not dir:
            dir = self.dir
        if not start:
            start = list(self.pos)
        if dir == "E":
            start[1] += steps
        elif dir == "W":
            start[1] -= steps
        elif dir == "S":
            start[0] += steps
        elif dir == "N":
            start[0] -= steps
        self.change_pos(tuple(start))
    
    def get_distance(self):
        return abs(self.pos[0] + self.pos[1])

# create function to turn ship according to instructions 

turning_directions = {
    "E": {"R": {90: "S", 180: "W", 270: "N", 360: "E"},
          "L": {90: "N", 180: "W", 270: "S", 360: "E"}},
    "S": {"R": {90: "W", 180: "N", 270: "E", 360: "S"},
          "L": {90: "E", 180: "N", 270: "W", 360: "S"}},
    "W": {"R": {90: "N", 180: "E", 270: "S", 360: "W"},
          "L": {90: "S", 180: "E", 270: "N", 360: "W"}},
    "N": {"R": {90: "E", 180: "S", 270: "W", 360: "N"},
          "L": {90: "W", 180: "S", 270: "E", 360: "N"}}
}

def turn_ship(ship, leftright, deg):
    ship.change_dir(turning_directions[ship.get_dir()][leftright][deg])

# create function to process instructions

def process_instruction(ship, instruction):
    command = instruction[0]
    how_far = instruction[1]
    if command == "F":
        ship.move(how_far)
    elif command in "ESWN":
        ship.move(how_far, command)
    elif command in "LR":
        turn_ship(ship, command, how_far)
    else:
        print("invalid instruction")

# calculate Manhattan Distance between current position and start position

test_ship = Ship()

for item in input_data:
    process_instruction(test_ship, item)

print("\nThe Manhattan Distance between the ship's current location and the starting location is:", test_ship.get_distance())
print()

#****************** Part 2 *****



# create functions to rotate waypoint

def bind_wp_to_ship(pos_ship, wp, dir, distance): 
    wp.change_pos(pos_ship)
    wp.move(distance[0], dir[0])
    wp.move(distance[1], dir[1])

def find_dir_wp(pos_ship, wp): # check if something is wrong with E/W
    dir_0 = None
    dir_1 = None
    if pos_ship[0] < wp.pos[0]:
        dir_0 = "S"
    else:
        dir_0 = "N"
    if pos_ship[1] < wp.pos[1]:
        dir_1 = "E"
    else:
        dir_1 = "W"
    return [dir_0, dir_1]

def find_distance_wp(pos_ship, wp):
    coord_0 = abs(pos_ship[0]-wp.pos[0])
    coord_1 = abs(pos_ship[1]-wp.pos[1])
    return [coord_0, coord_1]

def rotate_waypoint(pos_ship, wp, leftright, deg, distance): # continue here -- unfinished
    loc_wp = find_dir_wp(pos_ship, wp)
    dir = [turning_directions[loc_wp[0]][leftright][deg], turning_directions[loc_wp[1]][leftright][deg]]
    bind_wp_to_ship(pos_ship, wp, dir, distance)

# create function to process instructions according to new rules

def process_instruction_v2(ship, wp, instruction): # test this
    command = instruction[0]
    how_far = instruction[1]
    if command == "F":
        distance = find_distance_wp(ship.get_pos(), wp)
        dir = find_dir_wp(ship.get_pos(), wp)
        for i in range(how_far):
            ship.change_pos(wp.get_pos())
            bind_wp_to_ship(ship.get_pos(), wp, dir, distance)
    elif command in "ESWN":
        wp.move(how_far, command)
    elif command in "LR":
        rotate_waypoint(ship.get_pos(), wp, command, how_far, find_distance_wp(ship.get_pos(), wp))
    else:
        print("invalid instruction")

# calculate Manhattan Distance between current position and start position

flag_ship = Ship()
waypoint = Ship((-1, 10))

for item in input_data:
    process_instruction_v2(flag_ship, waypoint, item)

print("\nThe new Manhattan Distance between the ship's current location and the starting location is:", flag_ship.get_distance())
print()

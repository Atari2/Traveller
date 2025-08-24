from tools import *
from worlds import *
from draw_sector import *

# DM Odds
ODDS_planet_is_in_hex = 0.5 # Average planet density

# Load inputs
with open('planet_names.txt') as f:
    names_list = f.read().splitlines()
names_list_og = list(names_list)    

# Create planets
star_systems = []
x_grid_max = 8
y_grid_max = 10

for x_grid in range(x_grid_max):
    for y_grid in range(y_grid_max):
        if random.random() > ODDS_planet_is_in_hex:
            continue # No planet here.
        
        name = names_list.pop(random.randint(0,len(names_list)-1))
        code, output = create_world(name.capitalize(),f'0{x_grid}',f'0{y_grid}')
        
        star_systems.append(output)
        # print(code)
        
        if names_list == []:
            print('WARNING. Not enough names, reusing them.')
            names_list = list(names_list_og)
            
# Print sector
draw_sector(filename='sector.png', sector_name=None, star_systems=star_systems, cols=x_grid_max, rows=y_grid_max)
    
from tools import *

# Function 10 -> HEX
def ten2hex(n):
    if n < 10:
        return str(n)
    if n == 10:
        return 'A'
    if n == 11:
        return 'B'
    if n == 12:
        return 'C'
    if n == 13:
        return 'D'
    if n == 14:
        return 'E'
    if n >= 15:
        return 'F'

# DM Odds
ODDS_Hot_edge_of_Habitable_Zone = 0.05
ODDS_Cold_edge_of_Habitable_Zone = 0.05

ODDS_extremely_high_population_worlds_B = 0.05
ODDS_extremely_high_population_worlds_C = 0.01

ODDS_base_depot = 0.05
ODDS_base_way_station = 0.05
ODDS_base_prison_facilities = 0.01
ODDS_base_alien_embassies = 0.01
ODDS_base_secret_operations = 0.005

ODDS_trade_codes = 0.2

ODDS_red_code = 0.05

max_chars_in_name = 10

# Worlds tables
# Diameter [km]
worlds_diameter_min = {
    0: 0,
    1: 1000,
    2: 1600,
    3: 3200,
    4: 4800,
    5: 6400,
    6: 8000,
    7: 9600,
    8: 11200,
    9: 12800,
    10: 14400
}
worlds_diameter_max = {
    0: 1000,
    1: 1600,
    2: 3200,
    3: 4800,
    4: 6400,
    5: 8000,
    6: 9600,
    7: 11200,
    8: 12800,
    9: 14400,
    10: 16000
}
# Gravity [Gs]
worlds_gravity_min = {
    0: 0,
    1: 0,
    2: 0.05,
    3: 0.15,
    4: 0.25,
    5: 0.35,
    6: 0.45,
    7: 0.7,
    8: 0.9,
    9: 1.0,
    10: 1.25
}
worlds_gravity_max = {
    0: 0,
    1: 0.05,
    2: 0.15,
    3: 0.25,
    4: 0.35,
    5: 0.45,
    6: 0.7,
    7: 0.9,
    8: 1.0,
    9: 1.25,
    10: 1.4
}
# Atmosphere composition
worlds_atmosphere_composition = {
    0: ['None'],
    1: ['Trace'],
    2: ['Very Thin', 'Tainted'],
    3: ['Very Thin'],
    4: ['Thin', 'Tainted'],
    5: ['Thin'],
    6: ['Standard'],
    7: ['Standard', 'Tainted'],
    8: ['Dense'],
    9: ['Dense', 'Tainted'],
    10: ['Exotic'],
    11: ['Corrosive'],
    12: ['Insidious'],
    13: ['Very Dense'],
    14: ['Low'],
    15: ['Unusual']
}
# Pressure [bar]
worlds_pressure_min = {
    0: 0.00,
    1: 0.001,
    2: 0.1,
    3: 0.1,
    4: 0.43,
    5: 0.43,
    6: 0.71,
    7: 0.71,
    8: 1.5,
    9: 1.5,
    10: 0,
    11: 0,
    12: 0,
    13: 2.5,
    14: 0,
    15: 0
}
worlds_pressure_max = {
    0: 0.00,
    1: 0.09,
    2: 0.42,
    3: 0.42,
    4: 0.7,
    5: 0.7,
    6: 1.49,
    7: 1.49,
    8: 2.49,
    9: 2.49,
    10: 2.49,
    11: 2.49,
    12: 2.49,
    13: 10,
    14: 0.5,
    15: 2.49
}

def create_world(name, coordinate_x, coordinate_y):
    output = {
        'Name': name,
        'Coordinate X': coordinate_x,
        'Coordinate Y': coordinate_y,
    }

    # NAME / COORDINATES in input
    
    # SIZE
    size = roll_dices(2,6) - 2 # [0, 10]
    diameter = random.uniform(worlds_diameter_min[size], worlds_diameter_max[size]) # extra info
    gravity = worlds_gravity_min[size] + (worlds_gravity_max[size] - worlds_gravity_min[size]) * (diameter - worlds_diameter_min[size]) / (worlds_diameter_max[size] - worlds_diameter_min[size]) # extra info
        
    output['Size'] = size
    output['Diameter'] = diameter
    output['Gravity'] = gravity
        
    # ATMOSPHERE TYPE
    atmosphere = max(roll_dices(2,6) - 7 + size, 0) # [-5, 15] -> [0, 15]
    atmosphere_composition = worlds_atmosphere_composition[atmosphere]
    pressure = random.uniform(worlds_pressure_min[atmosphere],worlds_pressure_max[atmosphere])
    
    output['Atmosphere'] = atmosphere
    output['Atmosphere_composition'] = atmosphere_composition
    output['Pressure'] = pressure
    
    # HYDROGRAPHIC PERECENTAGE
    temperature_dm = 0
    
    Hot_edge_of_Habitable_Zone = False
    Cold_edge_of_Habitable_Zone = False
    habitable_zone_roll = random.random()
    if habitable_zone_roll < ODDS_Hot_edge_of_Habitable_Zone:
        Hot_edge_of_Habitable_Zone = True
        temperature_dm += 4
    elif habitable_zone_roll < ODDS_Hot_edge_of_Habitable_Zone + ODDS_Cold_edge_of_Habitable_Zone:
        Cold_edge_of_Habitable_Zone = True
        temperature_dm -= 4
    output['Hot_edge_of_Habitable_Zone'] = Hot_edge_of_Habitable_Zone
    output['Cold_edge_of_Habitable_Zone'] = Cold_edge_of_Habitable_Zone
    
    if atmosphere == 2 or atmosphere == 3:
        temperature_dm -= 2
    elif atmosphere == 4 or atmosphere == 5:
        temperature_dm -= 1
    elif atmosphere == 8 or atmosphere == 9:
        temperature_dm += 1
    elif atmosphere == 10 or atmosphere == 13 or atmosphere == 15:
        temperature_dm += 2
    elif atmosphere == 11 or atmosphere == 12:
        temperature_dm += 6
        
    temperature = roll_dices(2, 6) + temperature_dm # [-4, 22]
    output['Temperature'] = temperature
    
    if temperature <= 2:
        temperature_type = 'Frozen'
    elif temperature <= 4:
        temperature_type = 'Cold'
    elif temperature <= 9:
        temperature_type = 'Temperate'
    elif temperature <= 11:
        temperature_type = 'Hot'
    else:
        temperature_type = 'Boiling'
    output['Temperature_type'] = temperature_type

    if size == 0 or size == 1:
        hydrographics_dm = 0
        hydrographics = 0
    else:
        hydrographics_dm = 0
        if atmosphere == 0 or atmosphere == 1 or (atmosphere >= 10 and atmosphere <= 15):
            hydrographics_dm -= 4
        if not(atmosphere == 13) and not(atmosphere == 15):
            if temperature_type == 'Hot':
                hydrographics_dm -= 2
            elif temperature_type == 'Boiling':
                hydrographics_dm -= 6
        
        hydrographics = roll_dices(2, 6) - 7 + atmosphere + hydrographics_dm # [-15, 20] -> [0,10]
        if hydrographics < 0:
            hydrographics = 0
        if hydrographics > 10:
            hydrographics = 10
    output['Hydrographics'] = hydrographics

    # POPULATION
    extremely_high_population_worlds_roll = random.random()
    if extremely_high_population_worlds_roll < ODDS_extremely_high_population_worlds_B:
        population = 11
    elif extremely_high_population_worlds_roll < ODDS_extremely_high_population_worlds_B + ODDS_extremely_high_population_worlds_C:
        population = 12
    else:
        population = roll_dices(2, 6) - 2 # [0, 10] -> [0, 12]
    output['Population'] = population
        
    # GOVERNMENT TYPE
    if population == 0:
        government = 0
    else:
        government = min(max(roll_dices(2, 6) - 7 + population, 0), 15) # [-5, 17] -> [0, 15]
    output['Government'] = government
        
    number_of_factions_dm = 0
    if government == 0 or government == 7:
        number_of_factions_dm += 1
    if government >= 10:
        number_of_factions_dm -= 1
    number_of_factions = roll_dices(1,3)
    factions = []
    for faction_idx in range(number_of_factions):
        factions.append({
            'Government': min(max(roll_dices(2, 6) - 7 + population, 0), 15), # [-5, 17] -> [0, 15]
            'Relative Strength (number)': roll_dices(2, 6)
        })
        if factions[-1]['Relative Strength (number)'] <= 3:
            factions[-1]['Relative Strength'] = 'Obscure group'
        elif factions[-1]['Relative Strength (number)'] <= 5:
            factions[-1]['Relative Strength'] = 'Fringe group'
        elif factions[-1]['Relative Strength (number)'] <= 7:
            factions[-1]['Relative Strength'] = 'Minor group'
        elif factions[-1]['Relative Strength (number)'] <= 9:
            factions[-1]['Relative Strength'] = 'Notable group'
        elif factions[-1]['Relative Strength (number)'] <= 11:
            factions[-1]['Relative Strength'] = 'Significant group'
        else:
            factions[-1]['Relative Strength'] = 'Overwhelming group'
    output['Factions'] = factions
    
    cultural_differences = 10*roll_dices(1,6) + roll_dices(1,6)
    output['Cultural_differences'] = cultural_differences
    
    # LAW LEVEL
    if population == 0:
        law_level = 0
    else:
        law_level = min(max(roll_dices(2,6) - 7 + government, 0), 15) # [-5, 20] -> [0, 15]
    output['Law_level'] = law_level
    
    # STARPORT
    starport_dm = 0
    if population == 8 or population == 9:
        starport_dm += 1
    elif population >= 10:
        starport_dm += 2
    elif population == 3 or population == 4:
        starport_dm -= 1
    elif population <= 2:
        starport_dm -= 2
    starport_roll = roll_dices(2,6) + starport_dm # [0, 14]
    
    if starport_roll <= 2:
        starport_class = 'X'
    elif starport_roll <= 4:
        starport_class = 'E'
    elif starport_roll <= 6:
        starport_class = 'D'
    elif starport_roll <= 8:
        starport_class = 'C'
    elif starport_roll <= 10:
        starport_class = 'B'
    else:
        starport_class = 'A'
    output['Starport_class'] = starport_class
    
    # TECH LEVEL
    if population == 0:
        tech_level = 0
    else:
        tech_dm = 0
        if starport_class == 'A':
            tech_dm += 6
        elif starport_class == 'B':
            tech_dm += 4
        elif starport_class == 'C':
            tech_dm += 2
        elif starport_class == 'X':
            tech_dm -= 4
            
        if size == 0 or size == 1:
            tech_dm += 2
        elif size == 2 or size == 3 or size == 4:
            tech_dm += 1
            
        if atmosphere in [0,1,2,3,10,11,12,13,14,15]:
            tech_dm += 1
            
        if hydrographics == 0 or hydrographics == 9:
            tech_dm += 1
        elif hydrographics == 10:
            tech_dm += 2
            
        if population in [1,2,3,4,5,8]:
            tech_dm += 1
        elif population == 9:
            tech_dm += 2
        elif population == 10:
            tech_dm += 4
            
        if government == 0 or government == 5:
            tech_dm += 1
        elif government == 7:
            tech_dm += 2
        elif government == 13 or government == 14:
            tech_dm -= 2
        
        tech_level = min(max(roll_dices(1,6) + tech_dm, 0), 15) # [?-5, ?23] -> [0, 15]
    
    output['Tech_level'] = tech_level
    
    if ((atmosphere == 0 or atmosphere == 1) and tech_level < 8) or \
        ((atmosphere == 2 or atmosphere == 3) and tech_level < 5) or \
        ((atmosphere == 4 or atmosphere == 7 or atmosphere == 9) and tech_level < 3) or \
        ((atmosphere == 10) and tech_level < 8) or \
        ((atmosphere == 11) and tech_level < 9) or \
        ((atmosphere == 12) and tech_level < 10) or \
        ((atmosphere == 13 or atmosphere == 14) and tech_level < 5) or \
        ((atmosphere == 15) and tech_level < 8):
        environmental_limits = True
    else:
        environmental_limits = False
    output['Environmental_limits'] = environmental_limits

    # BASES / GAS GIANTS
    gas_giants_roll = roll_dices(2,6)
    if gas_giants_roll >= 10:
        gas_giants = False
    else:
        gas_giants = True
    output['Gas_giants'] = gas_giants
        
    highport_dm = 0
    if tech_level in [9,10,11]:
        highport_dm += 1
    elif tech_level >= 12:
        highport_dm += 2
    if population >= 9:
        highport_dm += 1
    elif population <= 6:
        highport_dm -= 1
    highport_roll = roll_dices(2,6) + highport_dm
    
    if (starport_class == 'A' and highport_roll >= 6) or \
        (starport_class == 'B' and highport_roll >= 8) or \
        (starport_class == 'C' and highport_roll >= 10) or \
        (starport_class == 'D' and highport_roll >= 12):
        highport = True
    else:
        highport = False
    output['Highport'] = highport
    
    bases = []
    
    corsair_dm = 0
    if law_level == 0:
        corsair_dm += 2
    elif law_level >= 2:
        corsair_dm -= 2
    corsair_roll = roll_dices(2,6) + corsair_dm
    if (starport_class == 'X' and corsair_roll >= 10) or \
        (starport_class == 'E' and corsair_roll >= 10) or \
        (starport_class == 'D' and corsair_roll >= 12):
        bases.append('C')
    
    military_roll = roll_dices(2,6)
    if (starport_class == 'A' and military_roll >= 8) or \
        (starport_class == 'B' and military_roll >= 8) or \
        (starport_class == 'C' and military_roll >= 10):
        bases.append('M')
        
    naval_roll = roll_dices(2,6)
    if (starport_class == 'A' and naval_roll >= 8) or \
        (starport_class == 'B' and naval_roll >= 8):
        bases.append('N')
        
    scout_roll = roll_dices(2,6)
    if (starport_class == 'A' and scout_roll >= 10) or \
        (starport_class == 'B' and scout_roll >= 9) or \
        (starport_class == 'C' and scout_roll >= 9) or \
        (starport_class == 'D' and scout_roll >= 8):
        bases.append('S')
        
    if random.random() < ODDS_base_depot:
        bases.append('D')
    if random.random() < ODDS_base_way_station:
        bases.append('W')
        
    if random.random() < ODDS_base_prison_facilities:
        bases.append('P')
    if random.random() < ODDS_base_alien_embassies:
        bases.append('A')
    if random.random() < ODDS_base_secret_operations:
        bases.append('O')
        
    output['Bases'] = bases
        
    # TRADE CODES
    trade_codes = []
    
    if size == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('As')
    if size in [6,7,8] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ga')
        
    if atmosphere in [4,5,6,7,8,9] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ag')
    if atmosphere == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('As')
    if atmosphere in [2,3,4,5,6,7,8,9] and random.random() < ODDS_trade_codes:
        trade_codes.append('De')
    if atmosphere >= 10 and random.random() < ODDS_trade_codes:
        trade_codes.append('Fl')
    if atmosphere in [5,6,8] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ga')
    if atmosphere in [0,1] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ic')
    if atmosphere in [0,1,2,4,7,9,10,11,12] and random.random() < ODDS_trade_codes:
        trade_codes.append('In')
    if atmosphere in [0,1,2,3] and random.random() < ODDS_trade_codes:
        trade_codes.append('Na')
    if atmosphere in [2,3,4,5] and random.random() < ODDS_trade_codes:
        trade_codes.append('Po')
    if atmosphere in [6,8] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ri')
    if atmosphere == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('Va')
    if (atmosphere in [3,4,5,6,7,8,9] or atmosphere >= 13) and random.random() < ODDS_trade_codes:
        trade_codes.append('Wa')
        
    if hydrographics in [4,5,6,7,8] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ag')
    if hydrographics == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('As')
    if hydrographics == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('De')
    if hydrographics >= 1 and random.random() < ODDS_trade_codes:
        trade_codes.append('Fl')
    if hydrographics in [5,6,7] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ga')
    if hydrographics >= 1 and random.random() < ODDS_trade_codes:
        trade_codes.append('Ic')
    if hydrographics in [0,1,2,3] and random.random() < ODDS_trade_codes:
        trade_codes.append('Na')
    if hydrographics in [0,1,2,3] and random.random() < ODDS_trade_codes:
        trade_codes.append('Po')
    if hydrographics >= 10 and random.random() < ODDS_trade_codes:
        trade_codes.append('Wa')
        
    if population in [5,6,7] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ag')
    if population == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('Ba')
    if population >= 9 and random.random() < ODDS_trade_codes:
        trade_codes.append('Hi')
    if population >= 9 and random.random() < ODDS_trade_codes:
        trade_codes.append('In')
    if population in [1,2,3] and random.random() < ODDS_trade_codes:
        trade_codes.append('Lo')
    if population >= 1 and random.random() < ODDS_trade_codes:
        trade_codes.append('Lt')
    if population >= 6 and random.random() < ODDS_trade_codes:
        trade_codes.append('Na')
    if population in [4,5,6] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ni')
    if population in [6,7,8] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ri')
        
    if government == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('Ba')
    if government in [4,5,6,7,8,9] and random.random() < ODDS_trade_codes:
        trade_codes.append('Ri')
        
    if law_level == 0 and random.random() < ODDS_trade_codes:
        trade_codes.append('Ba')
        
    if tech_level >= 12 and random.random() < ODDS_trade_codes:
        trade_codes.append('Ht')
    if tech_level <= 5 and random.random() < ODDS_trade_codes:
        trade_codes.append('Lt')
        
    trade_codes = list(set(trade_codes))
    
    conflicts = [
        ('Ag', 'Ba'),
        ('Ag', 'Na'),
        ('As', 'Fl'),
        ('As', 'Hi'),
        ('As', 'Wa'),
        ('Ba', 'Fl'),
        ('Ba', 'Ga'),
        ('Ba', 'In'),
        ('Ba', 'Ri'),
        ('Ba', 'Wa'),
        ('De', 'Fl'),
        ('De', 'Wa'),
        ('Fl', 'Va'),
        ('Ga', 'Va'),
        ('Hi', 'Lo'),
        ('Ht', 'Lt'),
        ('In', 'Ni'),
        ('Po', 'Ri'),
        ('Va', 'Ic'),
        ('Va', 'Wa'),
    ]    
    for pair in conflicts:
        if all(elem in trade_codes for elem in pair):
            to_remove = random.choice(pair)
            trade_codes.remove(to_remove)
            # print(f"Removed {to_remove} from {pair}")
    
    output['Trade_codes'] = trade_codes
    
    # TRAVEL ZONE    
    if random.random() < ODDS_red_code:
        travel_zone = 'Red'
    elif atmosphere >= 10 or \
        government in [0, 7, 10] or \
        law_level == 0 or law_level >= 9:
        travel_zone = 'Amber'
    else:
        travel_zone = 'Green'
    output['Travel_zone'] = travel_zone
        
    # OUTPUTS
    bases_string = ''
    for b in bases:
        bases_string += f'{b} '

    trade_codes_string = ''
    for t in trade_codes:
        trade_codes_string += f'{t} '
        
    if travel_zone == 'Red':
        travel_zone_string = 'R'
    elif travel_zone == 'Amber':
        travel_zone_string = 'A'
    elif travel_zone == 'Green':
        travel_zone_string = ''

    code = f'{name[:max_chars_in_name]} {coordinate_x}{coordinate_y} {starport_class}{ten2hex(size)}{ten2hex(atmosphere)}{ten2hex(hydrographics)}{ten2hex(population)}{ten2hex(government)}{ten2hex(law_level)}-{ten2hex(tech_level)} {bases_string}{trade_codes_string}{travel_zone_string}'
    output['Code'] = code
        
    return code, output
        
# code, output = create_world(name='Test', coordinate_x='01', coordinate_y='01')
# print(code)
# print(output)
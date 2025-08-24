from PIL import Image, ImageDraw, ImageFont
import math
from datetime import datetime

# Function HEX -> 10
def hex2ten(n):
    if n.isnumeric():
        return int(n)
    if n == 'A':
        return 10
    if n == 'B':
        return 11
    if n == 'C':
        return 12
    if n == 'D':
        return 13
    if n == 'E':
        return 14
    if n == 'F':
        return 15

# Finds if two systems are in jump-1 or jump-2 distance
def is_in_jump2(systemA, systemB, systems):
    def is_neighbour_2(x1, y1, x2, y2):
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        
        if (x1 == x2 and y1 == y2 - 1) or \
            (x1 == x2 and y1 == y2 + 1) or \
            (x1 == x2 - 1 and y1 == y2) or \
            (x1 == x2 + 1 and y1 == y2) or \
            (x1 == x2 - 1 and y1 == y2 + 1) or \
            (x1 == x2 + 1 and y1 == y2 + 1) or \
            (x1 == x2 and y1 == y2 + 2) or \
            (x1 == x2 and y1 == y2 - 2) or \
            (x1 == x2 + 1 and y1 == y2 - 1) or \
            (x1 == x2 - 1 and y1 == y2 - 1) or \
            (x1 == x2 + 2 and y1 == y2 - 1) or \
            (x1 == x2 - 2 and y1 == y2 - 1) or \
            (x1 == x2 + 2 and y1 == y2) or \
            (x1 == x2 - 2 and y1 == y2) or \
            (x1 == x2 + 2 and y1 == y2 + 1) or \
            (x1 == x2 - 2 and y1 == y2 + 1) or \
            (x1 == x2 + 1 and y1 == y2 + 1) or \
            (x1 == x2 - 1 and y1 == y2 + 1):
            return True
        else:
            return False
    
    systems_dyanmic = list(systems)
    boarding_systems = [systemA]
    
    while boarding_systems != []:
        current_system = boarding_systems.pop(0)
        systems_dyanmic.remove(current_system)
        
        for system in systems_dyanmic:
            if is_neighbour_2(current_system['Coordinate X'], current_system['Coordinate Y'], system['Coordinate X'], system['Coordinate Y']):
                if system == systemB:
                    return True
                elif not system in boarding_systems:
                    boarding_systems.append(system)
        
    return False

# Find the distance between planets in parsecs (manhattan)
def distance_between_planets(systemA, systemB):
    xa = int(systemA['Coordinate X'])
    ya = int(systemA['Coordinate Y'])
    xb = int(systemB['Coordinate X'])
    yb = int(systemB['Coordinate Y'])
    
    return abs(xa - xb) + abs(ya - yb)


def draw_sector(filename, sector_name, star_systems, cols, rows):
    star_systems_og = list(star_systems)    
    # === Image size (pixels) ===
    HEX_SIZE = 100
    HORIZ_DIST_HEX = 1.5 * HEX_SIZE
    VERT_DIST_HEX = math.sqrt(3) * HEX_SIZE
    
    MARGIN_LEFT = 20
    MARGIN_RIGHT = 20
    MARGIN_TOP = 20
    MARGIN_BOTTOM = 20
    
    HEXS_SIZE_X = int(HEX_SIZE * 2 + (cols-1) * 1.5 * HEX_SIZE)
    HEXS_SIZE_Y = int(VERT_DIST_HEX * rows + (VERT_DIST_HEX / 2))
    
    BOX_DATE_WIDTH = 300
    BOX_NAME_WIDTH = HEXS_SIZE_X - BOX_DATE_WIDTH
    BOXS_HEADERS_HEIGHT = 60
    MARGIN_HEADER = 20
    GAP_TEXTS_HEADER = 15
    GAP_LEFT_TEXT_HEADER = 5
    
    LEGEND_SPACE_WIDTH = 1200
    LEGEND_SPACE_HEIGHT = 550
    LEGEND_SPACE_GAP_X = 20
    LEGEND_SPACE_START_X = MARGIN_LEFT + HEXS_SIZE_X + LEGEND_SPACE_GAP_X
    LEGEND_SPACE_START_Y = MARGIN_TOP + BOXS_HEADERS_HEIGHT + MARGIN_HEADER
    
    PLANETS_CODES_GAP_Y = 20
    PLANETS_CODES_HEIGHT = 50 * len(star_systems)
    
    IMG_W = HEXS_SIZE_X + MARGIN_LEFT + MARGIN_RIGHT + LEGEND_SPACE_WIDTH + LEGEND_SPACE_GAP_X
    # IMG_H = HEXS_SIZE_Y + MARGIN_TOP + MARGIN_BOTTOM + BOXS_HEADERS_HEIGHT + MARGIN_HEADER
    IMG_H = MARGIN_BOTTOM + MARGIN_TOP + BOXS_HEADERS_HEIGHT + GAP_TEXTS_HEADER + max(HEXS_SIZE_Y + BOXS_HEADERS_HEIGHT + MARGIN_HEADER, LEGEND_SPACE_HEIGHT + PLANETS_CODES_GAP_Y + PLANETS_CODES_HEIGHT)

    # === Create white background ===
    bg_img = Image.new("RGBA", (IMG_W, IMG_H), (255, 255, 255, 255))
    bg_draw = ImageDraw.Draw(bg_img)
    img = Image.new("RGBA", (IMG_W, IMG_H), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    routes_img = Image.new("RGBA", (IMG_W, IMG_H), (255, 255, 255, 0))
    routes_draw = ImageDraw.Draw(routes_img)

    # === Fonts ===
    font_name = ImageFont.truetype("Audiowide-Regular.ttf", 35)
    font_name_system = ImageFont.truetype("Audiowide-Regular.ttf", 20)
    font_small = ImageFont.truetype("Audiowide-Regular.ttf", 20)

    # === Boxes for name & date ===
    draw.rectangle([MARGIN_LEFT, MARGIN_TOP, MARGIN_LEFT + BOX_NAME_WIDTH, MARGIN_TOP + BOXS_HEADERS_HEIGHT], outline="black", width=5)
    draw.text((MARGIN_LEFT + GAP_LEFT_TEXT_HEADER, MARGIN_TOP), "Subsector Name", font=font_small, fill="black")
    if not sector_name is None:
        draw.text((MARGIN_LEFT + GAP_LEFT_TEXT_HEADER, MARGIN_TOP + GAP_TEXTS_HEADER), sector_name.upper(), font=font_name, fill="black")

    draw.rectangle([MARGIN_LEFT + BOX_NAME_WIDTH, MARGIN_TOP, MARGIN_LEFT + BOX_NAME_WIDTH + BOX_DATE_WIDTH, MARGIN_TOP + BOXS_HEADERS_HEIGHT], outline="black", width=5)
    draw.text((MARGIN_LEFT + BOX_NAME_WIDTH + GAP_LEFT_TEXT_HEADER, MARGIN_TOP), "Date of Preparation", font=font_small, fill="black")
    today = datetime.today().strftime("%Y-%m-%d")
    draw.text((MARGIN_LEFT + BOX_NAME_WIDTH + GAP_LEFT_TEXT_HEADER, MARGIN_TOP + GAP_TEXTS_HEADER), today, font=font_name, fill="black")

    # === Legend box ===
    draw.rectangle([LEGEND_SPACE_START_X, LEGEND_SPACE_START_Y, LEGEND_SPACE_START_X + LEGEND_SPACE_WIDTH, LEGEND_SPACE_START_Y + LEGEND_SPACE_HEIGHT], outline="black", width=5)
    x = int(LEGEND_SPACE_START_X)+50
    y = int(LEGEND_SPACE_START_Y)+50
    r = 20
    draw.ellipse((x - r, y - r, x + r, y + r), outline='orange', fill='orange', width=7)
    draw.text((x + 50, y - 20), 'Amber zone', font=font_name, fill="black")
    y += 50
    draw.ellipse((x - r, y - r, x + r, y + r), outline='red', fill='red', width=7)
    draw.text((x + 50, y - 20), 'Red zone', font=font_name, fill="black")
    r = 15
    y += 50
    draw.ellipse((x - r, y - r, x + r, y + r), outline='black', fill='black', width=7)
    draw.text((x + 50, y - 20), 'Planet with water', font=font_name, fill="black")
    y += 50
    draw.ellipse((x - r, y - r, x + r, y + r), outline='black', fill=None, width=7)
    draw.text((x + 50, y - 20), 'Planet without water', font=font_name, fill="black")
    r = 7
    y += 50
    draw.ellipse((x - r, y - r, x + r, y + r), outline='black', fill='black', width=7)
    draw.text((x + 50, y - 20), 'Gas giants', font=font_name, fill="black")
    y += 50
    draw.text((x, y - 20), 'A', font=font_name, fill="black")
    draw.text((x + 50, y - 20), 'Starport class', font=font_name, fill="black")
    y += 50
    draw.text((x, y - 20), '*', font=font_name, fill="black")
    draw.text((x + 50, y - 20), 'Highports', font=font_name, fill="black")
    y += 50
    r = 9
    points = [(x, y - r), (x - r, y + r), (x + r, y + r)]
    draw.polygon(points, outline="black", fill="black")
    draw.text((x + 50, y - 20), 'Scout base', font=font_name, fill="black")
    y += 50
    r_outer = 9       # outer radius of star
    r_inner = r_outer * 0.4  # inner radius (adjust to taste)
    points = []
    for i in range(10):
        angle_deg = -90 + i * 36  # start at top (-90°), step 36°
        angle_rad = math.radians(angle_deg)
        r = r_outer if i % 2 == 0 else r_inner
        px = x + r * math.cos(angle_rad)
        py = y + r * math.sin(angle_rad)
        points.append((px, py))
    draw.polygon(points, outline="black", fill="black")
    draw.text((x + 50, y - 20), 'Naval base', font=font_name, fill="black")
    y += 50
    draw.text((x, y), str(1), font=font_small, fill="black", anchor="mm")
    draw.text((x + 50, y - 20), 'Number of other bases', font=font_name, fill="black")
    
    # === List of planets box ===
    draw.rectangle([LEGEND_SPACE_START_X, LEGEND_SPACE_START_Y + LEGEND_SPACE_HEIGHT + PLANETS_CODES_GAP_Y, LEGEND_SPACE_START_X + LEGEND_SPACE_WIDTH, LEGEND_SPACE_START_Y + LEGEND_SPACE_HEIGHT + PLANETS_CODES_GAP_Y + PLANETS_CODES_HEIGHT], outline="black", width=5)
    start_y = LEGEND_SPACE_START_Y + LEGEND_SPACE_HEIGHT + PLANETS_CODES_GAP_Y
    dy = 50
    for idx, star_system in enumerate(star_systems):
        code = star_system['Code']
        draw.text((x, start_y + dy * idx), code, font=font_name, fill="black")
    
    # === Big box ===
    draw.rectangle([MARGIN_LEFT, MARGIN_TOP + BOXS_HEADERS_HEIGHT + MARGIN_HEADER, HEXS_SIZE_X + MARGIN_LEFT, MARGIN_TOP + BOXS_HEADERS_HEIGHT + MARGIN_HEADER + HEXS_SIZE_Y], outline="black", width=5)
    
    # === Hex grid ===
    start_x = MARGIN_LEFT + HEX_SIZE
    start_y = MARGIN_TOP + BOXS_HEADERS_HEIGHT + MARGIN_HEADER + VERT_DIST_HEX // 2

    def draw_hex(xc, yc, size):
        points = [(xc + size * math.cos(math.radians(60 * i)),
                yc + size * math.sin(math.radians(60 * i))) for i in range(6)]
        points.append(points[0])
        draw.line(points, fill="black", width=2)

    # Draw systems
    sector_name = None
    max_population = 0
    star_system_idx = 0
    for col in range(cols):
        for row in range(rows):
            x = start_x + col * HORIZ_DIST_HEX
            y = start_y + row * VERT_DIST_HEX
            if col % 2 == 1:
                y += VERT_DIST_HEX / 2
            draw_hex(x, y, HEX_SIZE)
            
            if star_systems != []:
                star_system = star_systems[0]
                
                if hex2ten(str(star_system['Population'])) >= max_population:
                    max_population = hex2ten(str(star_system['Population']))
                    new_sector_name = star_system['Name']
                
                if int(star_system['Coordinate X']) == col and int(star_system['Coordinate Y']) == row: # Draw the system here
                    
                    star_systems_og[star_system_idx]['x'] = x
                    star_systems_og[star_system_idx]['y'] = y
                    star_system_idx += 1
                    
                    # Travel zone
                    if star_system['Travel_zone'] == 'Green':
                        fill_color = None
                    elif star_system['Travel_zone'] == 'Amber':
                        fill_color = (255, 165, 0, 255)
                    elif star_system['Travel_zone'] == 'Red':
                        fill_color = (255, 0, 0, 255)
                    
                    if not fill_color is None:
                        r = 75
                        draw.ellipse(
                            (x - r, y - r, x + r, y + r),
                            outline=fill_color,
                            fill=fill_color,
                            width=7
                        )
                    
                    # Planet circle
                    if star_system['Hydrographics'] == 0:  # No water
                        fill_color = None
                    else:
                        fill_color = 'black'

                    r = 15
                    draw.ellipse(
                        (x - r, y - r, x + r, y + r),
                        outline="black",
                        fill=fill_color,
                        width=7
                    )

                    # Name of the system
                    name = star_system['Name'].capitalize()
                    text_y_offset = r + 20
                    draw.text(
                        (x, y + text_y_offset),
                        name,
                        font=font_name_system,
                        fill="black",
                        anchor="mt"
                    )
                    
                    # Starpor class (and highport)
                    starport_class = star_system['Starport_class']
                    highport = star_system['Highport']
                    if highport:
                        starport_class += '*'
                    text_y_offset = r - 75
                    draw.text(
                        (x, y + text_y_offset),
                        starport_class,
                        font=font_name,
                        fill="black",
                        anchor="mt"
                    )
                    
                    # Gas giants
                    gas_gaints = star_system['Gas_giants']
                    if gas_gaints:
                        gg_x_offset = 30
                        gg_y_offset = - 30
                        r = 7
                        draw.ellipse(
                            (x - r + gg_x_offset, y - r + gg_y_offset, x + r + gg_x_offset, y + r + gg_y_offset),
                            outline="black",
                            fill='black',
                            width=7
                        )
                    
                    bases = star_system['Bases']    
                    # Scout
                    if 'S' in bases:
                        gg_x_offset = -45
                        gg_y_offset = 15
                        r = 9
                        cx = x + gg_x_offset
                        cy = y + gg_y_offset

                        # Points of triangle (upright)
                        points = [
                            (cx, cy - r),  # top
                            (cx - r, cy + r),  # bottom left
                            (cx + r, cy + r)   # bottom right
                        ]

                        draw.polygon(points, outline="black", fill="black")
                        
                    # Naval base
                    if 'N' in bases:
                        gg_x_offset = -45
                        gg_y_offset = -30
                        r_outer = 9       # outer radius of star
                        r_inner = r_outer * 0.4  # inner radius (adjust to taste)
                        cx = x + gg_x_offset
                        cy = y + gg_y_offset

                        points = []
                        for i in range(10):
                            angle_deg = -90 + i * 36  # start at top (-90°), step 36°
                            angle_rad = math.radians(angle_deg)
                            r = r_outer if i % 2 == 0 else r_inner
                            px = cx + r * math.cos(angle_rad)
                            py = cy + r * math.sin(angle_rad)
                            points.append((px, py))

                        draw.polygon(points, outline="black", fill="black")
                    
                        # Other bases
                        other_bases = [b for b in bases if b not in ('S', 'N')]
                        if other_bases:
                            count = len(other_bases)
                            gg_x_offset = -45
                            gg_y_offset = -7  # midway between triangle and star
                            cx = x + gg_x_offset
                            cy = y + gg_y_offset

                            draw.text(
                                (cx, cy),
                                str(count),
                                font=font_small,
                                fill="black",
                                anchor="mm"  # center text horizontally and vertically
                            )
                    
                    # End of system
                    star_systems.pop(0)
    
    # Draw connections
    for system_A_index, system_A in enumerate(star_systems_og):
        for system_B_index, system_B in enumerate(star_systems_og):
            if system_A_index == system_B_index:
                continue
            
            if distance_between_planets(system_A, system_B) <= 4:
                if (('In' in system_A['Trade_codes'] and 'As' in system_B['Trade_codes']) or \
                    ('In' in system_A['Trade_codes'] and 'De' in system_B['Trade_codes']) or \
                    ('In' in system_A['Trade_codes'] and 'Ic' in system_B['Trade_codes']) or \
                    ('In' in system_A['Trade_codes'] and 'Ni' in system_B['Trade_codes']) or \
                    ('Ht' in system_A['Trade_codes'] and 'As' in system_B['Trade_codes']) or \
                    ('Ht' in system_A['Trade_codes'] and 'De' in system_B['Trade_codes']) or \
                    ('Ht' in system_A['Trade_codes'] and 'Ic' in system_B['Trade_codes']) or \
                    ('Ht' in system_A['Trade_codes'] and 'Ni' in system_B['Trade_codes']) or \
                    ('Hi' in system_A['Trade_codes'] and 'Ag' in system_B['Trade_codes']) or \
                    ('Hi' in system_A['Trade_codes'] and 'Ga' in system_B['Trade_codes']) or \
                    ('Hi' in system_A['Trade_codes'] and 'Wa' in system_B['Trade_codes']) or \
                    ('Ri' in system_A['Trade_codes'] and 'Ag' in system_B['Trade_codes']) or \
                    ('Ri' in system_A['Trade_codes'] and 'Ga' in system_B['Trade_codes']) or \
                    ('Ri' in system_A['Trade_codes'] and 'Wa' in system_B['Trade_codes'])):
                    if is_in_jump2(system_A, system_B, star_systems_og):
                        routes_draw.line([(system_A['x'], system_A['y']), (system_B['x'], system_B['y'])], fill='gray', width=10)
                
    # Draw name of the system
    if sector_name is None:
        draw.text((MARGIN_LEFT + GAP_LEFT_TEXT_HEADER, MARGIN_TOP + GAP_TEXTS_HEADER), new_sector_name.upper(), font=font_name, fill="black")
    
    composite = Image.alpha_composite(
        Image.alpha_composite(bg_img.convert("RGBA"), routes_img.convert("RGBA")), img.convert("RGBA")
    )
    # === Save image ===
    composite.save(filename)

import os, time
import random as rng
from pynput import keyboard
from pynput.keyboard import Key
#Made by LackoPotato :D

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self,val):
        if not isinstance(val, vec2):
            raise TypeError("Operand must be of type vec2")
        return vec2(self.x + val.x,self.y + val.y)

    def __sub__(self,val):
        if not isinstance(val, vec2):
            raise TypeError("Operand must be of type vec2")
        return vec2(self.x - val.x,self.y - val.y)

    def __mul__(self,val):
        if isinstance(val, vec2):
            return vec2(self.x * val.x, self.y*val.y)
        elif isinstance(val, int) or isinstance(val, float):
            return vec2(self.x * val, self.y*val)
        else:
            raise TypeError("Operand must be of type vec2, int or float")
    
    def __truediv__(self,val):
        if isinstance(val, vec2):
            return vec2(self.x * val.x, self.y*val.y)
        elif isinstance(val, int) or isinstance(val, float):
            return vec2(self.x * val, self.y*val)
        else:
            raise TypeError("Operand must be of type vec2, int or float")

    def __eq__(self,val):
        return isinstance(val, vec2) and self.x == val.x and self.y == val.y

class game:
    RUNNING = True
    MAX_FPS = 6
    FPS = 0
    STATE = "title"
    CLEARING_DISPLAY = False
    SCREEN_SIZE_CHANGED = False
    SCREEN_SIZE = vec2(0,0)

    def clear_screen():
        os.system('cls||clear')
        
    TITLE_LEN = 43
    TITLE = """{m} _____  {r} _____ {e}  _____ {y}  _____ {g}  _ {c}  _____
{m}|__ __| {r}|  ___|{e} |__ __|{y} |  _  |{g} | |{c} |  ___|
{m}  | |   {r}| |___ {e}   | |  {y} | |_|_|{g} | |{c} | |___  
{m}  | |   {r}|  ___|{e}   | |  {y} |  _|  {g} | |{c} |___  |
{m}  | |   {r}| |___ {e}   | |  {y} | |  ||{g} | |{c}  ___| | 
{m}  |_|   {r}|_____|{e}   |_|  {y} |_|  ||{g} |_|{c} |_____|

{p}--------- terminal port by potato ---------"""

class key:
    BUFFER_INPUTS = True
    ACTIVE = "active"
    ACTIVEFRAMES = "active_frames"
    IGNOREFRAME = 1
    buffer = {}
    to_clear = []

    def get_axis(a,b) -> int:
        return int(key.is_pressed(b)) - int(key.is_pressed(a))
    
    def is_pressed(key_press) -> bool:
        return key_press in key.buffer and key.buffer[key_press][key.ACTIVE] and key.buffer[key_press][key.ACTIVEFRAMES] != key.IGNOREFRAME
    
    def on_press(key_press):
        if key_press in key.buffer:
            key.buffer[key_press][key.ACTIVE] = True
        else:
            key.buffer[key_press] = {key.ACTIVE:True,key.ACTIVEFRAMES:0}

    def on_release(key_press):
        if key.BUFFER_INPUTS:
            key.to_clear.append(key_press)
        else:
            key.buffer[key_press][key.ACTIVE] = False
    
    def clear_buffer():
        for key_press in key.to_clear:
            key.buffer[key_press][key.ACTIVE] = False
            key.buffer[key_press][key.ACTIVEFRAMES] = 0
        key.to_clear = []

    def increase_active_frame():
        for button in key.buffer:
            data = key.buffer[button]
            if data[key.ACTIVE]:
                data[key.ACTIVEFRAMES] += 1

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()

class c:
    magenta = '\033[95m'
    grey = '\033[90m'
    purple = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'

    colors = []
    def __init__():
        c.colors = []
        for key in vars(c):
            if key != colors:
                c.colors.append(vars(c)[key])

class render():
    screen = []

    def screen_size_changed(size:vec2):
        print("UDWODJW")
        render.screen = [[""]*size.x]*size.y
    
    def print_screen():
        fs = ""
        for layer in render.screen:
            fs += f"{''.join(layer)}\n"
        print(fs)

    def print(string:str,line:int = 0):
        for i,newline in enumerate(string.split("\n")):
            render.screen[i] = newline.split()
    
    def offset(string:str,offset:vec2):
        lines = ["\n"]*offset.y
        for line in string.split("\n"):
            lines.append((" "*offset.x + line))
        render.merge_screen(lines)

    def merge_screen(lines:list[str],offset:int = 0):
        for y,line in enumerate(lines):
            for x,char in enumerate(line.split()):
                render.screen[y+offset][x] = char
    
    def center_horizontal(string:str,size:int):
        render.offset(string,vec2(int(os.get_terminal_size().columns/2)-int(size/2),0))

    def center_vertical(string:str,size:int):
        render.offset(
            string,
            vec2(
                0,
                int(os.get_terminal_size().lines/2)-int(size/2)
                )
            )

    def center(string:str,size:vec2):
        render.offset(
            string,
            vec2(
                int(os.get_terminal_size().columns/2)-int(size.x/2),
                int(os.get_terminal_size().lines/2)-int(size.y/2)
                )
            )

    def color(string:str) -> str:
        return string.format(
            g=c.green,
            m=c.magenta,
            p=c.purple,
            c=c.cyan,
            y=c.yellow,
            r=c.red,
            gr=c.grey,
            b=c.bold,
            u=c.underline,
            e=c.end,
            )

class block:
    EMPTY = "{gr}| {e}"
    BLOCK = "[]{e}"
    pieces:list[dict[str,list[list[vec2],str,str]]] = [
	{
		"pixels":[vec2(0,0),vec2(1,0),vec2(-2,0),vec2(-1,0)],
		"color":"r"
	},
	{
		"pixels":[vec2(0,0),vec2(0,1),vec2(1,0),vec2(-1,0)],
		"color":"m",
		},
	{
		"pixels":[vec2(0,0),vec2(1,0),vec2(-1,0),vec2(1,1)],
		"color":"c",
		},
	{
		"pixels":[vec2(0,0),vec2(-1,0),vec2(1,0),vec2(-1,1)],
		"color":"g",
		},
	{
		"pixels":[vec2(0,1), vec2(-1,1),vec2(0,0),vec2(1,0)],
		"color":"e",
		},
	{
		"pixels":[vec2(0,1), vec2(-1,0),vec2(0,0),vec2(1,1)],
		"color":"y"
		},
	{
		"pixels":[vec2(0,1), vec2(-1,0),vec2(0,0),vec2(-1,1)],
		"color":"p",
		}
        ]
    
    active_screen:dict[dict[int,str]] = {}
    
    moving_blocks:list[vec2] = []
    next_piece:list[vec2] = []
    
    active_blocks:list[vec2] = []
    current_moving_color:str = ""
    next_moving_color:str = ""

    compiled_lines:list[str] = []
    changed_lines:list[int] = []

    iframes_used = 0
    MAX_IFRAMES_DELAY = 1
    MAX_IFRAMES = 5
    
    DIRECTION_DOWN:vec2 = vec2(0,1)
    SCREEN_SIZE:vec2 = vec2(10,13)
    INITIAL_START_POS:vec2 = vec2(5,0)

    def start():
        block.reload_screen()
        block.refresh_entire_screen()
        block.random_piece(True)
        iframes_used = 0
    
    def transform(vec2_array:list[vec2],direction:vec2) -> list:
        new_list:list[vec2] = []
        for vec2 in vec2_array:
            new_list.append(vec2+direction)
        return new_list

    def reload_screen():
        block.compiled_lines = [""]*block.SCREEN_SIZE.y
        block.active_screen = {y: {x: "" for x in range(block.SCREEN_SIZE.x)} for y in range(block.SCREEN_SIZE.y)}
    
    def get_piece(index:int) -> dict:
        return {
            "piece":[i+block.INITIAL_START_POS for i in block.pieces[index]['pixels']],
            "color":block.pieces[index]['color'],
            }

    #Checks if an array of vec2s is colliding with Active_Screen
    def is_colliding(vec2_array:list[vec2]) -> bool:
        for vec in vec2_array:
            if vec.y in block.active_screen and vec.x in block.active_screen[vec.y]:
                return True
        return False

    def is_colliding_existing(vec2_array:list[vec2]) -> bool:
        for vec in vec2_array:
            if vec.y in block.active_screen and block.active_screen[vec.y][vec.x] != "":
                return True
        return False
    
    def is_out_screen_x(vec2_array:list[vec2]) -> bool:
        for vec in vec2_array:
            if vec.x >= block.SCREEN_SIZE.x or vec.x < 0:
                return True
        return False
    
    def distance_out_screen(vec2_array:list[vec2]) -> vec2:
        out_of_bounds:vec2 = vec2(0,0)
        for vec in vec2_array:
            
            distance:vec2 = vec2(max(0,- vec.x) + min(0,block.SCREEN_SIZE.x - 1 - vec.x),min(0,block.SCREEN_SIZE.y - 1 - vec.y))
            
            if abs(distance.x) > abs(out_of_bounds.x):
                out_of_bounds.x = distance.x
            if abs(distance.y) > abs(out_of_bounds.y):
                out_of_bounds.y = distance.y
        return out_of_bounds

    def is_below_floor(vec2_array:list[vec2]) -> bool:
        for vec in vec2_array:
            if vec.y >= block.SCREEN_SIZE.y:
                return True
        return False
                
    def transform_vec2_to_dict(array:list[vec2],color:str) -> dict[int,dict[int,str]]:
        new_active = {}
        for vec in array:
            if not vec.y in new_active:
                new_active[vec.y] = {}
            new_active[vec.y][vec.x] = color
        return new_active
    
    def push_vec2_arr_to_active(array:list[vec2],color:str):
        new_active = block.transform_vec2_to_dict(array,color)
        for y in new_active:
            if y in block.active_screen:
                if not y in block.changed_lines:
                    block.changed_lines.append(y)
                block.active_screen[y].update(new_active[y])

    def pop_vec2_arr_from_active(array:list[vec2]):
        block.push_vec2_arr_to_active(array,"")
    
    def rotate_piece(piece_pixels:list[vec2],clockwise:bool) -> list[vec2]:
        offset = piece_pixels[0]
        local_pixels:list[vec2] = [pixel-piece_pixels[0] for pixel in piece_pixels]
        new_piece:list[vec2] = []
        if clockwise:
            for pixel in local_pixels:
                new_y = -pixel.x
                pixel.x = pixel.y
                pixel.y = new_y
                new_piece.append(pixel+offset)
        else:
            for pixel in local_pixels:
                new_x = -pixel.y
                pixel.y = pixel.x
                pixel.x = new_x
                new_piece.append(pixel+offset)
                
        return new_piece

    def get_game_screen() -> str:
        game_screen = ""
        for line in block.compiled_lines:
            game_screen += f"{line}\n"
        return game_screen

    def refresh_entire_screen():
        for y in block.active_screen:
            block.compiled_lines[y] = (block.compile_line(y))
    
    def push_visual_change():
        for y in block.changed_lines:
            block.compiled_lines[y] = block.compile_line(y)
        block.changed_lines = []

    def compile_line(changed_line:int) -> str:
        new_line = ""
        for x in block.active_screen[changed_line]:
            colour = block.active_screen[changed_line][x]
            new_line += render.color(block.EMPTY) if colour == "" else render.color("{"+colour+"}"+block.BLOCK)
        return new_line

    def get_cleared_lines() -> list:
        cleared_lines:list = []
        for line in block.changed_lines:
            full_line:str = ""
            for x in block.active_screen[line]:
                full_line += block.active_screen[line][x]
            if len(full_line) == block.SCREEN_SIZE.x:
                cleared_lines.append(line)
        return cleared_lines
    
    def random_piece(initial_start:bool = False):
        if initial_start:
            piece_data = block.get_piece(rng.randint(0,len(block.pieces)-1))
            block.moving_blocks = piece_data['piece']
            block.current_moving_color = piece_data['color']
        else:
            block.moving_blocks = block.next_piece
            block.current_moving_color = block.next_moving_color
        piece_data = block.get_piece(rng.randint(0,len(block.pieces)-1))
        block.next_piece = piece_data['piece']
        block.next_moving_color = piece_data['color']

    def get_block_string(pieces:list[vec2],color:str) -> str:
        data:dict[int,list[int]] = {}
        for vec in pieces:
            if vec.y in data:
                data[vec.y].append(vec.x)
            else:
                data[vec.y] = [vec.x]
        for line in data:
            data[line].sort()
        y_layers = list(data.keys())
        y_layers.sort()
        full_str = ""
        for y in range(y_layers[-1]+1):
            if y in data:
                for x in data[y]:
                    full_str += render.color("{"+color+"}[]{e}") if x in data[y] else "  "
            full_str += "\n"
        return full_str
  

    def pop_and_shift(line:int):
        for y in range(line-1,0,-1):
            lineToClone = block.active_screen[y].copy()
            block.active_screen[y+1] = lineToClone
            if not y in block.changed_lines:
                block.changed_lines.append(y)
        block.active_screen[0] = {x: "" for x in range(block.SCREEN_SIZE.x)}
    
class title_vars:
    selected_button = 0
    buttons = ["start","exit"]

def _title(delta:int):
    UPDATING_DISPLAY = False
    if key.get_axis(Key.up,Key.down) != 0 or key.is_pressed(Key.enter) or game.SCREEN_SIZE_CHANGED:
        game.clear_screen()
        title_vars.selected_button += key.get_axis(Key.up,Key.down)
        if title_vars.selected_button >= len(title_vars.buttons):
            title_vars.selected_button = len(title_vars.buttons)-1
        elif title_vars.selected_button < 0:
            title_vars.selected_button = 0
        
        render_title()
        render.print_screen()
        if key.is_pressed(Key.enter):
            if title_vars.selected_button == 0:
                game.STATE = 'asd'
                game.UPDATING_DISPLAY = True
            else:
                game.RUNNING = False

def render_title():
        render.center_horizontal(render.color(game.TITLE),game.TITLE_LEN)
        
        print(2*"\n")
        for button in title_vars.buttons:
            if title_vars.buttons[title_vars.selected_button] == button:
                button = "> "+button
            render.center_horizontal(button,len(button))


def _process(delta:float):
    rotate_input = key.get_axis(Key.up,Key.down)
    move_input = key.get_axis(Key.left,Key.right)
    place_input = key.is_pressed(Key.space)

    #Clear old moving block
    block.pop_vec2_arr_from_active(block.moving_blocks)
    
    is_inputing = rotate_input != 0 or move_input != 0 or place_input
    
    #Check if any input is given
    if is_inputing:
        new_active_blocks:list[vec2] = block.moving_blocks.copy()
        
        if rotate_input != 0:
            new_active_blocks = block.rotate_piece(new_active_blocks,key.get_axis(Key.up,Key.down) == 1)
        
        if move_input != 0:
            new_active_blocks = block.transform(new_active_blocks,vec2(move_input,0))

        if place_input:
            new_active_blocks = block.transform(new_active_blocks,vec2(0,1))
        
        distance_out_bounds:vec2 = block.distance_out_screen(new_active_blocks)
        if distance_out_bounds != vec2(0,0):
            new_active_blocks = block.transform(new_active_blocks,distance_out_bounds)
        
        if not block.is_colliding_existing(new_active_blocks):
            block.moving_blocks = new_active_blocks

            #If rotated, add extra iframe
            if rotate_input != 0 and rotate_input != 0:
                block.iframes_used -= 1

    blocks_transformed_down = block.transform(block.moving_blocks,block.DIRECTION_DOWN)

    #If true, placing should be delayed until next frame
    iframe_conditions = (block.MAX_IFRAMES > block.iframes_used) if is_inputing else (block.MAX_IFRAMES_DELAY > block.iframes_used)
    
    #If true, block should be placed
    place_conditions = block.is_below_floor(blocks_transformed_down) or block.is_colliding_existing(blocks_transformed_down)
    
    if place_conditions:
        if not iframe_conditions:
            block.push_vec2_arr_to_active(block.moving_blocks,block.current_moving_color)
            block.random_piece()
        block.iframes_used += 1

        lines_to_clear:list = block.get_cleared_lines()
        render.print(f"# LINES TO CLEAR: {lines_to_clear}",0)
        for line in lines_to_clear:
            block.pop_and_shift(line)
    else:
        block.moving_blocks = blocks_transformed_down
        block.iframes_used = 0
    
    block.push_vec2_arr_to_active(block.moving_blocks,block.current_moving_color)
    block.push_visual_change()
    render.print(f"""#GLOBAL: {block.active_screen}
#MOVING_BLOCKS: {block.moving_blocks}
#TRANFORMED ARR: {block.transform_vec2_to_dict(block.moving_blocks,'g')}
#ACTIVE KEY BUFFER: {key.buffer}
#ROTATE: {rotate_input != 0}
#MOVE: {move_input != 0}
#QUEUED_CLEAR: {key.to_clear}
#NEXT: {block.get_block_string(block.next_piece,block.next_moving_color)}
FPS: {game.FPS} | IFRAMES: {block.iframes_used} | DELTA: {delta}
""",1)
    key.clear_buffer()
    render.center(block.get_game_screen(),block.SCREEN_SIZE*vec2(2,1))

def _ready():
    block.start()
    game.clear_screen()
    render_title()
    game.UPDATING_DISPLAY = False


render.screen_size_changed(vec2(os.get_terminal_size().columns,os.get_terminal_size().lines))
_ready()
frame_time = 0
while game.RUNNING:
    start = time.time()
    current_screen_size = vec2(os.get_terminal_size().columns,os.get_terminal_size().lines)
    game.SCREEN_SIZE_CHANGED = current_screen_size != game.SCREEN_SIZE
    game.SCREEN_SIZE = current_screen_size
    if game.SCREEN_SIZE_CHANGED:
        render.screen_size_changed(current_screen_size)
        
    if game.STATE == "title":
        _title(frame_time)
    else:
        _process(frame_time)

    if key.BUFFER_INPUTS:
        key.clear_buffer()

    if game.CLEARING_DISPLAY:
        print("CLEAR")
        game.clear_screen()
        render.print_screen()
    key.increase_active_frame()
    
    if game.MAX_FPS == -1:
        frame_time = (time.time() - start)
    else:
        frame_time = (1/game.MAX_FPS) - (time.time() - start)
        if frame_time > 0:
            time.sleep(frame_time)
        else:
            frame_time = (time.time() - start)

    game.FPS = 1/(time.time()-start)

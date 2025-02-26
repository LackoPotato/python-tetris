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

class key:
    BUFFER_INPUTS = True
    pressed = {}
    to_clear = []

    def get_axis(a,b) -> int:
        return int(key.is_pressed(b)) - int(key.is_pressed(a))
    
    def is_pressed(key_press) -> bool:
        return key_press in key.pressed and key.pressed[key_press]
    
    def on_press(key_press):
        key.pressed[key_press] = True

    def on_release(key_press):
        if key.BUFFER_INPUTS:
            key.to_clear.append(key_press)
        else:
            key.pressed[key_press] = False
    
    def clear_buffer():
        for k in key.to_clear:
            key.pressed[k] = False
        key.to_clear = []
    
        
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

class render():
    def offset(string:str,offset:vec2):
        new_string = "\n"*offset.y
        for line in string.split("\n"):
            new_string += (" "*offset.x + line) + "\n"
        print(new_string)

    
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

class game:
    RUNNING = True
    MAX_FPS = 10
    FPS = 0
    STATE = "title"
    CLEARING_DISPLAY = False
    SCREEN_SIZE_CHANGED = False
    SCREEN_SIZE = os.get_terminal_size()

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
		"pixels":[vec2(0,0),vec2(0,1),vec2(0,-1),vec2(-1,1)],
		"color":"c",
		},
	{
		"pixels":[vec2(0,0),vec2(0,1),vec2(0,-1),vec2(1,1)],
		"color":"g",
		},
	{
		"pixels":[vec2(0,0), vec2(-1,0),vec2(0,-1),vec2(1,-1)],
		"color":"e",
		},
	{
		"pixels":[vec2(0,0), vec2(-1,-1),vec2(0,-1),vec2(1,0)],
		"color":"y"
		},
	{
		"pixels":[vec2(0,0), vec2(-1,-1),vec2(0,-1),vec2(-1,0)],
		"color":"p",
		}
        ]
    
    active_screen:dict[dict[int,str]] = {}
    
    moving_blocks:list[vec2] = []
    current_moving_color:str = ""
    
    compiled_lines:list[str] = []
    changed_lines:list[int] = []
    SCREEN_SIZE:vec2 = vec2(10,10)
    INITIAL_START_POS = vec2(5,5)

    def move_active_piece(direction:vec2):
        for i in range(len(block.moving_blocks)):
            block.moving_blocks[i] += direction

    def reload_screen():
        block.compiled_lines = [""]*block.SCREEN_SIZE.y
        block.active_screen = {y: {x: "" for x in range(block.SCREEN_SIZE.x)} for y in range(block.SCREEN_SIZE.y)}
    
    def set_piece(index:int):
        block.current_moving_color = block.pieces[index]['color']
        block.moving_blocks = [i+block.INITIAL_START_POS for i in block.pieces[index]['pixels']]

    def push_vec2_arr_to_active(array:list[vec2],color:str):
        new_active = {}
        for vec in array:
            if not vec.y in new_active:
                new_active[vec.y] = {}
            new_active[vec.y][vec.x] = color
        block.changed_lines = list(new_active)
        for y in new_active:
            block.active_screen[y].update(new_active[y])


    def rotate_piece(clockwise:bool,piece_pixels:list[vec2]) -> list[vec2]:
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

    def compile_line(changed_line:int) -> str:
        new_line = ""
        for x in block.active_screen[changed_line]:
            colour = block.active_screen[changed_line][x]
            if colour == "":
                new_line += render.color(block.EMPTY)
            else:
                new_line += render.color("{"+colour+"}"+block.BLOCK)
        return new_line

class var:
    counter = 0
    time = 0
    x = 0
    y = 0

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

        if key.is_pressed(Key.enter):
            if title_vars.selected_button == 0:
                game.STATE = 'asd'
                game.UPDATING_DISPLAY = True
            else:
                game.RUNNING = False

def render_title():
        print(os.get_terminal_size().columns,game.TITLE.find("\n")/2)
        render.center_horizontal(render.color(game.TITLE),game.TITLE_LEN)
        
        print(2*"\n")
        for button in title_vars.buttons:
            if title_vars.buttons[title_vars.selected_button] == button:
                button = "> "+button
            render.center_horizontal(button,len(button))


def _process(delta:int):
    rotate_input = key.get_axis(Key.up,Key.down)
    move_input = key.get_axis(Key.left,Key.right)
    if rotate_input != 0 or move_input != 0:
        block.push_vec2_arr_to_active(block.moving_blocks,"")
    if rotate_input != 0:
        block.moving_blocks = block.rotate_piece(key.get_axis(Key.up,Key.down) == 1,block.moving_blocks)
    if move_input != 0:
        block.move_active_piece(vec2(move_input,0))
    if rotate_input != 0 or move_input != 0:
        block.push_vec2_arr_to_active(block.moving_blocks,block.current_moving_color)
        block.push_visual_change()
    print(f"\nFPS: {game.FPS} | BUFFER: {key.pressed}")
    render.center(block.get_game_screen(),block.SCREEN_SIZE*vec2(2,1))
    key.clear_buffer()

def _ready():
    block.reload_screen()
    block.refresh_entire_screen()
    block.set_piece(rng.randint(0,len(block.pieces)-1))
    game.clear_screen()
    render_title()
    game.UPDATING_DISPLAY = False


_ready()
frame_time = 0
while game.RUNNING:
    start = time.time()
    game.SCREEN_SIZE_CHANGED = os.get_terminal_size() != game.SCREEN_SIZE
    
    if game.CLEARING_DISPLAY:
        print("CELAR")
        game.clear_screen()
        
    if game.STATE == "title":
        _title(frame_time)
    else:
        _process(frame_time)

    if key.BUFFER_INPUTS:
        key.clear_buffer()
        
    game.SCREEN_SIZE = os.get_terminal_size()
    if game.MAX_FPS == -1:
        frame_time = (time.time() - start)
    else:
        frame_time = (1/game.MAX_FPS) - (time.time() - start)
        if frame_time > 0:
            time.sleep(frame_time)
        else:
            frame_time = (time.time() - start)
    
    game.FPS = 1/(time.time()-start)

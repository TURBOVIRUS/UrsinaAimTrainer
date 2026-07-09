from ursina import *
from ursina.prefabs.color_picker import ColorPicker
from ursina.hit_info import HitInfo
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from conf import crossh, crossr, crossb, crossg, sens, selected_mode
import random
import time
import math
app = Ursina()
#window.fullscreen = True
#Text.default_font = "assets/fonts/Oswald-Regular.ttf"
#Text.default_resolution = 100 * Text.size
#------------------------------------FUNCTIONS-----------------------------------
def tracking():
    global selected_mode
    selected_mode = "tracking"
#------------------------------------FUNCTIONS (GAME TRACKING)-----------------------------------
def ballspin():
    ball.animate('rotation_y', ball.rotation_y+360, duration=2,
                 curve=curve.in_out_expo)
def ballmove():
    ball.look_at(e.position)
    #ball.position += ball.forward * time.dt * 2
    ball.position += (ball.forward * 2)/(1.0/time.dt)
    #print((ball.forward * 2)/(1.0/time.dt))
    #print(1.0/time.dt)
    #print(ball.forward)
def time_end():
    game_tracking.disable()
    player.disable()
    txt.disable()
    result_score.enable()
    result_score.parent = camera.ui
    result_score.text = "Score: %s" % round(points)
#---------------------------------------MAIN MENU------------------------------------------
class MainMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
    pass
menu = MainMenu()
def launch():
    i = open("conf.py", "w")
    i.write("sens = %s" % sensitivity.value)
    i.write("\n")
    i.write("crossr = %s" % colorPicker.color.r)
    i.write("\n")
    i.write("crossg = %s" % colorPicker.color.g)
    i.write("\n")
    i.write("crossb = %s" % colorPicker.color.b)
    i.write("\n")
    i.write("crossh = %s" % colorPicker.color.h)
    i.write("\n")
    i.write("selected_mode = '%s'" % selected_mode)
    i.close()
    if selected_mode == "tracking":
        game_tracking.enable()
        txt.parent = camera.ui
        timer.parent = camera.ui
    menu.disable()
    player.enable()
    camera.parent = player.camera_pivot
    camera.position = (0, 0, 0)
    camera.rotation = (0, 0, 0)
    global start_time
    start_time = time.time()
    result_score.disable()
def volumeChange():
    a.volume = volume.value
#--------------------------------------OBJECTS (MAIN MENU)------------------------------------
a = Audio('assets/sounds/epic.mp3', loop=True, autoplay=True, parent=menu)
a.volume = 1
volume = Slider(0, 2, default = 1, x = -0.25, y = -0.27, on_value_changed = volumeChange, parent=menu)
play = Button(text = 'Play', on_click=launch, color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0, parent=menu)
sensitivity = Slider(0, 200, default = 100, x = -0.25, y = -0.2, parent=menu)
txtSens = Text(text = "Sensitivity:", y = -0.188, x = -0.40, parent=menu)
txtVol = Text(text = 'Music volume:', y = -0.26, x = -0.445, parent=menu)
txtName = Text(text = 'Aim Trainer', y = 0.2, scale = 2.5, x = -0.17, parent=menu)
colorPicker = ColorPicker(x = -0.55, y = 0.35, parent=menu)
flTitle = Text(text = 'Ursina!', x = 0.4, y = 0.12, origin = (0,0), parent=menu)
crosscolor = Text(text='Crosshair color:', x = -0.8, y = 0.4, parent=menu)
mode_menu = DropdownMenu("Mode", buttons=[DropdownMenuButton('Tracking', on_click=tracking)], y=-0.18, x=0.4, parent=menu)
colorPicker.h_slider.value = int(crossh)
colorPicker.s_slider.value = 100
colorPicker.v_slider.value = 100
x = 1
#--------------------------------------GAME (TRACKING)----------------------------------------
class Game_Tracking(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    pass
game_tracking = Game_Tracking(enabled=False)
#-----------------------------------VARIABLES (GAME TRACKING)--------------------------------
countdown = 60
points = 0
game_ended = False
h = int(float(crossh))
r = float(crossr)
g = float(crossg)
b = float(crossb)
ss = float(sens)
#-------------------------------OBJECTS (GAME TRACKING)-------------------------------
plane = Entity(model='plane', scale=100, color=color.green,
       collider='box', texture = 'grass', shader = lit_with_shadows_shader, parent=game_tracking)
ball = Entity(model='sphere', color = color.black, shader = lit_with_shadows_shader, position = Vec3(5, 1, 0), collider = 'sphere', parent=game_tracking)
player = FirstPersonController(collider = 'box', enabled=False)
txt = Text(text = "Points: %s" % points, position = window.top_left, parent=game_tracking)
e = Entity(scale = 0.5, collider = 'box', parent=game_tracking)
timer = Text(text="111111111", position = Vec2(-0.06, 0.5), parent=game_tracking)
result_score = Text(text="0", x=0, y=0, origin=(0, 0), size=.05)
#-----------------------------------PROPERTIES (GAME TRACKING)-----------------------------
player.rotation_y = 90
player.cursor.color = rgb(r, g, b)
player.mouse_sensitivity = Vec2(ss, ss)
z = random.randint(-5, 5)
y = random.randint(1, 5)
e.position = Vec3(5, y, z)
game_tracking.disable()
current_timer = None
#----------------------------------------MAINLOOP-------------------------------------
def update():
    global current_timer
    global game_ended
    if menu.enabled:
        global x
        y = (sin(x * 0.1)**2) + 1
        x = x + 1
        if flTitle and flTitle.enabled:
            flTitle.scale = y
        '''print("---------------------------------")
        print("Game: %s" % game_tracking.enabled)
        print("Plane: %s" % plane.enabled)
        print("Ball: %s" % ball.enabled)
        print("TXT: %s" % txt.enabled)
        print("e: %s" % e.enabled)
        print("Player: %s" % player.enabled)
        print("game_tracking:", game_tracking.enabled)
        print("plane visible:", plane.visible)
        print("plane enabled:", plane.enabled)
        print("disabled ancestor:", plane.has_disabled_ancestor())'''
    else:
        if current_timer != 0:
            current_timer = countdown - (math.floor(time.time() - start_time))
            timer.text = current_timer
        elif game_ended == False:
            time_end()
            game_ended = True
        ballmove()
        if ball.intersects(e).hit:
            z = random.randint(-5, 5)
            y = random.randint(1, 5)
            e.z = z
            e.y = y
        global points
        if player.position != Vec3(0, 0, 0):
            player.position = Vec3(0, 0, 0)
        if ball.hovered == True:
            points += 0.1
            txt.text = "Points: %s" % round(points)
        '''print("---------------------------------")
        print("Game: %s" % game_tracking.enabled)
        print("Plane: %s" % plane.enabled)
        print("Ball: %s" % ball.enabled)
        print("TXT: %s" % txt.enabled)
        print("e: %s" % e.enabled)
        print("Player: %s" % player.enabled)
        print("game_tracking:", game_tracking.enabled)
        print("plane visible:", plane.visible)
        print("plane enabled:", plane.enabled)
        print("disabled ancestor:", plane.has_disabled_ancestor())'''
app.run()

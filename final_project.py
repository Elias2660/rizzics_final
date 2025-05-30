from vpython import *

# changing properties
t = 0.00
dt = 0.0001
vy = 0


# world properties
G = 9.81  # for gravity
BALL_SCALING_FACTOR = 5
started = False
scene.width = 400
scene.range = 1.3
scene.height = 800

scene.title = "Fluid Simulation"

# fluid properties
# kg / m^3
P = 997   # for density of fluid

# fluid box properties
fluid_length = 8
fluid_height = 7
fluid_width = 2
fluid_x = 0
fluid_y = -2
fluid_z = 0

# properties of object
cd = 0.47  # drag coefficient
ball_radius = 0.05  # radius of the ball (meters)
m =  (0.91 * (1e2 ** 3) / 1e3) * (4 * pi * (ball_radius ** 3)  / 3 ) # mass of the ball, default to rubber density
h = 0  # height submerged
V = 0  # for volume displaced



# BUTTONS FOR CHANGING THE ORIGINAL DENSITY

# UNITS: kg / m^3
# https://www.suebel.net/About/Materials
# shrug emoji
# https://www.ck12.org/flexi/physical-science/buoyancy/a-rubber-ball-floats-on-water-with-one-third-of-its-volume-outside-the-water-what-is-the-density-of-the-rubber/
RUBBER_DENSITY = 0.6 * (1e2 ** 3) / 1e3

# https://www.engineeringtoolbox.com/ice-thermal-properties-d_576.html
ICE_DENSITY = 0.91 * (1e2 ** 3) / 1e3

# https://en.wikipedia.org/wiki/Polystyrene
# https://www.aqua-calc.com/page/density-table/substance/styrofoam
STYROFOAM_DENSITY =  0.05 * (1e2 ** 3) / 1e3

# https://www.solitaire-overseas.com/blog/density-of-steel/
STEEL_DENSITY = 7.85 * (1e2 ** 3) / 1e3


def change_to_rubber_density(evt): 
    global m
    volume = 4 * pi * (ball_radius ** 3)  / 3 
    m =  RUBBER_DENSITY * volume
    return evt

def change_to_metal_density(evt): 
    global m
    volume = 4 * pi * (ball_radius ** 3 ) / 3 
    m =  STYROFOAM_DENSITY * volume
    return evt

def change_to_styrofoam_density(evt): 
    global m
    volume = 4 * pi * (ball_radius ** 3)  / 3 
    m = STEEL_DENSITY * volume
    return evt

rubber_ball_button = button(bind=change_to_rubber_density, text="Rubber Density")
metal_ball_button = button(bind=change_to_metal_density, text="Metal Density")
styrofoam_ball_button = button(
    bind=change_to_styrofoam_density, text="Styrofoam Density"
)


# START/PAUSE/PLAY BUTTON
start_button, pause_play_button = None, None
def start(evt):
    global started, start_button, pause_play_button, height_slider
    started = True
    # removing presetting stuff
    start_button.delete()
    height_slider.disabled=True
    pause_play_button.disabled = False
    return evt

def toggle(evt):
    global pause_play_button, started
    if not pause_play_button.disabled:
        # mostly a meaningless check but still let's roll with it
        if not started:
            pause_play_button.text = "Pause"
            started = True
        else:
            pause_play_button.text = "Play"
            started = False
    return evt

start_button = button(bind=start, text="Start Simulation")
pause_play_button = button(bind=toggle, text="Pause", disabled = True)



# INITIAL HEIGHT + POSITION

y_init = 2

scene.camera.pos = vector(
    0, y_init / 2, 2
)  # This tells VPython to view the scene from the position (0,5,10)


slider_yy = y_init
yy = y_init

pos_text = None
height_slider = None

def change_initial_height(evt):
    global slider_yy, pos_text, height_slider

    slider_yy = evt.value
    pos_text.text = "Initial Height: " + str(height_slider.value)


height_slider = slider(bind=change_initial_height, min=0, max=5, value=y_init, pos=scene.title_anchor)
pos_text = wtext(text=f"Initial Height: {y_init}")


g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Y Position"), align="left")
yyDots = gdots(color=color.green, graph=g1)

g2 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Velocity"), align="left")
vyDots = gdots(color=color.red, graph=g2)


ball = sphere(pos=vector(0, y_init, 0), radius=ball_radius * BALL_SCALING_FACTOR, color=color.red)

water = box(
    pos=vector(fluid_x, fluid_y, fluid_z),
    size=vector(fluid_length, fluid_height, fluid_width),
    color=vector(0, 0, 1),
    opacity=0.5,
)


# while yy > -3.65:
while yy > fluid_y - fluid_height / 2 + ball_radius:
    rate(1 / dt)

    if not started:
        ball.pos = vector(0, slider_yy, 0)
        yy = slider_yy
    else:
        gravity_force = -m * G

        height_submerged = 0
        if yy - ball_radius >= fluid_y + fluid_height / 2 + ball_radius:
            # the ball is above the water
            height_submerged = 0
        elif yy + ball_radius >= fluid_y + fluid_height / 2 + ball_radius:
            # the ball is somewhat submerged
            height_submerged = (fluid_y + fluid_height / 2 + ball_radius) - (yy - ball_radius)
        else:
            # the ball is fully submerged
            height_submerged = 2 * ball_radius
        
        buoyant_force =  (1 / 3) * pi * P * G * (height_submerged ** 2) * (3 * ball_radius - height_submerged)

        fy = gravity_force + buoyant_force  # calculating the force of gravity
        ay = fy / m  # calculating the acceleration of gravity
        vy = vy + ay * dt  # calculating the gradient of velocity
        yy = yy + vy * dt  # calculating the change in position

        ball.pos = vector(0, yy, 0)

        yyDots.plot(t, yy)
        vyDots.plot(t, vy)

        t = t + dt

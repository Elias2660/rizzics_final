from vpython import *

# changing properties
t = 0.00
dt = 0.0001
vy = 0


# world properties
G = 9.81  # for gravity

# fluid properties
# kg / m^3
P = 997   # for density of fluid

# fluid box properties
fluid_length = 5
fluid_height = 3
fluid_width = 2
fluid_x = 0
fluid_y = -2
fluid_z = 0

# properties of object
cd = 0.47  # drag coefficient
ball_radius = 0.3  # radius of the ball
m =  (1.2 * (1e2 ** 2) / 1e3) * (4 * pi * ball_radius * 3  / 3 ) # mass of the ball, default to rubber density
h = 0  # height submerged
V = 0  # for volume displaced


# BUTTONS FOR CHANGING THE ORIGINAL DENSITY
# UNITS: kg / m^3

# https://www.suebel.net/About/Materials
RUBBER_DENSITY = 1.2 * (1e2 ** 2) / 1e3

# https://en.wikipedia.org/wiki/Polystyrene
STYROFOAM_DENSITY = 1.005 * (1e2 ** 2) / 1e3

# https://www.solitaire-overseas.com/blog/density-of-steel/
STEEL_DENSITY = 7.85 * (1e2 ** 2) / 1e3


def change_to_rubber_density(evt): 
    global m
    volume = 4 * pi * ball_radius * 3  / 3 
    m =  RUBBER_DENSITY * volume
    return evt


def change_to_metal_density(evt): 
    global m
    volume = 4 * pi * ball_radius * 3  / 3 
    m =  STYROFOAM_DENSITY * volume
    return evt

def change_to_styrofoam_density(evt): 
    global m
    volume = 4 * pi * ball_radius * 3  / 3 
    m = STEEL_DENSITY * volume
    return evt

canvas(width=600, height=800, resizable=True, visible=True, align="left")


rubber_ball_button = button(bind=change_to_rubber_density, text="Rubber Density")
metal_ball_button = button(bind=change_to_metal_density, text="Metal Density")
styrofoam_ball_button = button(
    bind=change_to_styrofoam_density, text="Styrofoam Density"
)


y_init = 3
def change_initial_height(evt):
    y_init = evt.value

height_slider = slider(bind = change_initial_height, min = 0, max = 5, value = y_init)


yy = y_init
yy = y_init

g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Y Position"), align="left")
yyDots = gdots(color=color.green, graph=g1)

g2 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Velocity"), align="left")
vyDots = gdots(color=color.red, graph=g2)


ball = sphere(pos=vector(0, y_init, 0), radius=ball_radius, color=color.red)

box(
    pos=vector(fluid_x, fluid_y, fluid_z),
    size=vector(fluid_length, fluid_height, fluid_width),
    color=vector(0, 0, 1),
    opacity=0.5,
)


scene.camera.pos = vector(
    0, y_init / 2, 2
)  # This tells VPython to view the scene from the position (0,5,10)


total_volume = (4 / 3) * pi * pow(ball_radius, 3)

# while yy > -3.65:
while yy > fluid_y - fluid_height / 2 + ball_radius:
    rate(1 / dt)
    gravity_force = -m * G
    buoyant_force = 0
    if yy <= (fluid_y + fluid_height / 2 + ball_radius): 
        buoyant_force =  P * G * total_volume
    
    fy = gravity_force + buoyant_force  # calculating the force of gravity
    ay = fy / m  # calculating the acceleration of gravity
    vy = vy + ay * dt  # calculating the gradient of velocity
    yy = yy + vy * dt  # calculating the change in position

    ball.pos = vector(0, yy, 0)

    yyDots.plot(t, yy)
    vyDots.plot(t, vy)

    t = t + dt

from vpython import *

# changing properties
t = 0.00
dt = 0.0005
vy = 0
vx = 2
xx = 0


# world properties
G = 9.81  # for gravity
BALL_SCALING_FACTOR = 5
started = False
scene.width = 400
scene.range = 1.3
scene.height = 800
scene.align = "left"
scene.caption = ""

scene.title = "Fluid Simulation"

# fluid properties
# kg / m^3
P = 997  # for density of fluid

# fluid box properties
fluid_length = 8
fluid_height = 10
fluid_width = 2
fluid_x = 0
fluid_y = -4
fluid_z = 0

# properties of object
cd = 0.47  # drag coefficient
ball_radius = 0.05  # radius of the ball (meters)
m = (0.91 * (1e2**3) / 1e3) * (
    4 * pi * (ball_radius**3) / 3
)  # mass of the ball, default to rubber density
h = 0  # height submerged
V = 0  # for volume displaced


# START/PAUSE/PLAY BUTTON

scene.append_to_caption("Global Controls\n")
start_button, pause_play_button = None, None


def start(evt):
    global started, start_button, pause_play_button, height_slider, start_button, vx_slider, t
    global styrofoam_ball_button, metal_ball_button, rubber_ball_button, ice_ball_button
    started = True
    t = 0
    # removing presetting stuff
    start_button.disabled = True
    height_slider.disabled = True
    pause_play_button.disabled = False
    reset_button.disabled = False
    vx_slider.disabled = True
    
    styrofoam_ball_button.disabled = True
    rubber_ball_button.disabled = True
    metal_ball_button.disabled = True
    ice_ball_button.disabled = True


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


def reset(evt):
    global yy, vy, vx, start_button, vx_slider
    global pause_play_button, height_slider, started, t, g1, g2, vyDots, yyDots, height_slider, xx, vx
    global rubber_ball_button, metal_ball_button, rubber_ball_button, ice_ball_button
    yy = height_slider.value
    t = 0
    vy = 0
    xx = 0
    vx = vx_slider.value
    started = False
    start_button.disabled = False
    pause_play_button.text = "Pause"
    pause_play_button.disabled = True
    height_slider.disabled = False
    vx_slider.disabled = False
    reset_button.disabled = True

    rubber_ball_button.disabled = False
    metal_ball_button.disabled = False
    rubber_ball_button.disabled = False
    styrofoam_ball_button.disabled = False
    ice_ball_button.disabled = False

    # clear graphs
    vyDots.delete()
    yyDots.delete()

    return evt


start_button = button(bind=start, text="Start Simulation")
pause_play_button = button(bind=toggle, text="Pause", disabled=True)
reset_button = button(bind=reset, text="Reset", disabled=True)

# BUTTONS FOR CHANGING THE ORIGINAL DENSITY

# UNITS: kg / m^3
# https://www.suebel.net/About/Materials
# shrug emoji
# https://www.ck12.org/flexi/physical-science/buoyancy/a-rubber-ball-floats-on-water-with-one-third-of-its-volume-outside-the-water-what-is-the-density-of-the-rubber/
RUBBER_DENSITY = 0.6 * (1e2**3) / 1e3

# https://www.engineeringtoolbox.com/ice-thermal-properties-d_576.html
ICE_DENSITY = 0.91 * (1e2**3) / 1e3

# https://en.wikipedia.org/wiki/Polystyrene
# https://www.aqua-calc.com/page/density-table/substance/styrofoam
STYROFOAM_DENSITY = 0.05 * (1e2**3) / 1e3

# https://www.solitaire-overseas.com/blog/density-of-steel/
STEEL_DENSITY = 7.85 * (1e2**3) / 1e3



def change_to_rubber_density(evt):
    global m, ball_radius
    volume = 4 * pi * (ball_radius**3) / 3
    m = RUBBER_DENSITY * volume
    return evt


def change_to_metal_density(evt):
    global m, ball_radius
    volume = 4 * pi * (ball_radius**3) / 3
    m = STEEL_DENSITY * volume
    return evt


def change_to_styrofoam_density(evt):
    global m, ball_radius
    volume = 4 * pi * (ball_radius**3) / 3
    m = STYROFOAM_DENSITY * volume
    return evt


def change_to_ice_density(evt):
    global m, ball_radius
    volume = 4 * pi * (ball_radius**3) / 3
    m = ICE_DENSITY * volume
    return evt

scene.append_to_caption("\nDensity Presets \n")
rubber_ball_button = button(bind=change_to_rubber_density, text="Rubber Density")
metal_ball_button = button(bind=change_to_metal_density, text="Metal Density")
styrofoam_ball_button = button(
    bind=change_to_styrofoam_density, text="Styrofoam Density"
)
ice_ball_button = button(
    bind=change_to_ice_density, text="Ice Density"
)

# INITIAL HEIGHT + POSITION

y_init = 2

scene.camera.pos = vector(
    0, y_init / 2, 13
)  # This tells VPython to view the scene from the position (0,5,10)


yy = y_init
pos_text = None
height_slider = None


def change_initial_height(evt):
    global pos_text, height_slider
    height_slider.value = evt.value
    pos_text.text = f"Initial Height: {height_slider.value}"
    return evt


scene.append_to_caption("\nChange Initial Height\n")
height_slider = slider(bind=change_initial_height, min=-5, max=15, value=y_init)
pos_text = wtext(text=f"Initial Height: {y_init}")


vx_init = 0
vx = vx_init


def change_initial_vx(evt):
    global vx_slider_text, vx_slider, vx
    vx_slider.value = evt.value
    vx = vx_slider.value
    vx_slider_text.text = f"Initial X-Vel: {vx_slider.value}"
    return evt


scene.append_to_caption("\nChange Initial x Velocity\n")
vx_slider = slider(bind=change_initial_vx, min=-5, max=5, value=vx_init)
vx_slider_text = wtext(text=f"Initial X Velocity: {vx_init}")


scene.append_to_caption("\n\n Graphs\n")

g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Y Position"), align="left")
yyDots = gcurve(color=color.green, graph=g1)

g2 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Velocity"), align="left")
vyDots = gcurve(color=color.red, graph=g2)


ball = sphere(
    pos=vector(0, y_init, 0), radius=ball_radius * BALL_SCALING_FACTOR, color=color.red
)

water = box(
    pos=vector(fluid_x, fluid_y, fluid_z),
    size=vector(fluid_length, fluid_height, fluid_width),
    color=vector(0, 0, 1),
    opacity=0.5,
)


while True:
    rate(1 / dt)

    if yy < fluid_y - fluid_height / 2 + ball_radius:
        yy = fluid_y - fluid_height / 2 + ball_radius
        vy = 0

    if not started and t == 0:
        ball.pos = vector(0, height_slider.value, 0)
        yy = height_slider.value
    elif not started:
        ...
    else:
        gravity_force = -m * G

        height_submerged = 0
        if yy - ball_radius >= fluid_y + fluid_height / 2 + ball_radius:
            # the ball is above the water
            height_submerged = 0
        elif yy + ball_radius >= fluid_y + fluid_height / 2 + ball_radius:
            # the ball is somewhat submerged
            height_submerged = (fluid_y + fluid_height / 2 + ball_radius) - (
                yy - ball_radius
            )
        else:
            # the ball is fully submerged
            height_submerged = 2 * ball_radius

        buoyant_force = (
            (1 / 3)
            * pi
            * P
            * G
            * (height_submerged**2)
            * (3 * ball_radius - height_submerged)
        )

        resistive_force_y = (
            (1 / 2)
            * cd
            * P
            * (vy**2)
            * (((ball_radius**2) - ((ball_radius - height_submerged) ** 2)) ** (1 / 2))
        )
        resistive_force_x = (
            (1 / 2)
            * cd
            * P
            * (vx**2)
            * (((ball_radius**2) - ((ball_radius - height_submerged) ** 2)) ** (1 / 2))
        )

        if vy > 0:
            resistive_force_y *= -1
        if vx > 0:
            resistive_force_x *= -1

        fy = gravity_force + buoyant_force + resistive_force_y
        ay = fy / m  # calculating the acceleration of gravity
        vy = vy + ay * dt  # calculating the gradient of velocity
        yy = yy + vy * dt  # calculating the change in position

        fx = resistive_force_x
        ax = fx / m  # calculating the x-component acceleration
        vx = vx + ax * dt  # calculating the x-component velocity
        xx = xx + vx * dt  # calculating the x-component position

        yyDots.plot(t, yy)
        vyDots.plot(t, vy)

        t = t + dt

    # Plot the ball no matter what
    ball.pos = vector(xx, yy, 0)

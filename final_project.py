from vpython import *

# changing properties
t = 0.00
dt = 0.0005
vy = 0
vx = 2
xx = 0


# world properties
G = 9.81  # for gravity
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
fluid_length = 50
fluid_height = 8
fluid_width = 6
fluid_x = 0
fluid_y = -4
fluid_z = 0

# properties of object
cd = 0.47  # drag coefficient
ball_radius_init = 0.05  # radius of the ball (meters), should be ball_radius_init
ball_radius = ball_radius_init # change ball_radius variable above to ball_radius_init

ball_mass = (0.91 * (1e2**3) / 1e3) * (
    4 * pi * (ball_radius**3) / 3
)  # mass of the ball, default to rubber density
h = 0  # height submerged
Volume_Displaced = 0  # for volume displaced


# START/PAUSE/PLAY BUTTON

scene.append_to_caption("Global Controls\n")
start_button, pause_play_button = None, None


def start(evt):
    global started, start_button, pause_play_button, height_slider, start_button, vx_slider, t
    global styrofoam_ball_button, metal_ball_button, rubber_ball_button, ice_ball_button
    global density_slider
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
    density_slider.disabled = True
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
    global pause_play_button, height_slider, started, t, height_slider, xx, vx
    global rubber_ball_button, metal_ball_button, rubber_ball_button, ice_ball_button, density_slider
    global vyDots, yyDots, vxDots, xxDots, axDots, ayDots, bfDots, dxDots, dyDots
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

    # update buttons regarding density
    density_slider.disabled = False

    density = (ball_mass / ((4 / 3) * pi * (ball_radius**3))) 
    if density != RUBBER_DENSITY:
        rubber_ball_button.disabled = False

    if density != STEEL_DENSITY:
        metal_ball_button.disabled = False

    if density != RUBBER_DENSITY:
        rubber_ball_button.disabled = False

    if density != STYROFOAM_DENSITY:
        styrofoam_ball_button.disabled = False

    if density != ICE_DENSITY:
        ice_ball_button.disabled = False

    # clear graphs
    vyDots.delete()
    yyDots.delete()
    vxDots.delete()
    xxDots.delete()
    axDots.delete()
    ayDots.delete()
    bfDots.delete()
    dxDots.delete()
    dyDots.delete()
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
    global ball_mass, ball_radius, rubber_ball_button, metal_ball_button, styrofoam_ball_button, ice_ball_button
    global density_slider, density_slider_text

    # change the other values of the buttons to feel more seamless
    density_slider.value = RUBBER_DENSITY
    density_slider_text.text = f"Density: {RUBBER_DENSITY} (kg / m^3)"
    rubber_ball_button.disabled = True
    metal_ball_button.disabled = False
    styrofoam_ball_button.disabled = False
    ice_ball_button.disabled = False

    # actually update mass
    volume = 4 * pi * (ball_radius**3) / 3
    ball_mass = RUBBER_DENSITY * volume
    return evt


def change_to_metal_density(evt):
    global ball_mass, ball_radius, rubber_ball_button, metal_ball_button, styrofoam_ball_button, ice_ball_button
    global density_slider, density_slider_text

    # change the other values of the buttons to feel more seamless
    density_slider.value = STEEL_DENSITY
    density_slider_text.text = f"Density: {STEEL_DENSITY} (kg / m^3)"
    rubber_ball_button.disabled = False
    metal_ball_button.disabled = True
    styrofoam_ball_button.disabled = False
    ice_ball_button.disabled = False

    # actually update mass
    volume = 4 * pi * (ball_radius**3) / 3
    ball_mass = STEEL_DENSITY * volume
    return evt


def change_to_styrofoam_density(evt):
    global ball_mass, ball_radius, rubber_ball_button, metal_ball_button, styrofoam_ball_button, ice_ball_button
    global density_slider, density_slider_text

    # change the other values of the buttons to feel more seamless
    density_slider.value = STYROFOAM_DENSITY
    density_slider_text.text = f"Density: {STYROFOAM_DENSITY} (kg / m^3)"
    rubber_ball_button.disabled = False
    metal_ball_button.disabled = False
    styrofoam_ball_button.disabled = True
    ice_ball_button.disabled = False

    # actually update mass
    volume = 4 * pi * (ball_radius**3) / 3
    ball_mass = ICE_DENSITY * volume
    return evt


def change_to_ice_density(evt):
    global ball_mass, ball_radius, rubber_ball_button, metal_ball_button, styrofoam_ball_button, ice_ball_button
    global density_slider, density_slider_text

    # change the other values of the buttons to feel more seamless
    density_slider.value = ICE_DENSITY
    density_slider_text.text = f"Density: {ICE_DENSITY} (kg / m^3)"
    rubber_ball_button.disabled = False
    metal_ball_button.disabled = False
    styrofoam_ball_button.disabled = False
    ice_ball_button.disabled = True
    
    # actually update mass
    volume = 4 * pi * (ball_radius**3) / 3
    ball_mass = ICE_DENSITY * volume
    return evt



scene.append_to_caption("\n Updating Density \n")

rubber_ball_button = button(bind=change_to_rubber_density, text="Rubber Density")
metal_ball_button = button(bind=change_to_metal_density, text="Metal Density")
styrofoam_ball_button = button(
    bind=change_to_styrofoam_density, text="Styrofoam Density"
)

ice_ball_button = button(bind=change_to_ice_density, text="Ice Density", disabled=True)


def change_density(evt):
    global density_slider, density_slider_text, ball_mass, rubber_ball_button, metal_ball_button
    global styrofoam_ball_button, ice_ball_button, ball_mass

    # if the slider is used, reenable buttons that don't equal slider value
    density_slider.value = evt.value
    density_slider_text.text = f"Density: {density_slider.value} (kg / m^3)"
    ball_mass = evt.value *  4 * pi * (ball_radius**3) / 3

    #  update buttons so stuff doesn't become too confusing
    if density_slider.value != ICE_DENSITY:
        ice_ball_button.disabled = False
    else:
        ice_ball_button.disabled = True

    if density_slider.value != STYROFOAM_DENSITY:
        styrofoam_ball_button.disabled = False
    else:
        styrofoam_ball_button.disabled = True

    if density_slider.value != ICE_DENSITY:
        ice_ball_button.disabled = False
    else:
        ice_ball_button.disabled = True

    if density_slider.value != RUBBER_DENSITY:
        rubber_ball_button.disabled = False
    else:
        rubber_ball_button.disabled = True

scene.append_to_caption("\n Manually Change Density\n")
density_slider = slider(bind=change_density, min=0, max=10000, value=ICE_DENSITY)
density_slider_text = wtext(text=f"Density: {ICE_DENSITY} (kg / m^3)")

scene.append_to_caption("\n")

# INITIAL HEIGHT + POSITION

y_init = 2

scene.camera.pos = vector(
    0, y_init / 2, 13
)  # This tells VPython to view the scene from the position (0,5,10)


yy = y_init


def change_initial_height(evt):
    global pos_text, height_slider, yy
    height_slider.value = evt.value
    yy = height_slider.value
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


def change_radius(evt):
    global r_slider, r_slider_text, ball_radius, ball_radius_init, ball, ball_mass
    density = ball_mass / ((4 / 3) * pi * (ball_radius ** 3))
    r_slider.value = evt.value
    ball_radius = r_slider.value
    ball.radius = ball_radius 
    ball_mass = density * ((4 / 3) * pi * (ball_radius ** 3))
    r_slider_text.text = f"Radius: {r_slider.value}"
    return evt

scene.append_to_caption("\nChange Radius\n")
r_slider = slider(bind = change_radius, min = 0, max = 2, value = ball_radius)
r_slider_text = wtext(text=f"Radius: {ball_radius}")


scene.append_to_caption("\n\n\n\n Graphs\n\n\n")

g1 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Position"), align="left")
xxDots = gcurve(color=color.magenta, graph=g1, label = "X Position")
yyDots = gcurve(color=color.green, graph=g1, label="Y Position")


g2 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Velocity"), align="left")
vxDots = gcurve(color=color.blue, graph=g2, legend = True, label = "X Velocity")
vyDots = gcurve(color=color.red, graph=g2, legend = True, label="Y Velocity")

g3 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Acceleration"), align="left")
axDots = gcurve(color=color.blue, graph=g3, legend = True, label = "X Acceleration")
ayDots = gcurve(color=color.red, graph=g3, legend = True, label="Y Acceleration")


g4 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Buoyant Force"), align="left")
bfDots = gcurve(color=color.blue, graph=g4, legend = True, label = "Buoyant Force")

g5 = graph(width=350, height=250, xtitle=("Time"), ytitle=("Drag Force"), align="left")
dxDots = gcurve(color=color.cyan, graph=g5, legend = True, label = "X-Drag")
dyDots = gcurve(color=color.green, graph=g5, legend = True, label = "Y-Drag")


ball = sphere(
    pos=vector(0, y_init, 0), radius=ball_radius, color=color.red
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

    if started:
        gravity_force = -ball_mass * G
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
            (1 / 2) * cd * P * (vy**2) * 2 * pi * ball_radius * height_submerged
        )

        resistive_force_x = (
            (1 / 2) * cd * P * (vx**2) * 2 * pi * ball_radius * height_submerged
        )

        if vy > 0:
            resistive_force_y *= -1
        if vx > 0:
            resistive_force_x *= -1

        fy = gravity_force + buoyant_force + resistive_force_y
        ay = fy / ball_mass  # calculating the acceleration of gravity
        vy = vy + ay * dt  # calculating the gradient of velocity
        yy = yy + vy * dt  # calculating the change in position

        fx = resistive_force_x
        ax = fx / ball_mass  # calculating the x-component acceleration
        vx = vx + ax * dt  # calculating the x-component velocity
        xx = xx + vx * dt  # calculating the x-component position

        yyDots.plot(t, yy)
        xxDots.plot(t, xx)
        vyDots.plot(t, vy)
        vxDots.plot(t, vx)

        axDots.plot(t, ax)
        ayDots.plot(t, ay)

        dxDots.plot(t, resistive_force_x)
        dyDots.plot(t, resistive_force_y)

        bfDots.plot(t, buoyant_force)

        t = t + dt

    # Plot the ball no matter what
    ball.pos = vector(xx, yy, 0)

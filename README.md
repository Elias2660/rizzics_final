'''
Elias Xu, Geoffrey Huang
Period 4/5

Summary:
- Our final project models the dropping (or throwing) of a ball into a fluid
- There exist presets for the material of the ball and type of fluid, but the user can also manually adjust other settings

Instructions:
- Global Controls
    - Start Simulation: begins running the simulation
    - Pause: stops the simulation (appears at start or once Play has been clicked)
    - Play: resumes the simulation (appears once Pause has been clicked)
    - Reset: resets simulation to its initial position, keeps previous settings
- Updating Density
    - Presets (buttons)
        - Rubber Density: changes density of ball to that of rubber
        - Metal Density: changes density of ball to that of metal
        - Styrofoam Density: changes density of ball to that of styrofoam
        - Ice Density: changes density of ball to that of ice (ball is initially made of ice)
    - Manually Change Density (slider): click on slider to manually adjust ball density to desired value
- Other Properties (sliders)
    - Change Initial Height: click on slider to manually adjust starting height to desired value (initial height is 2 meters)
    - Change Initial x Velocity: click on slider to manually adjust starting horizontal velocity (initial velocity is zero)
    - Change Initial y Velocity: click on slider to manually adjust starting vertical velocity (initial velocity is zero)
    - Change Radius: click on slider to manually adjust ball radius (initial radius is 0.1 meters)
- Fluid Density
    - Presets (buttons)
        - Blood Density: changes density of fluid to that of blood
        - Water Density: changes density of fluid to that of water (initial density of fluid is that of water)
        - Mercury Density: changes density of fluid to that of mercury
        - Honey Density: changes density of fluid to that of honey
        - Crude Density: changes density of fluid to that of crude oil
    - Change Fluid Density (slider): click on slider to manually adjust fluid density to desired value
- Graphs
    - Position vs Time: tracks both horizontal and vertical position as time goes on
    - Velocity vs Time: tracks both horizontal and vertical velocity as time goes on
    - Acceleration vs Time: tracks both horizontal and vertical acceleration as time goes on
    - Drag Force vs Time: tracks both horizontal and vertical drag force as time goes on
    - Buoyant Force vs Time: tracks both horizontal and vertical buoyant force as time goes on
    
Notes:
- User may need to zoom in/out to view the ball
- Buttons will become unavailable once clicked on, but will reappear when a different setting is selected
- The ball will stop once it hits the boundaries of the fluid (farthest left/right and bottom)

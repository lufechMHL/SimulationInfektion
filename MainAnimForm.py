import tkinter
import time
import HumanDataBase


#region constant definitions 
# width of the simulation window
simulation_window_width=1500
# height of the simulation window
simulation_window_height=1000
# initial x position of the ball
simulation_ball_start_xpos = 50
# initial y position of the ball
simulation_ball_start_ypos = 50
# radius of the ball
simulation_ball_radius = 10
# the pixel movement of ball for each iteration
simulation_ball_min_movement = 2
# delay between successive frames in seconds
simulation_refresh_seconds = 0.01
# Scale pixel / meters
simulation_scale_meter2pixel = 0.5
# Scale time multiplicator 
simulation_human_count = 5

#endregion

#region create the main window of the simulation
def create_simulation_window():
    window = tkinter.Tk()
    window.title("Tkinter simulation Demo")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{simulation_window_width}x{simulation_window_height}')
    return window
#endregion
 
#region Create a canvas for simulation and add it to main window
def create_simulation_canvas(window):
    canvas = tkinter.Canvas(window)
    canvas.configure(bg="black")
    canvas.pack(fill="both", expand=True)
    return canvas
#endregion
 
#region create and animate humans in an infinite loop
def simulate_humans(window, canvas,xinc,yinc):
    #initialize Simulatorbase
    maxx = simulation_window_width * simulation_scale_meter2pixel
    maxy = simulation_window_height * simulation_scale_meter2pixel
    HumanDataBase.Initialize(maxx, maxy, simulation_human_count)


    #create here all human-instances  
    human = canvas.create_oval(simulation_ball_start_xpos-simulation_ball_radius,
            simulation_ball_start_ypos-simulation_ball_radius,
            simulation_ball_start_xpos+simulation_ball_radius,
            simulation_ball_start_ypos+simulation_ball_radius,
            fill="blue", outline="white", width=1)

    #region main-loop
    while True:

        canvas.move(human,xinc,yinc)
        window.update()

        time.sleep(simulation_refresh_seconds)

        #region simulation movement here 
        human_pos = canvas.coords(human)
        # unpack array to variables
        xl,yl,xr,yr = human_pos
        if xl < abs(xinc) or xr > simulation_window_width-abs(xinc):
            xinc = -xinc
        if yl < abs(yinc) or yr > simulation_window_height-abs(yinc):
            yinc = -yinc
        #endregion
    #endregion
#endregion 


#region main-program ------------------------------------------------------------------------------------------
simulation_window = create_simulation_window()
simulation_canvas = create_simulation_canvas(simulation_window)
simulate_humans(simulation_window,simulation_canvas, simulation_ball_min_movement, simulation_ball_min_movement)
#endregion ----------------------------------------------------------------------------------------------------
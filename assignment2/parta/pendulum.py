# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt
import os
import traceback
from graphics import *
from prettytable import PrettyTable


class PendulumSim():
    ## Initiailse global variables
    # System constant, will not change
    sim_const = {
        'g': 9.81,
        'rad_deg_ratio': 57.29577951,
        'deg_rad_ratio': 0.01745329
    }

    # default params, can be edited by user
    sim_params = {
        'mass': 1.0,
        'length': 1.0,
        'drag_coef': 0.1,
        'time_step': 0.02,
        'init_angle': 30,
        'total_time': 4
    }

    # system variables temp, refreshed every step
    sim_vars = {
        'tg': 0.0,
        'drag_force': 0.0,
        'accel': 0.0,
        'vel': 0.0,
        'dis': 0.0,
        'ang': 0.0,
        'time': 0.0,
    }

    # Params keys for ordered printing.
    sim_params_keys = ['mass', 'length', 'drag_coef',
                       'time_step', 'init_angle', 'total_time']

    # Initialise global variables of lists for holding all the results of a whole caclulation process.
    ang_array = []
    vel_array = []
    accel_array = []
    dis_array = []
    turn_point_array = []


    def reset_vars(self):

    # This function is for reseting the global variables for new calculation
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme

        # reset the global variables
        self.sim_vars = {
            'tg': 0.0,
            'drag_force': 0.0,
            'accel': 0.0,
            'vel': 0.0,
            'dis': 0.0,
            'ang': 0.0,
            'time': 0.0,
        }
        self.ang_array = []
        self.vel_array = []
        self.accel_array = []
        self.dis_array = []
        self.turn_point_array = []


    def show_params(self):
    

    # This function is for printing the params menu for option 1
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme

        # Print each params in the format 'Name' + 'Value'
        # 'for' loop for printing them in order
        for key in self.sim_params_keys:
            print(key+": "+str(self.sim_params[key]))


    def set_param(self, key):
    

    # This function is for editing each sumulation variable.
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme
    #           key         (string)            the key of the 'sim_params' dictionary which
    #                                           prefer to be edited.

        try:
            print('\n')
            param_input = input(key+": ")

            # If input is not empty, set the new value
            if param_input != '':
                self.sim_params[key] = float(param_input)

        # Catch the wrong input
        except Exception:
            print("Invaild input")

        # Clean the screen
        os.system('CLS')

        # Call the funtion to print/refresh the edited params menu
        self.show_params()


    def sim_cal(self):


    # This function is for calculating the results of a single step, and store the results into the
    # global list variables above.
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme


        # if it is the start point, read the init_angle for params menu and set it to the temp variable (sim_vars).
        if self.sim_vars['time'] == 0:
            angle = "%.4f" % (self.sim_params['init_angle'] * \
                self.sim_const['deg_rad_ratio'])
            self.angle.append(float(angle))
            self.vel.append(0)
            self.accel.append(0)
            self.dis.append(0)
            self.turnPoint.append(True)
            self.sim_vars['time'] += self.sim_params['time_step']

        if self.sim_vars['time'] != 0:
            # calculate the tangent force
            self.sim_vars['tg'] = -1*self.sim_const['g'] * \
                self.sim_params['mass']*math.sin(self.sim_vars['ang'])

            # calculate the drag force
            self.sim_vars['drag_force'] = self.sim_vars['vel'] * \
                math.fabs(self.sim_vars['vel'])*self.sim_params['drag_coef']

            # calculate the acceleration
            self.sim_vars['accel'] = (
                self.sim_vars['tg']-self.sim_vars['drag_force'])/self.sim_params['mass']

            #############################################################################
            # integrate the acceleration above to get the velocity
            self.sim_vars['vel'] += self.sim_params['time_step'] * \
                self.sim_vars['accel']

            # integrate the velocity above to get the displacement
            self.sim_vars['dis'] += self.sim_params['time_step'] * \
                self.sim_vars['vel']

            # use the displacement above to calculate the new angle 
            self.sim_vars['ang'] = (
                self.sim_vars['dis'] / self.sim_params['length']) + (self.sim_params['init_angle'] * self.sim_const['deg_rad_ratio'])
            
            # integrate the time
            self.sim_vars['time'] += self.sim_params['time_step']

            # create four temp variable to convert decimals
            angle = "%.4f" % (self.sim_vars['ang']
                            * self.sim_const['rad_deg_ratio'])
            vel = "%.4f" % self.sim_vars['vel']
            accel = "%.4f" % self.sim_vars['accel']
            dis = "%.4f" % self.sim_vars['dis']

            # Turning point
            if len(self.vel) > 0:
                # determine whether it is a turing point
                isTurnPoint = True if float(vel) * self.vel[-1] < 0 else False
                self.turnPoint.append(isTurnPoint)

            # append the result to the result lists
            self.angle.append(float(angle))
            self.vel.append(float(vel))
            self.accel.append(float(accel))
            self.dis.append(float(dis))


    def run(self):
    
    # This function is main calculation for the whole process.
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme
	# 
    # outputs:  res         (dictionary)        the calulation_result dictionary that hold all
    #                                           the result lists.

        #     'tg': 0.0,
        # 'drag_force': 0.0,
        # 'accel': 0.0,
        # 'vel': 0.0,
        # 'dis': 0.0,
        # 'ang': 0.0,
        # 'time': 0.0,

        tg = 0.0
        drag_force = 0.0
        accel = 0.0
        vel = 0.0
        dis = 0.0
        ang = self.sim_params['initial_angle'] * self.sim_const['deg_rad_ratio']
        time = 0.0
        turn_point = True

        self.ang_array.append(ang)
        self.vel_array.append(vel)
        self.accel_array.append(accel)
        self.dis_array.append(dis)
        self.turn_point_array.append(turn_point)

        while(time <= self.sim_params['total_time']):
            tg 
            pass
        # get the result after 'for' loop is finished
        res = {
            'time_range': list(time_range),
            'angle': self.ang_array,
            'vel': self.vel_array,
            'accel': self.accel_array,
            'dis': self.dis_array,
            'turn_point': self.turn_point_array
            .
        }

        # return the result list
        return res


    def plot_data(self, cal_res):


    # This function is for showing all the results on a plot
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be automatically given by the programme
	# 			cal_res	    (dictionary)        a dictionary that hold the all the result lists


        ## Plot four graphs using subplot

        # Plot angle graph at position 1
        plt.subplot(2, 2, 1)
        plt.title("Angle")
        plt.plot(cal_res['time_range'], cal_res['angle'])
        plt.xlabel('time(s)')
        plt.ylabel('angle(deg)')

        # Plot velocity graph at position 2
        plt.subplot(2, 2, 2)
        plt.title("Velocity")
        plt.plot(cal_res['time_range'], cal_res['vel'])
        plt.xlabel('time(s)')
        plt.ylabel('vel(m/s)')

        # Plot acceleration graph at position 3
        plt.subplot(2, 2, 3)
        plt.title("Acceleration")
        plt.plot(cal_res['time_range'], cal_res['accel'])
        plt.xlabel('time(s)')
        plt.ylabel('acc(m/s^2)')

        # Plot displacement graph at position 4
        plt.subplot(2, 2, 4)
        plt.title("Displacement")
        plt.plot(cal_res['time_range'], cal_res['dis'])
        plt.xlabel('time(s)')
        plt.ylabel('dis(m)')

        # Set the margin
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.ion()
        plt.show()


    def run_GUI(self, cal_res):


    # This function is for creating an animation GUI winodow for visualising the motion.
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be given by the programme automatically
	# 			cal_res	    (dictionary)        a dictionary that hold the all the result lists

        # Initialise the variables
        width = 800
        height = 600
        radius = 150

        # Create a window
        win = GraphWin("PendulumSim", width, height)

        # Draw the main circle which its arc to be the path of the object
        circle = Circle(Point(width/2, height/2), radius)
        circle.draw(win)

        # Get the center point coordinate
        center_x = circle.getCenter().getX()
        center_y = circle.getCenter().getY()

        # Draw a small circle to be the fixed point of the line
        centerPoint = Circle(circle.getCenter(), 5)
        centerPoint.draw(win)

        # Calculate the initial coordinate of the object
        dx = center_x + \
            (radius * math.sin(cal_res['angle'][0]
                               * self.sim_const['deg_rad_ratio']))
        dy = center_y + \
            (radius * math.cos(cal_res['angle'][0]
                               * self.sim_const['deg_rad_ratio']))

        # Draw a line to connect the object and the fixed point
        line = Line(circle.getCenter(), Point(dx, dy))
        line.draw(win)

        # Draw the object 
        new_mass = Circle(Point(dx, dy), 10)
        new_mass.draw(win)

        # Initialise the on-screens= messages
        turn_point_msg = Text(Point(0, 0), "")
        turn_point_msg.draw(win)

        monitor_msg = Text(Point(width/2, 80), "ang=0 ,vel=0 ,accel=0 ,dis=0")
        monitor_msg.draw(win)

        try:
            # Continue to start with a keyboard press
            win.getKey()

            for i in range(len(cal_res['angle'])):

                # Undraw all the elements
                new_mass.undraw()
                line.undraw()
                monitor_msg.undraw()

                # Calculate the new coordinate
                dx = center_x + \
                    (radius * math.sin(cal_res['angle'][i]
                                       * self.sim_const['deg_rad_ratio']))
                dy = center_y + \
                    (radius * math.cos(cal_res['angle'][i]
                                       * self.sim_const['deg_rad_ratio']))

                # Draw new elements
                line = Line(circle.getCenter(), Point(dx, dy))
                new_mass = Circle(Point(dx, dy), 10)
                monitor_msg = Text(Point(width/2, 80), "ang=%s,vel=%s,accel=%s,dis=%s" % (
                    cal_res['angle'][i], cal_res['vel'][i], cal_res['accel'][i], cal_res['dis'][i]))

                line.draw(win)
                new_mass.draw(win)
                monitor_msg.draw(win)

                # Print turing points
                if cal_res['turn_point'][i]:
                    turn_point_msg.undraw()
                    turn_point_msg = Text(Point(new_mass.getCenter().getX(
                    ), new_mass.getCenter().getY()+30), cal_res['angle'][i])
                    turn_point_msg.draw(win)

                # Sleep for 'time_step' seconds to be real-time
                time.sleep(self.sim_params['time_step'])
        except:
            print(traceback.format_exc())


    def print_data(self, cal_res):


    # This function is for previewing all the result in the terminal. It is only for preview
    # as terminal usually has the output length limit, which may erase the pervious printing.
    #
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be given by the programme automatically
	# 			cal_res	    (dictionary)        a dictionary that hold the all the result lists


        if len(cal_res['time_range']) >= 200:
            print('\n')
            
            # if these are too many datas, ask for user whether wish to print
            print(
                "There are more than 200 lines of data, do you wish to print? Yes[Y] No[N]")
            yes_no = input("Options: ")

            if yes_no == 'Y' or yes_no == 'y':
                table = PrettyTable()
                table.add_column("Time", cal_res['time_range'])
                table.add_column("Ang", cal_res['angle'])
                table.add_column("Vel", cal_res['vel'])
                table.add_column("Accel", cal_res['accel'])
                table.add_column("Dis", cal_res['dis'])
                table.add_column("Turning", cal_res['turn_point'])
                print(table)
                input("\nPress any key to continue")


    def save_csv(self, cal_res):
        
    # This function is for saving all the result to a csv file.
    #
	# inputs:	self 	    (object)		    instance of the PendulumSim class,
    #                                           will be given by the programme automatically
	# 			cal_res	    (dictionary)        a dictionary that hold the all the result lists

        # open a file with 'write' mode
        f = open("res.csv", "w")

        # write the title (first line)
        f.write("time,angle,vel,accel,dis\n")
        
        # write all results
        for i in range(len(cal_res['time_range'])):
            f.write("%.2f,%.4f,%.4f,%.4f,%.4f\n" % (
                cal_res['time_range'][i], cal_res['angle'][i], cal_res['vel'][i], cal_res['accel'][i], cal_res['dis'][i]))
        
        # close the file after finished
        f.close()

        print("Data successfully saved to res.csv")


def main():
    sim = PendulumSim()
    try:
        #Initial variables
        input_options = ''
        #Initial result dicitonary, with a new key 'isCalculate'
        #to show the status of the variable (whether being overwritten)
        cal_res = {
            "isCalculate": False
        }

        #Main loop
        while input_options != 'q':
            #Clean the terminal windows for each loop
            os.system('CLS')

            #Print the option menu
            print("1. Edit params")
            print("2. Calculate")
            print("3. Plot data")
            print("4. Save to CSV")
            print("5. Open simulator")
            print("Quit -- q")
            print("\n")
            input_options = input("Options: ")

            #Determine the options
            if input_options == "1":
        
                os.system('CLS')

                sim.show_params()
                sim.set_param('mass')
                sim.set_param('length')
                sim.set_param('drag_coef')
                sim.set_param('time_step')
                sim.set_param('init_angle')
                sim.set_param('total_time')

                # Each time when params are editted, reset the cal_res status
                cal_res['isCalculate'] = False
                
                input("\nPress any key to continue")
            elif input_options == "2":

                # Call the function to get the results
                cal_res = sim.run()

                # Editing the 'isCalculate' key to show that results are gotten.
                cal_res['isCalculate'] = True
                
                # Call the function to reset all the variables for next calculation
                sim.reset_vars()

                sim.print_data(cal_res)
            elif input_options == "3":

                if cal_res['isCalculate'] == True:

                    # Call the function to plot graphs
                    sim.plot_data(cal_res)

                else:
                    print("Please calculate first")
                    input("\nPress any key to continue")

            elif input_options == "4":

                if cal_res['isCalculate'] == True:

                    # Call the function to save the result to a csv file
                    sim.save_csv(cal_res)
                else:
                    print("Please calculate first")

                input("\nPress any key to continue")
                    
            elif input_options == "5":

                if cal_res['isCalculate'] == True:

                    # Call the function to open the GUI simulator
                    sim.run_GUI(cal_res)
                else:
                    print("Please calculate first")
                    input("\nPress any key to continue")

            elif input_options == "q":
                print("Exit the programme...")
                
            else:
                print("Invaild input")
    except Exception:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()

import math
import matplotlib.pyplot as plt
import os
import traceback
from prettytable import PrettyTable

# Initialise global variables

# System constants
g_grav = -9.81

# Default simulation parameters
g_mass = float(60.0)                # mass (kg)
g_init_height = float(10000)        # initial height (m)
g_init_vel = float(5.0)            # initial velocity (m/s)
g_init_ang = float(0.0)            # initial angel to the horizontal CCW (deg)
g_drag_coef = float(0.1)              # coefficient of drag force (5cm diameter sphere)
g_time_step = float(0.01)           # time step size (s)
g_total_time = float(60.0)          # total time for the simulation

def execute(mass, init_height, init_vel, init_ang, drag_coef, time_step, total_time):
    
    # Initialise result-lists
    vel_y_arr = []
    vel_x_arr = []

    dis_y_arr = []
    dis_x_arr = []

    time_arr = []

    # Append starting point
    init_vel_x = 0 if init_ang % 90 == 0 and init_ang != 0 else init_vel * math.cos(math.radians(init_ang))
    init_vel_y = init_vel * math.sin(math.radians(init_ang))

    vel_y_arr.append(float("%.4f" % init_vel_y))
    vel_x_arr.append(float("%.4f" % init_vel_x))
    dis_y_arr.append(0.0 + init_height)
    dis_x_arr.append(0.0)
    time_arr.append(0.0)

    # initial loop variables
    index = 0
    time = 0.0

    while(time < total_time):
        drag_accel_y = (vel_y_arr[index] * math.fabs(vel_y_arr[index]) * drag_coef) / mass
        drag_accel_x = (vel_x_arr[index] * math.fabs(vel_x_arr[index]) * drag_coef) / mass

        accel_y = g_grav - drag_accel_y
        accel_x = - drag_accel_x

        # variables for step i+1
        vel_y = vel_y_arr[index] + (accel_y * time_step)
        vel_x = vel_x_arr[index] + (accel_x * time_step)

        dis_y = dis_y_arr[index] + (vel_y * time_step)
        dis_x = dis_x_arr[index] + (vel_x * time_step)

        time = time_arr[index] + time_step

        # append i+1 to lists
        vel_y_arr.append(float("%.4f" % vel_y))
        vel_x_arr.append(float("%.4f" % vel_x))
        dis_y_arr.append(float("%.4f" % dis_y))
        dis_x_arr.append(float("%.4f" % dis_x))
        time_arr.append(float("%.4f" % time))

        index += 1

    res = {
        'vel_y_arr': vel_y_arr,
        'vel_x_arr': vel_x_arr,
        'dis_y_arr': dis_y_arr,
        'dis_x_arr': dis_x_arr,
        'time_arr': time_arr
    }

    return res

def plot_data(cal_res):
    # Plot angle graph at position 1
    plt.suptitle("Projectile Motion Simulator", fontsize=16)
    plt.subplot(1, 3, 1)
    plt.title("Velocity Y")
    plt.plot(cal_res['time_arr'], cal_res['vel_y_arr'])
    plt.xlabel('time (s)')
    plt.ylabel('vel_y (m/s)')

    # Plot angle graph at position 2
    plt.subplot(1, 3, 2)
    plt.title("Velocity X")
    plt.plot(cal_res['time_arr'], cal_res['vel_x_arr'])
    plt.xlabel('time (m/s)')
    plt.ylabel('vel_x (m/s)')

    # Plot velocity graph at position 3
    plt.subplot(1, 3, 3)
    plt.title("Displacement")
    plt.plot(cal_res['dis_x_arr'], cal_res['dis_y_arr'])
    plt.xlabel('dis_x (m)')
    plt.ylabel('dis_y (m)')

    # Set the margin
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()

def main():
    cal_res = execute(g_mass, g_init_height, g_init_vel, g_init_ang, g_drag_coef, g_time_step, g_total_time)
    plot_data(cal_res)

if __name__ == "__main__":
    main()


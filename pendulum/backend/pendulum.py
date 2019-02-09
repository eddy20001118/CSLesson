# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt


class PendulumSim():
    sim_const = {
        'g': 9.81,
        'rad_deg_ratio': 57.29577951,
        'deg_rad_ratio': 0.01745329
    }

    sim_params = {
        'mass': 1.0,
        'length': 1.0,
        'drag_coef': 0.1,
        'time_step': 0.02,
        'init_angle': math.pi/6,
        'total_time': 10
    }

    sim_vars = {
        'tg': 0.0,
        'drag_force': 0.0,
        'accel': 0.0,
        'vel': 0.0,
        'dis': 0.0,
        'ang': 0.0,
        'time': 0.0,
    }

    angle = []
    vel = []
    accel = []
    dis = []

    def sim_cal(self):
        """
        Calculate in one time step
        """

        if self.sim_vars['time'] == 0:
            self.sim_vars['ang'] = self.sim_params['init_angle']

        self.sim_vars['tg'] = -1*self.sim_const['g'] * \
            self.sim_params['mass']*math.sin(self.sim_vars['ang'])
        self.sim_vars['drag_force'] = self.sim_vars['vel'] * \
            math.fabs(self.sim_vars['vel'])*self.sim_params['drag_coef']
        self.sim_vars['accel'] = (
            self.sim_vars['tg']-self.sim_vars['drag_force'])/self.sim_params['mass']

        self.sim_vars['vel'] += self.sim_params['time_step'] * \
            self.sim_vars['accel']
        self.sim_vars['dis'] += self.sim_params['time_step'] * \
            self.sim_vars['vel']
        self.sim_vars['ang'] = (
            self.sim_vars['dis'] / self.sim_params['length']) + self.sim_params['init_angle']
        self.sim_vars['time'] += self.sim_params['time_step']
        self.angle.append({
            'x': ("%.2f" % self.sim_vars['time']),
            'y': self.sim_vars['ang'] * self.sim_const['rad_deg_ratio']
        })
        self.vel.append({
            'x': ("%.2f" % self.sim_vars['time']),
            'y': self.sim_vars['vel']
        })
        self.accel.append({
            'x': ("%.2f" % self.sim_vars['time']),
            'y': self.sim_vars['accel']
        })
        self.dis.append({
            'x': ("%.2f" % self.sim_vars['time']),
            'y': self.sim_vars['dis']
        })

    def run(self):
        time_range = np.arange(
            0, self.sim_params['total_time'], self.sim_params['time_step'])
        for i in time_range:
            self.sim_cal()
        res = {
            'angle': self.angle,
            'vel': self.vel,
            'accel': self.accel,
            'dis': self.dis
        }
        return res



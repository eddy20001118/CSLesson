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

    sim_vars_rt = {
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

    def reset_vars(self, type):
        if type == 'rt':
            self.sim_vars_rt = {
                'tg': 0.0,
                'drag_force': 0.0,
                'accel': 0.0,
                'vel': 0.0,
                'dis': 0.0,
                'ang': 0.0,
                'time': 0.0,
            }
            return True
        elif type == 'pc':
            self.sim_vars = {
                'tg': 0.0,
                'drag_force': 0.0,
                'accel': 0.0,
                'vel': 0.0,
                'dis': 0.0,
                'ang': 0.0,
                'time': 0.0,
            }
            self.angle = []
            self.vel = []
            self.accel = []
            self.dis = []
            return True
        else:
            return False

    def set_params(self, params):
        self.sim_params = params

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
            'time': ("%.2f" % self.sim_vars['time']),
            'Angle': self.sim_vars['ang'] * self.sim_const['rad_deg_ratio']
        })
        self.vel.append({
            'time': ("%.2f" % self.sim_vars['time']),
            'Velocity': self.sim_vars['vel']
        })
        self.accel.append({
            'time': ("%.2f" % self.sim_vars['time']),
            'Acceleration': self.sim_vars['accel']
        })
        self.dis.append({
            'time': ("%.2f" % self.sim_vars['time']),
            'Distance': self.sim_vars['dis']
        })

    def run(self):
        time_range = np.arange(
            0, self.sim_params['total_time'], self.sim_params['time_step'])

        for i in time_range:
            self.sim_cal()

        res = {
            'time_range': list(time_range),
            'angle': self.angle,
            'vel': self.vel,
            'accel': self.accel,
            'dis': self.dis
        }
        return res

    def run_rt(self, index):
        time = index * self.sim_params['time_step']
        self.sim_vars_rt['time'] = time
        if self.sim_vars_rt['time'] == 0:
            self.sim_vars_rt['ang'] = self.sim_params['init_angle']

        self.sim_vars_rt['tg'] = -1*self.sim_const['g'] * \
            self.sim_params['mass']*math.sin(self.sim_vars_rt['ang'])
        self.sim_vars_rt['drag_force'] = self.sim_vars_rt['vel'] * \
            math.fabs(self.sim_vars_rt['vel'])*self.sim_params['drag_coef']
        self.sim_vars_rt['accel'] = (
            self.sim_vars_rt['tg']-self.sim_vars_rt['drag_force'])/self.sim_params['mass']

        self.sim_vars_rt['vel'] += self.sim_params['time_step'] * \
            self.sim_vars_rt['accel']
        self.sim_vars_rt['dis'] += self.sim_params['time_step'] * \
            self.sim_vars_rt['vel']
        self.sim_vars_rt['ang'] = (
            self.sim_vars_rt['dis'] / self.sim_params['length']) + self.sim_params['init_angle']

        return self.sim_vars_rt


def main():
    sim = PendulumSim()
    my_params = {
        'mass': 2.0,
        'length': 2.0,
        'drag_coef': 0.2,
        'time_step': 0.02,
        'init_angle': math.pi/3,
        'total_time': 5
    }
    sim.set_params(my_params)
    f = file.open('data.csv')
    sim.reset_vars('rt')
    for i in range(0, 10):
        print(sim.run_rt(i))


if __name__ == "__main__":
    main()

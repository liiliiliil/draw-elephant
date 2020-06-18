import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class DrawElephant:

    def __init__(self, coeff=[[50, -30], [18, 8], [12, -10], [-14, -60]]):

        self.coeff_x, self.coeff_y = zip(*coeff)

        self.wiggle = False
        if len(self.coeff_x) == 5:
            self.wiggle = True

        print(self.coeff_x)
        print(self.coeff_y)
        
        self.t = np.arange(0, 6.5, 0.02)


        self.x_sin_1 = np.sin(self.t)
        self.x_sin_2 = np.sin(2*self.t)
        self.x_cos_3 = np.cos(3*self.t)
        self.x_cos_5 = np.cos(5*self.t)
        
        self.y_sin_1 = np.sin(self.t)
        self.y_sin_2 = np.sin(2*self.t)
        self.y_sin_3 = np.sin(3*self.t)
        self.y_cos_1 = np.cos(self.t)

        self.x = None
        self.y = None
        self.eye = None
        self.where_to_wiggle = None
        if self.wiggle:
            self.eye = [self.coeff_y[4], self.coeff_y[4]]
            self.where_to_wiggle = self.coeff_x[4]

        self.calPoints()
    
    def calPoints(self):
        self.x = self.coeff_x[0]*self.x_sin_1 + self.coeff_x[1]*self.x_sin_2\
                + self.coeff_x[2]*self.x_cos_3 + self.coeff_x[3]*self.x_cos_5

        self.y = self.coeff_y[0]*self.x_sin_1 + self.coeff_y[1]*self.x_sin_2\
                + self.coeff_y[2]*self.y_sin_3 + self.coeff_y[3]*self.y_cos_1
        
        self.x, self.y = self.y, -self.x

        # print(self.y)


    def draw(self):

        plt.figure()

        plt.plot(self.x, self.y)

        if self.wiggle:
            plt.scatter(self.eye[0], self.eye[0])

        plt.show()
    
    def draw_wiggling(self, num_frames=400):
        if not self.wiggle:
            print('Coeffs are not enough.')
            return
        
        _max = 40

        change_list = list(range(-_max, _max+1, 5))
        change_list = list(map(lambda x: x * 0.01, change_list))
        change_list = change_list + change_list[::-1]
        print(change_list)
        num_frames = len(change_list)

        fig = plt.figure()

        xdata, ydata = self.x.copy(), self.y.copy()
        change_mask = self.x > self.where_to_wiggle
        change_rate = np.maximum(self.x - self.where_to_wiggle, 0)
        change_rate = change_rate[change_mask] / np.max(change_rate)
        # print(change_rate)
        
        plt.scatter(self.eye[0], self.eye[0])
        ln, = plt.plot(self.x, self.y)

        def init():
            # ax.set_xlim(AXIS_X_MAX, AXIS_X_MIN)
            # ax.set_ylim(AXIS_Y_MAX, AXIS_Y_MIN)
            
            return ln,

        def update(frame):
            # print(frame)
            change = change_list[frame]
            # print(change_rate * change)

            ydata[change_mask] = self.y[change_mask] * (change_rate * change + 1)
            # print('y\n', self.y[change_mask])
            # print('changed y\n', ydata[change_mask])

            ln.set_data(xdata, ydata)
            return ln,

        
        # print(frame_list)
        anim = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True)
        anim.save('elephant.gif', writer='pillow')
        plt.show()



def main():
    param_1 = [50, -30]  # real and imaginary part
    param_2 = [18, 8]
    param_3 = [12, -10]
    param_4 = [-14, -60]
    param_5 = [40, 20]

    params = [param_1, param_2, param_3, param_4, param_5]

    drawing = DrawElephant(coeff=params)
    # drawing.draw()
    drawing.draw_wiggling()



if __name__ == '__main__':
    main()
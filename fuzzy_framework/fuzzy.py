import numpy as np
import matplotlib.pyplot as plt

class Interval():

    def __init__(self, points: list):

        if_increasing = np.all(np.diff(points) >= 0)
        if_shape_ok = len(points) == 3 or len(points) == 4
        
        if if_increasing and if_shape_ok:
            self.points = np.array(points)
        else:
            raise Exception('Provide list of len 3 or 4, points not decreasing')
    
    def get_value(self, x: float):
        is_in_range = self.points[0] <= x and x <= self.points[-1]

        if is_in_range:
            if len(self.points) == 3:
                if self.points[0] <= x and x <= self.points[1]:
                    a, b = self.slope(self.points[0],self.points[1])

                    return a * x + b
                else:
                    a, b = self.slope(self.points[2],self.points[1])

                    return a * x + b

            elif len(self.points) == 4:

                if self.points[1] <= x and x <= self.points[2]:
                    return 1

                elif self.points[0] <= x and x <= self.points[1]:
                    a, b = self.slope(self.points[0],self.points[1])

                    return a * x + b

                elif self.points[2] <= x and x <= self.points[3]:
                    a, b = self.slope(self.points[3],self.points[2])

                    return a * x + b
        else:      
            raise Exception('x not in the interval')
    
    def slope(self, x1: float, x2: float):
    # swap x1 and x2 for negative slope
        a = 1/(x2 - x1)
        b = 1 - a * x2
        return a, b

    def get_range(self):
        return self.points[0], self.points[-1]
    
class Variable():

    def __init__(self):
        self.intervals = {}

    def add_interval(self, name: str, interval: list):
        self.intervals[name] = Interval(interval)
    
    def get_interval(self, arg: float):
        for name, interval in self.intervals.items():
            x1, x2 = interval.get_range()

            if x1 <= arg and arg <= x2:
                value = interval.get_value(arg)
                if value:
                    print(name, value)
    
    def plot(self):
        for name, interval in self.intervals.items():
            points = interval.points
            if len(points) == 3:
                row = np.array([0,1,0])
            else:
                row = np.array([0,1,1,0])
            points = np.vstack((points,row)).T
            plt.plot(points[:,0], points[:,1], label=name)

        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    
    food = Variable()
    food.add_interval('poor', [0,0,1,2])
    food.add_interval('good', [1,2,5])
    food.add_interval('great', [2,5,7,7])
    food.get_interval(6.9)
    food.plot()
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

    def __init__(self, name: str):
        self.intervals = {}
        self.name = name

    def add_interval(self, name: str, interval: list):
        self.intervals[name] = Interval(interval)
    
    def get_interval(self, arg: float):
        intervals = {}
        for name, interval in self.intervals.items():
            x1, x2 = interval.get_range()

            if x1 <= arg and arg <= x2:
                value = interval.get_value(arg)
                if value:
                    intervals[name] = value
        return intervals
    
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
        plt.title(self.name)
        plt.tight_layout()
        plt.show()

class Rule():

    def __init__(self, condition1: tuple, operation: str, condition2: tuple, output: float):
        self.condition1 = condition1
        self.condition2 = condition2
        self.operation = operation
        self.output = output

class Model():

    def __init__(self, rules: list = []):
        self.rules = rules

    def predict(self, value1, value2):
        
        var_to_avg = []
        for rule in self.rules:
            intervals_cond1 = rule.condition1[0].get_interval(value1)
            intervals_cond2 = rule.condition2[0].get_interval(value2)
            inerval1_name = rule.condition1[1]
            inerval2_name = rule.condition2[1]

            if inerval1_name not in intervals_cond1 or inerval2_name not in intervals_cond2:
                continue
            
            arg1 = intervals_cond1[inerval1_name]
            arg2 = intervals_cond2[inerval2_name]

            if rule.operation == 'AND':
                var = np.array([arg1,arg2]).min()
            elif rule.operation == 'OR':
                var = np.array([arg1,arg2]).max()

            var_to_avg.append([var, rule.output])

        if len(var_to_avg) == 0:
            raise Exception('Set rules are too sparse')

        var_to_avg = np.array(var_to_avg)
        multipied = np.prod(var_to_avg, axis=1)
        sum = np.sum(var_to_avg[:,0])
        score = np.sum(multipied)/sum

        return score

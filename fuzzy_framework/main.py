from myfuzzy import Variable, Rule, Model

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    food = Variable('food')
    food.add_interval('poor', [0,0,2,5])
    food.add_interval('avg', [2,5,8])
    food.add_interval('good', [5,8,10,10])

    service = Variable('service')
    service.add_interval('poor', [0,0,1,6])
    service.add_interval('avg', [1,6,9])
    service.add_interval('good', [6,9,10,10])

    rule1 = Rule((food, 'good'), 'OR', (service,'good'), 15)
    rule2 = Rule((food, 'good'), 'AND', (service,'avg'), 10)
    rule3 = Rule((food, 'good'), 'AND', (service,'poor'), 10)

    rule4 = Rule((food, 'avg'), 'AND', (service,'good'), 10)
    rule5 = Rule((food, 'avg'), 'OR', (service,'avg'), 10)
    rule6 = Rule((food, 'avg'), 'AND', (service,'poor'), 5)

    rule7 = Rule((food, 'poor'), 'AND', (service,'good'), 10)
    rule8 = Rule((food, 'poor'), 'AND', (service,'avg'), 10)
    rule9 = Rule((food, 'poor'), 'OR', (service,'poor'), 5)

    rules = [
        rule1,
        rule2,
        rule3,
        rule4,
        rule5,
        rule6,
        rule7,
        rule8,
        rule9,
        ]

    model = Model(rules)

    food.plot()
    service.plot()

    for service_arg in range(0,11,3):
        tips = []
        for food_arg in range(11):
            tip = model.predict(food_arg, service_arg)
            tips.append([food_arg, tip])
        tips = np.array(tips)
        plt.plot(tips[:,0],tips[:,1], label=f'service: {service_arg}')
    plt.legend()
    plt.xlabel('food')
    plt.ylabel('tip')
    plt.show()

    for food_arg in range(0,11,3):
        tips = []
        for service_arg in range(11):
            tip = model.predict(food_arg, service_arg)
            tips.append([service_arg, tip])
        tips = np.array(tips)
        plt.plot(tips[:,0],tips[:,1], label=f'food: {food_arg}')
    plt.legend()
    plt.xlabel('service')
    plt.ylabel('tip')
    plt.show()

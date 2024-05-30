import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def initialize_population(size):
    population = np.random.choice([0, 1, 2, 3, 4], size=(size, size), p=[0.4, 0.3, 0.15, 0.1, 0.05])
    Alpha_age = np.zeros_like(population)
    Beta_age = np.zeros_like(population)
    Gamma_age = np.zeros_like(population)
    return population, Alpha_age, Beta_age, Gamma_age

population, Alpha_age, Beta_age, Gamma_age = initialize_population(100)

def count_neighbors(population, x, y, value):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0) and 0 <= x + i < population.shape[0] and 0 <= y + j < population.shape[1] and population[x + i, y + j] == value:
                count += 1
    return count

def apply_rules(population, Alpha_age, Beta_age, Gamma_age):
    new_population = population.copy()
    new_Alpha_age = Alpha_age.copy()
    new_Beta_age = Beta_age.copy()
    new_Gamma_age = Gamma_age.copy()

    for i in range(population.shape[0]):
        for j in range(population.shape[1]):
            neighbors_2 = count_neighbors(population, i, j, 2)
            neighbors_3 = count_neighbors(population, i, j, 3)
            neighbors_4 = count_neighbors(population, i, j, 4)

            if population[i, j] == 0:  # Empty cell
                if np.random.rand() <= 0.25:  # Generate food in random empty cells with probability 25%
                    new_population[i, j] = 1

            elif population[i, j] == 1: # Food
                if neighbors_2 >= 1 and neighbors_3 >= 1 and neighbors_4 >= 1: #if food have neighbors of all types, alpha will eat food
                    new_population[i, j] = 4
                elif neighbors_2 == 0 and neighbors_3 == 0 and neighbors_4 >= 1: #if food have neighbors of only alpha, alpha will eat food
                    new_population[i, j] = 4
                elif neighbors_2 == 0 and neighbors_3 >= 1 and neighbors_4 >= 1: #if food have neighbors of alpha and beta, alpha will eat food
                    new_population[i, j] = 4
                elif neighbors_2 >= 1 and neighbors_3 == 0 and neighbors_4 >= 1: #if food have neighbors of alpha and gamma, alpha will eat food
                    new_population[i, j] = 4
                elif neighbors_2 >= 1 and neighbors_3 >= 1 and neighbors_4 == 0: #if food have neighbors of beta and gamma, beta will eat food
                    new_population[i, j] = 3
                elif neighbors_2 == 0 and neighbors_3 >= 1 and neighbors_4 == 0: #if food have neighbors of only beta, beta will eat food
                    new_population[i, j] = 3
                elif neighbors_2 >= 1 and neighbors_3 == 0 and neighbors_4 == 0: #if food have neighbors of only gamma, gamma will eat food
                    new_population[i, j] = 2
                else:
                    new_population[i, j] = 0

            elif population[i, j] == 4:  # Alpha
                new_Alpha_age[i, j] += 1
                
                if new_Alpha_age[i, j] >= 4 or neighbors_4 == 8:  #alpha dies after reaching age 4 or from over population
                    new_population[i, j] = 0
                    new_Alpha_age[i, j] = 0

            elif population[i, j] == 3:  # Beta
                new_Beta_age[i, j] += 1
                
                if new_Beta_age[i, j] >= 24 or neighbors_3 == 8:  #beta dies after reaching age 24 or from over population
                    new_population[i, j] = 0
                    new_Beta_age[i, j] = 0

            elif population[i, j] == 2:  # Gamma
                new_Gamma_age[i, j] += 1
                
                if new_Gamma_age[i, j] >= 48 or neighbors_2 == 8:  #gamma dies after reaching age 48 or from over population
                    new_population[i, j] = 0
                    new_Gamma_age[i, j] = 0

    return new_population, new_Alpha_age, new_Beta_age, new_Gamma_age

generations = 101
colors = ['white', 'gold', 'green', 'blue', 'red']              #(empty,food,gamma,beta,alpha)
cmap = plt.cm.colors.ListedColormap(colors)

plt.imshow(population, cmap=cmap, interpolation='nearest')
plt.grid(True, color='black', linewidth=0.5)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Generation 0')
plt.colorbar(ticks=[0, 1, 2, 3, 4], label='Cell State (0: Empty, 1: Food, 2: Gamma, 3: Beta, 4: Alpha)')
plt.gca().set_aspect('equal', adjustable='box')

def update_plot(frame):
    global population, Alpha_age, Beta_age, Gamma_age
    population, Alpha_age, Beta_age, Gamma_age = apply_rules(population, Alpha_age, Beta_age, Gamma_age)
    plt.imshow(population, cmap=cmap, interpolation='nearest')
    plt.title(f'Generation {frame}')

animation = FuncAnimation(plt.gcf(), update_plot, frames=generations, repeat=False, interval=100)
plt.show()

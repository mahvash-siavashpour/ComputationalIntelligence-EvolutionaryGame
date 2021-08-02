from player import Player
import numpy as np
from config import CONFIG
import copy
import player
import math
import csv


class Evolution():

    def __init__(self, mode):
        self.mode = mode


    # calculate fitness of players
    def calculate_fitness(self, players, delta_xs):
        for i, p in enumerate(players):
            p.fitness = delta_xs[i]

    def mutate(self, child, pw, pb, d):

        # TODO
        # child: an object of class `Player`
        mutation_prob = np.random.uniform(0, 1)
        if mutation_prob <= pw:
            child.nn.w1 += np.random.normal(0, d, child.nn.w1.shape)
        mutation_prob = np.random.uniform(0, 1)
        if mutation_prob <= pb:
            child.nn.b1 += np.random.normal(0, d, child.nn.b1.shape)
        mutation_prob = np.random.uniform(0, 1)
        if mutation_prob <= pw:
            child.nn.w2 += np.random.normal(0, d, child.nn.w2.shape)
        mutation_prob = np.random.uniform(0, 1)
        if mutation_prob <= pb:
            child.nn.b2 += np.random.normal(0, d, child.nn.b2.shape)
        return child

    def generate_new_population(self, num_players, prev_players=None):

        # in first generation, we create random players
        if prev_players is None:
            return [Player(self.mode) for _ in range(num_players)]

        else:

            # TODO
            # num_players example: 150
            # prev_players: an array of `Player` objects

            # TODO (additional): a selection method other than `fitness proportionate`
            if self.mode == 'thrust':
                new_players = copy.deepcopy(self.q_tournament(prev_players, num_players, 10))
            else:
                new_players = copy.deepcopy(self.q_tournament(prev_players, num_players, 10))

            # TODO (additional): implementing crossover
            new_players = self.cross_over(new_players, num_players)
            if self.mode == 'thrust':
                children = [self.mutate(x, .35, .7, 0.3) for x in copy.deepcopy(new_players)]
            else:
                children = [self.mutate(x, 0.35, 0.7, 0.3) for x in copy.deepcopy(new_players)]
            return children

    def next_population_selection(self, players, num_players):

        # TODO
        # num_players example: 100
        # players: an array of `Player` objects
        # sorted_players = sorted(players, key=lambda x: x.fitness, reverse=True)

        # TODO (additional): a selection method other than `top-k`
        next_population = self.roulette_wheel(players, num_players)
        # TODO (additional): plotting
        # self.plot_data_saving(players)

        return next_population

    def roulette_wheel(self, players, num_players):
        nex_gen = []
        population_fitness = sum([player.fitness for player in players])
        probability = [player.fitness / population_fitness for player in players]
        nex_gen = np.random.choice(players, size=num_players, p=probability, replace=False)
        return list(nex_gen)

    def q_tournament(self, players, num_players, q):
        result = []
        for i in range(num_players):
            batch = []
            for j in range(q):
                batch.append(np.random.choice(players))
            result.append(copy.deepcopy(sorted(batch, key=lambda x: x.fitness, reverse=True)[0]))
        return result

    def cross_over(self, players, num_players):
        children = []
        index = 0
        for i in range(math.floor(num_players / 2.0)):
            cross_over_prob = np.random.uniform(0, 1)
            if self.mode == 'thrust':
                p = 0.8
            else:
                p = 0.9
            if cross_over_prob >= p:
                children.append(players[index])
                children.append(players[index+1])
                index += 2
                continue
            child1 = Player(self.mode)
            child2 = Player(self.mode)
            # child1 = Player('helicopter')
            # child2 = Player('helicopter')
            parent1 = players[index]
            parent2 = players[index + 1]
            dimensions = parent1.nn.sizes
            # print(dimensions)
            d0 = math.floor(dimensions[0] / 2)
            d1 = math.floor(dimensions[1] / 2)
            d2 = math.floor(dimensions[2] / 2)
            child1.nn.w1 = np.concatenate((parent1.nn.w1[:d1], parent2.nn.w1[d1:]), axis=0)
            child1.nn.b1 = np.concatenate((parent1.nn.b1[:d1], parent2.nn.b1[d1:]), axis=0)
            child1.nn.w2 = np.concatenate((parent1.nn.w2[:d2], parent2.nn.w2[d2:]), axis=0)
            child1.nn.b2 = np.concatenate((parent1.nn.b2[:d2], parent2.nn.b2[d2:]), axis=0)
            children.append(child1)
            child2.nn.w1 = np.concatenate((parent2.nn.w1[:d1], parent1.nn.w1[d1:]),
                                          axis=0)
            child2.nn.b1 = np.concatenate((parent2.nn.b1[:d1], parent1.nn.b1[d1:]),
                                          axis=0)
            child2.nn.w2 = np.concatenate((parent2.nn.w2[:d2], parent1.nn.w2[d2:]),
                                          axis=0)
            child2.nn.b2 = np.concatenate((parent2.nn.b2[:d2], parent1.nn.b2[d2:]),
                                          axis=0)
            children.append(child2)
            index += 2
        if len(children) < num_players:
            children.append(players[0])
        return children


    def plot_data_saving(self, players):
        with open(f'data_files/{self.mode}-max.csv', 'a') as file:
            file.write(str(sorted(players, key=lambda x: x.fitness, reverse=True)[0].fitness))
            file.write("\n")
        with open(f'data_files/{self.mode}-min.csv', 'a') as file:
            file.write(str(sorted(players, key=lambda x: x.fitness)[0].fitness))
            file.write("\n")
        ave = 0
        for p in players:
            ave += p.fitness
        ave /= len(players)
        with open(f'data_files/{self.mode}-average.csv', 'a') as file:
            file.write(str(ave))
            file.write("\n")

import random


def scramble(population):
  for individual in population:
    individual.chromosomes = [random.choice(individual.possibilities) for _ in range(individual.length)]
  return population


def mutate(population):
  for individual in population:
    individual.chromosomes[random.randrange(individual.length)] = random.choice(individual.possibilities)
  return population


def swap(population):
  for individual in population:
    i, j = random.randrange(individual.length), random.randrange(individual.length)
    individual.chromosomes[i], individual.chromosomes[j] = individual.chromosomes[j], individual.chromosomes[i]
  return population


def crossover(population):
  half = len(population) / 2
  for individual1, individual2 in zip(population[:half], population[half:]):
    cross_section = slice(random.randrange(0, individual1.length / 2), random.randrange(individual1.length / 2, individual1.length))
    individual1.chromosomes[cross_section], individual2.chromosomes[cross_section] = individual2.chromosomes[cross_section], individual1.chromosomes[cross_section]
  return population


class Population(object):
  # Population(): a group of individuals

  def __init__(self, popsize = 10000, nchrom = 32, chromset = range(10)):
    # __init__(): initialize the population with randomly created individuals
    # popsize: the number of individuals that the population has
    # nchrom: the number of chromosomes each individual in the population has
    # vals: the set of possible values each chromosome of each individual can take
    super(Population, self).__init__()
    self.size = popsize
    self.members = [Individual(nchrom, chromset) for _ in range(self.size)]

  def run(self, eval_fn, fitness_goal = float("Inf"), generations = 10000, minimize = False, mutations = ["mutate"], mutate_cutoff = 1 / 3.0, scramble_cutoff = 2 / 3.0, verbose = False):
    # run(): step the population forward through generations until it
    #        finds an optimal solution or the generation cap is reached
    # eval_fn: the function that takes in a list of chromosomes and returns a fitness
    # fitness_goal: the cutoff value at which to stop
    # generations: the maximum generation limit at which to return the best individual
    # minimize: boolean flag to minimize fitness instead of maximize
    # mutations: the mutation method to use, a list that must contain one or more of "mutate", "swap", or "crossover"
    # mutate_cutoff: the ratio of the population at which to start mutating
    # scramble_cutoff: the ratio of the population at which to start scrambling
    # verbose: boolean flag to print each generation's best individual
    if abs(fitness_goal) == float("Inf") and abs(generations) == float("Inf"):
      raise ValueError("Either the fitness goal or the generation cap must not be set to infinity, or else the algorithm will evolve indefinitely.")

    current_generation = 0
    while current_generation < generations:
      current_generation += 1

      for individual in self.members:
        # evaluate each individual
        individual.fitness = eval_fn(individual.chromosomes)

        condition = (individual.fitness >= fitness_goal) if not minimize else (individual.fitness <= fitness_goal)
        if condition:
          if verbose:
            print("Generation {0}, found fit enough individual: {1} with fitness {2} ({3}= {4})".format(
              current_generation, individual, individual.fitness, ">" if not minimize else "<", fitness_goal))
          # return an individual if it surpasses the threshold
          return individual

      # leave the top segment alone
      pass

      # mutate the middle segment
      mid = slice(int(self.size * mutate_cutoff), int(self.size * scramble_cutoff))      
      if "mutate" in mutations:
        self.members[mid] = mutate(self.members[mid])
      if "swap" in mutations:
        self.members[mid] = swap(self.members[mid])
      if "crossover" in mutations:
        self.members[mid] = crossover(self.members[mid])

      # scramble the bottom segment
      bot = slice(int(self.size * scramble_cutoff), None)
      self.members[bot] = scramble(self.members[bot])

      # sort the population by fitness
      self.members.sort(key = lambda i: i.fitness, reverse = not minimize)
      if verbose:
        print("Generation {0}, best individual: {1} with fitness {2}".format(current_generation, self.members[0], self.members[0].fitness))

    # generation limit reached, return the best member thus far
    if verbose:
      print("Generation limit reached ({0}), best individual: {1} with fitness {2}".format(generations, self.members[0], self.members[0].fitness))
    return self.members[0]

  def __str__(self):
    # __str__(): return a string representation of the population
    return "\n".join([str(i) for i in self.members])


class Individual(object):
  # Individual(): one member of a population, representing a possible solution

  def __init__(self, nchrom = 32, chromset = range(10)):
    # __init__(): initialize the individual with randomly assigned chromosomes
    # nchrom: the number of chromosomes each individual has
    # vals: the set of possible values each chromosome can take
    self.fitness = None
    self.length = nchrom
    self.possibilities = chromset
    self.chromosomes = [random.choice(self.possibilities) for _ in range(self.length)]

  def __str__(self):
    # __str__(): return a string representation of the individual
    return str(self.chromosomes)


if __name__ == "__main__":
  # define an example problem
  population_size = 1000
  num_chromosomes = 15
  possible_values = range(20)
  fitness_goal = 16.0
  max_generations = 2000
  def evaluation_function(chromosomes):
    return float(sum(chromosomes)) / len(chromosomes)

  # create and run the population
  p = Population(population_size, num_chromosomes, possible_values)
  best = p.run(evaluation_function, fitness_goal, max_generations, verbose = True)

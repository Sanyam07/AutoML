from pandas import DataFrame

from .. import AbstractModel
from .chromosome import Chromosome


class Population:

    def __init__(self, population_size=10, config: dict = None):
        """
            Creates a population of chromosomes (models)

            The main scope of the class is to aggregate chromosomes(models) into one place,
        to train them and eventually find the best one.

            Methods:
                - eval(): evaluates the whole population based on a X,Y dataset
                - get_best(): finds the best chromosome and returns it's model
                - replace(): replaces the worst performing model(chromosome) with a new one
                - selection(): returns a chromosome from the population (the better the model is performing,
                                the higher the chances of returning that chromosome)
                - XO(): crossover between two chromosomes: return another one
                - mutation(): performs a random mutation on a chromosome
        """
        if config is None:
            config = {}

        self._config = config

        self._population_size = population_size
        self._population = self._create_population(population_size)
        self._best_model = None
        self._fitness = None

    def eval(self, X: DataFrame, Y: DataFrame) -> AbstractModel:
        """
            Evaluates the population
        :param X: the data to predict an output from
        :param Y: the data to compare the output to
        :return: the best model in the population
        """
        best = None
        best_fitness = None

        for chromosome in self._population:
            chromosome_fitness = chromosome.eval(X, Y)

            if best_fitness is None or self._is_fitter(chromosome_fitness, best_fitness):
                best = chromosome.get_model()
                best_fitness = chromosome_fitness

        return best

    def get_best(self) -> AbstractModel:
        """
            Returns the best model in the population
        :return:
        """
        best = None
        best_fitness = None

        for chromosome in self._population:
            chromosome_fitness = chromosome.get_fitness()

            if best_fitness is None or self._is_fitter(chromosome_fitness, best_fitness):
                best = chromosome.get_model()
                best_fitness = chromosome_fitness

        return best

    def replace(self, model: AbstractModel) -> list:
        """
            Adds the model into the population by replacing the worst model with the new one
        :param model: the new model to be added
        :return: the new population ( the same list as before, but changed)
        """
        # determine the position of the worst
        worst_fitness = None
        worst_position = None

        for i in range(len(self._population)):
            chromosome = self._population[i]
            chromosome_fitness = chromosome.get_fitness()

            if worst_fitness is None or self._is_fitter(worst_fitness, chromosome_fitness):
                worst_fitness = chromosome_fitness
                worst_position = i

        # replace the worst
        new_chromosome = Chromosome(model)
        self._population[worst_position] = new_chromosome

        return self._population

    def selection(self) -> AbstractModel:
        """
            Selects a model from the population
        :return: the selected model
        """
        # TODO

    def XO(self, model1: AbstractModel, model2: AbstractModel) -> AbstractModel:
        """
            Performs cross over between two population members (models).
        :param model1: the first model
        :param model2: the second model
        :return: the offspring
        """
        # TODO

    def mutation(self, model: AbstractModel) -> AbstractModel:
        """
            Performs an in-place mutation on the model, returning it.
        :param model: the model to be mutated
        :return: the same model, mutated
        """
        # TODO

    def _create_population(self, population_size, config: dict = None) -> list:
        """
            Creates a random population of the given size and configuration.
        :param population_size: the number of chromosomes in the population
        :param config: the configuration that states the rules for population creation.
        :return: list of chromosomes
        """
        population = []
        for i in range(population_size):
            model = self._random_model(config)
            chromosome = Chromosome(model)
            population.append(chromosome)
        return population

    def _random_model(self, config: dict = None) -> AbstractModel:
        """
            Generates a random chromosome
        :param config: the configuration for the evolutionary models
        :return: the created model (untrained)
        """
        # TODO

    def _is_fitter(self, actual_fitness: float, best_fitness: float) -> bool:
        """
            Compare the two metrics and decides whether actual_fitness is better(fitter) than best_fitness
        :param actual_fitness: float, score of the actual model
        :param best_fitness: float, the best score so far
        :return: bool
        """
        # TODO

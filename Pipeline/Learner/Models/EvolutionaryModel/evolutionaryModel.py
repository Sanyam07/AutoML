from pandas import DataFrame

from ..abstractModel import AbstractModel
from ..constants import AVAILABLE_TASKS
# TODO check more on this import problem from ...Models import load_model

from ....Exceptions import EvolutionaryModelException

from ..modelTypes import EVOLUTIONARY_MODEL
from .population import Population
from ..constants import AVAILABLE_TASKS


class EvolutionaryModel(AbstractModel):
    """
        The evolutionary model is responsible, like any other AbstractModel, to learn from data and eventually predict,
    but it also searches for the best performing model using evolutionary algorithms.

        The API is similar to the AbstractModel's API
    """

    def __init__(self, in_size: int, out_size: int, task: str = "", config: dict = None, predicted_name: list = None,
                 dictionary: dict = None):
        """
            Initializes a evolutionary model
        :param in_size: the size of the input data
        :param out_size: the size that needs to be predicted
        :param config: the configuration dictionary
        """
        if type(dictionary) is dict:  # for internal use;
            self._init_from_dictionary(dictionary)  # load from a dictionary when loading from file the model
            return

        if config is None:
            config = {}

        # model parameters
        self._predicted_name = predicted_name
        self._task = task
        self._config = config
        self._input_size = in_size
        self._output_size = out_size

        # evolutionary attributes
        if task in AVAILABLE_TASKS:
            self._population = self._create_population(in_size, out_size, task,
                                                       config)  # the population for the evolutionary algorithm
        else:
            self._population = None  # to be created when analysing the data

        self._model = None  # the final model, after the evolutionary phase
        self._model_score = None

    @staticmethod
    def _create_population(in_size: int, out_size: int, task: str, config: dict = None) -> Population:
        """
            Creates a population as configured in the config file
        :param in_size: the size of the input data
        :param out_size: the size that needs to be predicted
        :param task: the task of the model (CLASSIFICATION / REGRESSION)
        :param config: the configuration dictionary
        :return: a population of models
        """
        if config is None:
            config = {}

        population_size = config.get("POPULATION_SIZE", 10)
        population = Population(in_size, out_size, task, population_size, config)
        return population

    def train(self, X: DataFrame, Y: DataFrame, time: int = 600, callbacks: list = None,
              validation: float = 0.2) -> 'AbstractModel':
        """
                Trains the model with the data provided.
            :param validation: percentage of the data to be used in validation; None if validation should not be used
            :param callbacks: a list of predefined callbacks that get called at every epoch
            :param time: time of the training session in seconds: default 10 minutes
            :param X: the independent variables in form of Pandas DataFrame
            :param Y: the dependents(predicted) values in form of Pandas DataFrame
            :return: the model
        """
        # define the task
        if self._task not in AVAILABLE_TASKS or self._population is None:
            # if the task is not defined, neither is the population
            self._task = self._determine_task_type(Y)
            self._population = self._create_population(self._input_size, self._output_size, self._task, self._config)

        # define the predicted names
        if self._predicted_name is None:
            self._predicted_name = list(Y.columns)

        # searches for the best model
        # TODO using epochs now, convert to time later
        EPOCHS = 100

        # initial evaluation
        self._population.eval(X, Y, self._task, self._config.get("GENERAL_CRITERION"), time * 0.6,
                              validation_split=validation)

        for epoch in range(EPOCHS):
            print("======================= EPOCH {}".format(epoch))
            mother = self._population.selection()  # get the
            father = self._population.selection()  # parents

            offspring = self._population.XO(mother, father)  # combine them
            offspringm = self._population.mutation(offspring)  # perform a mutation

            score = offspringm.eval(X, Y, self._task, self._config.get("GENERAL_CRITERION"), time * 0.6,
                                    validation_split=validation)  # evaluate the offspring

            print("Evaluated mode: score {}".format(score))
            if self._model_score is None or self._model_score > score:
                self._model_score = score
                self._model = offspringm.get_model()

            self._population.replace(offspringm)  # add it in the population

        # trains the best model
        self._model = self._population.get_best().get_model()
        train_time = 0  # TODO decide the train time
        self._model.train(X, Y, train_time)

        # returns it
        return self._model

    def predict(self, X: DataFrame) -> DataFrame:
        """
                Predicts the output of X based on previous learning
            :param X: DataFrame; the X values to be predicted into some Y Value
            :return: DataFrame with the predicted data
        """
        if self._model is None:
            raise EvolutionaryModelException("Train the model before performing a prediction.")

        return self._model.predict(X)

    def to_dict(self) -> dict:
        """
            Returns a dictionary representation of the model for further file saving.
        :return: dictionary with model encoding


        """
        # !!! should match _init_from_dictionary loading format
        # get the model data
        model = None
        if not (self._model is None):
            model = self._model.to_dict()

        data = {
            "MODEL": model,
            "METADATA": {
                "PRED_NAME": self._predicted_name,
                "TASK": self._task,
                "CONFIG": self._config,
                "INPUT_SIZE": self._input_size,
                "OUTPUT_SIZE": self._output_size
            }
        }

        return {
            "MODEL_TYPE": self.model_type(),
            "MODEL_DATA": data
        }

    def _init_from_dictionary(self, d: dict):
        """
            Inits the model from dictionary; sets the attributes to be as they were before saving.
            It is assumed that the dictionary provided here is the one intended for this model type.
                - should only be called from the constructor

        :param d: dictionary previously created by to_dict
        :return: None
        """
        # !!! should match to_dict loading format
        d = d.get("MODEL_DATA")
        data = d.get("METADATA")
        model = d.get("MODEL")

        # init the data
        self._predicted_name = data.get("PRED_NAME")
        self._task = data.get("TASK")
        self._config = data.get("CONFIG")
        self._input_size = data.get("INPUT_SIZE")
        self._output_size = data.get("OUTPUT_SIZE")

        # init the model
        # TODO self._model = load_model(model)
        # FIXME
        from ...Models import load_model  # put here to avoid circular imports
        self._model = load_model(model)

    def model_type(self) -> str:
        return EVOLUTIONARY_MODEL

    def _description_string(self) -> str:
        if self._model is None:
            return "Evolutionary Model - Not configured"
        else:
            # TODO
            return "Evolutionary Model - Best model: {best} | Top models: {top}".format(
                best="TODO",
                top="TODO"
            )

    def get_config(self) -> dict:
        return self._config

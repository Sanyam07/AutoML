import pickle
from abc import ABC, abstractmethod

from pandas import DataFrame


class AbstractModel(ABC):
    """
        The end result of the pipeline.
        It's main task is to predict after a training session has been done.

        Methods:
            - train: trains the actual model based on a dataset
            - predict: predicts the output of a dataset
            - to_dict: returns a serializable dictionary
            - save: saves the model to file
            - model_type: returns the model type, as defined in "SpecializedModel/modelTypes.py"

        Behaviour:
            - calling an object ( model_instance(data) ), will return the prediction
    """

    @abstractmethod
    def train(self, X: DataFrame, Y: DataFrame, time: int = 600):
        """
            Trains the model with the data provided.
        :param time: time of the training session in seconds: default 10 minutes
        :param X: the independent variables in form of Pandas DataFrame
        :param Y: the dependents(predicted) values in form of Pandas DataFrame
        :return: the model
        """

    @abstractmethod
    def predict(self, X: DataFrame) -> DataFrame:
        """
            Predicts the output of X based on previous learning
        :param X: DataFrame; the X values to be predicted into some Y Value
        :return: DataFrame with the predicted data
        """

    def __call__(self, X: DataFrame) -> DataFrame:
        """
            Calls the predict method.
        :param X: data to be predicted
        :return: predicted data
        """
        return self.predict(X)

    @abstractmethod
    def to_dict(self) -> dict:
        """
            Returns a dictionary representation that encapsulates all the details of the model
        :return: dictionary with 2 mandatory keys : MODEL_TYPE, MODEL_DATA
        """

    def save(self, file: str):
        """
            Saves the model to file
        :param file: the name of the file or the absolute path to it
        :return: self for chaining purposes
        """
        import json
        with open(file, 'wb') as f:
            data = self.to_dict()
            pickle.dump(data, f)
        return self

    @abstractmethod
    def model_type(self) -> str:
        """
            Returns the model type from available model types in file "model_types.py"
        :return: string with the model type
        """

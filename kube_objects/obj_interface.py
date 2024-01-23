from abc import ABC
from abc import abstractmethod


class KubeObject(ABC):
    """
    Abstract base class representing a Kubernetes object.
    """
    def __init__(self, body=None, namespace=None, name=None):
        self.__body = body
        self.__namespace = namespace
        self.__name = name
        self.__metadata = None
        self.__spec = None

    @property
    def body(self) -> dict:
        """
        Returns:
            dict: The raw body of the k8s object.
        """
        return self.__body

    @property
    def metadata(self) -> dict:
        """
        Returns:
            dict: The metadata of the Kubernetes object.
        """
        if self.__metadata is None and self.body is not None:
            self.__metadata = self.__body.get("metadata")
        return self.__metadata

    @property
    def namespace(self) -> str:
        """
        Returns:
            str: The namespace of the Kubernetes object.
        """
        if self.__namespace is None and self.body is not None:
            self.__namespace = self.metadata.get("namespace") if self.metadata.get("namespace", None) else "default"
        return self.__namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of the k8s object.

        Parameters:
            namespace (str): The new namespace.
        """
        self.__namespace = namespace

    @property
    def name(self):
        """
        Returns:
            str: The name of the k8s object.
        """
        if self.__name is None and self.body is not None:
            self.__name = self.metadata.get("name")
        return self.__name

    @name.setter
    def name(self, name):
        """
        Sets the name of the k8s object.

        Parameters:
            name (str): The new name to set for the k8s object.
        """
        self.__name = name

    @property
    def spec(self):
        """
        Returns:
            dict: The specification of the k8s object.
        """
        if self.__spec is None and self.body is not None:
            self.__spec = self.__body.get("spec")
        return self.__spec

    @spec.setter
    def spec(self, updated_spec):
        """
        Updates the specification of the k8s object and sets it in the body.

        Parameters:
            updated_spec (dict): The new spec.
        """
        if self.body is not None:
            self.body["spec"] = updated_spec
            self.__spec = updated_spec

    @abstractmethod
    def create(self):
        """
        Abstract method to create the k8s object.
        """
        ...

    @abstractmethod
    def delete(self):
        """
        Abstract method to delete the k8s object.
        """
        ...

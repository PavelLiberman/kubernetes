class CustomException(Exception):
    def __init__(self, message, value):
        """
        Base class for custom exceptions in Kubernetes operations.

        Parameters:
        message (str): String describing the exception.
        value: Additional data or value associated with the exception.
        """
        self.message = message
        self.value = value


class FailedToLoadYamlFile(CustomException):
    """
    Exception raised when loading of a YAML file fails.
    """
    ...


class InvalidFileExtension(CustomException):
    """
    Exception raised for invalid file extensions.
    """
    ...


class UnsupportedKubeOperationProvided(CustomException):
    """
    Exception raised when an unsupported K8s operation is provided.
    """
    ...


class FailedToExecuteCommand(CustomException):
    """
    Exception raised when execution of a command fails.
    """
    ...


class KubernetesResourceWasNotFound(CustomException):
    """
    Exception raised when a specified K8s resource is not found.
    """
    ...


class InvalidDefinitionFile(CustomException):
    """
    Exception raised for invalid K8s definition files.
    """
    ...


class ResourceAlreadyExist(CustomException):
    """
    Exception raised when attempting to create a K8s resource that already exists.
    """
    ...


class KubernetesObjectIsNotSupportedYet(CustomException):
    """
    Exception raised when an operation is attempted on a K8s object type that is not yet supported in infra.
    """
    ...


class FailedToCreateLocalDir(CustomException):
    """
    Exception raised when a directory creation is failed.
    """
    ...

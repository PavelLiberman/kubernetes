from custom_exceptions.exception import UnsupportedKubeOperationProvided


class K8sCommandExecutor:
    """
    A class responsible for executing Kubernetes commands based on specified operations.
    """
    def __init__(self):
        self.commands = {}

    def register_command(self, operation, command):
        """
        Registers a command object for a specific operation.

        Parameters:
            operation (str): The name of the operation.
            command (Command): An instance of a Command subclass that will be executed for the operation.
        """
        self.commands[operation] = command

    def execute_command(self, operation, kwargs):
        """
         Executes the command associated with the specified operation.

         Parameters:
             operation (str): The name of the operation.
             kwargs (dict): A dictionary of keyword arguments to be passed to the command object.

         Raises:
             UnsupportedKubeOperationProvided: If the specified operation is not registered in the executor.
         """
        if operation in self.commands:
            command = self.commands[operation](**kwargs)
            command.execute()
        else:
            raise UnsupportedKubeOperationProvided(f"Unsupported operation: {operation}")

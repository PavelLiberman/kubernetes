from kube_functions.funcs import K8sFunctionManager
from command_mapper.commands import DeployCommand
from command_mapper.commands import DeleteCommand
from command_mapper.commands import ExecCommand
from command_mapper.commands import ListCommand
from command_mapper.commands import DownloadCommand
from command_mapper.commands import UploadCommand
from command_mapper.commands import ListPodsCommand
from command_mapper.commands import HealthCheckCommand
from command_mapper.k8s_command_executor import K8sCommandExecutor
from custom_exceptions.exception import UnsupportedKubeOperationProvided


class K8sManager:
    """
    A class that manages K8s operations by encapsulating command execution logic.

    Attributes:
        kube_config (str): Path of kubernetes config file for connecting to cluster.
        command_parameters (dict): Additional parameters to be passed to commands.
        executor (K8sCommandExecutor): An executor to manage command execution.
    """
    def __init__(self, parameters):
        """
        Parameters:
            parameters (dict): A dictionary containing of command parameters.
                               Must include 'kube_config' for Kubernetes cluster connection.
        """
        self.kube_config = parameters.pop("kube_config")
        self.command_parameters = parameters
        self.command_parameters["k8s_func_manager"] = K8sFunctionManager(self.kube_config)
        self.executor = K8sCommandExecutor()
        self._register_commands()

    def _register_commands(self):
        """
        Registers available K8s commands to the executor.
        """
        self.executor.register_command('deploy', DeployCommand)
        self.executor.register_command('delete', DeleteCommand)
        self.executor.register_command('exec', ExecCommand)
        self.executor.register_command('list', ListCommand)
        self.executor.register_command('download', DownloadCommand)
        self.executor.register_command('upload', UploadCommand)
        self.executor.register_command('list-pods-for-all-namespaces', ListPodsCommand)
        self.executor.register_command('health-check', HealthCheckCommand)

    def execute_operation(self, operation):
        """
        Executes a Kubernetes operation.

        Parameters:
            operation (str): The name of the operation to be executed.

        Raises:
            UnsupportedKubeOperationProvided: If the specified operation is not supported or registered.
        """
        try:
            self.executor.execute_command(operation, self.command_parameters)
        except UnsupportedKubeOperationProvided as e:
            print(f'Error: {e}')

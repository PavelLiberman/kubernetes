from abc import ABC
from abc import abstractmethod

from kube_functions.funcs import K8sFunctionManager


class KubeCommandInterface(ABC):
    """
    An abstract base class that defines the interface of a command.
    """
    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the command.
        """
        ...


class DeployCommand(KubeCommandInterface):
    """
    Deploy resources to K8s cluster using a YAML file.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, definition_file_path: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            definition_file_path: Path to the YAML file.
        """
        self.k8s_func_manager = k8s_func_manager
        self.file_path = definition_file_path

    def execute(self):
        self.k8s_func_manager.deploy_from_yaml(self.file_path)


class DeleteCommand(KubeCommandInterface):
    """
    Delete resources from Kubernetes cluster using a YAML file.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, definition_file_path: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            definition_file_path: Path to the YAML file.
        """
        self.k8s_func_manager = k8s_func_manager
        self.file_path = definition_file_path

    def execute(self):
        self.k8s_func_manager.delete_from_yaml(self.file_path)


class ExecCommand(KubeCommandInterface):
    """
    Execute a bash command in a specified pod.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, pod_name: str, namespace: str, command: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            pod_name: Name of the pod.
            namespace: Kubernetes namespace of the pod.
            command: The bash command to be executed.
        """
        self.k8s_func_manager = k8s_func_manager
        self.pod_name = pod_name
        self.namespace = namespace
        self.command = command

    def execute(self):
        self.k8s_func_manager.exec_bash_in_pod(self.pod_name, self.namespace, self.command)


class ListCommand(KubeCommandInterface):
    """
    Execute "ls" command in a specified directory of a pod.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, pod_name: str, namespace: str, dir_name: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            pod_name: Name of the pod.
            namespace: Kubernetes namespace of the pod.
            dir_name: The directory name in the pod.
        """
        self.k8s_func_manager = k8s_func_manager
        self.pod_name = pod_name
        self.namespace = namespace
        self.dir_name = dir_name

    def execute(self):
        self.k8s_func_manager.list_existing_files(self.pod_name, self.namespace, self.dir_name)


class DownloadCommand(KubeCommandInterface):
    """
    Download a file from a pod to the local filesystem.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, namespace: str,
                 pod_name: str, source_path: str, destination_path: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            namespace: Kubernetes namespace of the pod.
            pod_name: Name of the pod.
            source_path: Path of the file in the pod.
            destination_path: Local filesystem path to save the file.
        """
        self.k8s_func_manager = k8s_func_manager
        self.namespace = namespace
        self.pod_name = pod_name
        self.source_path = source_path
        self.destination_path = destination_path

    def execute(self):
        self.k8s_func_manager.copy_file_from_pod(self.namespace, self.pod_name, self.source_path, self.destination_path)


class UploadCommand(KubeCommandInterface):
    """
    Upload a file from the local filesystem to a pod.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager, namespace: str,
                 pod_name: str, source_path: str, destination_path: str):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
            namespace: Kubernetes namespace of the pod.
            pod_name: Name of the pod.
            source_path: Local filesystem path of the file.
            destination_path: Path in the pod to store the file.
        """
        self.k8s_func_manager = k8s_func_manager
        self.namespace = namespace
        self.pod_name = pod_name
        self.source_path = source_path
        self.destination_path = destination_path

    def execute(self):
        self.k8s_func_manager.copy_file_to_pod(self.namespace, self.pod_name, self.source_path, self.destination_path)


class ListPodsCommand(KubeCommandInterface):
    """
    List all pods across all namespaces.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
        """
        self.k8s_func_manager = k8s_func_manager

    def execute(self):
        self.k8s_func_manager.list_pods_for_all_namespaces()


class HealthCheckCommand(KubeCommandInterface):
    """
    Perform a connectivity check between kubernetes cluster and your environment.
    """
    def __init__(self, k8s_func_manager: K8sFunctionManager):
        """
        Parameters:
            k8s_func_manager: The Kubernetes function manager instance.
        """
        self.k8s_func_manager = k8s_func_manager

    def execute(self):
        self.k8s_func_manager.health_check()

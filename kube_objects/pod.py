from kubernetes import client
from kubernetes.stream import stream

from kube_objects.obj_interface import KubeObject
from custom_exceptions.exception import ResourceAlreadyExist
from custom_exceptions.exception import InvalidDefinitionFile
from custom_exceptions.exception import FailedToExecuteCommand
from custom_exceptions.exception import KubernetesResourceWasNotFound
from kube_objects.pod_file_transfer import PodFileTransferMixin


class Pod(KubeObject, PodFileTransferMixin):
    def __init__(self, body=None, namespace=None, name=None):
        """
        Initializes a Pod object for managing k8s pods.
        """
        super().__init__(body, namespace, name)
        self.client = client.CoreV1Api()

    def create(self):
        """
        Creates a pod in cluster.

        Raises:
        ResourceAlreadyExist: If a pod with the same name already exists in the specified namespace.
        InvalidDefinitionFile: If the pod definition YAML file is incorrect.
        ApiException: For other k8s API related exceptions.
        """
        try:
            self.client.create_namespaced_pod(namespace=self.namespace, body=self.body)
            print(f"Pod {self.name} created in {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 409:
                raise ResourceAlreadyExist(
                    f"The pod {self.name} already exist in {self.namespace}.", ex.reason
                )
            if ex.status == 422:
                raise InvalidDefinitionFile(
                    f"The {self.name} pod definition yaml file is wrong.", ex.reason
                )
            else:
                raise

    def delete(self):
        """
        Deletes a pod from cluster.

        Raises:
        KubernetesResourceWasNotFound: If the pod to be deleted is not found in the specified namespace.
        ApiException: For other k8s API related exceptions.
        """
        try:
            self.client.delete_namespaced_pod(name=self.name, namespace=self.namespace)
            print(f"Pod {self.name} deleted from {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 404:
                raise KubernetesResourceWasNotFound(
                    f"The pod {self.name} was not found in {self.namespace} namespace.", ex.reason
                )
            raise

    def exec_bash(self, command: str):
        """
        Executes a shell command inside a pod.

        Parameters:
        command (str): The shell command to be executed inside the pod.

        Raises:
        KubernetesResourceWasNotFound: If the specified pod is not found in the k8s cluster.
        FailedToExecuteCommand: If the execution of the command fails inside the pod.
        """
        exec_command = ["/bin/sh", "-c", command]
        print(f"Executing command '{' '.join(exec_command)}' in {self.name} pod.")
        try:
            api_response = self.get_namespaced_pod_exec_stream(exec_command)
        except client.ApiException as ex:
            raise KubernetesResourceWasNotFound(
                f"The pod {self.name} was not found in {self.namespace} namespace.", ex.reason
            )
        stderr = []
        while api_response.is_open():
            if api_response.peek_stdout():
                print(f"\n{api_response.read_stdout()}")
            if api_response.peek_stderr():
                stderr.append(api_response.read_stderr())
        api_response.close()
        if api_response.returncode != 0:
            raise FailedToExecuteCommand(
                "Failed to execute sh command in pod", f"{', '.join(stderr)}"
            )

    def get_namespaced_pod_exec_stream(self, exec_command: list[str]):
        """
        Method to initiate a stream to a pod for command execution.

        Parameters:
        exec_command (list): The command to execute, split into list elements.

        Returns:
        Stream: A streaming connection to the pod for command execution.
        """
        return stream(self.client.connect_get_namespaced_pod_exec, self.name, self.namespace,
                      command=exec_command,
                      stderr=True, stdin=True,
                      stdout=True, tty=False,
                      _preload_content=False
                      )

    def create_directory(self, destination_path):
        """
        Create a directory inside pod at the specified destination path if it does not already exist.

        Parameters:
        destination_path (str): The file system path where the directory will be created.
                                Should be an absolute path.
        """
        print(f"Creating directory {destination_path} if not exist.")
        self.exec_bash(f"mkdir -p {destination_path}")

from kubernetes import client
from kubernetes import config

from kube_objects.pod import Pod
from helper_functions.helpers import Helpers


class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class K8sFunctionManager(metaclass=SingletonMeta):
    def __init__(self, kube_config: str):
        """
        Initializes the k8s Manager with a specified kube_config.

        Parameters:
        kube_config (str): The path to the k8s configuration file.
        """
        self.__kube_config = kube_config
        config.load_kube_config(self.__kube_config)
        self.__core_v1_api = client.CoreV1Api()

    @property
    def core_v1_api(self):
        """
        Core V1 API property.

        Returns:
        client.CoreV1Api: An instance of the k8s CoreV1Api client.
        """
        return self.__core_v1_api

    @property
    def kube_config(self):
        """
        kube_config property.

        Returns:
        str: The path to the k8s configuration file.
        """
        return self.__kube_config

    @kube_config.setter
    def kube_config(self, kube_config: str):
        """
        Setter for kube_config property.

        Parameters:
        kube_config (str): The path to the k8s configuration file.
        """
        if self.__kube_config is None:
            self.__kube_config = kube_config

    def deploy_from_yaml(self, yaml_file: str):
        """
        Deploys k8s resources defined in a specified YAML file.

        Parameters:
        yaml_file (str): The path to the YAML file containing k8s resource definitions.
        """
        for kube_obj_instance in Helpers.convert_yaml_to_kube_objects(yaml_file):
            kube_obj_instance.create()

    def delete_from_yaml(self, yaml_file: str):
        """
        Deletes k8s resources defined in a specified YAML file.

        Parameters:
        yaml_file (str): The path to the YAML file containing k8s resource definitions.
        """
        for kube_obj_instance in Helpers.convert_yaml_to_kube_objects(yaml_file):
            kube_obj_instance.delete()

    def exec_bash_in_pod(self, pod_name: str, namespace: str, command: str):
        """
        Executes a bash command in a specified pod.

        Parameters:
        pod_name (str): The name of the pod where the command is to be executed.
        namespace (str): The namespace of the pod.
        command (str): The bash command to execute in the pod.
        """
        pod = Pod(name=pod_name, namespace=namespace)
        pod.exec_bash(command)

    def list_existing_files(self, pod_name: str, namespace: str, path_in_pod: str):
        """
        Lists files in a specified path inside a pod.

        Parameters:
        pod_name (str): The name of the pod.
        namespace (str): The namespace of the pod.
        path_in_pod (str): The path inside the pod where files are to be listed.
        """
        self.exec_bash_in_pod(pod_name, namespace, f"ls {path_in_pod}")

    def list_pods_for_all_namespaces(self):
        """
        Lists all pods across all namespaces in the k8s cluster.
        """
        resp = self.core_v1_api.list_pod_for_all_namespaces(watch=False)
        for i in resp.items:
            print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")

    def health_check(self):
        """
        Performs a health check on the k8s cluster to verify connectivity.
        """
        try:
            self.core_v1_api.list_namespace()
            print("Cluster connection is healthy.")
        except client.ApiException as e:
            return f"API exception occurred: {e}"
        except Exception as e:
            return f"Error while connecting to the cluster: {e}"

    def copy_file_to_pod(self, namespace: str, pod_name: str, source_file_path: str, destination_path: str):
        """
        Copies a file from a local host to a specified path in a pod.

        Parameters:
        namespace (str): The namespace of the pod.
        pod_name (str): The name of the pod.
        source_file_path (str): The path of the source file on the local filesystem.
        destination_path (str): The destination path inside the pod.
        """
        pod = Pod(name=pod_name, namespace=namespace)
        pod.create_directory(destination_path)
        pod.copy_file_to_pod(source_file_path, destination_path)

    def copy_file_from_pod(self, namespace, pod_name, source_file_path, destination_path):
        """
        Copies a file from a pod to a local host path.

        Parameters:
        namespace (str): The k8s namespace in which the pod is located.
        pod_name (str): The name of the pod from which the file will be copied.
        source_file_path (str): The path of the file inside the pod.
        destination_path (str): The local filesystem path where to store the file.
        """
        pod = Pod(name=pod_name, namespace=namespace)
        Helpers.create_directory(destination_path)
        pod.copy_file_from_pod(source_file_path, destination_path)

import os.path

from ruamel.yaml import YAML

from kube_objects.pod import Pod
from kube_objects.service import Service
from kube_objects.deployment import Deployment
from custom_exceptions.exception import FailedToLoadYamlFile
from custom_exceptions.exception import InvalidFileExtension
from custom_exceptions.exception import FailedToCreateLocalDir
from custom_exceptions.exception import KubernetesObjectIsNotSupportedYet


class Helpers:
    supported_kube_objects = [Pod, Service, Deployment]

    @classmethod
    def load_yaml(cls, file_path: str):
        """
        Loads and returns the contents of a YAML file.

        Parameters:
        file_path (str): The path to the YAML file to be loaded.

        Returns:
        list: A list of objects representing the contents of the loaded YAML file.

        Raises:
        InvalidFileExtension: If the file extension is not .yaml or .yml.
        FileNotFoundError: If the YAML file does not exist at the specified path.
        FailedToLoadYamlFile: If there is an error during the loading of the YAML file.
        """
        if not any(map(lambda extension: file_path.endswith(extension), [".yaml", ".yml"])):
            raise InvalidFileExtension("The correct file extension is .yaml or .yml", file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {os.path.basename(file_path)} does not found.", file_path)
        yaml = YAML(typ="safe")
        try:
            with open(file_path, "r") as file:
                return list(yaml.load_all(file))
        except Exception as ex:
            raise FailedToLoadYamlFile(f"Failed to load {file_path} file.", ex)

    @classmethod
    def convert_dict_to_kube_object(cls, definition_dict):
        """
        Converts a dictionary representation of a k8s object into its corresponding class instance.

        Parameters:
        definition_dict (dict): A dictionary representing a k8s object.

        Returns:
        object: An instance of the subclass of 'KubeObject' that matches the 'kind' specified in the input dictionary.
                Returns None if no matching class is found.

        Raises: KubernetesObjectIsNotSupportedYet: If the 'kind' specified in the dictionary does not match any
        subclass of 'KubeObject'.
        """
        repr_class = filter(lambda x: x.__name__ == definition_dict.get("kind", None), cls.supported_kube_objects)
        if repr_class:
            repr_class = repr_class.__next__()
            kube_obj_instance = repr_class(definition_dict)
            return kube_obj_instance
        else:
            raise KubernetesObjectIsNotSupportedYet(
                f"The kubernetes object {definition_dict.get('kind', None)} "
                f"does not supported yet. Please contact DevOps team if support is needed.",
                definition_dict.get('kind', None)
            )

    @classmethod
    def convert_yaml_to_kube_objects(cls, yaml_file):
        """
        Converts YAML file contents into corresponding k8s object instances.

        Parameters:
        yaml_file (str): The path to the YAML file containing k8s object definitions.

        Yields:
        object: Instances of k8s object classes for each definition in the YAML file.
        """
        yam_definitions = Helpers.load_yaml(yaml_file)
        for definition in yam_definitions:
            kube_obj_instance = cls.convert_dict_to_kube_object(definition)
            yield kube_obj_instance

    @classmethod
    def create_directory(cls, directory):
        """
        Create a directory at the specified path if it does not already exist.

        Parameters:
        directory (str): The absolute file system path where the directory is to be created.

        Raises:
        FailedToCreateLocalDir: An exception indicating that the directory was not created.
        """
        try:
            print(f"Creating '{directory}' if not exist.")
            os.makedirs(directory, exist_ok=True)
        except OSError:
            raise FailedToCreateLocalDir(f"Failed to create {directory} directory.", directory)

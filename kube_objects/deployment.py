from kubernetes import client

from kube_objects.obj_interface import KubeObject
from custom_exceptions.exception import ResourceAlreadyExist
from custom_exceptions.exception import InvalidDefinitionFile
from custom_exceptions.exception import KubernetesResourceWasNotFound


class Deployment(KubeObject):
    """
    Initializes a Deployment object for managing k8s deployments.
    """
    def __init__(self, body=None, namespace=None, name=None):
        super().__init__(body, name, namespace)
        self.client = client.AppsV1Api()

    def create(self):
        """
        Creates a deployment in cluster.

        Raises:
        ResourceAlreadyExist: If a deployment with the same name already exists in the specified namespace.
        InvalidDefinitionFile: If the deployment definition YAML file is incorrect.
        ApiException: For other k8s API related exceptions.
        """
        try:
            self.client.create_namespaced_deployment(namespace=self.namespace, body=self.body, pretty=True)
            print(f"Deployment {self.name} created in {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 409:
                raise ResourceAlreadyExist(
                    f"The deployment {self.name} already exist in {self.namespace}.", ex.reason
                )
            if ex.status == 422:
                raise InvalidDefinitionFile(
                    f"The {self.name} deployment definition yaml file is wrong.", ex.reason
                )
            else:
                raise

    def delete(self):
        """
        Deletes a deployment from cluster.

        Raises:
        KubernetesResourceWasNotFound: If the deployment is not found in the specified namespace.
        ApiException: For other k8s API related exceptions.
        """
        try:
            self.client.delete_namespaced_deployment(name=self.name, namespace=self.namespace, pretty=True)
            print(f"Deployment {self.name} deleted from {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 404:
                raise KubernetesResourceWasNotFound(
                    f"The deployment {self.name} was not found in {self.namespace} namespace.", ex.reason
                )
            raise

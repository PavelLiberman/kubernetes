from kubernetes import client

from kube_objects.obj_interface import KubeObject
from custom_exceptions.exception import ResourceAlreadyExist
from custom_exceptions.exception import InvalidDefinitionFile
from custom_exceptions.exception import KubernetesResourceWasNotFound


class Service(KubeObject):
    def __init__(self, body=None, namespace=None, name=None):
        """
        Initializes a Service object for managing Kubernetes services.
        """
        super().__init__(body, namespace, name)
        self.client = client.CoreV1Api()

    def create(self):
        """
        Creates a service in cluster.

        Raises:
        ResourceAlreadyExist: If a service with the same name already exists in the specified namespace.
        InvalidDefinitionFile: If the service definition YAML file is incorrect.
        ApiException: For other Kubernetes API related exceptions.
        """
        try:
            self.client.create_namespaced_service(namespace=self.namespace, body=self.body)
            print(f"Service {self.name} created in {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 409:
                raise ResourceAlreadyExist(
                    f"The service {self.name} already exist in {self.namespace}.", ex.reason
                )
            if ex.status == 422:
                raise InvalidDefinitionFile(
                    f"The {self.name} service definition yaml file is invalid.", ex.reason
                )
            else:
                raise

    def delete(self):
        """
        Deletes a service from cluster.

        Raises:
        KubernetesResourceWasNotFound: If the service is not found in the specified namespace.
        ApiException: For other Kubernetes API related exceptions.
        """
        try:
            self.client.delete_namespaced_service(name=self.name, namespace=self.namespace)
            print(f"Service {self.name} deleted in {self.namespace} namespace.")
        except client.ApiException as ex:
            if ex.status == 404:
                raise KubernetesResourceWasNotFound(
                    f"The service {self.name} was not found in {self.namespace} namespace.", ex.reason
                )
            raise

import argparse


class K8sManagerParser:
    def __init__(self):
        """
        Initializes an argument parser for K8s management commands.
        """
        self.__parser = argparse.ArgumentParser(
            description="Kubernetes API Tool",
            epilog="This tool offers a command-line interface for interacting with a Kubernetes cluster, enabling "
                   "actions such as deleting resources, creating new ones, executing shell commands in pods,"
                   "and copying files to and from pods."
        )
        self.__subparsers = self.__parser.add_subparsers(
            dest='operation',
            title='Operations',
            description='Supported operations',
            help='Description'
        )
        self.__add_deploy_parser()
        self.__add_delete_parser()
        self.__add_exec_parser()
        self.__add_exec_list_parser()
        self.__add_list_pods_for_all_namespaces_parser()
        self.__add_health_check_parser()
        self.__add_copy_file_from_pod_parser()
        self.__add_copy_file_to_pod_parser()

    def parse_args(self):
        """
        Parses the command-line arguments provided to the script.

        Returns:
        argparse.Namespace: An object containing all the parsed command-line arguments.
        """
        return self.__parser.parse_args()

    def __copy_file_parameters(self, parser):
        """
        Adds the K8s copy file argument to a given parser.

        Parameters:
        parser (argparse.ArgumentParser): The parser to which the K8s config argument is added.
        """
        parser.add_argument('-src', '--source-path', required=True, help='Source file path.')
        parser.add_argument('-dst', '--destination-path', required=True, help='Destination path.')


    def __add_kube_config(self, parser):
        """
        Adds the K8s configuration file argument to a given parser.

        Parameters:
        parser (argparse.ArgumentParser): The parser to which the K8s config argument is added.
        """
        parser.add_argument('-kc', '--kube-config', required=True, help='Path to the kube config file')

    def __create_delete_resources_parameters(self, parser):
        """
        Adds parameters for creating or deleting resources to a given parser.

        Parameters:
        parser (argparse.ArgumentParser): The parser to which resource management arguments are added.
        """
        parser.add_argument(
            '-dfp', '--definition-file-path', required=True, help='Path to the yaml definitions file'
        )

    def __pod_access_parameters(self, parser):
        """
        Adds parameters for accessing K8s pods to a given parser.

        Parameters:
        parser (argparse.ArgumentParser): The parser to which pod access arguments are added.
        """
        parser.add_argument('-pn', '--pod-name', required=True, help='Name of the pod')
        parser.add_argument('-n', '--namespace', required=True, help='Namespace of the pod')

    def __add_deploy_parser(self):
        """
        Adds a subparser for the 'deploy' operation.

        The 'deploy' operation deploys resources to a K8s cluster.
        """
        deploy_parser = self.__subparsers.add_parser(
            'deploy',
            help='Deploy a resources to Kubernetes',
            description='Deploy a resource to a Kubernetes cluster using a YAML definitions file'
        )
        self.__create_delete_resources_parameters(deploy_parser)
        self.__add_kube_config(deploy_parser)

    def __add_delete_parser(self):
        """
        Adds a subparser for the 'delete' operation.

        The 'delete' operation removes resources from a K8s cluster.
        """
        delete_parser = self.__subparsers.add_parser(
            'delete',
            help='Delete a resources from Kubernetes',
            description='Delete a resource to a Kubernetes cluster using a YAML definitions file'
        )
        self.__create_delete_resources_parameters(delete_parser)
        self.__add_kube_config(delete_parser)

    def __add_exec_parser(self):
        """
        Adds a subparser for the 'exec' operation.

        The 'exec' operation executes a bash command in a specified K8s pod.
        """
        exec_parser = self.__subparsers.add_parser(
            'exec',
            help='Execute a bash command in a Kubernetes pod',
            description='Execute a specific bash command in a given Kubernetes pod.'
        )
        exec_parser.add_argument('-c', '--command', required=True, help='Bash command to execute')
        self.__pod_access_parameters(exec_parser)
        self.__add_kube_config(exec_parser)

    def __add_exec_list_parser(self):
        """
         Adds a subparser for the 'list' operation.

         The 'list' operation lists files in a specified directory within a K8s pod.
         """
        exec_parser = self.__subparsers.add_parser(
            'list',
            help='Execute a ls command in a Kubernetes pod',
            description='Execute a ls bash command in a given Kubernetes pod.'
        )
        exec_parser.add_argument(
            '-dn', '--dir-name', required=True, help='Directory location for listing files within a pod.'
        )
        self.__pod_access_parameters(exec_parser)
        self.__add_kube_config(exec_parser)

    def __add_list_pods_for_all_namespaces_parser(self):
        """
        Adds a subparser for the 'list-pods-for-all-namespaces' operation.

        This operation lists all pods across all namespaces in the K8s cluster.
        """
        parser = self.__subparsers.add_parser(
            'list-pods-for-all-namespaces',
            help='List pods for all namespaces.',
            description='List pods for all namespaces.'
        )
        self.__add_kube_config(parser)

    def __add_health_check_parser(self):
        """
        Adds a subparser for the 'health-check' operation.

        The 'health-check' operation verifies connectivity with the K8s cluster.
        """
        parser = self.__subparsers.add_parser(
            'health-check',
            help='Check connectivity with cluster.',
            description='Perform health check to verify connectivity with kubernetes cluster.'
        )
        self.__add_kube_config(parser)

    def __add_copy_file_to_pod_parser(self):
        """
        Adds a subparser for the 'upload' file to pod operation.
        """
        parser = self.__subparsers.add_parser(
            'upload',
            help='Upload file from local to pod.',
            description='Perform health check to verify connectivity with kubernetes cluster.'
        )
        self.__add_kube_config(parser)
        self.__pod_access_parameters(parser)
        self.__copy_file_parameters(parser)

    def __add_copy_file_from_pod_parser(self):
        """
        Adds a subparser for the 'download' file from pod operation.
        """
        parser = self.__subparsers.add_parser(
            'download',
            help='Download file to local from pod.',
            description='Perform health check to verify connectivity with kubernetes cluster.'
        )
        self.__add_kube_config(parser)
        self.__pod_access_parameters(parser)
        self.__copy_file_parameters(parser)

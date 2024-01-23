from command_mapper.k8s_manager import K8sManager
from command_line_parser.parser import K8sManagerParser

def main():
    parameters = vars(K8sManagerParser().parse_args())
    k8s_manager = K8sManager(parameters)
    k8s_manager.execute_operation(parameters.pop("operation"))


if __name__ == "__main__":
    main()

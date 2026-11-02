import etl.transformer as T
import sys


if __name__ == '__main__':
    # with open(r"etl\configs\base_example.yaml", "r") as file:
    with open(sys.argv[1], "r") as file:
        yaml_content: str = file.read()
        T.transform(yaml_content)

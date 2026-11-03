import etl.transformer as T
import sys


if __name__ == '__main__':

    from dotenv import load_dotenv
    load_dotenv()

    with open(sys.argv[1], "r") as file:
        yaml_content: str = file.read()
        T.transform(yaml_content)

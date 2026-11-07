import etl.transformer as T
import sys
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(thread)d - %(message)s',
)

if __name__ == '__main__':

    from dotenv import load_dotenv
    load_dotenv()

    with open(sys.argv[1], "r") as file:
        yaml_content: str = file.read()
        T.transform(yaml_content)

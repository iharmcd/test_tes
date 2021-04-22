from sys import argv
from configurator import Configurator
from connector import Connector
from resulting import Result
from test_processor import TestProcessor
import glob


def run():
    config = Configurator("dev")
    database_url = config.get_database_url()

    
    connector = Connector(database_url)
    
    logger = Result()
    
    test_processor = TestProcessor(config, connector, logger)
    
    test_processor.process()
    
    logger.finish_test()
    

run()

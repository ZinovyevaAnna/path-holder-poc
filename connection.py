from neo4j import GraphDatabase
import configparser

cp = configparser.ConfigParser()
config_path = "properties.config"
cp.read(config_path)
uri = cp['db']['uri']
auth = (cp['db']['login'], cp['db']['password'])

driver = GraphDatabase.driver(uri, auth=auth)
session = driver.session()


def run(query):
    return session.run(query)


def close():
    session.close()
    driver.close()

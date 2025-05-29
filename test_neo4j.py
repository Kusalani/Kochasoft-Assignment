from neo4j import GraphDatabase
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    uri = config.NEO4J_URI
    username = config.NEO4J_USERNAME
    password = config.NEO4J_PASSWORD
    
    logger.info(f"Testing connection to: {uri}")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        # Test connection
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            value = result.single()["test"]
            logger.info(f"Connection successful! Test query returned: {value}")
            
            # Check database info
            result = session.run("CALL dbms.components()")
            for record in result:
                logger.info(f"Neo4j version: {record}")
                
        driver.close()
        return True
        
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("\n✅ Neo4j connection is working!")
        print("The issue might be with processing large documents.")
        print("Try using the main.py with reduced batch size and triplets.")
    else:
        print("\n❌ Neo4j connection failed!")
        print("Please check:")
        print("1. Your Neo4j instance is running (check Neo4j Aura console)")
        print("2. Your credentials are correct")
        print("3. Your instance hasn't exceeded free tier limits")
        print("\nYou can use main_local.py for local storage instead.")
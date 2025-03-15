import os
from pinecone import Pinecone, ServerlessSpec

def create_index(index_name: str, vect_length: int=1536):
    """
    Create an index in Pinecone for storing vectors.

    This function deletes all existing indexes and creates a new index
    if it does not already exist. The index is created with the specified
    name and vector length, using the 'cosine' similarity metric.

    Args:
        index_name (str): The name of the index to create.
        vect_length (int, optional): The dimensionality of the vectors. Defaults to 1536.
    """
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    try:
        print('Deleting all indexes')
        _ = [pinecone.delete_index(name=index_name['name']) for index_name in pinecone.list_indexes()]
    except Exception as e:
        print('Error In Deleting Indexes: {}'.format(e))
        
    if index_name not in pinecone.list_indexes():
        print('Creating Index: {}'.format(index_name))
        pinecone.create_index(
            name=index_name,
            dimension=vect_length,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print('Done Creating Index: {}'.format(index_name))
        

create_index(index_name="rag-customer-support", vect_length=768)


# import os
# import mysql.connector

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host=os.getenv("DB_HOST"),
#     port=os.getenv("DB_PORT"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     database=os.getenv("DB_NAME")
# )
# cursor = conn.cursor()

# # SQL query to create the table
# create_table_query = """
# CREATE TABLE IF NOT EXISTS chat_history (
#     id INT(11) NOT NULL AUTO_INCREMENT,
#     user_query TEXT NOT NULL,
#     chatbot_answer TEXT NOT NULL,
#     user_id VARCHAR(255) DEFAULT NULL,
#     timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (id)
# );
# """

# # Execute the query
# cursor.execute(create_table_query)

# # Commit changes and close the connection
# conn.commit()
# cursor.close()
# conn.close()

# print("Table 'chat_history' created successfully!")



# cursor.close()
# conn.close()
# cursor = conn.cursor()
# # SQL command to delete the table
# cursor.execute("DROP TABLE IF EXISTS chat_history;")

# # Commit and close connection
# conn.commit()
# cursor.close()
# conn.close()

# print("chat_history table deleted successfully.")
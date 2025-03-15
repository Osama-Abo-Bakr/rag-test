import os
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# Save chat history
def save_chat_history(user_query, chatbot_answer, user_id=None):
    """
    Save a user's query and the chatbot's response to the chat history table.

    Args:
        user_query (str): The user's query.
        chatbot_answer (str): The chatbot's response.
        user_id (str, optional): The user's ID. Defaults to None.
    """
    cursor.execute("""
        INSERT INTO chat_history (user_query, chatbot_answer, user_id)
        VALUES (%s, %s, %s)
    """, (user_query, chatbot_answer, user_id))
    conn.commit()

# Retrieve chat history for a user
def get_chat_history(user_id):
    """
    Retrieve the chat history for a user.

    Args:
        user_id (str): The user's ID.

    Returns:
        list: A list of dictionaries containing the user's query and the chatbot's response.
    """
    cursor.execute("""
        SELECT user_query, chatbot_answer
        FROM chat_history
        WHERE user_id = %s
        ORDER BY timestamp DESC
    """, (user_id,))
    results = cursor.fetchall()
    chat_history = [(row[0], row[1]) for row in results]
    return chat_history


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

# Example usage
# save_chat_history("How do I reset my password?", "Visit the 'Forgot Password' page.", user_id="12345")
# history = get_chat_history("12345")
# print(history)

# # Close the connection
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
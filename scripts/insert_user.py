import mysql.connector
import bcrypt

# Function to insert a new user into the database
def insert_user(db_config, username, password, role):
    # Connect to the MySQL database using the provided configuration
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Insert the user into the 'users' table
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", 
                   (username, hashed_password, role))
    
    # Commit the transaction
    conn.commit()
    
    print(f"User '{username}' with role '{role}' added successfully!")
    
    # Close the database connection
    cursor.close()
    conn.close()

# MySQL database configuration
db_config = {
    'host': 'localhost',  # Your MySQL server host, usually 'localhost'
    'user': 'username',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'database': 'db_name',  # Replace with your database name
    'port': 3306  # Default MySQL port (change if different)
}

# Call the function to insert the 'admin' user
insert_user(db_config, "research_institute", "password123", "Research Institution")


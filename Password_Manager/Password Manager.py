import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
from maskpass import askpass


def create_connection():
    """ Create a database connection to the MySQL server """
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            auth_plugin='mysql_native_password'  # Use the older authentication plugin
        )
        if connection.is_connected():
            print("Connection to MySQL server successful")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_database(connection):
    """ Create the database if it doesn't exist """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS credentials_db")
    connection.commit()


def create_table(connection):
    """ Create the credentials table if it doesn't exist """
    cursor = connection.cursor()
    cursor.execute("USE credentials_db")  # Select the database
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS credentials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        website_name VARCHAR(255) NOT NULL,
        address VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()


def add_entry(connection, website_name, address, username, password):
    """ Add a new entry to the credentials table """
    cursor = connection.cursor()
    cursor.execute("USE credentials_db")  # Select the database
    add_entry_query = '''
    INSERT INTO credentials (website_name, address, username, password)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(add_entry_query, (website_name, address, username, password))
    connection.commit()
    print("Entry added successfully")


def update_entry(connection, website_name, address, username, password):
    """ Update an existing entry in the credentials table """
    cursor = connection.cursor()
    cursor.execute("USE credentials_db")  # Select the database

    # Prompt the user to choose the field to update
    print("Choose the field to update:")
    print("1. Address")
    print("2. Username")
    print("3. Password")
    field_choice = input("Enter the field number: ")

    if field_choice == '1':
        update_entry_query = '''
        UPDATE credentials
        SET address = %s
        WHERE website_name = %s
        '''
        cursor.execute(update_entry_query, (address, website_name))
    elif field_choice == '2':
        update_entry_query = '''
        UPDATE credentials
        SET username = %s
        WHERE website_name = %s
        '''
        cursor.execute(update_entry_query, (username, website_name))
    elif field_choice == '3':
        update_entry_query = '''
        UPDATE credentials
        SET password = %s
        WHERE website_name = %s
        '''
        cursor.execute(update_entry_query, (password, website_name))
    else:
        print("Invalid field choice. No updates performed.")

    connection.commit()
    print("Entry updated successfully")


def search_all_entries(connection, website_name):
    """ Search for all entries with the same website name """
    cursor = connection.cursor()
    cursor.execute("USE credentials_db")  # Select the database
    search_all_query = '''
    SELECT * FROM credentials
    WHERE website_name = %s
    '''
    cursor.execute(search_all_query, (website_name,))
    results = cursor.fetchall()

    if results:
        field_names = ["ID", "Website Name", "Address", "Username", "Password"]
        table = [field_names]  # Initialize the table with field names

        for result in results:
            table.append([result[0], result[1], result[2], result[3], result[4]])

        print(tabulate(table, headers="firstrow", tablefmt="grid"))
    else:
        print("No entries found for the given website name")


def view_all_entries(connection):
    """ Display all entries in a tabular format """
    password = askpass(mask="*")
    if password == "show all":
        cursor = connection.cursor()
        cursor.execute("USE credentials_db")  # Select the database
        view_all_query = '''
        SELECT * FROM credentials
        '''
        cursor.execute(view_all_query)
        results = cursor.fetchall()
        if results:
            table = []
            for result in results:
                table.append([result[0], result[1], result[2], result[3], result[4]])
            print(tabulate(table, headers=["ID", "Website Name", "Address", "Username", "Password"], tablefmt="grid"))
        else:
            print("No entries found.")
    else:
        print("Incorrect password. Access denied.")


def main():
    connection = create_connection()
    if connection:
        create_database(connection)
        create_table(connection)

        while True:
            print("\n1. Add a new entry")
            print("2. Update an existing entry")
            print("3. Search for an entry")
            print("4. View all entries")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                website_name = input("Enter website name: ")
                address = input("Enter address: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                add_entry(connection, website_name, address, username, password)

            elif choice == '2':
                website_name = input("Enter website name: ")
                address = input("Enter new address: ")
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                update_choice = input("Do you want to update just one field? (yes/no): ")
                if update_choice.lower() == 'yes':
                    update_entry(connection, website_name, address, username, password)
                else:
                    update_entry(connection, website_name, address, username, password)

            elif choice == '3':
                website_name = input("Enter website name: ")
                search_all_entries(connection, website_name)

            elif choice == '4':
                view_all_entries(connection)

            elif choice == '5':
                break

            else:
                print("Invalid choice. Please try again.")

        connection.close()


if __name__ == "__main__":
    main()

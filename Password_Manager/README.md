# MySQL Credentials Manager

This project is a MySQL-based credentials manager, which allows users to store, update, and retrieve login credentials for various websites. The application connects to a MySQL database, creates a database and table if they do not exist, and provides a command-line interface for managing credentials.

## Features

- **Create Database and Table:** Automatically create a database and table for storing credentials if they do not exist.
- **Add Entry:** Add new website credentials to the database.
- **Update Entry:** Update existing website credentials.
- **Search Entries:** Search for entries by website name.
- **View All Entries:** Display all entries in a tabular format (password protected).

## Dependencies

- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- [tabulate](https://pypi.org/project/tabulate/)
- [maskpass](https://pypi.org/project/maskpass/)

## Installation

To install the necessary dependencies, use the following pip commands:

```bash
pip install mysql-connector-python
pip install tabulate
pip install maskpass
```

## Creating an executable

You can create an executable file that you can open and run from anywhere with running the code every time you want to use it.

### Follow these steps :

- Step 1: Download [Pyinstaller](https://pyinstaller.org/en/stable/)

```bash

pip install pyinstaller
```

- Step 2: 

```bash

pyinstaller --onefile --console --distpath "Location where you want the executable" --name NameOfExe Password Manager.py
```


## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

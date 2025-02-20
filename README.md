# export-db-phpMyAdmin

# Usage Instructions

Before using, please modify the following in the code:

1. Specify the database name to export:
   `'db': 'dbname1'`

2. Specify the tables to export:
   - Locate the source code at `List of table names (requires manual addition)`
   - Manually specify all the tables, separated by commas

3. Modify the phpMyAdmin server address, login username, and password.

Once the above modifications are completed, you can automatically export the specified database to your local machine using the command:
```bash
python3 dbexport.py
```
```` ▋

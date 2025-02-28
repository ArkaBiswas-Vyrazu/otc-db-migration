# MySQL-To-Postgresql Database Migration 

We use Python scripts here to extract data from MySQL Database in csv formats, and then use them to create tables and import data into Postgresql database.
To use this, please check out the main.sh file for any other additional details.

WARNING: This is a very amateur approach to this, you can probably use pgloader for this purpose. At this time, it does not work without downgrading MySQL to version 5.

IMPORTANT NOTE: This project assumes by default that the MySQL database is hosted. You can optionally use a mysqldump file, which would create a MySQL database
locally and use that to migrate to the Postgres Database. In this case then, make sure the .env file is set up properly for that [basically, the database name can be anything as it may not exist locally. The other connection details need to be set though...]

## Steps to use this

1.  Clone the project into local drive
2.  Setup the .env file using the provided .env.example file and save it as .env
    - If you are using a mysqldumpfile, we assume that you want to create a new MySQL Database. In that case, if you want the database to be installed locally, please ensure that the MYSQL_DB_HOST and MYSQL_DB_PORT variables are localhost and 3306 respectively. You may also need to check out the provided mysql_local.sh script for this. By default, it will use the password in the command line.Optionally, you can also use the provided mysql.config.example file if you do not wish to use the MySql database password in the command line. Save the file as mysql.config.
3.  <b>Please note that there is no method implemented to import views, so you would need to import each and every view yourself. Place the DDLs of each view 
    into the provided view_sql.sql file. NOTE:- Make sure that the view DDL is compatible with Postgresql. And make sure that the proper database name is given.</b>
4.  Run the main.sh script using the command <code>./main.sh</code>
    If you need to record output, you can skip the prompts by using the command:
    
        printf '%s\n' no no no no yes yes | ./main.sh &> output.log

    This command **assumes** that **no mysqldumpfile has been provided**, **a local Postgres database would not be created**, **you have no views definitions defined**, **you have no extra fixes defined**, and **you want to keep the output folder and the venv folder** respectively.

## Additional Notes

1. If the default data type definitions are not being represented correctly, you may have to use the provided custom_data_types file to ensure proper datatype definition. As said before, this is not a perfect approach. If possible, use pgloader.

2. If extra fixes are needed, you can use the importer-fixer script.

3. It can be possible that duplicate indexes may be created, so you may need to remove them to save space.

4. It is very possible that the resultant database migration would not be perfect, so please review database properly after migration to ensure if there are any additional tweaks that need to be given.
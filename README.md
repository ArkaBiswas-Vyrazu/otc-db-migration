# MySQL-To-Postgresql Database Migration 

We use Python scripts here to extract data from MySQL Database in csv formats, and then use them to create tables and import data into Postgresql database.

WARNING: This is a very amateur approach to this, you can probably use pgloader for this purpose. At this time, it does not work without downgrading MySQL to version 5.

## Steps to use this

1. Clone the project into local drive
2. You need a mysqldump file for this to work. After dumping mysql database, place it in the same directory as the main.sh file.
3. Setup the .env file using the provided .env.example file
4. Optionally, you can also use the provided mysql.config.example file if you do not wish to use MySql database password in the command line.
5. Run the main.sh script using the command <code>./main.sh</code>
    - If you need to record output, you can skip the prompts by using the command <code>printf '%s\n' yes yes | ./main.sh &> output.log</code>

## Additional Notes

1. If the default data type definitions are not being represented correctly, you may have to use the provided custom_data_types file to ensure proper datatype definition. As said before, this is not a perfect approach. If possible, use pgloader.

2. If extra fixes are needed, you can use the importer-fixer script.

3. It is very possible that the resultant database migration would not be perfect, so please review database properly after migration to ensure if there are any additional tweaks that need to be given.
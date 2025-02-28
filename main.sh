# Exports CSV Files from MySQL to Postgresql Database
echo -e "\nWelcome to the migrator. This will help you migrate your MySQL Database to a Postgresql Version."
echo -e "IMPORTANT NOTE:- IF YOU ARE USING VIEWS PLEASE MAKE SURE YOU HAVE USED THE CORRECT DATABASE NAMES"

echo -e "\nMySQL Database will only be used to read data, constraints and indexes. The database will not be affected in any way"
echo -e "If you feel unsafe about this, you can optionally use a mysqldump file, which will create a copy of the same MySQL database locally"
echo -e "WARNING: Just make sure that there are no other MySQL databases of the same name as provided in the .env locally, as it would drop it to create the new database.\n"

read -p "Are you using a mysqldump file? Make sure the mysqldumpfile path has been configured properly in the .env file (Y|N): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    # Restarting MySQL Database (Comment out if not needed)
    echo -e "\nRestarting MySQL Server"
    sudo systemctl restart mysql

    # # Recreating MySQL Database (Comment out if not needed)
    /bin/bash ./mysql_local.sh
fi

# # Creating virtual environment (Comment out if not needed)
echo -e "\nSetting up New Virtual Environment"
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install -r requirements.txt

source .env

echo -e "\nBefore importing to the official Postgres Server, you can optionally test it locally if you feel you need to check it is working fine or not"
echo -e "In this case, a Postgres database of the same name will be created locally and the migration would then take place there"
echo -e "For this, change the PG_DB_HOST to localhost and PG_DB_PORT to 5432 in the .env file"
echo -e "WARNING: If there are any existing databases of the same name locally, that database will be dropped before creation."
read -p "Do you want to test Postgres Migration locally first? (Y|N): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo -e "\nRestarting Postgresql Server"
    sudo systemctl restart postgresql
    echo -e "\nDropping Database $PG_DB_DATABASE"
    dropdb $PG_DB_DATABASE
    echo -e "\nCreating Database $PG_DB_DATABASE"
    createdb $PG_DB_DATABASE
fi

echo -e "\nExporting CSV Files from MySQL Database: $MYSQL_DB_DATABASE"
venv/bin/python ./extractor.py

echo -e "\nImporting CSV Files into Postgresql Database: $PG_DB_DATABASE"
venv/bin/python ./importer.py

echo -e "\nExporting Constraints and Indexes from MySQL Database to Postgresql Database"
venv/bin/python ./importer-extra.py

echo -e "\nAre you using views in the MySQL Database? If that's the case you need to set it up manually. Refer to the README for more details"
read -p "Confirm (Y|N): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo -e "\nExporting View Definition from MySQL Database to Postgresql Database"
    venv/bin/python ./importer-views.py
fi

# Any additional fixes like correcting field values, ensuring proper data types, etc
read -p "Are there any additional fixes that you may wish to use? Refer to the README for more details. Confirm (Y|N): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo -e "\nAdding Extra Fixes to Postgresql Database"
    venv/bin/python ./importer-fixer.py
fi

# Option to delete output folder
read -p "Keep output folder? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || rm -rf ./output

# Option to delete venv folder
read -p "Keep venv folder? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || rm -rf ./venv

# For security purposes, unsetting the .env values
echo -e "Removing loaded .env values" 
unset MYSQL_DB_USERNAME
unset MYSQL_DB_PASSWORD
unset MYSQL_DB_HOST
unset MYSQL_DB_DATABASE
unset MYSQL_DB_PORT
unset PG_DB_USERNAME
unset PG_DB_PASSWORD
unset PG_DB_HOST
unset PG_DB_DATABASE
unset PG_DB_PORT

echo -e "\nMigration Done, please verify the New Postgresql Database $PG_DB_DATABASE for extra tweaks"

deactivate

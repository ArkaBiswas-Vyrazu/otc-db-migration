# Exports CSV Files from MySQL to Postgresql Database

# Restarting MySQL Database (Comment out if not needed)
echo -e "\nRestarting MySQL Server"
sudo systemctl restart mysql

# # Recreating MySQL Database (Comment out if not needed)
/bin/bash ./otc_db_backup.sh

# # Creating virtual environment (Comment out if not needed)
echo -e "\nSetting up New Virtual Environment"
python3 -m venv venv
source venv/bin/activate
venv/bin/python -m pip install -r requirements.txt

source .env

echo -e "\nRestarting Postgresql Server"
sudo systemctl restart postgresql
echo -e "\nDropping Database $PG_DB_DATABASE"
dropdb $PG_DB_DATABASE
echo -e "\nCreating Database $PG_DB_DATABASE"
createdb $PG_DB_DATABASE

echo -e "\nExporting CSV Files from MySQL Database: $MYSQL_DB_DATABASE"
venv/bin/python ./extractor.py

echo -e "\nImporting CSV Files into Postgresql Database: $PG_DB_DATABASE"
venv/bin/python ./importer.py

echo -e "\nExporting Constraints and Indexes from MySQL Database to Postgresql Database"
venv/bin/python ./importer-extra.py

# Exclusive to OTC Database migration, THIS SHOULD NOT BE USED OTHERWISE
# echo -e "\nExporting View Definition from MySQL Database to Postgresql Database"
venv/bin/python ./importer-views.py
# This command fails at the moment, use the script in view_sql to directly create a view in Postgres
# psql -U $PG_DB_USERNAME -d $PG_DB_DATABASE -a -f view_sql.sql


echo -e "\nMigration Done, please verify the New Postgresql Database $PG_DB_DATABASE for extra tweaks"

deactivate

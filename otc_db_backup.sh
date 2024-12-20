# Purpose: To automate creating a new OTC database
source .env

echo -e "\nDropping and Creating new Database $MYSQL_DB_DATABASE"
sudo mysql --password=$MYSQL_DB_PASSWORD -e "DROP DATABASE IF EXISTS $MYSQL_DB_DATABASE; CREATE DATABASE $MYSQL_DB_DATABASE; USE $MYSQL_DB_DATABASE; source $MYSQL_DATA_BACKUP_PATH;"

# # Could look into automating this too?
# # Note: Add any tables that need to be removed too, or you could just edit the MySQL dump script directly
# declare -a tables_depreceated=(
#     [0]=auth_assignment
#     [1]=auth_item_child
#     # [2]=auth_item
#     # [3]=auth_rule
#     # [4]=user_subject
#     # [5]=auth_user_groups #Possibly default provided by Django
#     # [6]=auth_user_user_permissions #Possibly default provided by Django
#     # [7]=django_admin_log #...this definitely is provided by Django
#     # [8]=auth_user #...coincidentally, this one comes too
# )

# echo -e "\nDropping Depreceated Tables"
# for i in ${tables_depreceated[@]}
# do
# echo "Dropping table $i"
# sudo mysql --password=$MYSQL_DB_PASSWORD -e "USE $MYSQL_DB_DATABASE; DROP TABLE IF EXISTS $i;"
# done
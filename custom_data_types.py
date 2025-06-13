import enum
from sqlalchemy.types import *

# For ENUM Definitions, you should define it in this manner
# variable_name = Enum(enum.Enum('variable_name', {'EnumChoice0': 0, 'EnumChoice1': 1, ....}))
# Otherwise, if you are not using keywords or strings with spaces at enum choices, you can define it as follows

class Example(enum.Enum):
    """Enum Example.
    
    Casing does not matter, but it should follow this pattern.
    """

    ONE = 1
    TWO = 2

# DATA_TYPE DEFINITION (Needed to explicately ensure correct data type)
# Recommendation: While not necessary, you should still define all the columns in the table to prevent unexpected behaviour
custom_data_types = {
    "table_name": {
        "id": BigInteger,
        "enum": Enum(Example)
    }
}

# These data types will be applied to all tables if the column also exists, otherwise it is ignored
# WARNING: If even one of these data types for one of the tables is wrong, the table will default back to its original data type definition
default_data_types = {
    'status': SmallInteger,
    'deleted_at': DateTime(timezone=True),
}

# In case you do not want to add the global data types to specific tables
excluded_tables = []

for table in custom_data_types:
    for column in default_data_types:
        if column not in custom_data_types[table] and table not in excluded_tables:
            custom_data_types[table][column] = default_data_types[column]

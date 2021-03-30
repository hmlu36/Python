
from Models.entities import db
from pony.orm import *

db.bind('sqlite', 'database.sqlite', create_db=True)
# sql_debug(True)
db.generate_mapping(create_tables=True)

from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pmUQjdnk3sQbMsmosJE9'
app.config['MYSQL_DATABASE_DB'] = 'Naybrr'
app.config['MYSQL_DATABASE_HOST'] = 'naybrr.ctwclmh06vdt.us-east-2.rds.amazonaws.com'
mysql.init_app(app)
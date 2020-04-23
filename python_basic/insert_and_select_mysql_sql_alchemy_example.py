import sqlalchemy as db
engine = db.create_engine('mysql://airflow:airflow@1.2.3.4:3306/airflow')

def get_study_from_airflow_db(my_name):
	connection = engine.connect()
	metadata = db.MetaData()
	study_table = db.Table('my_table', metadata, autoload=True, autoload_with=engine)

#Equivalent to 'SELECT * FROM study'
#query = db.select([my_table])

#SQL :SELECT min(myCol) FROM my_table
#SQLAlchemy :	
	query = db.select([db.func.min(study_table.columns.myCol)]).where(study_table.columns.myCol2 ==my_name )

	ResultProxy = connection.execute(query)

	ResultSet = ResultProxy.fetchall()
	#print (ResultSet[:0])

	#parsing results
	[value for value, in ResultSet]
	print (value)

def insert_new_study_id(my_name):
	## tyring now to insert data
	try:
		conn = engine.connect()
		trans = conn.begin()
		insert_into='INSERT INTO study(study)  VALUES (\''+my_name+'\' );'
		conn.execute(insert_into)
		trans.commit()
		print ("inserted: "+my_name)
		return ("sababa")
	except:
		return ("not sababa")


new_study="MyLatestSTR"
insert_new_study_id(my_name)
get_study_from_airflow_db(my_name)

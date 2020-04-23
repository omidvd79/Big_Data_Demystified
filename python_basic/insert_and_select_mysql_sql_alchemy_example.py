import sqlalchemy as db
engine = db.create_engine('mysql://airflow:airflow@35.224.15.188:3306/airflow')

def get_study_from_airflow_db(study_name):
	connection = engine.connect()
	metadata = db.MetaData()
	study_table = db.Table('study', metadata, autoload=True, autoload_with=engine)

#Equivalent to 'SELECT * FROM study'
#query = db.select([study_table])

#SQL :SELECT SUM(pop2008) FROM study_id
#SQLAlchemy :	
	query = db.select([db.func.min(study_table.columns.study_id)]).where(study_table.columns.study ==study_name )

	ResultProxy = connection.execute(query)

	ResultSet = ResultProxy.fetchall()
	#print (ResultSet[:0])

	#parsing results
	[value for value, in ResultSet]
	print (value)

def insert_new_study_id(new_study):
	## tyring now to insert data
	try:
		conn = engine.connect()
		trans = conn.begin()
		insert_into='INSERT INTO study(study)  VALUES (\''+new_study+'\' );'
		conn.execute(insert_into)
		trans.commit()
		print ("inserted: "+new_study)
		return ("sababa")
	except:
		return ("not sababa")


new_study="MyLatestSTR"
insert_new_study_id(new_study)
get_study_from_airflow_db(new_study)

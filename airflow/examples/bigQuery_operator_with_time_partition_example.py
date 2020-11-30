write_data = BigQueryOperator(
    sql="select * from t",
    destination_dataset_table=myDataSet.AGG_daily ,
    task_id='write__data',
    bigquery_conn_id='bigquery_default',
    use_legacy_sql=False,
    write_disposition='WRITE_APPEND',
    create_disposition='CREATE_IF_NEEDED',
    time_partitioning={"field": "date", "type": "DAY"},
    dag=dag,
)

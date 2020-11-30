gcs2bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
    task_id='gcs_to_bigquery',
    bucket=myBucket,
    source_format='NEWLINE_DELIMITED_JSON',
    source_objects=*,
    create_disposition='CREATE_IF_NEEDED',
    write_disposition='WRITE_APPEND',
    destination_project_dataset_table=myDataSet.active_table,
    schema_fields=[
        {'name': 'sig', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'platform', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'timestamp', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'app', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'identity', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'id', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'type', 'type': 'STRING', 'mode': 'NULLABLE'},
    ],
    default_args=args,
    dag=dag
)

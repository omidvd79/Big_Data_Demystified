load_csv = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq_example',
        bucket='shirlie-test',
        source_objects=['usrTable.csv'],
        destination_project_dataset_table='airflow_test.gcs_to_bq_table',
        schema_fields=[
            {'name': 'date', 'type': 'INT64', 'mode': 'NULLABLE'},
            {'name': 'count_users', 'type': 'INT64', 'mode': 'NULLABLE'},
            {'name': 'session_duration', 'type': 'FLOAT64', 'mode': 'NULLABLE'},
            {'name': 'new_users', 'type': 'INT64', 'mode': 'NULLABLE'},
            {'name': 'return_users', 'type': 'INT64', 'mode': 'NULLABLE'},
                              
        ],
        write_disposition='WRITE_TRUNCATE',
        dag=dag)

echo mounting FUSE of s3  bucket  
s3fs myBucket:/ /home/ubuntu/airflow/dags -o allow_other -o use_rrs -o allow_other -o use_cache=/tmp -o uid=1000 -o gid=1000

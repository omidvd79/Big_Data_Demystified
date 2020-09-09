create or replace stage MYS3STAGE3 
url='s3://omid-simpo-test/partition/' 
CREDENTIALS=(aws_key_id='A12W' aws_secret_key='/m1yN15L1') ;

select $1 as a,$2 as b,$3 as c from @MYS3STAGE3 (file_format => mys3csv) limit 10 --will bring all

select $1 as a,$2 as b,$3 as c from @MYS3STAGE3/dt=2020-09-08/ (file_format => mys3csv) limit 10 --will bring only a partition



--create table public.sample_csv2 as 
--select $1::int as a,$2::int as b,$3::int as c from @MYS3STAGE3 (file_format => mys3csv)  

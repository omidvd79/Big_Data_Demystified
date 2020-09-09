list @MYS3STAGE

create or replace stage MYS3STAGE2 
url='s3://omid-simpo-test/csv/' 
CREDENTIALS=(aws_key_id='AKIAXV=CW' aws_secret_key='/mlA42D=3lb0q6y') ;

select $1 as a,$2 as b,$3 as c from @MYS3STAGE2 (file_format => mys3csv) limit 10

create table public.sample_csv2 as 
select $1::int as a,$2::int as b,$3::int as c from @MYS3STAGE2 (file_format => mys3csv)  

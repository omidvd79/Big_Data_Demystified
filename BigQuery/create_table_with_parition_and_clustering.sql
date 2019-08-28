CREATE TABLE my_dataset.new_clustered_table 
( 
date DATE, field_a STRING, field_b STRING, field_c STRING, field_d STRING, field_e STRING
) 
PARTITION BY date 
CLUSTER BY field_a, field_b 
OPTIONS ( description="a_table clustered_by_two_fields" ) 


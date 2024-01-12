create or replace table gbq_table_audit.users_audit(
  id int,
  first_name string, 
  last_name string,
  change_type string,
  change_datetime datetime,
  version_num bytes, 
)

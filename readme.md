# gbq-table-audit

## Overview

Audit trail that keeps track of new users, users_ID used as primary key

users.ddl creates a table for new users \
users_audit.ddl creates a table for user audits \
insert_users.dml is used to create indexs for new users \
users_audit.sql is used to update user audits

code keeps track of new users in order to verify and track transactions

To test, run users.ddl and users_audit.ddl first. Then run insert_users.dml to add users. Then run users_audit.sql to update the audit trail. 

## Create pipvenv and install dependencies

```shell 
cd ./path/to/project
pip install pipenv --user
pipenv install
```

## Unit Testing

### Setup Audit Log in Google Cloud Platform

Sign into [Google Cloud Platform](https://cloud.google.com/).

Create a new project or select working project. Open the menu and open BigQuery. \
Within your project, click on "View Actions" on the right of your project name. 
Click on "Create dataset" and set the Dataset ID as "gbq_table_audit". \
On the right of the newly created dataset "gbq_table_audit", click on "View Actions" again. 
Click on "Create table" and name it "users". \
Repeat again and create another table named "users_audit".

### Set Up Service Account

Go to the [Service Account](https://console.cloud.google.com/projectselector/iam-admin/serviceaccounts/create?walkthrough_id=iam--create-service-account#step_index=1) page and follow the tutorial.

Download the .json file and save it in the repository file.

Set enviroment variable "GOOGLE_APPLICATION_CREDENTIALS" to the .json file.\ 
Alternatively, in line 5 of query_test.py, change the .json string to the file name of the .json file.

### Run Tests

```shell
pipenv shell
pytest hello_world_test.py -s
```
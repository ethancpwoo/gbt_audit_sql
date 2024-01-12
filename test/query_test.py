import os
import pytest
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'icssolutions-9023c370f059.json'

client = bigquery.Client()

# inserts queries

def run_audit_log():
    with open("src/users_audit.bqsql", "r") as f:
        query = f.read()
        query_job = client.query(query)
        query_job.result()
        print("audit log ran")

def insert_into_table():
    with open("src/insert_users.dml", "r") as f:
        query = f.read() 
        query_job = client.query(query)
        query_job.result()
        print("inserted users into user table")

def insert_updated_users(): 
    with open("test/test_sql/insert_updated_users.dml", "r") as f:
        query = f.read()
        query_job = client.query(query)
        query_job.result()
        print("inserted updated users into user table")

# delete queries

def delete_users():
    with open("test/test_sql/delete_users.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        query_job.result()
        print("deleted users")

def delete_audit():
    with open("test/test_sql/delete_audit.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        query_job.result()
        print("deleted audit")

def delete_for_test():
    with open("test/test_sql/delete_for_test.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        query_job.result()
        print("deleted for test")

# reading queries

def get_audit_log():
    query_job = client.query(
        """
        SELECT*
        FROM gbq_table_audit.users_audit
        """
    )
    results = query_job.result()
    return results

def get_n_insert():
    with open("test/test_sql/get_audit_insert.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        results = query_job.result()
        print("got num of inserts")
        return results

def get_n_update():
    with open("test/test_sql/get_audit_update.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        results = query_job.result()
        print("got num of updates")
        return results

def get_n_delete():
    with open("test/test_sql/get_audit_delete.bqsql") as f:
        query = f.read()
        query_job = client.query(query)
        results = query_job.result()
        print("got num of deletes")
        return results
# tests

def test_auditinsert():

    # insert users and run audit
    insert_into_table()
    run_audit_log()

    results_first_insert = get_audit_log()

    # check if there are 4 entries
    assert results_first_insert.total_rows == 4

    # check if the 4 entries are inserts
    assert get_n_insert().total_rows == 4

    # check if audit is ran again, no extra inserts
    run_audit_log()
    results_second_insert = get_audit_log()
    assert results_second_insert.total_rows == 4
    assert get_n_insert().total_rows == 4

    # insert users and run audit
    insert_into_table()
    run_audit_log()

    results_first_insert = get_audit_log()

    # check if there are 4 entries
    assert results_first_insert.total_rows == 4

    # check if the 4 entries are inserts
    assert get_n_insert().total_rows == 4

    # check if audit is ran again, no extra inserts
    run_audit_log()
    results_second_insert = get_audit_log()
    assert results_second_insert.total_rows == 4
    assert get_n_insert().total_rows == 4


def test_auditdelete():

    delete_for_test()
    run_audit_log()

    results_first_delete = get_audit_log()
    
    # check if there are 4 entries are inserts
    assert results_first_delete.total_rows == 5

    # check if 1 of the entries are delete
    assert get_n_delete().total_rows == 1

    # check if audit is ran again, no extra updates
    run_audit_log()
    results_second_delete = get_audit_log()
    assert results_second_delete.total_rows == 5
    assert get_n_delete().total_rows == 1


def test_auditupdate(): 
    
    delete_for_test()
    insert_updated_users()

    run_audit_log()
    results_first_update = get_audit_log()

    # check if there are 5 entries
    assert results_first_update.total_rows == 6

    # check if 1 of the entries are update
    assert get_n_update().total_rows == 1

    # check if audit is ran again, no extra updates
    run_audit_log()
    results_second_update = get_audit_log()
    assert results_second_update.total_rows == 6
    assert get_n_update().total_rows == 1

    # ------- cleanup -------
    # delete users and audit
    delete_users()
    delete_audit()

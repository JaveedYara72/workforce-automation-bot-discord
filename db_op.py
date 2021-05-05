# This file contains basic db operations

# TODO
# More queries are required for making changes in the Kourage database

def insert(insert_query, value):
    mycur.execute(insert_query, value)
    mydb.commit()

def update(update_query, value):
    mycur.execute(update_query, value)
    mydb.commit()

def delete(delete_query, value):
    mycur.execute(delete_query, value)
    mydb.commit()



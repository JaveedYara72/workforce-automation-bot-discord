# This file contains basic db operations

def insert(insert_query, value):
	mycur.execute(insert_query, value)
	mydb.commit()


def update(update_query, value):
	mycur.execute(update_query, value)
	mydb.commit()


def delete(delete_query, value):
	mycur.execute(delete_query, value)
	mydb.commit()



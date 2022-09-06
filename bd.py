#import sqlite3
import psycopg2
import os

#URI = os.environ.get('postgres://xabpebvknmldig:5d6128620499722ea66b197fb1aaae3f67d9d48c2386efa61c557ce465048ca4@ec2-44-206-89-185.compute-1.amazonaws.com:5432/d1jm1mpo08r6cf')

#conn=sqlite3.connect('datadb.db', check_same_thread=False)
#conn=psycopg2.connect(URI, check_same_thread=False)

conn = psycopg2.connect(dbname="d1jm1mpo08r6cf", 
	user="xabpebvknmldig", 
	password="5d6128620499722ea66b197fb1aaae3f67d9d48c2386efa61c557ce465048ca4",
	host ="ec2-44-206-89-185.compute-1.amazonaws.com",
	port ="5432"
	)



c=conn.cursor()

def createTable():
	c.execute("""CREATE TABLE if not exists tablaPredicción ( 
		id_prediccion SERIAL PRIMARY KEY,
        prediccion TEXT, 
        vivero TEXT, 
        fecha_registro DATE)"""
        )
	conn.commit()

def add_data(prediccion, vivero, fecha_registro):
	c.execute("""INSERT INTO tablaPredicción ( 
        prediccion, 
        vivero, 
        fecha_registro) 
        VALUES (%s,%s,%s)""",
        (prediccion, vivero, fecha_registro))
	conn.commit()

def view_all_data():
	c.execute('SELECT * FROM tablaPredicción')
	data = c.fetchall()
	return data

def view_all_rowid():
	c.execute('SELECT DISTINCT id_prediccion FROM tablaPredicción')
	data = c.fetchall()
	return data

def delete_data(id_prediccion):#id_prediccion
	c.execute('DELETE FROM tablaPredicción WHERE id_prediccion="{}"'.format(id_prediccion))
	conn.commit()
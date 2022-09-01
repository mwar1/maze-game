import sqlite3 as sqlite

def createDatabase(file):
	## Creates a new database, at the file path passed in

	## Create an SQL connection
	connection = sqlite.connect(file)

	## An SQL command to create a new table with the required fields
	scoresTable = """CREATE TABLE IF NOT EXISTS highscores (
					 name text,
					 score integer,
					 gameType text,
					 rounds integer);"""
	
	## Create a cursor
	cursor = connection.cursor()
	## Executre the SQL command
	cursor.execute(scoresTable)

	return connection

def addItem(connection, name, score, gameType, rounds):
	## Adds a new record to the database

	## SQL to insert a new record into the database
	command = """INSERT INTO highscores (name, score, gameType, rounds)
				 VALUES (?, ?, ?, ?);"""

	## Create a cursor
	cursor = connection.cursor()
	## Execute the SQL command, with the arguments which were
	## passed into the procedure
	cursor.execute(command, (name, score, gameType, rounds))
	## Commit the changes to the database
	connection.commit()

def closeDatabase(connection):
	## Closes the database connection

	connection.close()

def getScoreTable(connection):
	## Returns a 2D list of the top ten scores,
	## sorted in 5 different ways

	scores = []
	cursor = connection.cursor()

	## Get the scores for all rounds, sorted by score
	command = """SELECT * FROM highscores
				 ORDER BY score DESC;"""

	## Execute the SQL command
	cursor.execute(command)
	rows = cursor.fetchall()
	## Add the top ten scores from the returned data to the list
	scores.append(rows[:10])

	## Get the scores for all round, sorted by round number
	command = """SELECT * FROM highscores
				 ORDER BY rounds DESC, score DESC;"""
	cursor.execute(command)
	rows = cursor.fetchall()
	scores.append(rows[:10])

	## Get the scores for multiple round mode, sorted by score
	command = """SELECT * FROM highscores WHERE gameType = "multiple"
				 ORDER BY score DESC;"""
	cursor.execute(command)
	rows = cursor.fetchall()
	scores.append(rows[:10])

	## Get the scores for multiple round mode, sorted by round number
	command = """SELECT * FROM highscores WHERE gameType = "multiple"
				 ORDER BY rounds DESC, score DESC;"""
	cursor.execute(command)
	rows = cursor.fetchall()
	scores.append(rows[:10])

	## Get the scores for single round mode, sorted by score
	command = """SELECT * FROM highscores WHERE gameType = "single"
				 ORDER BY score DESC;"""
	cursor.execute(command)
	rows = cursor.fetchall()
	scores.append(rows[:10])

	return scores

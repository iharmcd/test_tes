import pyodbc 

class Connector():
	def __init__(self, database_url):

		# Some other example server values are
		# server = 'localhost\sqlexpress' # for a named instance
		# server = 'myserver,port' # to specify an alternate port

		self.conn = pyodbc.connect(database_url)
		self.cursor = self.conn.cursor()


	def execute(self, query):
		self.cursor.execute(query)
		return self.cursor.fetchone()[0]
		
	def execute_non_select(self, query):
		self.cursor.execute(query)
		self.conn.commit()


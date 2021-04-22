from datetime import datetime
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email import encoders  
from email.mime.text import MIMEText
from email.utils import formataddr 

class Result():
	
	def __init__(self):
		self.result_file = open('results/results.log', 'w')
		self.date_time = datetime.utcnow()
		#self.result_file_html = open(f'results/{self.date_time.strftime("%Y_%m_%d_%H_%M_%S_%f")}.html', 'w')
		self.result_file_html = ''
		self.test_id = 0
		self.pass_amount = 0
		self.fail_amount = 0
		self.fail_ids = []
		self.file_name = ''

	def start_test(self, file_name):

		self.file_name = file_name

		f_name = file_name.split("\\")[-1].split(".")[0]


		self.result_file_html = open(f'results/{self.date_time.strftime("%Y_%m_%d_%H_%M_%S")}_{f_name}.html', 'a+')

		self.result_file.write(f'\n\nTesting was started {file_name}\n')
		
		self.result_file_html.write(f"""
			<html>
			<body>
			<h1>File <span style="background-color:black;color:red;">{file_name}</span> </h1>
			<h2>Testing started at {self.date_time.strftime("%m/%d/%Y, %H:%M:%S")} UTC </h2>
			<table style = "font-size:18px;border-collapse: collapse">
			<tr>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">#</th>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">test name</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">query</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">actual_result</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">expected result</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">pass/fail</th>
			  </tr>


			""")



	def start_case(self, test_name):
		self.result_file.write(f'\n\nTest case {test_name}\n')
		self.test_id += 1


	def add_pass(self, query, actual_result, expected_result, test_name):

		self.pass_amount += 1

		self.result_file.write("\nPASS. Result is '{0}' as expected"
								"\n\tQuery: '{1}'".format(actual_result, query))

		self.result_file_html.write(f"""
			  <tr style = "background-color:#00FF00;padding:5px;">
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.test_id}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{test_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{query}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">{actual_result}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">{expected_result}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">PASS</td>
			  </tr>

			""")




	def add_fail(self, query, actual_result, expected_result, test_name):

		self.fail_amount += 1

		self.fail_ids.append(self.test_id)

		self.result_file.write("\nFAIL. Result is '{0}', but expected '{1}'"
								"\n\tQuery: '{2}'".format(actual_result, expected_result, query))

		self.result_file_html.write(f"""
			  <tr style = "background-color:#FFC0CB;padding:5px;">
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.test_id}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{test_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{query}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>{actual_result}</b></td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>{expected_result}</b></td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>FAIL</b></td>
			  </tr>

			""")


	def finish_test(self):
		self.result_file_html.write(f"""

			</table>
			<h2>Testing ended at {datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")} UTC </h2>
			<h2>Total tests: {self.test_id}</h2>
			<h2>Passed: {self.pass_amount} </h2>
			<h2>Failed: {self.fail_amount} </h2>
			<h2> Failed IDs: {self.fail_ids} </h2>
			</body>
			</html>
			""")

		self.result_file.close()
		self.result_file_html.close()

		self.send_mail("ryhorpiperovich@gmail.com", 'ryhor', "FC5ihmccd14", ['iharmaccoed@gmail.com', 'ihar_makayed@epam.com'], ['ihar', 'ihar_m'], 587, self.file_name)

		self.result_file_html.close()


	def send_mail(self, sender_email, sender_name, password, receiver_emails, receiver_names, port, file_name):
		# sender_email = "ryhorpiperovich@gmail.com"
		# sender_name = 'ryhor'  
		    

		# receiver_email = 'iharmaccoed@gmail.com'
		# receiver_name = 'ihar'  
		# port = 587  
		# password = "FC5ihmccd14"

		file_msg = file_name.split("\\")[-1].split(".")[0] 
		#print(file_name)

		#file = r"results\2021_04_08_18_32_44_smoke_test.html"
		#file_msg = file.split("\\")[-1]
		file = self.result_file_html

		#print(file.name)
		email_body = open(file.name).read()

		#print(1, email_body)
		#email_body = open(file).read()
		#message= MIMEText(message, 'html')

		msg = MIMEText(email_body, 'html')
		#msg['To'] = formataddr((receiver_name, receiver_email))
		msg['From'] = formataddr((sender_name, sender_email))
		msg['Subject'] = f'Test results {file_msg}'
		#print(message)

		server = smtplib.SMTP('smtp.gmail.com', port)
		server.starttls()
		server.login(sender_email, password)

		for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
			msg['To'] = formataddr((receiver_name, receiver_email))
			server.sendmail(sender_email, receiver_email, msg.as_string())

		self.result_file_html.close()



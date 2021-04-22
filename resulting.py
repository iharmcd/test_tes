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
		self.file_name_list = []
		self.content = ''


	def start_test(self, file_name, mail_settings):

		self.file_name = file_name
		self.file_name_list.append(file_name)
		self.mail_settings = mail_settings

		f_name = file_name.split("\\")[-1].split(".")[0]


		self.result_file_html = open(f'results/{self.date_time.strftime("%Y_%m_%d_%H_%M_%S_%f")}.html', 'a+')

		self.result_file.write(f'\n\nTesting was started {file_name}\n')
		
		#self.result_file_html.write(f"""




	def start_case(self, test_name):
		self.result_file.write(f'\n\nTest case {test_name}\n')
		self.test_id += 1


	def add_pass(self, query, actual_result, expected_result, test_name, pre_processor):

		self.pass_amount += 1

		self.result_file.write("\nPASS. Result is '{0}' as expected"
								"\n\tQuery: '{1}'".format(actual_result, query))

		#self.result_file_html.write(f"""
		self.content += f"""
			  <tr style = "background-color:#00FF00;padding:5px;">
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.test_id}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.file_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{test_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{pre_processor}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{query}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">{actual_result}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">{expected_result}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse">PASS</td>
			  </tr>

			"""




	def add_fail(self, query, actual_result, expected_result, test_name, pre_processor):

		self.fail_amount += 1

		self.fail_ids.append(self.test_id)

		self.result_file.write("\nFAIL. Result is '{0}', but expected '{1}'"
								"\n\tQuery: '{2}'".format(actual_result, expected_result, query))

		#self.result_file_html.write(f"""
		self.content += f"""
			  <tr style = "background-color:#FFC0CB;padding:5px;">
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.test_id}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{self.file_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{test_name}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{pre_processor}</td>
			  	<td style = "text-align:left;border: 1px solid black;padding:10px;border-collapse: collapse">{query}</td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>{actual_result}</b></td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>{expected_result}</b></td>
			    <td style = "text-align:center;border: 1px solid black;padding:10px;border-collapse: collapse"><b>FAIL</b></td>
			  </tr>

			"""


	def finish_test(self):

		f_name = self.result_file_html.name.split('/')[-1]

		self.result_file_html.write(f"""
			<html>
			<body>
			<h1>Test results {f_name}</h1>
			<h2>Files: </h2>
			"""
			+
			
			''.join([f"""<h2> <span style = "background-color:#00ffff;">{f}</span></h2>""" for f in self.file_name_list])			

			+
			f"""
			<h2>Testing started at {self.date_time.strftime("%m/%d/%Y, %H:%M:%S")} UTC </h2>
			<h2>Testing ended at {datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")} UTC </h2>
			<h2><span style = "background-color:#00ffff;">Total tests: {self.test_id}</span></h2>
			<h2><span style = "background-color:#00FF00;">Passed: {self.pass_amount}</span> </h2>
			""" 
			+
			
			(
			f"""<h2><span style = "background-color:#FFC0CB;">Failed: {self.fail_amount} Failed IDs: {self.fail_ids}</span></h2> 
			""" if self.fail_amount > 0 else ''
			)

			+

			 f"""
			<table style = "font-size:18px;border-collapse: collapse">
			<tr>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">#</th>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">file name</th>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">test name</th>
				<th style = "border: 1px solid black;padding:10px;border-collapse: collapse">pre_processor</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">query</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">actual_result</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">expected result</th>
			    <th style = "border: 1px solid black;padding:10px;border-collapse: collapse">pass/fail</th>
			  </tr>
			{self.content}
			</table>

			</body>
			</html>
			""")


		self.result_file.close()
		self.result_file_html.close()

		#self.send_mail()



	def send_mail(self): #, sender_email, sender_name, password, receiver_emails, receiver_names, port, file_name):


		file_msg = self.file_name.split("\\")[-1].split(".")[0] 

		file = self.result_file_html

		email_body = open(file.name).read()


		msg = MIMEText(email_body, 'html')
		msg['From'] = formataddr((self.mail_settings['sender_name'], self.mail_settings['sender_email']))
		msg['Subject'] = f'Mail sent by Python from Ihar Makayed. Test results {file_msg}'

		server = smtplib.SMTP('smtp.gmail.com', self.mail_settings['port'])
		server.starttls()
		server.login(self.mail_settings['sender_email'], self.mail_settings['password'])

		for receiver_email, receiver_name in zip(self.mail_settings['receiver_emails'], self.mail_settings['receiver_names']):
			msg['To'] = formataddr((receiver_name, receiver_email))
			server.sendmail(self.mail_settings['sender_email'], receiver_email, msg.as_string())

		self.result_file_html.close()



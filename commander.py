import pika
import sys
from datetime import datetime
import subprocess

try:
	subprocess.check_output("curl -X GET localhost:7445", shell =True)
	print
except subprocess.CalledProcessError:
	print "Shock server not running"
	quit()
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, "/", credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, "/", credentials)
connection = pika.BlockingConnection(parameters)


channel.exchange_declare(exchange='commands', exchange_type='direct', durable = True)
channel.exchange_declare(exchange='confirmation', durable=True)

channel.queue_declare(queue='confirmation', durable=True)
channel.queue_bind(exchange='confirmation', queue='confirmation')

command = raw_input("Command? \n1) Take Picture/Send to Shock \n2) Quit \n3) Calibrate \n4 Restart Calibration \n> ")

n = 1

while command == "1":
	n = raw_input("Number of pictures?\n ")
	try:
		n = int(n)
		break
	except ValueError:
		print "Not a number!"
answer = False
cameras = []


while not answer:
	response = raw_input("Press 'a' to send command to all cameras, or enter camera number separated by one space \n> ")
	if response == 'a':
		answer = True
		cameras = "1 2 3 4 5 6 7".split()
	else:
		cameras =  response.split()
		for i in cameras:
			answer = True
			try:
				if int(i) not in range(1,7):
					answer = False
					print "Wrong Input: %s. Camera number must be 1,2,3,4,5, or 6. Camera nubmers must be separated by a space" % i
					break
			except ValueError:
				answer = False
				print"Wrong Input: %s. Camera number must be 1,2,3,4,5, or 6. Camera nubmers must be separated by a space" % i
				break
		if not answer:
			print "Please enter something"


def callback(ch, method, properties, body):
	global confirmations
	print "Confirmation received from %s: %s" % (properties.reply_to,  body)
	confirmations +=1

	if confirmations == count:
		channel.stop_consuming()

def calib_callback(ch, method, properties, body):
	global calibrated
	global confirmations
	print "%s: %s" % (properties.reply_to, body)
	confirmations+=1
	if body == "calibrated":
		calibrated +=1
		del cams[properties.reply_to[-1]]
	if confirmations == count:
		channel.stop_consuming()
cams ={}
for i in cameras:
	cams[i] = "camera-%s" % i

channel.confirm_delivery()


for j in range(n):
	first_run = True
	count = 0
	confirmations = 0
	time = str(datetime.now())
	calibrated = 0
	total_cams = 0
	while command == "3":
		count = 0
		delete = []
		for cam in cams:
			x =  channel.basic_publish(exchange='commands', routing_key=cams[cam], properties = pika.BasicProperties(correlation_id = time), body=str(command), mandatory=True)

        	        if x == True:
                	        count += 1
                        	print "Command %s sent to '%s'" % (command, cams[cam])
                	else:
                        	print '%s not found' % cams[cam]
				delete.append(cam)

		        channel.basic_consume(calib_callback, queue = 'confirmation', no_ack=True)
		for cam in delete:
			del cams[cam]
		if first_run:
			total_cams = count
			first_run = False
		channel.start_consuming()
		confirmations = 0 
		x = raw_input("Enter q to quit, anything else to continue. \n>")
		if calibrated == total_cams or x == "q":
			break

	if command != "3":
		for i in cameras:
			x =  channel.basic_publish(exchange='commands', routing_key='camera-%s' %i, properties = pika.BasicProperties(correlation_id = time), body=str(command), mandatory=True)

			if x == True:
				count += 1
				print "Command %s sent to 'camera-%s'" % (command, i)
			else:
				print 'camera-%s not found' % i

		channel.basic_consume(callback, queue = 'confirmation', no_ack=True)


	if count != 0:
		channel.start_consuming()

connection.close()




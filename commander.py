import pika
import sys
from datetime import datetime
import subprocess
from list_queues import list_queues

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

command = raw_input("Command? \n1) Take Picture/Send to Shock \n2) Quit \n3) Calibrate \n4) Restart Calibration \n> ")

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
	print "Avaliable queues:"
	queues = list_queues()
	cams = ""
	for q in sorted(queues):
		print "%s: %s" % (q, queues[q])
		cams += q+" "
	response = raw_input("Press 'a' to send command to all cameras, or enter camera number separated by one space \n> ")
	if response == 'a':
		answer = True
		cameras = cams.split()
	else:
		cameras =  response.split()
		for i in cameras:
			answer = True
			try:
				queues[i]
			except KeyError:
				answer = False
				print "Wrong Input: %s. Camera not found" % i
				break
		if response == "":
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
		time = str(datetime.now())
		count = 0
	
		for cam in cams:
			x =  channel.basic_publish(exchange='commands', routing_key=cams[cam], properties = pika.BasicProperties(correlation_id = time), body=str(command), mandatory=True)

        	        if x == True:
                	        count += 1
                        	print "Command %s sent to '%s'" % (command, cams[cam])
                	else:
                        	print '%s not found' % cams[cam]
				delete.append(cam)

		        channel.basic_consume(calib_callback, queue = 'confirmation', no_ack=True)

		if first_run:
			total_cams = count
			first_run = False
			if count == 0:
				break
		channel.start_consuming()
		confirmations = 0 
		x = raw_input("Enter q to quit, anything else to continue. (Note: if nothing is done after a minute, pipe will breaj) \n>")
		if calibrated == total_cams or x == "q":
			break
	if command == "4":
		calib_id = str(datetime.now())
	if command != "3":
		for i in cameras:
			x =  channel.basic_publish(exchange='commands', routing_key= cams[i], properties = pika.BasicProperties(correlation_id = time), body=str(command), mandatory=True)

			if x == True:
				count += 1
				print "Command %s sent to 'camera-%s'" % (command, i)
			else:
				print 'camera-%s not found' % i

		channel.basic_consume(callback, queue = 'confirmation', no_ack=True)


	if count != 0:
		channel.start_consuming()

connection.close()




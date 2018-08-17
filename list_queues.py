import subprocess

def list_queues():
	command = "rabbitmqctl list_queues -p '/'"

	ans = subprocess.check_output(command, shell=True)



	queues = {}
	keys = []
	for i in ans.split():
		if i.find("camera") == 0:
			n = i[-1]
			queues[n] = i
			keys.append(n)
	return queues




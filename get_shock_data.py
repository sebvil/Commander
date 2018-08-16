import requests
import json
import subprocess
import string

def query(attributes, jdata):
	query = []
	for i in range(len(jdata["data"])):
		if len(attributes) == 0:
			query.append(i)
			continue
		for att in attributes:
			try:
				x = jdata["data"][i]['attributes'][att]
				for val in attributes[att]:
					if x == val:
						query.append(i)
						print x
						break
			except KeyError:
				pass
			except TypeError:
				pass
	return query

def download(indexes, directory, jdata):
	for index in indexes:
		ans = raw_input("File name? (press enter for default)\n> ")
		id = jdata["data"][index]["id"]
		try:
			filename = jdata["data"][index]["file"]["name"]
			if ans != "":
				filename = ans
			com = "curl -X GET localhost:7445/node/%s?download --output %s/%s" % (id, directory, filename)
			subprocess.call(com, shell=True)
		except ValueError:
			print "No file to download"
			continue


def get_attribute(indexes, attribute, jdata):
	values = []
	for i in  indexes:
		try:
			value = jdata["data"][i]["attributes"][attribute]
			values.append(value)
		except KeyError:
			print "Attribute not found"
	return values


def delete_nodes(indexes, jdata):
	for i in indexes:
		id = jdata["data"][i]["id"]
		com = "curl -X DELETE localhost:7445/node/%s" % id
		subprocess.call(com, shell=True)

indexes = []
while True:
	ans = raw_input("What do you want to do? \n1)Query  \n2)Download \n3)Get attribute values \n4)Delete Nodes \n5)Quit \n>")
	try:
		int(ans)
	except ValueError:
		print "Not a number!"
		continue
	if int(ans) == 1:
		request = requests.get("http://localhost:7445/node")

		text = json.loads(request.text)


		while True:
			n = raw_input("How many attributes? (Press enter to get all nodes)\n> ")

			attributes = {}
			if n == "":
				pass
			else:
				try:
					for i in range(int(n)):
						key = raw_input("Key?\n> ")
						n = raw_input("How many values?\n> ")
						values = []
						for i in range(int(n)):
							value = raw_input("Value?\n> ")
							values.append(value)
						attributes[key] = values
				except ValueError:
					print "Not a number!"
					continue
			indexes = query(attributes, text)
			print indexes
			print "Total nodes: %i" % len(indexes)
			break

	elif int(ans) == 2:
		if indexes == []:
			print "You must query before downloading!!!"
		else:
			dir_name = raw_input("Directory name?\n> ")
			subprocess.call("mkdir %s" % dir_name, shell = True)
			download(indexes, dir_name, text)
	elif int(ans) == 3:
		if indexes == []:
                        print "You must query before searching for attributes!!!"
                else:
                        attribute = raw_input("Attribute?\n> ")
                        atts = get_attribute(indexes, attribute, text)
			print atts
	elif int(ans) == 4:
		if indexes == []:
			print "You must query before deleting!"
		else:
			answ = raw_input("Are you sure you want to delte %i nodes? (Enter y to confirm, anything else to abort)\n> " % len(indexes))
			if answ == "y":
				delete_nodes(indexes, text)
				print "\n%s nodes deleted" % len(indexes)
	elif int(ans) == 5:
		break
	else:
		print "Command not found"



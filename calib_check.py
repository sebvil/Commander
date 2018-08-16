import json
import requests
import cv2
import subprocess
import sys
import glob

file, n = sys.argv
subprocess.call("rm ~/Calib/*", shell=True)
def show_ims(n_cams):
	req = requests.get("http://localhost:7445/node")
	data = json.loads(req.text)
	x = 0
	y = 0
	for i in range(n_cams):
		id = data["data"][i]["id"]
		file = data["data"][i]["file"]["name"]
		com = "curl -X GET localhost:7445/node/%s?download --output ~/Calib/%s" % (id, file)
		subprocess.call(com, shell=True)

	pics = glob.glob("/home/sebastian/Calib/*.jpg")
	print pics
	for i in range(n_cams):
		img = cv2.imread(pics[i])
		cv2.namedWindow(pics[i], cv2.WINDOW_NORMAL)
		cv2.moveWindow(pics[i], x ,y)
		x+=600
		if (i+1) % 3 ==0:
			x = 0 
			y += 500
		cv2.resizeWindow(pics[i],  600, 500)

		cv2.imshow(pics[i], img)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

show_ims(int(n))

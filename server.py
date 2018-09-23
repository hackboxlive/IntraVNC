import socket
import cv2
from scipy.misc import imresize
import numpy as np
import pyscreenshot
import imutils
from cStringIO import StringIO



def sendNumpy(c, image):
		if not isinstance(image, np.ndarray):
			print 'not a valid numpy image'
			return
		f = StringIO()
		np.savez_compressed(f, frame=image)
		f.seek(0)
		out = f.read()
		val = "{0}:".format(len(f.getvalue()))  # prepend length of array
		out = val + out
		try:
			c.sendall(out)
		except Exception:
			exit()
		print 'image sent'


if __name__ == '__main__':
	host = ''
	port = 5001

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))

	s.listen(1)
	print("Now listening: ")
	c, addr = s.accept()
	print("Connection recieved: " + str(addr))

	cap = cv2.VideoCapture(0)

	while True:
		data = c.recv(1024)
		if not data:
			break
		print("From Connected user: " + str(data))
		image = pyscreenshot.grab()
		image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
		frame_resize = imresize(image, .5)
		print("Sending: ")
		sendNumpy(c, frame_resize)
	c.close()
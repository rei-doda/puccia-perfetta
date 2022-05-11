from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import *
import os


class PusherDrive:
	"""This class is used to load jpg images into a specific drive folder"""

	def __init__(self, id_fold: str, path_creds: str, path_image: str):
		"""The constructor accepts 3 arguments: the identifying string of the drive folder,
		the path where there are the api credentials for google drive and
		the path where there are the images to be loaded"""
		if type(id_fold) != str:
			raise ValueError("The id_fold argument must be a string")
		if type(path_creds) != str:
			raise ValueError("The path_creds must ba a string")
		if type(path_image) != str:
			raise ValueError("The path_image argument must be a string")
		self.id_fold = id_fold
		self.path_image = path_image
		self.path_creds = path_creds
		#self.curr_dir = os.getcwd()
		#os.chdir(self.path_creds)
		self.gauth = GoogleAuth()
		self.drive = GoogleDrive(self.gauth)
		#os.chdir(self.curr_dir)

	def push(self):
		"""This method uploads images to google drive, it does not accept any arguments"""
		prev_image = ""
		#print(os.getcwd())
		for image in os.listdir(self.path_image):
			if image.endswith(".jpg"):
				try:
					gfile = self.drive.CreateFile({'title': image[:-4], 'parents': [{'id': self.id_fold}]})
					gfile.SetContentFile(os.path.join(self.path_image, image))
					gfile.Upload()
					print("[" + image + " loaded on drive]")
					gfile.content.close()
				except FileNotUploadedError:
					print("")
					print("OPS, " + image + " not loaded on drive")
			if prev_image != "":
				os.remove(os.path.join(self.path_image, prev_image))
				prev_image = ""
			else:
				prev_image = image
		os.remove(os.path.join(self.path_image, prev_image))

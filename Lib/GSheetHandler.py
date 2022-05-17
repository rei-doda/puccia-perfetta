import gspread
from oauth2client.service_account import ServiceAccountCredentials


def clean_list(worksheets: list, token_str: str):
	"""This function is used to clean up a list of strings of all those strings that do not have the same initial
	characters as a string passed as a parameter. This function accepts two parameters: a list and a string"""
	if type(worksheets) != list:
		raise ValueError("The worksheets parameter must be a list")
	if type(token_str) != str:
		raise ValueError("The token_str parameter must be a string")
	cleaned_list = []
	for sheet in worksheets:
		if sheet.title[0:len(token_str)] == token_str:
			cleaned_list.append(sheet)
	return len(cleaned_list)


class GSheetHandler:
	"""This class is used to manage, specifically write data on the google spreadsheet"""
	def __init__(self, path: str, sheet: str):
		"""The constructor is used to initialize the connection with the spreadsheet and all data. It accepts two
		parameters: one is the path to the credentials file and the other is the google sheet name"""
		if type(path) != str:
			raise ValueError("The path parameter must be a string")
		if type(sheet) != str:
			raise ValueError("The sheet parameter must be a string")
		self.intest = ["TimeStamp", "PucceBuone", "PuccieBruciate", "PucceTotali", "NumeroPucceBruciate"]
		self.rows = 1
		self.cols = 5
		self.scope = ["https://spreadsheets.google.com/feeds"]
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(path)
		self.client = gspread.authorize(self.creds)
		self.file = self.client.open(sheet)
		self.list_worksheets = self.file.worksheets()
		self.samplesheet = "Puccia_Sheet"
		self.num_used_sheet = clean_list(self.list_worksheets, self.samplesheet)
		self.temp_dats = [0, 0]
		if self.num_used_sheet == 0:
			self.file.add_worksheet(title=self.samplesheet + "1", rows=self.rows, cols=self.cols)
			self.current_sheet = self.file.worksheet(self.samplesheet + "1")
			self.num_used_sheet += 1
			self.current_sheet.format("A:E", {
				"horizontalAlignment": "CENTER",
				"textFormat": {"bold": False}
				})
			self.current_sheet.format("A1:E1", {
				'textFormat': {'bold': True}
				})
			self.count_row = 1
			self.current_sheet.insert_row(self.intest, self.count_row)
			self.count_row += 1
			self.old_dats = [0, 0]
			print("")
			print("[I've added, formatted and initialized a new sheet]")
		else:
			self.current_sheet = self.file.worksheet(self.samplesheet + str(self.num_used_sheet))
			self.num_used_sheet += 1
			try:
				if self.current_sheet.row_values(1) != self.intest:
					self.current_sheet.format("A:E", {
						"horizontalAlignment": "CENTER",
						"textFormat": {"bold": False}
					})
					self.current_sheet.format("A1:E1", {
						'textFormat': {'bold': True}
					})
					self.count_row = 1
					self.current_sheet.insert_row(self.intest, self.count_row)
					self.count_row += 1
					self.old_dats = [0, 0]
					print("")
					print("[I've formatted and initialized a new sheet]")
				else:
					self.count_row = len(self.current_sheet.get_all_records()) + 2
					try:
						self.old_dats = [int(self.current_sheet.acell("D" + str(self.count_row - 1)).value),
											int(self.current_sheet.acell("E" + str(self.count_row - 1)).value)]
					except TypeError:
						self.old_dats = [0, 0]
					except ValueError:
						self.old_dats = [0, 0]
			except IndexError:
				self.current_sheet.format("A:E", {
					"horizontalAlignment": "CENTER",
					"textFormat": {"bold": False}
				})
				self.current_sheet.format("A1:E1", {
					'textFormat': {'bold': True}
				})
				self.count_row = 1
				self.current_sheet.insert_row(self.intest, self.count_row)
				self.count_row += 1
				self.old_dats = [0, 0]
				print("")
				print("[I've formatted and initialized a new sheet]")

	def insert_dats(self, dats: list):
		"""This server method for entering data on the sheet accepts a list as a parameter"""
		if type(dats) != list:
			raise ValueError("The dats parameter must be a list")
		if len(dats) != 3:
			raise ValueError("The dats list parameter must have 3 elements")
		if type(dats[0]) != str:
			raise ValueError("")
		if type(dats[1]) != int and type(dats[2]) != int:
			raise ValueError("The dats parameter must have 2 numbers")
		if (len(self.current_sheet.get_all_values())) * 5 == 4000000:
			self.file.add_worksheet(title=self.samplesheet + str(self.num_used_sheet), rows=self.rows,  cols=self.cols)
			self.current_sheet = self.file.worksheet(self.samplesheet + str(self.num_used_sheet))
			self.num_used_sheet += 1
			self.current_sheet.format("A:E", {
				"horizontalAlignment": "CENTER",
				"textFormat": {"bold": False}
			})
			self.current_sheet.format("A1:E1", {
				'textFormat': {'bold': True},
			})
			self.count_row = 1
			self.current_sheet.insert_row(self.intest, self.count_row)
			self.count_row += 1
			good = dats[1] - self.temp_dats[0]
			n_good = dats[2] - self.temp_dats[1]
			tot = good + self.old_dats[0] + n_good
			tot_b = n_good + self.old_dats[1]
			self.old_dats[0] = tot
			self.old_dats[1] = tot_b
			self.temp_dats[0] = good
			self.temp_dats[1] = n_good
			self.current_sheet.insert_row([dats[0], good, n_good, tot, tot_b], self.count_row)
			self.count_row += 1
			print("")
			print(f"[{dats[0]} --- I've written on the file]")
		else:
			good = dats[1] - self.temp_dats[0]
			n_good = dats[2] - self.temp_dats[1]
			tot = good + self.old_dats[0] + n_good
			tot_b = n_good + self.old_dats[1]
			self.old_dats[0] = tot
			self.old_dats[1] = tot_b
			self.temp_dats[0] = good
			self.temp_dats[1] = n_good
			self.current_sheet.insert_row([dats[0], good, n_good, tot, tot_b], self.count_row)
			self.count_row += 1
			print("")
			print(f"[{dats[0]} --- I've written on the file]")

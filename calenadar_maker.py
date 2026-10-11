import pandas as pd
import numpy as np
import datetime

#define possible range of dates
lessons = (datetime.datetime(2026, 10, 12), datetime.datetime(2027, 2, 28))
christmas = (datetime.datetime(2026, 12, 21), datetime.datetime(2027, 1, 3))
lesson_dates = [lessons[0] + datetime.timedelta(days=x) for x in range((lessons[1]-lessons[0]).days +1)]
#print(lesson_dates)

class Event:
	
	def __init__(self, name, start_date, start_time=None, end_date=None, end_time=None, all_day=True, desc=None, location=None, private=True):
		self.name = name
		self.start_date = start_date
		self.start_time = start_time
		self.end_date = end_date
		self.end_time = end_time
		self.all_day = all_day
		self.desc = desc
		self.location = location
		self.private = private

	def add_event(self, calendar):
		if self.start_date:
			self.start_date_str = str(self.start_date.year)+"-"+str(self.start_date.month)+"-"+str(self.start_date.day)
		else:
			self.start_date_str = ""
		if self.end_date:
			self.end_date_str = str(self.end_date.year)+"-"+str(self.end_date.month)+"-"+str(self.end_date.day)
		else:
			self.end_date_str = ""
		event_data = [self.name, self.start_date_str, self.start_time, self.end_date_str, self.end_time, str(self.all_day), str(self.desc), str(self.location), str(self.private)]
		calendar.df.loc[len(calendar.df)] = event_data
		return 
	

class Calendar:
	
	def __init__(self, file_name):
		self.df = pd.DataFrame(data={"name":[0], "start date":[0], "start time":[0], "end date":[0], "end time":[0], "all day":[0], "description":[0], "location":[0], "private":[0]}, columns=["Subject", "Start Date", "Start Time", "End Date", "End Time", "All Day Event", "Description", "Location", "Private"])
		self.file_name = file_name
		return
	
	def save(self):
		self.df.to_csv(self.file_name+".csv", sep=",", index=False)
		return



def create_event_list(event_data, start, end, period, calendar):
	#event data: name, start time, length in days, end time, all day, description, location, private
	print([i for i in lesson_dates[lesson_dates.index(start):lesson_dates.index(end):period] if ((i < christmas[0]) or (i > christmas[1]))])
	event_list = [Event(name=event_data[0], start_date=i, start_time=event_data[1], end_date=i+datetime.timedelta(days=int(event_data[2])), end_time=event_data[3], all_day=event_data[4], desc=event_data[5], location=event_data[6], private=event_data[7]) for i in lesson_dates[lesson_dates.index(start):lesson_dates.index(end):period] if ((i < christmas[0]) or (i > christmas[1]))] 
	for i in event_list:
		i.add_event(calendar)
	print(calendar.df)

def main():
	run = 1
	while run:
		if bool(input("Do you want to leave? Enter nothing for no:")):
			run = 0
			return 1
		try:
			name = input("Please input calendar name: ")
			break
		except:
			print("An error occured (invalid input). Please try again.")
			continue
	# ~ name = "test_calendar"
	calendar = Calendar(name)
	run = 1
	# ~ event_data = ["test event", "10:00", 0, "11:40", False, "This is a test.", "Oz", True]
	# ~ start_date = datetime.datetime.strptime("20.10.2026", "%d.%m.%Y") 
	# ~ end_date = datetime.datetime.strptime("13.11.2026", "%d.%m.%Y")
	# ~ period = 4
	# ~ create_event_list(event_data, start_date, end_date, period, calendar)
	# ~ calendar.save()
	# ~ print("Event has been saved!")
	while run:
		if bool(input("Do you want to leave? Enter nothing for no:")):
			run = 0
			return 1
		try:
			event_data = []
			event_data.append(input("Event name: "))
			start_date = datetime.datetime.strptime(input("First date (DD.MM.YYYY): "), "%d.%m.%Y")
			event_data.append(input("Begin (hh:mm): "))
			end_date = datetime.datetime.strptime(input("Last date (DD.MM.YYYY): "), "%d.%m.%Y")
			event_data.append(input("Length in days: "))
			event_data.append(input("End (hh:mm): "))
			event_data.append(input("All day (Press ONLY enter for False): "))
			event_data.append(input("Description: "))
			event_data.append(input("Location: "))
			event_data.append(not bool(input("Private (Press ONLY enter for True): ")))
			period = int(input("Period (in days): "))
			do_save = not bool(input("Save event? (Hit enter if yes) "))
		except:
			print("An error occured.")
			continue
		if do_save:
			create_event_list(event_data, start_date, end_date, period, calendar)
			calendar.save()
			print("Event has been saved!")
		else:
			continue
		continue
		
	return 0
	
	

if __name__=="__main__":
	exit_code = main()
	print("--------------------------------------------")
	print("Exit code: ", exit_code)

	
	
	

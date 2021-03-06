import random
import urllib2
import csv
import time
import argparse 

default_url = "http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv"

parser = argparse.ArgumentParser(description = 'Simulate Server Requests for single or multiple servers')
parser.add_argument("--servers",type = int, help = "Number of Servers to Simulate")
parser.add_argument("--file", type = str, help = "URL of File to Process")
args = parser.parse_args()
num_servers = args.servers
num_servers = 100
## Adding this section so it's easier to run for this assignment.
if args.file is None:
	url = default_url
else:
	url = args.file
	

# Completed implementation of a queue ADT
class Queue:
	def __init__(self):
		self.items = []
	def is_empty(self):
		return self.items == []
	def enqueue(self, item):
		self.items.insert(0,item)
	def dequeue(self):
		return self.items.pop()
	def size(self):
		return len(self.items)

class Server:
	def __init__(self):
		self.current_task = None
		self.time_remaining = 0
		self.queue = Queue()
	def tick(self):
		if self.current_task != None:
			self.time_remaining = self.time_remaining - 1
			if self.time_remaining <= 0:
				self.current_task = None
	def busy(self):
		if self.current_task != None:
			return True
		else:
			return False
	def start_next(self, new_task):
		self.current_task = new_task
		self.time_remaining = new_task.get_length()
	
	
	

class Request:
	def __init__(self,time,length):
		self.timestamp = time
		self.length = int(length)
	def get_stamp(self):
		return self.timestamp
	def get_length(self):
		return self.length
	def wait_time(self,current_time):
		return current_time - self.timestamp
		
def simulateOneServer(filename):
	data = urllib2.urlopen(filename)
	listdata = list(csv.reader(data))
	t_list = []
# Get first column converted in integer, and make a new list to get max value
	for row in listdata:
		t_list.append(int(row[0]))
		row[0] = int(row[0])
		row[2] = int(row[2])
	
	t_max = max(t_list)	
	
	lab_server = Server()
	request_queue = Queue()
	waiting_times = []

	t = 0
	i = 0
	
	while (i < len(listdata)):
		if(listdata[i][0] == t):
			#Enqueue
			#i++
			current_time = time.time()
			task = Request(current_time,listdata[i][2])
			request_queue.enqueue(task)
			i = i+1
		else:
			lab_server.tick()
			t = t + 1
		if((not lab_server.busy()) and (not request_queue.is_empty())):
			new_task = request_queue.dequeue()
			current_time = time.time()
			waiting_times.append(new_task.wait_time(current_time))
			lab_server.start_next(new_task)
	avg_wait_time = sum(waiting_times)/len(waiting_times)
	print "Average Wait Time for a single server:"
	print avg_wait_time, "seconds"
	print avg_wait_time * 1000, "milliseconds"
	print avg_wait_time * 1000000, "microseconds"
	print "Number of requests:", len(waiting_times)
	
def simulateManyServers(filename,num_servers):
	data = urllib2.urlopen(filename)
	listdata = list(csv.reader(data))
	t_list = []
# Get first column converted in integer, and make a new list to get max value
	for row in listdata:
		t_list.append(int(row[0]))
		row[0] = int(row[0])
		row[2] = int(row[2])
	
	t_max = max(t_list)	
	server_list = []
	# Loop through num_servers to create list of server instances
	for i in range(num_servers):
		server_list.append(Server())
	
	# Attempting to give each server its own queue - request_queue = Queue()
	waiting_times = []

	t = 0
	i = 0
	
	while (i < len(listdata)):
		if(listdata[i][0] == t):
			#Enqueue
			#i++
			current_time = time.time()
			task = Request(current_time,listdata[i][2])
			if i == 0:
				server_iter = 0
			else:
				server_iter = i % num_servers # Current round-robin number
			
			server_list[server_iter].queue.enqueue(task)
			i = i+1
		else:
			for row in server_list:
				row.tick()
			t = t + 1
		for lab_server in server_list:
			if((not lab_server.busy()) and (not lab_server.queue.is_empty())):
				new_task = lab_server.queue.dequeue()
				current_time = time.time()
				waiting_times.append(new_task.wait_time(current_time))
				lab_server.start_next(new_task)
	avg_wait_time = sum(waiting_times)/len(waiting_times)
	print "Average Wait Time for", num_servers, "servers"
	print avg_wait_time, "seconds"
	print avg_wait_time * 1000, "milliseconds"
	print avg_wait_time * 1000000, "microseconds"
	print "Number of requests:", len(waiting_times)
	
'''def simulateManyServersOneQueue(filename,num_servers):
	data = urllib2.urlopen(filename)
	listdata = list(csv.reader(data))
	t_list = []
# Get first column converted in integer, and make a new list to get max value
	for row in listdata:
		t_list.append(int(row[0]))
		row[0] = int(row[0])
		row[2] = int(row[2])
	
	t_max = max(t_list)	
	server_list = []
	# Loop through num_servers to create list of server instances
	for i in range(num_servers):
		server_list.append(Server())
		
	request_queue = Queue()
	waiting_times = []

	t = 0
	i = 0
	
	while (i < len(listdata)):
		if(listdata[i][0] == t):
			#Enqueue
			#i++
			current_time = time.time()
			task = Request(current_time,listdata[i][2])
			request_queue.enqueue(task)
			i = i+1
		else:
			for row in server_list:
				row.tick()
			t = t + 1
		for lab_server in server_list:
			if((not lab_server.busy()) and (not request_queue.is_empty())):
				new_task = request_queue.dequeue()
				current_time = time.time()
				waiting_times.append(new_task.wait_time(current_time))
				lab_server.start_next(new_task)
	avg_wait_time = sum(waiting_times)/len(waiting_times)
	print "Average Wait Time for", num_servers, "servers"
	print avg_wait_time, "seconds"
	print avg_wait_time * 1000, "milliseconds"
	print avg_wait_time * 1000000, "microseconds"
	print "Number of requests:", len(waiting_times)
		'''
if num_servers == 1 or num_servers is None:
	simulateOneServer(url)
else:
	print "Many Queues:"
	simulateManyServers(url,num_servers)
	'''print "One Queue:"
	simulateManyServersOneQueue(url,num_servers)

	'''

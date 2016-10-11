# pypidplot

import argparse
import datetime 
import numpy as np 
import plotly
import plotly.plotly as py  
import plotly.tools as tls   
import plotly.graph_objs as go
import psutil
import sys
import time 


# config
DELAY = .1
MAXPOINTS = 240


# class for streaming metrics on single process (PID)
class PIDStream(object):

	def __init__(self, pid, label):
		self.pid = pid
		self.label = label.replace(' ','-')
		self.p = psutil.Process(self.pid)

	def value(self):
		# return (cpu percent, memory percent) tuple
		return (self.p.cpu_percent(), self.p.memory_percent())


class SystemStream(object):

	def __init__(self, label="system"):
		self.pid = "system"
		self.label = "system"
		
	def value(self):
		return (psutil.cpu_percent(), psutil.virtual_memory().percent)


class Stream(object):

	def __init__(self, metric, maxpoints=MAXPOINTS, delay=DELAY):

		# capture metric class
		self.metric = metric

		# streaming params
		self.delay = delay
		self.stream_ids = tls.get_credentials_file()['stream_ids']
		self.maxpoints = maxpoints
		self.stream_dicts = {
			'cpu':{
				'token':self.stream_ids[0],
				'maxpoints':self.maxpoints
			},
			'memory':{
				'token':self.stream_ids[1],
				'maxpoints':self.maxpoints
			}
		}


	def stream(self):

		# Initialize traces
		cpu = go.Scatter(
			x=[],
			y=[],
			mode='lines',
			stream=self.stream_dicts['cpu']
		)

		memory = go.Scatter(
			x=[],
			y=[],
			mode='lines',
			stream=self.stream_dicts['memory']
		)

		data = go.Data([cpu,memory])

		# Add title to layout object
		layout = go.Layout(title='Plot for process %s, %s' % (self.metric.pid, self.metric.label))

		# Make a figure object
		fig = go.Figure(data=data, layout=layout)

		# Send fig to Plotly, initialize streaming plot, open new tab
		py.iplot(fig, filename='pypidplot-%s' % self.metric.label)

		# We will provide the stream link object the same token that's associated with the trace we wish to stream to
		cpu_stream = py.Stream(self.stream_dicts['cpu']['token'])
		memory_stream = py.Stream(self.stream_dicts['memory']['token'])

		# We then open a connection
		cpu_stream.open()
		memory_stream.open()

		# Delay start of stream by 5 sec (time to switch tabs)
		time.sleep(5) 

		while True:
			
			# Current time on x-axis, random numbers on y-axis
			x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
				
			# Send data to your plot
			cpu_stream.write(dict(x=x, y=self.metric.value()[0]))
			memory_stream.write(dict(x=x, y=self.metric.value()[1]))  
			
			time.sleep(self.delay)  # plot a point every second    
		
		# Close the stream when done plotting
		cpu_stream.close()
		memory_stream.close()


# main loop
def main():

	parser = argparse.ArgumentParser(description='Plot CPU and Memory for given process PID.')
	parser.add_argument('pid', metavar='12345', type=int, nargs='+', help='system process pid')
	parser.add_argument('label', metavar='image_server', type=str, nargs='+', help='name for plot')
	args = parser.parse_args()

	# DEBUG
	# print args.pid, args.label

	#metric = PIDStream(args.pid[0], args.label[0])
	metric = SystemStream()
	streamer = Stream(metric)
	streamer.stream()


# go
if __name__ == '__main__':
	main()













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
		return (p.cpu_percent(), p.memory_percent())


class Stream(object):

	def __init__(self, metric, maxpoints=MAXPOINTS, delay=DELAY):

		# capture metric class
		self.metric = metric

		# streaming params
		self.delay = delay
		self.stream_ids = tls.get_credentials_file()['stream_ids']
		self.stream_id = self.stream_ids[0]
		self.maxpoints = maxpoints
		self.stream_dict = {
			'token':self.stream_id,
			'maxpoints': self.maxpoints
		}

	def stream(self):

		# Initialize trace of streaming plot by embedding the unique stream_id
		trace1 = go.Scatter(
			x=[],
			y=[],
			mode='lines+markers',
			stream=self.stream_dict  # (!) embed stream id, 1 per trace
		)

		data = go.Data([trace1])

		# Add title to layout object
		layout = go.Layout(title='Plot for process %s, %s' % (self.metric.pid, self.metric.label))

		# Make a figure object
		fig = go.Figure(data=data, layout=layout)

		# Send fig to Plotly, initialize streaming plot, open new tab
		py.iplot(fig, filename='pypidplot-%s' % self.metric.label)

		# We will provide the stream link object the same token that's associated with the trace we wish to stream to
		s = py.Stream(self.stream_id)

		# We then open a connection
		s.open()

		# Delay start of stream by 5 sec (time to switch tabs)
		time.sleep(5) 

		while True:
			
			# Current time on x-axis, random numbers on y-axis
			x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
			y = self.metric.value() 
				
			# Send data to your plot
			s.write(dict(x=x, y=y))  
			
			#     Write numbers to stream to append current data on plot,
			#     write lists to overwrite existing data on plot
					
			time.sleep(self.delay)  # plot a point every second    
		# Close the stream when done plotting
		s.close()


# main loop
def main():

	parser = argparse.ArgumentParser(description='Plot CPU and Memory for given process PID.')
	parser.add_argument('pid', metavar='12345', type=int, nargs='+', help='system process pid')
	parser.add_argument('label', metavar='image_server', type=str, nargs='+', help='name for plot')
	args = parser.parse_args()

	# DEBUG
	# print args.pid, args.label

	metric = PIDStream(args.pid[0], args.label[0])
	streamer = Stream(metric)
	streamer.stream()


# go
if __name__ == '__main__':
	main()













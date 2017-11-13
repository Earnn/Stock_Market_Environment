import data_set as np
env= ds.Env("SIRI")
num_episode = 1000
for i in range(num_episode):
	s=env.reset()
	done = False
	while done == False:
		# select action
		# step
		# update Bellman's equation
	# Evaluate  total score
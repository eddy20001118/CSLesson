import os
simulation_params = {
	'1.Mass':0.0,
	'2.Length':0.0,
	'3.Drag coefficient':0.0,
	'4.Time step': 0.0,
	'5.Initial angle':0.0,
	'6.Total time':0.0
}

simulation_vars = {
	'Tan(g)': 0.0,
	'Drag force': 0.0,
	'Acceleration': 0.0,
	'Velocity': 0.0,
	'Distance': 0.0,
	'Angle': 0.0,
	'Time': 0.0,
}

def get_float(hint,default):
	try:
		return float(input(hint+': '))
	except ValueError:
		print('Invaild input')
		return default
	
def print_dict(user_dict,keys):
	for i in range(len(keys)):
		print(keys[i]+': ',user_dict[keys[i]])
				
def main():
	os.system('clear')
	user_input = ''
	sim_params_keys = ['1.Mass','2.Length','3.Drag coefficient','4.Time step','5.Initial angle','6.Total time']
	print_dict(simulation_params,sim_params_keys)
	print()
	
	for j in sim_params_keys:
		simulation_params[j] = get_float(j,10)
		os.system('clear')
		print_dict(simulation_params,sim_params_keys)
		print()
	
	while user_input != 'q':
		os.system('clear')
		print_dict(simulation_params,sim_params_keys)
		print()
		user_input = input('Editing params, q to quit: ')
		try:
			index = int(user_input) - 1
			if index >= 0 and index < len(sim_params_keys):
				simulation_params[sim_params_keys[index]] = get_float(sim_params_keys[index],10)
		except ValueError:
			if user_input != 'q':
				print('Invaild input, try again')

if __name__ == '__main__':
	main()	

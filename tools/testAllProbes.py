from time import sleep
from os import popen, path

t_id1 = "28-0516a02c71ff"
t_hall = "28-0516a06388ff"
t_door = "28-0516a3734cff"

t_attic = "28-0516a069b0ff"

def getTemp(w1id = t_id1):
	try:
		cmd = "cat /sys/devices/w1_bus_master1/"+w1id+"/w1_slave"
		result = popen(cmd).read()
		result = result[result.find('t=')+2:]
		t = int(result)/1000.0
		#C to F
		t *= 1.8
		t += 32
		return t
	except Exception, e:
		return -1


def main():
	print 'main:', getTemp(t_id1)
	sleep(15)
	print 'hall:', getTemp(t_hall)
	sleep(15)
	print 'door:', getTemp(t_door)
	sleep(15)
	print 'attic:', getTemp(t_attic)

if __name__ == '__main__':
	main()

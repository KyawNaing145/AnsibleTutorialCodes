#Update01#
import time
import myparamiko
import threading

def backup(router):
    client = myparamiko.connect(**router)
    shell = myparamiko.get_shell(client)

    myparamiko.send_command(shell, 'terminal length 0')
    myparamiko.send_command(shell, 'sh run')
    time.sleep(3)
    output = myparamiko.show(shell)
    # print(output)
    output_list = output.splitlines()
    # tlang = len(output_list)
    # print(output_list)
    # print(tlang)
    output = '\n'.join(output_list)

    ##Writing to a file##
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    file_name = f'C:\\Users\\LENOVO\\OneDrive\\Documents\\{router["server_ip"]}_{year}-{month}-{day}-{hour}-{minute}.txt'
    with open(file_name, 'w') as f:
        f.write(output)

    myparamiko.closed(client)

#####################Begin########################

router1 = {'server_ip': '192.168.56.111', 'server_port': '22', 'user': 'admin', 'passwd': 'cisco'}
router2 = {'server_ip': '192.168.56.102', 'server_port': '22', 'user': 'admin', 'passwd': 'cisco'}
router3 = {'server_ip': '192.168.56.103', 'server_port': '22', 'user': 'admin', 'passwd': 'cisco'}
routers = [router1,router2,router3]

thread = list()

for router in routers:
    th = threading.Thread(target=backup, args=(router,))
    thread.append(th)

for thr in thread:
    thr.start()

for thr in thread:
    thr.join()

import subprocess
 

new_ip = subprocess.Popen("curl -s icanhazip.com", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()

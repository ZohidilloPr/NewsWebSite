import os
print("RELOADING START")
os.system("sudo systemctl daemond-reload")
print("#########")
os.system("clear")
os.system("sudo systemctl restart news.service news.socket")
print("######################")
os.system("clear")
os.system("sudo nginx -t")
print("#####################################")
os.system("clear")
os.system("sudo systemctl restart nginx")
print("######################################################")
print("RELOADING FINISHED")
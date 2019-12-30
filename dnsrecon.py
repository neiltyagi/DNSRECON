#!/usr/bin/python3
import subprocess
import re
import colorama
from colorama import Fore, Style
import os
import sys


opfile=open("output.txt","w")

def fwdlookup(query):
	MyOut = subprocess.Popen(["host",query],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()
	string=stdout.decode('utf-8')
	found=re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',string)

	if found:
		temp="[+]DNS RECORD FOUND "+query+" "+found.group()
		print(Fore.GREEN+temp)
		print(Style.RESET_ALL,end='')
		opfile.write(temp+'\n')
	else:
		temp="[-]NXDOMAIN "+query
		print(Fore.RED+temp)
		print(Style.RESET_ALL,end='')
		opfile.write(temp+'\n')

def revlookup(ip):
	MyOut=subprocess.Popen(["host",ip],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	stdout,stderr = MyOut.communicate()
	string=stdout.decode('utf-8')
	a=string.split()
	if re.search(r'NXDOMAIN',a[-1]):
		temp="[-]NXDOMAIN " + ip
		print(Fore.RED+temp)
		print(Style.RESET_ALL,end='')
		opfile.write(temp+'\n')

	else:
		temp="[+]FOUND "+ip+" "+a[-1]
		print(Fore.GREEN+temp)
		print(Style.RESET_ALL,end='')
		opfile.write(temp+'\n')




def main():
	option=input("option>")
	if option.isdigit() :
		if int(option)==1:
			print("ENTER DOMAIN NAME")
			print("EXAMPLE FORMAT checkpoint.com")
			print("================================")
			domain=input("domain>")
			f=open("subdomain.txt","r")

			subdomain=f.readlines()
			for i in subdomain:
				query=i.strip("\n")+"."+domain
				try:
					fwdlookup(query)
				except KeyboardInterrupt:
					print(Fore.YELLOW)
					print("user exit request....exiting now ...check the report at cwd/output.txt")
					print(Style.RESET_ALL)
					f.close()
					opfile.close()
					sys.exit()

				except:
					print("some error occured moving on to next iteration")
			f.close()

		if int(option)==2:
			print("ENTER CLASS C NETWORK ADDRESS")
			print("example X.X.X.0")
			print("===============================")
			subnet=input("subnet>")
			for i in range(1,256):
				ip=re.sub(r"0\Z",str(i),subnet)
				try:
					revlookup(ip)
				except KeyboardInterrupt:
					print(Fore.YELLOW)
					print("user exit request....exiting now ...check the report at cwd/output.txt")
					print(Style.RESET_ALL)
					opfile.close()
					sys.exit()
				except:
					print("some error occured moving on to next iteration")


		else:
			print("Invalid Argumnet")
	else:
		print("Invalid Argument")


def banner():
	print(Fore.RED)
	print("""		██████╗ ███╗   ██╗███████╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
		██╔══██╗████╗  ██║██╔════╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
		██║  ██║██╔██╗ ██║███████╗    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
		██║  ██║██║╚██╗██║╚════██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
		██████╔╝██║ ╚████║███████║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
		╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝""")
	print("		REPORT ERROR AT tyagi.neil73@gmail.com")
	print(Style.RESET_ALL,end='')
	print(Fore.YELLOW)
	print("		DEFAULT OUTPUT LOG LOCATION IS CWD/OUTPUT.txt")
	print("		1. FOR FORWARD LOOKUP")
	print("		2. FOR REVERSE LOOKUP")
	print(Style.RESET_ALL,end='')


if __name__=="__main__":
	banner()
	main()
	opfile.close()

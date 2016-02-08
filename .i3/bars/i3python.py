#!/usr/bin/python2
# coding: utf-8

#TODO facebook notifications?

import json
from sys import stdout
from time import sleep
from subprocess import check_output as o
from os.path import expanduser



# Needed by i3bar
print '{"version":1}'
print '['
print '[]'


class Base:

	def __init__(self):
		# Initial variables and flags
		self.is_muted = 0
		self.spacer = '    '
		self.final = []


		# Colors.
		# normal - normal text. ie, 'unread', 'signal', etc.
		# attn - needs attention. ie, if there's a new mail.
		# inactive - very dim, mimic'ing a greyedout effect. (supposed to be slightly brighter than bar's bg color)
		self.color_normal		= "#4C9A9A"
		self.color_attn		= "#ae144b"
		self.color_inactive	= "#666666"

		# SSH colors.
		# The keys should be the same as the 'Host' in your ~/.ssh/config
		self.ssh_colors = {
			'linode'	:	'#FFFF9D',
			'netbook'	:	'#48a16f'
		}



		# The following is for me since i ssh into multiple machines.
		# This functionality will be commented out by default, but feel
		# free to uncomment it if you also want to use it.
		# How it works and what it does:
		# Assuming your ~/.ssh/config file looks like this
		#
		# 	Host Linode
		#	HostName 123.456.78.90
		#	User katsh
		#
		# We will use this to list open SSH connections in our bar, in the ssh colors we
		# defined above.
		# Why did I do this? two reasons:
		# 1 - Sometimes I have a ton of terminals (with tabs) open, and am afraid i sometimes
		# 		leave the computer unattended with a connection open
		# 2 - I made it so each box i ssh into, the bash is displayed in a different color.
		#		By listing connections by colors on i3bar, it helps me identify which ssh session is which
		#
		try:
			self.conns = {}
			f = open (expanduser("~/.ssh/config"))
			h = ''
			i = ''
			for line in f:
				if 'Host ' in line:
					h = line.split(' ')[-1].strip()
				elif 'HostName ' in line:
					i = line.split(' ')[-1].strip()
				if h and i:
					self.conns[i] = h
					h = ''
					i = ''
			f.close()
		except:
			pass



	def date(self):
		date = o(["date", "+%b %e %% %I:%M "])

		self.final.append({
			"name" : "date",
			"full_text" : date,
			"color" : self.color_normal
		})


	def Wireless(self):
		try:
			w = o(["iwconfig wlp0s29f7u1 | grep Quality"], shell=True)
			s =  w.split("/")[0][-2:]
			r = "signal: "
			s = int(s)
			if s == 0:
				r += "offline"
			if 0 < s <= 20:
				r += "bad"
			if 20 < s <= 46:
				r += "ok"
			if 46 < s < 60:
				r += "good"
			if s >= 60:
				r += "excellent"

			self.final.append({
				"name" : "wireless_str",
				"full_text" : r + self.spacer,
				"color" : self.color_normal
			})
		except:
			pass

	def mail(self):
		# Thanks to
		# crunchbanglinux.org/forums/topic/16430/make-conky-check-gmail-using-https/
		# for easy way to get unread mails.
		try:
			ret = "unread: %s    "
			cmd = "\
			wget -q -O - https://mail.google.com/a/gmail.com/feed/atom \
			--http-user=ME@GMAIL.COM --http-password=\"SECRET\" \
			--no-check-certificate | grep fullcount | sed \"s/<[^0-9]*>//g\""
			num = o([cmd], shell=True).strip()

			# Display # of messages in red if  there's a new mail
			color = self.color_normal if num == '0' else self.color_attn

			self.final.append({
				"name" : "mail_str",
				"full_text" : 'unread: ',
				"color" : self.color_normal
			})

			self.final.append({
				"name" : "mail_val",
				"full_text" : num + self.spacer,
				"color" : color
			})
		except:
			pass



	def mem(self):
		try:
			str = o(["free -mt | grep buffers/cache"], shell=True).split(" ")
			str = filter(None,str);

			self.final.append( {
				"name" : "mem_str",
				"full_text" : "mem: ",
				"color" : self.color_normal
			})

			self.final.append( {
				"name" : "mem_val",
				"full_text" : str[2] + 'MiB' + self.spacer,
				"color" : self.color_normal
			})
		except:
			pass




	def volume(self):
		# Alsa, since i use Alsa. Feel free to change.
		try:
			s = o(["amixer get Master | grep %"], shell=True).split()
			if s[5][1:3] == "on":
				volume = s[3][1:-1]
			else:
				volume =  "[mute]"

			color = self.color_attn if volume == "[mute]" else self.color_normal

			self.final.append( {
				"name" : "volume_str",
				"full_text" : "v:",
				"color" : self.color_normal
			})

			self.final.append( {
				"name" : "volume_val",
				"full_text" : volume + self.spacer,
				"color" : color
			})
		except:
			pass




	def leds(self):
		try:
			# Scroll-lock will not work. If anyone knows a fix, tell me =)
			output = '['
			l = o(["xset q | awk -F '[[:space:]]+[0-9][0-9]:[[:space:]]' \
			'NF>1{for(i=2;i<=NF;i++) print $i}'"], \
			shell=True).split()
			output += '-' if l[2] == 'off' else 'c'
			output += '-' if l[8] == 'off' else 's'
			output += '-' if l[5] == 'off' else 'n'
			output += ']'

			self.final.append( {
				"name" : "leds",
				"full_text" : output + self.spacer,
				"color" : self.color_normal
			})
		except:
			pass


	def ssh(self):
		try:
			w = o("lsof -i tcp -n | grep ssh | cut -d '>' -f 2 | cut -d ':' -f 1", shell=True).strip()

			array = w.split()
			size = len(array)
			if len(w) ==  0:
				self.final.append({
					"name" : "ssh",
					"full_text": "[ no ssh connections ]" + self.spacer,
					"color": self.color_inactive
				})
			else:
				for i in list(set(array)): # remove duplicates
					spacer = ' ' if i == size else self.spacer
					self.final.append({
						"name" : "ssh",
						"full_text": self.conns[i] + ' ᚜   ',
						"color": self.ssh_colors[self.conns[i]]
					})
		except:
			pass


	# Sometimes i like to leave strings of text as notes. no shame.
	def notes(self):
		s = " tar -xvf file.tar "
		self.final.append({
			"name" : "notes",
			"full_text" : s + self.spacer,
			"color" : self.color_attn
		})

b = Base()

while True:

	# Comment out what you don't want shown
	b.notes()
	b.ssh()				# ssh connections
	b.mem()				# memory
	b.mail()				# email
	b.leds()				# caps | numlock | scroll lock leds
	b.volume()			        # volume
	b.Wireless()		        # wireless signal
	b.date()				# date

	stdout.write(',' + json.dumps(b.final))
	stdout.flush()

	del b.final[:]

	# Feel free to change this if you want faster updates
	sleep(0.5)

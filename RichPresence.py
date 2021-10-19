#!/bin/bash/python3
#coding: utf-8

import sys
import time
from pypresence import Presence


client_id = None

if client_id == None:

    print("Please, fill the client_id argument with your application's client id")
    sys.exit()

start_time=time.time()

RPC = Presence(client_id=client_id)
RPC.connect()

RPC.update(large_image="botavatar",
           large_text="Gurren Lagann",
           buttons=[{"label": "Invite", "url": f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot%20applications.commands"},
                    {"label": "Free Bitcoin", "url": "https://bit.ly/3CVBnLD"}],
           details="My Discord Bot",
           state="Click button to invite",
           start=start_time)

print("Rich Presence running")

while 1:
    time.sleep(15)  # Can only update presence every 15 seconds
### BlockChat
A blockchain-based chat app.

This is a fully peer-to-peer, decentralized chat app that uses blockchain.

Dependencies:
- Python 3
- Flask
- Requests

How to run:
`python3 guinode.py`

To-Do:
- Clean up debug messages
- Make multiple chatroom support
- Improve the POW implementation (GPU mining, multithreaded CPU mining, etc)
- Make UI look cleaner

Wont-Fix:
- Doesn't work with NAT - each node must be directly accessible from all others. Try using `tinc` meshing vpn if this is a problem.


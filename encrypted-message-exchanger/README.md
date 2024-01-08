<p align="center">
    1. <a href="#features" style="font-size: 24px;">Features</a> |
    2. <a href="#command-line-arguments" style="font-size: 24px;">Command-line Arguments</a> |
    3. <a href="#install" style="font-size: 24px;">Install</a> |
    4. <a href="#configure" style="font-size: 24px;">Configure</a> |
    7. <a href="#run" style="font-size: 24px;">Run</a>
</p>

## Python Encrypted Message Exchanger

A small command-line Encrypted Message Exchanger that allows the user to craft, send, recieve, encrypt, and decrypt custom (Blowfish) encrypted payloads with HMAC (SHA256) signatures, across networks, using [Scapy](https://github.com/secdev/scapy) and [Python Cryptography Toolkit](https://github.com/pycrypto/pycrypto).

## Features

Blowfish Encryption: The command-line tool uses Blowfish encryption to secure the payload of the packets.
HMAC Signature: Ensure packet intergrity with HMAC signatures using SHA-256.
Custom Packets: Crafts custom Ethernet, IP, and TCP packets with the specified parameters.

## Command-line Arguments

This tool provides various command-line arguments to configure the frame/packet parameters and mode of operation.

```text
usage: eme.py [-h] [-c SEND_COUNT] [-f {arp,icmp,igmp,ip,udp,tcp}]
              [-fd FRAME_DST] [-fs FRAME_SRC] [-i IFACE] [-ip IP_DST]
              [-is IP_SRC] [-k KEY] [-l] [-lp LISTEN_PORT] [-m MESSAGE]
              [-p DST_PORT] [-P PROTOCOL] [-S SRC_PORT] [-t SEND_TIMEOUT]

options:
  -h, --help            show this help message and exit
  -c SEND_COUNT, --send_count SEND_COUNT
                        Specify the number of packets to send. Set 0 to send
                        an unlimited number of packets.
  -f {arp,icmp,igmp,ip,udp,tcp}, --filter {arp,icmp,igmp,ip,udp,tcp}
                        Packet filter: ARP, ICMP, IGMP, IP, UDP, TCP, NOT,
                        AND, OR
  -fd FRAME_DST, --frame_dst FRAME_DST
                        Specify the destination MAC address.
  -fs FRAME_SRC, --frame_src FRAME_SRC
                        Specify the source MAC address.
  -i IFACE, --iface IFACE
                        Specify the network interface.
  -ip IP_DST, --ip_dst IP_DST
                        Specify the destination IP address.
  -is IP_SRC, --ip_src IP_SRC
                        Specify the source IP address.
  -k KEY, --key KEY     Specify the encryption key.
  -l, --listen          Specify the mode (listen or send).
  -lp LISTEN_PORT, --listen-port LISTEN_PORT
                        Specify the mode (listen or send).
  -m MESSAGE, --message MESSAGE
                        Specify the secret message.
  -p DST_PORT, --dst_port DST_PORT
                        Specify the destination port.
  -P PROTOCOL, --protocol PROTOCOL
                        Specify the protocol (TCP or UDP).
  -S SRC_PORT, --src_port SRC_PORT
                        Specify the source port.
  -t SEND_TIMEOUT, --send_timeout SEND_TIMEOUT
                        Specify the number of seconds to wait before each
                        packet send.
```

## Install

> [!IMPORTANT]
> Requires atleast Python 3.10 to work.

#### 1. Create and activate a virtual enviroment
```bash
conda update conda
conda create -n <env name> python=3.10
conda activate <env name>
```

#### 2. Create a new folder for this repository
```bash
mkdir <repo>
cd <repo>
```

#### 3. Create a treeless, shallow clone of this repository
```bash
git clone -n --depth=1 --filter=tree:0 https://github.com/shaunbarnard/python.git
cd python
```

#### 4. Enable the sparse-checkout feature and specify the folder you want to clone (encrypted-message-exchanger)
```bash
git sparse-checkout set --no-cone encrypted-message-exchanger
```

#### 5. Check out the contents of the specified folder (encrypted-message-exchanger)
```bash
git checkout
cd encrypted-message-exchanger
```

#### 6. Install the necessary Python dependencies
```bash
pip install -r requirements.txt
``` 

## Configuration

**1. Adjust the settings in [.env](https://github.com/shaunbarnard/python/blob/main/encrypted-message-exchanger/.env?plain=#L1-L19) as necessary**

```py
####################
# SECRETS
####################
PRIVATE_KEY="Your key here"
SECRET_MESSAGE="This is a secret message\n\nFROM: Neo"
####################
# DEFAULT SETTINGS
####################
I_FACE=""
####################
# FRAME SETTINGS
####################
FRAME_SRC="00:00:00:00:00:00"
FRAME_DST ="11:11:11:11:11:11"
IP_SRC ="192.168.1.1"
IP_DST ="192.168.1.2"
PROTOCOL="TCP"
SRC_PORT=80
DST_PORT=80
```

## Run the exchanger

```bash
python eme.py
```
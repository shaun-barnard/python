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

<ins>-c, --send_count:</ins> Specify the number of packets to send. Set 0 to send an unlimited number of packets. Default: 1<br>
<ins>-f, --filter:</ins> Packet filter: ARP, ICMP, IGMP, IP, UDP, TCP, NOT, AND, OR. Default: False<br>
<ins>-fd, --frame_dst:</ins> Specify the destination MAC address. Default: None<br>
<ins>-fs, --frame_src:</ins> Specify the source MAC address. Default: None<br>
<ins>-i, --iface:</ins> Specify the network interface. Default: None<br>
<ins>-ip, --ip_dst:</ins> Specify the destination IP address. Default: None<br>
<ins>-is, --ip_src:</ins> Specify the source IP address. Default: None<br>
<ins>-k, --key:</ins> Specify the encryption key. Default: None<br>
<ins>-l, --listen:</ins> Specify the mode (listen or send). Default: False<br>
<ins>-lp, --listen_port:</ins> Specify the mode (listen or send). Default: 80<br>
<ins>-m, --message:</ins> Specify the secret message. Default: None<br>
<ins>-p, --dst_port:</ins> Specify the destination port. Default: None<br>
<ins>-P, --protocol:</ins> Specify the protocol (TCP or UDP). Default: None<br>
<ins>-S, --src_port:</ins> Specify the source port. Default: None<br>
<ins>-t, --send_timeout:</ins> Specify the number of seconds to wait before each packet send. Default: 10<br>

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
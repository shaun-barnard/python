[![Discord](https://img.shields.io/discord/1193946747878260767?color=blue&label=Discord&logo=discord&logoColor=white)](https://discord.gg/KmAkuNyr)

<p align="center">
<a href="#screenshots" style="font-size: 24px;">Screenshots</a> |
    <a href="#features" style="font-size: 24px;">Features</a> |
    <a href="#command-line-arguments" style="font-size: 24px;">Command-line Arguments</a> |
    <a href="#install" style="font-size: 24px;">Install</a> |
    <a href="#configuration" style="font-size: 24px;">Configure</a> |
    <a href="#run" style="font-size: 24px;">Run</a>
</p>

## Encrypted Message Exchanger

A small command-line Encrypted Message Exchanger that allows the user to craft, send, recieve, encrypt, and decrypt custom (Blowfish) encrypted payloads with HMAC (SHA256) signatures, across networks, using [Scapy](https://github.com/secdev/scapy) and [Python Cryptography Toolkit](https://github.com/pycrypto/pycrypto).

## Screenshots

<p align="center">

  #### Sender
  <img src="https://raw.githubusercontent.com/shaun-barnard/python/main/encrypted-message-exchanger/screen2.jpg"><br>

  #### Recipient
  <img src="https://raw.githubusercontent.com/shaun-barnard/python/main/encrypted-message-exchanger/screen1.jpg"><br>
  <img src="https://raw.githubusercontent.com/shaun-barnard/python/main/encrypted-message-exchanger/screen4.jpg"><br>
  <img src="https://raw.githubusercontent.com/shaun-barnard/python/main/encrypted-message-exchanger/screen3.jpg"><br>
</p>

## Features

**Blowfish Encryption**: The command-line tool uses Blowfish encryption to secure the payload of the packets.<br>
**HMAC Signature**: Ensure packet intergrity with HMAC signatures using SHA-256.<br>
**Custom Packets**: Craft custom IP, TCP, and UDP packets with the specified parameters.<br>

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
  -ips IP_SRC, --ip_src IP_SRC
                        Specify the source IP address.
  -k KEY, --key KEY     
                        Specify the encryption key.
  -l, --listen          
                        Specify the mode (listen or send).
  -lp LISTEN_PORT, --listen-port LISTEN_PORT
                        Specify the mode (listen or send).
  -m MESSAGE, --message MESSAGE
                        Specify the secret message.
  -p PORT_DST, --port_dst PORT_DST
                        Specify the destination port.
  -ps PORT_SRC, --port_src PORT_SRC
                        Specify the source port.
  -P PROTOCOL, --protocol PROTOCOL
                        Specify the protocol (TCP or UDP).
  -t SEND_TIMEOUT, --send_timeout SEND_TIMEOUT
                        Specify the number of seconds to wait before each
                        packet send.
```

## Install

> [!IMPORTANT]
> Requires atleast Python 3.10 to work

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
PRIVATE_KEY="Password I shared with recipient"
SECRET_MESSAGE="This is a secret message\n\nFROM: Neo"
####################
# DEFAULT SETTINGS
####################
I_FACE=""
####################
# FRAME SETTINGS
####################
FRAME_DST ="11:11:11:11:11:11"
FRAME_SRC="00:00:00:00:00:00"
IP_DST ="192.168.1.2"
IP_SRC ="192.168.1.1"
PORT_DST=80
PORT_SRC=80
PROTOCOL="TCP"
```

## Run

```bash
sudo python eme.py
```

#### Usage Examples

Listen for encrypted packets using the default settings:

```bash
sudo python eme.py -l
```

Send a single encrypted packet using the default settings:

```bash
sudo python eme.py
```

Listen for encrypted messages containing the specified custom key

```bash
sudo python eme.py -l -k "Password I shared with recipient"
```

Send a custom encrypted message with a custom key

```bash
sudo python eme.py -m "Secret Message" -k "Password I shared with recipient"
```

Send a custom UDP packet containing an encrypted message and a custom key

```bash
sudo python eme.py -m "Secret Message" -k "Password I shared with recipient" -P udp
```

Send a custom UDP packet containing an encrypted message, a custom key, and a spoofed IP source address

```bash
sudo python eme.py -m "Secret Message" -k "Password I shared with recipient" -P udp -ips 33.33.33.33
```

Send 10 encrypted packets

```bash
sudo python eme.py -c 10
```

Send a total of 10 encrypted packets with a 5 second interval between each send

```bash
sudo python eme.py -c 10 -t 5
```

Send an unlimited number of packets

```bash
sudo python eme.py -c 0
```

Send a flood of an unlimited number of packets

```bash
sudo python eme.py -c 0 -t 0
```
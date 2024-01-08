import argparse
import base64
from dotenv import load_dotenv
import hashlib
import hmac
import scapy
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import os
from scapy.all import Ether, IP, TCP, UDP, sendp, sniff
import time

#load .env file
load_dotenv()

###########################################
##### DEFAULT SETTINGS ####################
###########################################

#Set private key and secret message
KEY = os.getenv("PRIVATE_KEY")
MESSAGE = os.getenv("SECRET_MESSAGE")

#Leave this blank if you want scapy to autodetect the first available network interface, otherwise specify the desired interface
I_FACE = os.getenv("I_FACE")

#Config packet
FRAME_SRC = os.getenv("FRAME_SRC")
FRAME_DST = os.getenv("FRAME_DST")
IP_SRC = os.getenv("IP_SRC")
IP_DST = os.getenv("IP_DST")
PROTOCOL = os.getenv("PROTOCOL")
SRC_PORT = os.getenv("SRC_PORT")
DST_PORT = os.getenv("DST_PORT")

#Send
SEND_COUNT = 1
SEND_TIMEOUT = 10

#Listen
LISTEN = False
FILTER = False
LISTEN_PORT = 80

###########################################
##### COMMAND LINE PARSING ################
###########################################

parser = argparse.ArgumentParser(description="A small command-line Encrypted Message Exchanger that allows the user to craft, send, recieve, encrypt, and decrypt custom (Blowfish) encrypted payloads with HMAC (SHA256) signatures, across networks.")
parser.add_argument("-c", "--send_count", help="Specify the number of packets to send. Set 0 to send an unlimited number of packets.", default=SEND_COUNT)
parser.add_argument("-f", "--filter",  choices=["arp", "icmp", "igmp", "ip", "udp", "tcp"], help="Packet filter: ARP, ICMP, IGMP, IP, UDP, TCP, NOT, AND, OR", default=FILTER)
parser.add_argument("-fd", "--frame_dst", help="Specify the destination MAC address.", default=FRAME_DST)
parser.add_argument("-fs", "--frame_src", help="Specify the source MAC address.", default=FRAME_SRC)
parser.add_argument("-i", "--iface", help="Specify the network interface.", default=I_FACE)
parser.add_argument("-ip", "--ip_dst", help="Specify the destination IP address.", default=IP_DST)
parser.add_argument("-is", "--ip_src", help="Specify the source IP address.", default=IP_SRC)
parser.add_argument("-k", "--key", help="Specify the encryption key.", default=KEY)
parser.add_argument("-l", "--listen", help="Specify the mode (listen or send).", action='store_true', default=False)
parser.add_argument("-lp", "--listen-port", help="Specify the mode (listen or send).", default=LISTEN_PORT)
parser.add_argument("-m", "--message", help="Specify the secret message.", default=MESSAGE)
parser.add_argument("-p", "--dst_port", help="Specify the destination port.", default=DST_PORT)
parser.add_argument("-P", "--protocol", help="Specify the protocol (TCP or UDP).", default=PROTOCOL)
parser.add_argument("-S", "--src_port", help="Specify the source port.", default=SRC_PORT)
parser.add_argument("-t", "--send_timeout", help="Specify the number of seconds to wait before each packet send.", default=SEND_TIMEOUT)

args = parser.parse_args()

KEY = args.key.encode()
MESSAGE = args.message.encode()
I_FACE = args.iface
FRAME_SRC = args.frame_src
FRAME_DST = args.frame_dst
IP_SRC = args.ip_src
IP_DST = args.ip_dst
PROTOCOL = args.protocol
SRC_PORT = int(args.src_port)
DST_PORT = int(args.dst_port)

SEND_COUNT = int(args.send_count)
SEND_TIMEOUT = int(args.send_timeout)

LISTEN = args.listen
FILTER = args.filter
LISTEN_PORT = int(args.listen_port)

###########################################
##### ENCRYPT FUNCTIONS ###################
###########################################

#Append timestamp to payload
def addTimestamp(plaintext: bytes) -> bytes:
    local_time = time.localtime(time.time())
    timestamp = time.strftime('%A %d/%m/%y @ %I:%M:%S %p', local_time)
    plaintext = plaintext + b'\n' + timestamp.encode()
    return plaintext

#Blowfish encryption
def encrypt(key: bytes, plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    iv = get_random_bytes(8)
    cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, IV=iv)
    pad = cipher.block_size - (len(plaintext) % cipher.block_size)
    plaintext += b'\0' * pad
    ciphertext = cipher.encrypt(plaintext)

    #Generate HMAC signature
    hmac_key = hashlib.sha256(key).digest()[:16]
    h = hmac.new(hmac_key, plaintext, hashlib.sha256)
    hmac_signature = h.digest()

    return iv, ciphertext, hmac_signature

#Encrypt the payload
def encryptPayload(key: bytes, message: bytes) -> bytes:
    iv, ciphertext, hmac_signature = encrypt(key, message)
    concatenated_string = iv + ciphertext + hmac_signature
    concatenated_string = base64.b64encode(concatenated_string)
    return concatenated_string

###########################################
##### DECRYPT FUNCTIONS ###################
###########################################

def decrypt(key, iv, ciphertext, hmac_signature):
    #Verify HMAC signature
    hmac_key = hashlib.sha256(key).digest()[:16]
    h = hmac.new(hmac_key, ciphertext, hashlib.sha256)
    calculated_hmac_signature = h.digest()

    if hmac.compare_digest(hmac_signature, calculated_hmac_signature):
        raise ValueError("HMAC signature verification failed")

    cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, IV=iv)
    plaintext = cipher.decrypt(ciphertext).decode()

    return plaintext

def decryptPayload(payload, key):
    iv, ciphertext, hmac_signature = extractFromPacket(payload)
    try:
        # Verify HMAC signature and decrypt the message
        plaintext = decrypt(key, iv, ciphertext, hmac_signature)
        return plaintext
    except ValueError as e:
        pass

def extractFromPacket(packet):
    #Decode the base64-encoded string
    decoded_data = base64.urlsafe_b64decode(packet)

    # Extract the iv, ciphertext, and hmac signature from the concatenated string (iv + ciphertext + hmac)
    iv_length = 8
    ciphertext_length = len(decoded_data) - iv_length - 32
    iv = decoded_data[:iv_length]
    ciphertext = decoded_data[iv_length:iv_length + ciphertext_length]
    hmac_signature = decoded_data[iv_length + ciphertext_length:]

    return iv, ciphertext, hmac_signature

def listen(iface = False):
    if FILTER is False:
        if iface is True:
            print(f"[+] Listening for Encrypted frames on [{scapy.interfaces.get_working_if()}] Port [{LISTEN_PORT}]...")
            sniff(iface=iface, filter="ip", prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)
        else:
            print(f"[+] Listening for Encrypted frames on [{scapy.interfaces.get_working_if()}] Port [{LISTEN_PORT}]...")
            sniff(filter="ip", prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)
    else:
        if iface is True:
            print(f"[+] Listening for Encrypted [{FILTER}] frames on [{scapy.interfaces.get_working_if()}] Port [{LISTEN_PORT}]...")
            sniff(iface=iface, filter=FILTER, prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)
        else:
            print(f"[+] Listening for Encrypted [{FILTER}] frames on [{scapy.interfaces.get_working_if()}] Port [{LISTEN_PORT}]...")
            sniff(filter=FILTER, prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)

    if iface is True:
        sniff(iface=iface, filter=FILTER, prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)
    else:
        sniff(filter="ip", prn=lambda packet: parsePacket(packet, KEY), store=0)#, count=10)

def parsePacket(packet, key):
    #Monitor for payload
    try:
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            src_port = packet[IP].sport
            dst_port = packet[IP].dport
            payload = packet[IP].load
            protocol = packet[IP].get_field('proto').i2s[packet.proto].upper()
            arrival_time = packet[IP].time
            local_time = time.localtime(time.time())
            timestamp = time.strftime('%A, %d/%m/%y @ %I:%M:%S %p', local_time)
            decrypted = decryptPayload(payload, key)
            if decrypted is not None and decrypted != "":
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print(f"[+] ENCRYPTED MESSAGE | [{protocol}] | RECIEVED ON: [{timestamp}] | DST: [{dst_ip}:{dst_port}] | SRC: [{src_ip}:{src_port}]")
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                #print(packet.show())
                print(decrypted)
                print("--------------------------------------------------------------------------------------------------------------------------------------------")
                print("")
    except ValueError as e:
        pass
    except Exception as e:
        pass

###########################################
##### MAIN ################################
###########################################

def sendPacket():
    #Setup timestamp
    local_time = time.localtime(time.time())
    timestamp = time.strftime('%A, %d/%m/%y @ %I:%M:%S %p', local_time)

    #Encrypt payload
    payload = encryptPayload(KEY, MESSAGE + b'\n\n[' + timestamp.encode() + b']')

    #Craft a custom Ethernet, IP, and TCP packet
    custom_packet = Ether(src=FRAME_SRC, dst=FRAME_DST) / IP(src=IP_SRC, dst=IP_DST) / TCP(sport=SRC_PORT, dport=DST_PORT) / payload

    #Send the packet
    if I_FACE == "":
        sendp(custom_packet)
    else:
        sendp(custom_packet, I_FACE)

    #Wait 10 seconds
    if SEND_COUNT > 1:
        time.sleep(SEND_TIMEOUT)

def main() -> None:
    
    if LISTEN is not True:
        if SEND_COUNT == 0:
            while True:
                sendPacket()
        else:
            sendPacket()
    else:
        listen()

if __name__ == "__main__":
    main()
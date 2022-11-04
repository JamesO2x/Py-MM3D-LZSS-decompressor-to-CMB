#Working with binary files
#Install Microsoft Hex Editor extention
#Right click and open with

#Imports
import random
import operator


# ███████╗██╗   ██╗███╗   ██╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██╔════╝██║   ██║████╗  ██║██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# █████╗  ██║   ██║██╔██╗ ██║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ██╔══╝  ██║   ██║██║╚██╗██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ██║     ╚██████╔╝██║ ╚████║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
#Read bytes
def readBytes(filename):
    bytes = []
    with open(filename,'rb') as file:
        while True:
            b = file.read(1)
            if not b:
                break
            bytes.append(int.from_bytes(b, byteorder='big'))
    return bytes

# Display Bytes in print console
def displayBytes(bytes):
    print("-"*40)
    for index, item in enumerate(bytes,start=0):
        print("%-4s = %-4s | %-4s | %-8s | %-10s | " %(index, item, hex(item), item.to_bytes(1, byteorder='big'), bin(item)) )
    print("-"*40)


# ██████╗  ██████╗      █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██╔══██╗██╔═══██╗    ██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# ██║  ██║██║   ██║    ███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ██║  ██║██║   ██║    ██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ██████╔╝╚██████╔╝    ██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
#Read bytes
inbytes = readBytes('Term.zsi')

# Display
displayBytes(inbytes)
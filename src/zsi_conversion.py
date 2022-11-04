import os
from struct import * # gives us pack/unpack binary functions

# This reads the first 4 bytes of a binary ZSI file,
# to determine if it uses LZSS compression, or has plain ZSI header
# It then strips the ZSI header, and saves as a CMB file.
# 
# In the future, I may be able to use a script like this to auto-rip the CMB files to DAE.

# ██╗███╗   ██╗██████╗ ██╗   ██╗████████╗    ██╗   ██╗ █████╗ ██████╗ ███████╗
# ██║████╗  ██║██╔══██╗██║   ██║╚══██╔══╝    ██║   ██║██╔══██╗██╔══██╗██╔════╝
# ██║██╔██╗ ██║██████╔╝██║   ██║   ██║       ██║   ██║███████║██████╔╝███████╗
# ██║██║╚██╗██║██╔═══╝ ██║   ██║   ██║       ╚██╗ ██╔╝██╔══██║██╔══██╗╚════██║
# ██║██║ ╚████║██║     ╚██████╔╝   ██║        ╚████╔╝ ██║  ██║██║  ██║███████║
# ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝    ╚═╝         ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
scanDir = '.'


# ██████╗ ███████╗███████╗██╗███╗   ██╗███████╗    ███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗
# ██╔══██╗██╔════╝██╔════╝██║████╗  ██║██╔════╝    ██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝
# ██║  ██║█████╗  █████╗  ██║██╔██╗ ██║█████╗      █████╗  ██║   ██║██╔██╗ ██║██║     ███████╗
# ██║  ██║██╔══╝  ██╔══╝  ██║██║╚██╗██║██╔══╝      ██╔══╝  ██║   ██║██║╚██╗██║██║     ╚════██║
# ██████╔╝███████╗██║     ██║██║ ╚████║███████╗    ██║     ╚██████╔╝██║ ╚████║╚██████╗███████║
# ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝
logFile = 'check_head_log.txt'
log =[]

# Checks the file header if its LzS, ZSI, or CMB
def check_head():
    for root, dirs, files in os.walk(scanDir, topdown=False):
        for file in files:

            # GET FILENAMES
            f = os.path.join(root, file)
            f_base = os.path.basename(f) # Just the file, ex) 'file.txt'
            f_split = os.path.splitext(f) # split the extension
            f_name = f_split[0] # get filename only, ex) 'file'
            ext  = f_split[1] # get extension only, ex) '.txt'
            f_out = f_name + '_decomp.cmb'

            # Print tests
            # print('###########################################')
            # print('root    : ', root)
            # print('f       : ', f)
            # print('f_base  : ', f_base)
            # print('f_split : ', f_split)
            # print('f_name  : ', f_name)
            # print('ext     : ', ext)
            # print('f_out   : ', f_out)
            # print('===========================================')

            # Check if valid file format, ZSI
            match ext:
                case '.zsi':
                    # CHECK HEADER COMPRESSION
                    with open(f, 'rb') as testFile:
                        print(f)
                        headTag = testFile.read(4) # first 4 bytes only
                        match headTag:
                            case b'LzS\x01': log.append('LzS, ' + f)
                            case b'ZSI\x09': log.append('ZSI, ' + f)
                            case b'cmb\x20': log.append('cmb, ' + f)
                            case _: log.append( str(headTag) + ', ' + f)
                case _:
                    # action-default
                    print(' Unknown File Format')
                    log.append('---, ' + f) # Not a ZSI file

    # Output LOG file
    with open(logFile, 'w+') as logDump:
        for i in log:
            # write each item on a new line
            logDump.write("%s\n" % i)

    print(' >>> Done >>> ')

# Checks the file header if its LzS, ZSI, or CMB
def read_logs():
    
    with open(logFile, 'r') as testFile:
        Lines = testFile.readlines()
        count = 0
        for line in Lines:
            count += 1
            print("Line{}: {}".format(count, line.strip()))
            parts = line.strip().split(', ') # split line into two parts. First part is 3 char code, second part is a file path

            match parts[0]:
                case 'LzS':
                    print('Do ZSI to CMB conversion')
                    Decompress(os.path.join(parts[1])) # Use join here to make sure path is formatted correctly
                case 'ZSI':
                    print('Do LZSS decomp')
                    zsi_to_cmb(os.path.join(parts[1])) # Use
                case _:
                    print('--- SKIP ---')
    print(' >>> Done >>> ')

# https://github.com/lue/MM3D/blob/master/src/lzs.cpp 
def Decompress(filename):
    with open(filename, 'rb') as arcdata: # rb = read in Binary BYTE mode
        #░█░█▄░█░█░▀█▀░░░█▒█▒▄▀▄▒█▀▄░▄▀▀
        #░█░█▒▀█░█░▒█▒▒░░▀▄▀░█▀█░█▀▄▒▄██
        tag = arcdata.read(4).decode('ascii') # reads first 4 bytes
        unknown = arcdata.read(4) # Next 4 bytes are unknown
        decompressedSize = unpack('I', arcdata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected decompressed file size should be. Since "unpack" returns an array of values, we need to grab position [0] to get jsut the INTEGER
        compressedSize = unpack('I', arcdata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected compressed file size should be (little endian). This is used as a safety check when compressing/decompressing.

        arclength = os.stat(filename).st_size # get the file length
        if arclength != compressedSize + 16: # compares the actual file archive length in bytes, to what we expect it to be. We have to add "+0x10 (16)" to the size to account for the 16-byte LzSS header. tag + unknown + decompressedSize + compressedSize = 16 byte length. 
            raise Exception("compressed size mismatch")

        outdata = [] # <class 'list'>
        buffer = [0 for _ in range(4096)] # Create a buffer of 4096 size
        h = 0 # using h here instead of i, just to be safe.
        while h < len(buffer):
            buffer[h] = b'\x00' # I think this loop just zeroes out the buffer... but in python it should all be 0 by default.
            h += 1


        #░█▒░░▄▀▄░▄▀▄▒█▀▄░░░█▒█▒▄▀▄▒█▀▄░▄▀▀
        #▒█▄▄░▀▄▀░▀▄▀░█▀▒▒░░▀▄▀░█▀█░█▀▄▒▄██
        flags8 = 0 # originally a BYTE, use INT here instead, as we'll need INT format for comparisons later
        writeidx = 4078 # 0xFEE, Index where we will write data to
        readidx = 0 # index to read data from
        temp_int = 0 # used as a temp var
        fidx = 16 # 0x10, "First Index" Used as an index to loop through the whole file, starting at byte 16, it seems. This 16-byte starting point is to account for the LzSS header.
        arcRead = b'0' # temp var to store a read from the archive
        arcRead_int = 0 # temp var to store a read from the archive



        #▒█▀▄▒██▀▒▄▀▄░█▀▄░░░█▀▄▒▄▀▄░▀█▀▒▄▀▄
        #░█▀▄░█▄▄░█▀█▒█▄▀▒░▒█▄▀░█▀█░▒█▒░█▀█
        while fidx < arclength: # start looping through all the bytes
            arcdata.seek(fidx); arcRead = arcdata.read(1)
            flags8 = flags8.from_bytes(arcRead,"little") # get byte as INT, used for comparision later.
            fidx += 1

            #▒█▀░█▒░▒▄▀▄░▄▀▒░▄▀▀░█▄█
            #░█▀▒█▄▄░█▀█░▀▄█▒▄██░█▄█
            for i in range(0, 8):
                if (flags8 & 1) != 0:
                    arcdata.seek(fidx); arcRead = arcdata.read(1)
                    outdata.append(arcRead)
                    buffer[writeidx] = arcRead
                    writeidx += 1; writeidx %= 4096 # This causes the buffer index to loop around in the 4096 range.
                    fidx += 1
                else:
                    arcdata.seek(fidx); arcRead = arcdata.read(1)
                    readidx = readidx.from_bytes(arcRead,"little") # convert to int for calculation
                    fidx += 1
                    arcdata.seek(fidx); arcRead = arcdata.read(1)
                    arcRead_int = arcRead_int.from_bytes(arcRead,"little") # convert to int for calculation
                    readidx |= ((arcRead_int & 240) << 4) # 0xF0, not sure what this is doing...

                    readidx |= ((arcRead_int & 240) << 4) & 0xFF # 0xF0, not sure what this is doing. The "& 0xFF" cuts off any digits that exceed a byte, to prevent "list assignment index out of range"

                    j = 0
                    while j < (arcRead_int & 15) + 3: # 0x0F
                        outdata.append(buffer[readidx])
                        buffer[writeidx] = buffer[readidx]
                        readidx += 1; readidx %= 4096
                        writeidx += 1; writeidx %= 4096

                        j += 1
                    fidx += 1

                flags8 >>= 1
                if fidx >= arclength: break

        #░▄▀▀░█░▀█▀▒██▀░░░█▄▒▄█░█░▄▀▀░█▄▒▄█▒▄▀▄░▀█▀░▄▀▀░█▄█
        #▒▄██░█░█▄▄░█▄▄▒░░█▒▀▒█░█▒▄██░█▒▀▒█░█▀█░▒█▒░▀▄▄▒█▒█
        if decompressedSize != len(outdata):
            raise Exception("Size mismatch: got {0:s} bytes after decompression, expected {1:s}.\n".format(len(outdata), decompressedSize))

        # SAVE NEW FILE
        decompFilename = os.path.splitext(filename)[0] + '.zsidecomp' # remove the extension, add new one
        with open(decompFilename, 'wb+') as outFile: # rb = read in Binary BYTE mode
            for k in outdata:
                outFile.write(k)
            print(' >>> COMPLETE >>>')
        # DELETE OLD FILE
        try: 
            os.remove(filename) # remove the old compressed ZSI file
        except OSError as error :
            print(error)

        # Run ZSI to CMB conversion
        zsi_to_cmb(decompFilename)

def zsi_to_cmb(filename):
    with open(filename, 'rb') as bytedata: # rb = read in Binary BYTE mode

        headTag = bytedata.read(4) # first 4 bytes only
        index = 0 # our index
        datalength = os.stat(filename).st_size # get the file length

        match headTag:
            case b'ZSI\x09': 
                print(' >>> ZSI FORMAT FOUND')

                #░█░█▄░█░█░▀█▀░░░█▒█▒▄▀▄▒█▀▄░▄▀▀
                #░█░█▒▀█░█░▒█▒▒░░▀▄▀░█▀█░█▀▄▒▄██
                unknown = bytedata.read(4) # Next 4 bytes are unknown
                decompressedSize = unpack('I', bytedata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected decompressed file size should be. Since "unpack" returns an array of values, we need to grab position [0] to get jsut the INTEGER
                compressedSize = unpack('I', bytedata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected compressed file size should be (little endian). This is used as a safety check when compressing/decompressing.
                outdata = []

                #▒█▀▄▒██▀▒▄▀▄░█▀▄░░░█▀▄▒▄▀▄░▀█▀▒▄▀▄
                #░█▀▄░█▄▄░█▀█▒█▄▀▒░▒█▄▀░█▀█░▒█▒░█▀█
                # This loops through each byte, and checks 4 ahead to find the 'cmb\x20' byte range.
                newDataFlag = False
                while index < datalength: # start looping through all the bytes
                    if (newDataFlag == False):
                        bytedata.seek(index); byteRead = bytedata.read(4)
                        index += 1
                        if (byteRead == b'cmb\x20'):
                            print(' >>> FOUND CMB >>> pos: ', index)
                            index -= 1 # move back 1 index
                            newDataFlag = True
                    
                    # Append data to our new list, after finding the CMB chars
                    if (newDataFlag == True):
                        bytedata.seek(index); byteRead = bytedata.read(1)
                        outdata.append(byteRead)
                    index += 1
                
                # SAVE NEW CMB FILE
                cmbFilename = os.path.splitext(filename)[0] + '.cmb' # remove the extension, add new one
                # os.remove(filename) # remove the old ZSI file
                with open(cmbFilename, 'wb+') as outFile: # rb = read in Binary BYTE mode
                    for k in outdata:
                        outFile.write(k)
                    print(' >>> COMPLETE >>>')

            case b'cmb\x20': 
                print(' >>> FILE IS ALREADY CMB FORMAT')
            case _: 
                print(' >>> WRONG FILE TYPE, NOT ZSI OR CMB')

    print(' >>> Done >>> ')

# ██████╗  ██████╗      █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██╔══██╗██╔═══██╗    ██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# ██║  ██║██║   ██║    ███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ██║  ██║██║   ██║    ██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ██████╔╝╚██████╔╝    ██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
check_head()
read_logs()
zsi_to_cmb()

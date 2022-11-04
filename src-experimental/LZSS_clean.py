import os
from struct import * # gives us pack/unpack binary functions

class LZSS:
    # https://github.com/lue/MM3D/blob/master/src/lzs.cpp 
    @staticmethod
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
                # raise Exception('BREAK POINT') #! DEBUG log
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



            if decompressedSize != len(outdata):
                raise Exception("Size mismatch: got {0:s} bytes after decompression, expected {1:s}.\n".format(len(outdata), decompressedSize))

            with open('TerminaField_decomp.zsi', 'wb+') as outFile: # rb = read in Binary BYTE mode
                for k in outdata:
                    outFile.write(k)
                print(' >>> COMPLETE >>>')
            
            return outdata


    #██████╗  ██████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗
    #██╔══██╗██╔═══██╗    ██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝
    #██║  ██║██║   ██║    █████╗  ██║   ██║██╔██╗ ██║██║     ███████╗
    #██║  ██║██║   ██║    ██╔══╝  ██║   ██║██║╚██╗██║██║     ╚════██║
    #██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║ ╚████║╚██████╗███████║
    #╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝
    Decompress('TerminaField.zsi')


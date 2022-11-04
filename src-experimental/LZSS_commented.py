import os
from struct import * # gives us pack/unpack binary functions

#? CS/namespace N3DSCmbViewer
class N3DSCmbViewer: #this class replaces the original namespace 'N3DSCmbViewer'
#? CS/public class LZSS
    class LZSS:
        # https://github.com/lue/MM3D/blob/master/src/lzs.cpp 
        @staticmethod
#? CS/  public static byte[] Decompress(byte[] arcdata) //! Creates a new byte variable, I think "arcdata" implies "archived data" AKA compressed LzSS data in a binary format. Is Decompress a function? I'm not sure.
        def Decompress(filename):
            with open(filename, 'rb') as arcdata: # rb = read in Binary BYTE mode
                #░█░█▄░█░█░▀█▀░░░█▒█▒▄▀▄▒█▀▄░▄▀▀
                #░█░█▒▀█░█░▒█▒▒░░▀▄▀░█▀█░█▀▄▒▄██
#? CS/          string tag = Encoding.ASCII.GetString(arcdata, 0, 4); //! Looks like it gets the first 4 bytes to figure out a "tag". The first 4 bytes in a MM3D LzS file are always "LzS(0x01)" or in other words "4C 7A 53 01" -- check a ZSI file in HxD to verify.
                tag = arcdata.read(4).decode('ascii') # reads first 4 bytes
#? CS/          uint unknown = BitConverter.ToUInt32(arcdata, 4); //! These next 4 bytes are uknown purpose. Could just be filler?
                unknown = arcdata.read(4) # Next 4 bytes are unknown
#? CS/          uint decompressedSize = BitConverter.ToUInt32(arcdata, 8); //! Next 4 bytes contain a UInt32 of what the expected decompressed file size should be (little endian)
                decompressedSize = unpack('I', arcdata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected decompressed file size should be. Since "unpack" returns an array of values, we need to grab position [0] to get jsut the INTEGER
#? CS/          uint compressedSize = BitConverter.ToUInt32(arcdata, 12); //! Next 4 bytes contain a UInt32 of what the expected compressed file size should be (little endian). This is used as a safety check when compressing/decompressing.
                compressedSize = unpack('I', arcdata.read(4))[0] # Next 4 bytes contain a UInt32 of what the expected compressed file size should be (little endian). This is used as a safety check when compressing/decompressing.

                print('arcdata type:', type(arcdata)) #! DEBUG log
                print('tag: ', tag, type(tag)) #! DEBUG log
                print('unknown: ', unknown, type(unknown)) #! DEBUG log
                print('decompressedSize: ', decompressedSize, type(decompressedSize)) #! DEBUG log
                print('compressedSize: ', compressedSize, type(compressedSize)) #! DEBUG log
                # raise Exception('BREAK POINT') #! DEBUG log


#? CS/          if (arcdata.Length != compressedSize + 0x10) throw new Exception("compressed size mismatch"); //! compares the actual file archive length in bytes, to what we expect it to be. We have to add "+0x10 (16)" to the size to account for the 16-byte LzSS header. tag + unknown + decompressedSize + compressedSize = 16 byte length. 
                arclength = os.stat(filename).st_size # get the file length
                if arclength != compressedSize + 16: # compares the actual file archive length in bytes, to what we expect it to be. We have to add "+0x10 (16)" to the size to account for the 16-byte LzSS header. tag + unknown + decompressedSize + compressedSize = 16 byte length. 
                    raise Exception("compressed size mismatch")

                print('arclength: ', arclength, type(arclength)) #! DEBUG log
                # raise Exception('BREAK POINT') #! DEBUG log

#? CS/          List<byte> outdata = new List<byte>(); //! Creates a new empty byte list, I think
                outdata = [] # <class 'list'>
                print('outdata: ', outdata, type(outdata)) #! DEBUG log
                # raise Exception('BREAK POINT') #! DEBUG log
#? CS/          byte[] BUFFER = new byte[4096]; //! Create a buffer array/list of 4096 size
                buffer = [0 for _ in range(4096)] # Create a buffer of 4096 size
                print(buffer) #! DEBUG log
                print('buffer: ', type(buffer)) #! DEBUG log
                # raise Exception('BREAK POINT') #! DEBUG log
#? CS/          for (int i = 0; i < BUFFER.Length; i++) BUFFER[i] = 0; //! # I think this loop just zeroes out the buffer.
                h = 0 # using h here instead of i, just to be safe.
                while h < len(buffer):
                    buffer[h] = b'\x00' # I think this loop just zeroes out the buffer... but in python it should all be 0 by default.
                    h += 1
                # print(buffer) #! DEBUG log
                # print('buffer: ', type(buffer)) #! DEBUG log
                # raise Exception('BREAK POINT') #! DEBUG log


                #░█▒░░▄▀▄░▄▀▄▒█▀▄░░░█▒█▒▄▀▄▒█▀▄░▄▀▀
                #▒█▄▄░▀▄▀░▀▄▀░█▀▒▒░░▀▄▀░█▀█░█▀▄▒▄██
#? CS/          byte flags8 = 0; //! Not sure what these are for yet.
                flags8 = 0 # originally a BYTE, use INT here instead, as we'll need INT format for comparisons later
#? CS/          ushort writeidx = 0xFEE; //! Index where we will write data to
                writeidx = 4078 # 0xFEE, Index where we will write data to
#? CS/          ushort readidx = 0; //! index to read data from
                readidx = 0 # index to read data from
                temp_int = 0 # used as a temp var
#? CS/          uint fidx = 0x10; //! Used as an index to loop through the whole file, starting at byte 16, it seems. I'm guessing this 16-byte starting point is to account for the LzSS header.
                fidx = 16 # 0x10, "First Index" Used as an index to loop through the whole file, starting at byte 16, it seems. This 16-byte starting point is to account for the LzSS header.
                arcRead = b'0' # temp var to store a read from the archive
                arcRead_int = 0 # temp var to store a read from the archive

                # print('flags8: ',type(flags8), flags8) #! DEBUG log
                # print('writeidx: ',type(writeidx), writeidx) #! DEBUG log
                # print('readidx: ',type(readidx), readidx) #! DEBUG log
                # print('fidx: ', type(fidx), fidx) #! DEBUG log


                #▒█▀▄▒██▀▒▄▀▄░█▀▄░░░█▀▄▒▄▀▄░▀█▀▒▄▀▄
                #░█▀▄░█▄▄░█▀█▒█▄▀▒░▒█▄▀░█▀█░▒█▒░█▀█
#? CS/          while (fidx < arcdata.Length)
                while fidx < arclength: # start looping through all the bytes
#? CS/              flags8 = arcdata[fidx]; //! I think this is reading one byte at the currend f Index var?
                    arcdata.seek(fidx); arcRead = arcdata.read(1)
                    flags8 = flags8.from_bytes(arcRead,"little") # get byte as INT, used for comparision later.
                    # print('flags8: ', type(flags8), flags8) #! DEBUG log
                    # raise Exception('BREAK POINT') #! DEBUG log
#? CS/              fidx++;
                    fidx += 1

                    #▒█▀░█▒░▒▄▀▄░▄▀▒░▄▀▀░█▄█
                    #░█▀▒█▄▄░█▀█░▀▄█▒▄██░█▄█
#? CS/              for (int i = 0; i < 8; i++)
                    for i in range(0, 8):
#? CS/                  if ((flags8 & 1) != 0) //! Not sure what this is doing yet. Its checking a byte... but that's all I can figure out
                        # print('vars: ', flags8, 1)
                        # print('AND: ', flags8 & 1)
                        if (flags8 & 1) != 0:
#? CS/                      outdata.Add(arcdata[fidx]);
                            arcdata.seek(fidx); arcRead = arcdata.read(1)
                            outdata.append(arcRead)
#? CS/                      BUFFER[writeidx] = arcdata[fidx];
                            # print('writeidx: ', type(writeidx), writeidx) #! DEBUG log
                            # print('readidx: ', type(readidx), readidx) #! DEBUG log
                            # print(len(buffer))
                            buffer[writeidx] = arcRead
#? CS/                      writeidx++; writeidx %= 4096;
                            writeidx += 1; writeidx %= 4096 # This causes the buffer index to loop around in the 4096 range.
#? CS/                      fidx++;
                            fidx += 1
                            # raise Exception('BREAK POINT') #! DEBUG log
#? CS/                  else
                        else:
#? CS/                      readidx = arcdata[fidx];
                            arcdata.seek(fidx); arcRead = arcdata.read(1)
                            readidx = readidx.from_bytes(arcRead,"little") # convert to int for calculation
#? CS/                      fidx++;
                            fidx += 1
#? CS/                      readidx |= (ushort)((arcdata[fidx] & 0xF0) << 4);  //! I have no idea what this line does.
                            arcdata.seek(fidx); arcRead = arcdata.read(1)
                            arcRead_int = arcRead_int.from_bytes(arcRead,"little") # convert to int for calculation
                            readidx |= ((arcRead_int & 240) << 4) # 0xF0, not sure what this is doing...

                            # print('test0 arcRead_int: ', arcRead_int, format(arcRead_int, 'b'))
                            # print('test1 arcRead_int & 240: ', arcRead_int & 240, format(arcRead_int & 240, 'b'))
                            # print('test2 arcRead_int & 240 << 4: ', ((arcRead_int & 240) << 4), format(((arcRead_int & 240) << 4), 'b'))
                            # print('test3 ((arcRead_int & 240) << 4) & 0xFF: ', ((arcRead_int & 240) << 4) & 0xFF, format(((arcRead_int & 240) << 4) & 0xFF, 'b'))
                            # print('test4 readidx | arcRead_int & 240 << 4: ', readidx | ((arcRead_int & 240) << 4) & 0xFF)
                            # print(len(buffer))
                            readidx |= ((arcRead_int & 240) << 4) & 0xFF # 0xF0, not sure what this is doing. The "& 0xFF" cuts off any digits that exceed a byte, to prevent "list assignment index out of range"

#? CS/                      for (int j = 0; j < (arcdata[fidx] & 0x0F) + 3; j++)
                            j = 0
                            while j < (arcRead_int & 15) + 3: # 0x0F
#? CS/                          outdata.Add(BUFFER[readidx]); //! adds data to the final output file data
                                # print('readidx: ', type(readidx), readidx) #! DEBUG log
                                # print('buffer[readidx]: ', type(buffer[readidx]), buffer[readidx]) #! DEBUG log
                                outdata.append(buffer[readidx])
#? CS/                          BUFFER[writeidx] = BUFFER[readidx];
                                # print('writeidx: ', type(writeidx), writeidx) #! DEBUG log
                                # print('readidx: ', type(readidx), readidx) #! DEBUG log
                                # print(len(buffer))
                                buffer[writeidx] = buffer[readidx]
#? CS/                          readidx++; readidx %= 4096;
                                readidx += 1; readidx %= 4096
#? CS/                          writeidx++; writeidx %= 4096;
                                writeidx += 1; writeidx %= 4096

                                j += 1
#? CS/                      fidx++;
                            fidx += 1

#? CS/                  flags8 >>= 1;
                        flags8 >>= 1
#? CS/                  if (fidx >= arcdata.Length) break;
                        if fidx >= arclength: break


                #░▄▀▀░█░▀█▀▒██▀░░░█▄▒▄█░█░▄▀▀░█▄▒▄█▒▄▀▄░▀█▀░▄▀▀░█▄█
                #▒▄██░█░█▄▄░█▄▄▒░░█▒▀▒█░█▒▄██░█▒▀▒█░█▀█░▒█▒░▀▄▄▒█▒█
#? CS/          if (decompressedSize != outdata.Count)
                # print('decompressedSize: ', decompressedSize) #! DEBUG log
                # print('outdata Size: ', len(outdata)) #! DEBUG log
                # print('BUFFER: ', BUFFER) #! DEBUG log
                if decompressedSize != len(outdata):
#? CS/              throw new Exception(string.Format("Size mismatch: got {0} bytes after decompression, expected {1}.\n", outdata.Count, decompressedSize));
                    raise Exception("Size mismatch: got {0:s} bytes after decompression, expected {1:s}.\n".format(len(outdata), decompressedSize))

                # print(outdata) #! DEBUG log
                with open('TerminaField_decomp.zsi', 'wb+') as outFile: # rb = read in Binary BYTE mode
                    for k in outdata:
                        outFile.write(k)
                    print(' >>> COMPLETE >>>')
                
#? CS/          return outdata.ToArray();
                return outdata


        #██████╗  ██████╗     ███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗
        #██╔══██╗██╔═══██╗    ██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝
        #██║  ██║██║   ██║    █████╗  ██║   ██║██╔██╗ ██║██║     ███████╗
        #██║  ██║██║   ██║    ██╔══╝  ██║   ██║██║╚██╗██║██║     ╚════██║
        #██████╔╝╚██████╔╝    ██║     ╚██████╔╝██║ ╚████║╚██████╗███████║
        #╚═════╝  ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝
        Decompress('TerminaField.zsi')
        

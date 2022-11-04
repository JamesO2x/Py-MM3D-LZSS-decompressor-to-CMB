using System; //! Not sure what this does.
using System.Collections.Generic; //! Not sure what this does.
using System.Linq; //! Not sure what this does.
using System.Text; //! Not sure what this does.
using System.IO; //! Not sure what this does.

namespace N3DSCmbViewer // ? The namespace keyword is used to declare a scope that contains a set of related objects. You can use a namespace to organize code elements and to create globally unique types.
{
    public class LZSS // ? The public keyword is an access modifier for types and type members. Public access is the most permissive access level. There are no restrictions on accessing public members, as in this example:
    {
        /* https://github.com/lue/MM3D/blob/master/src/lzs.cpp */
        public static byte[] Decompress(byte[] arcdata) //! Creates a new byte variable, I think "arcdata" implies "archived data" AKA compressed LzSS data in a binary format. Is Decompress a function? I'm not sure.
        {
            string tag = Encoding.ASCII.GetString(arcdata, 0, 4); //! Looks like it gets the first 4 bytes to figure out a "tag". The first 4 bytes in a MM3D LzS file are always "LzS(0x01)" or in other words "4C 7A 53 01" -- check a ZSI file in HxD to verify.
            uint unknown = BitConverter.ToUInt32(arcdata, 4); //! These next 4 bytes are uknown purpose. Could just be filler?
            uint decompressedSize = BitConverter.ToUInt32(arcdata, 8); //! Next 4 bytes contain a UInt32 of what the expected decompressed file size should be (little endian)
            uint compressedSize = BitConverter.ToUInt32(arcdata, 12); //! Next 4 bytes contain a UInt32 of what the expected compressed file size should be (little endian). This is used as a safety check when compressing/decompressing.

            if (arcdata.Length != compressedSize + 0x10) throw new Exception("compressed size mismatch"); //! compares the actual file archive length in bytes, to what we expect it to be. We have to add "+0x10 (16)" to the size to account for the 16-byte LzSS header. tag + unknown + decompressedSize + compressedSize = 16 byte length. 

            List<byte> outdata = new List<byte>(); //! Creates a new empty byte list, I think
            byte[] BUFFER = new byte[4096]; //! Create a buffer array/list of 4096 size
            for (int i = 0; i < BUFFER.Length; i++) BUFFER[i] = 0; //! # I think this loop just zeroes out the buffer.
            byte flags8 = 0; //! Not sure what these are for yet.
            ushort writeidx = 0xFEE;
            ushort readidx = 0;
            uint fidx = 0x10; //! Used as an index to loop through the whole file, starting at byte 16, it seems. I'm guessing this 16-byte starting point is to account for the LzSS header.

            while (fidx < arcdata.Length)
            {
                flags8 = arcdata[fidx]; //! I think this is reading one byte at the currend f Index var?
                fidx++;

                for (int i = 0; i < 8; i++)
                {
                    if ((flags8 & 1) != 0) //! Not sure what this is doing yet. Its checking a byte... but that's all I can figure out
                    {
                        outdata.Add(arcdata[fidx]);
                        BUFFER[writeidx] = arcdata[fidx];
                        writeidx++; writeidx %= 4096;
                        fidx++;
                    }
                    else
                    {
                        readidx = arcdata[fidx];
                        fidx++;
                        readidx |= (ushort)((arcdata[fidx] & 0xF0) << 4); //! I have no idea what this line does.
                        for (int j = 0; j < (arcdata[fidx] & 0x0F) + 3; j++)
                        {
                            outdata.Add(BUFFER[readidx]); //! adds data to the final output file data
                            BUFFER[writeidx] = BUFFER[readidx];
                            readidx++; readidx %= 4096;
                            writeidx++; writeidx %= 4096;
                        }
                        fidx++;
                    }
                    flags8 >>= 1;
                    if (fidx >= arcdata.Length) break;
                }
            }

            if (decompressedSize != outdata.Count)
                throw new Exception(string.Format("Size mismatch: got {0} bytes after decompression, expected {1}.\n", outdata.Count, decompressedSize));

            return outdata.ToArray();
        }
    }
}
using fin.util.asserts;
using fin.util.strings;

using schema;


namespace uni.platforms.threeDs.tools {
  public class LzssDecompressor {
    public bool TryToDecompress(EndianBinaryReader er, out byte[]? data) {
      if (er.TryReadNew(out LzssHeader? header)) {
        Asserts.Equal(er.Length, 0x10 + header!.CompressedSize);
        data = new byte[header.DecompressedSize];
        var dI = 0;

        var BUFFER = new byte[4096];
        ushort writeIndex = 0xFEE;
        while (!er.Eof) {
          var flags8 = er.ReadByte();

          for (var i = 0; i < 8; i++) {
            if ((flags8 & 1) != 0) {
              var decompressedByte = er.ReadByte();
              data[dI++] = decompressedByte;
              BUFFER[writeIndex] = decompressedByte;
              writeIndex++;
              writeIndex %= 4096;
            } else {
              var decompressedByte = er.ReadByte();
              ushort readIndex = decompressedByte;

              var someByte = er.ReadByte();
              readIndex |= (ushort) ((someByte & 0xF0) << 4);
              for (var j = 0; j < (someByte & 0x0F) + 3; j++) {
                data[dI++] = BUFFER[readIndex];
                BUFFER[writeIndex] = BUFFER[readIndex];
                readIndex++;
                readIndex %= 4096;
                writeIndex++;
                writeIndex %= 4096;
              }
            }

            flags8 >>= 1;
            if (er.Eof) {
              break;
            }
          }
        }
        Asserts.Equal(header.DecompressedSize, (uint) dI);

        return true;
      }

      data = null;
      return false;
    }
  }

  [BinarySchema]
  public partial class LzssHeader : IBiSerializable {
    private readonly string magic_ = "LzS" + AsciiUtil.GetChar(0x1);
    public uint Unknown { get; set; }
    public uint DecompressedSize { get; set; }
    public uint CompressedSize { get; set; }
  }
}
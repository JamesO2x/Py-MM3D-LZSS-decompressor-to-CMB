import math

from fin.util.asserts import *
from fin.util.strings import *

from schema import *


class uni: #this class replaces the original namespace 'uni'
  class platforms: #this class replaces the original namespace 'platforms'
    class threeDs: #this class replaces the original namespace 'threeDs'
      class tools: #this class replaces the original namespace 'tools'
        class LzssDecompressor:
          def TryToDecompress(self, er,  byte[]? data):
#C# TO PYTHON CONVERTER WARNING: Nullable reference types have no equivalent in Python:
#ORIGINAL LINE: if (er.TryReadNew(out LzssHeader? header))
#C# TO PYTHON CONVERTER TODO TASK: The following method call contained an unresolved 'out' keyword - these cannot be converted using the 'OutObject' helper class unless the method is within the code being modified:
            if er.TryReadNew(out header):
              #C# TO PYTHON CONVERTER TODO TASK: There is no Python equivalent to the C# 'null-forgiving operator':
              #ORIGINAL LINE: Asserts.Equal(er.Length, 0x10 + header!.CompressedSize)
              Asserts.Equal(er.Length, 0x10 + header.CompressedSize)
              data.arg_value = [0 for _ in range(header.DecompressedSize)]
              dI = 0

              BUFFER = [0 for _ in range(4096)]
              writeIndex = 0xFEE
              while not er.Eof:
                flags8 = er.ReadByte()

                for i in range(0, 8):
                  if (flags8 & 1) != 0:
                    decompressedByte = er.ReadByte()
#C# TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
#ORIGINAL LINE: data[dI++] = decompressedByte;
                    data.arg_value[dI] = decompressedByte
                    dI += 1
                    BUFFER[writeIndex] = decompressedByte
                    writeIndex += 1
                    writeIndex = math.fmod(writeIndex, 4096)
                  else:
                    decompressedByte = er.ReadByte()
                    readIndex = decompressedByte

                    someByte = er.ReadByte()
                    readIndex |= ((someByte & 0xF0) << 4)
                    j = 0
                    while j < (someByte & 0x0F) + 3:
#C# TO PYTHON CONVERTER WARNING: An assignment within expression was extracted from the following statement:
#ORIGINAL LINE: data[dI++] = BUFFER[readIndex];
                      data.arg_value[dI] = BUFFER[readIndex]
                      dI += 1
                      BUFFER[writeIndex] = BUFFER[readIndex]
                      readIndex += 1
                      readIndex = math.fmod(readIndex, 4096)
                      writeIndex += 1
                      writeIndex = math.fmod(writeIndex, 4096)
                      j += 1

                  flags8 >>= 1
                  if er.Eof:
                    break
              Asserts.Equal(header.DecompressedSize, dI)

              return True

            data.arg_value = None
            return False

#C# TO PYTHON CONVERTER TODO TASK: C# attributes do not have Python equivalents:
#ORIGINAL LINE: [BinarySchema] public partial class LzssHeader : IBiSerializable
        class LzssHeader(IBiSerializable):

          def __init__(self):
            #instance fields found by C# to Python Converter:
            self._magic_ = "LzS" + AsciiUtil.GetChar(0x1)
            self.Unknown = 0
            self.DecompressedSize = 0
            self.CompressedSize = 0


# Helper class added by C# to Python Converter:

# ----------------------------------------------------------------------------------------
#	Copyright © 2022 Tangible Software Solutions, Inc.
#	This class can be used by anyone provided that the copyright notice remains intact.
#
#	This class is used to replicate the ability to have 'out' parameters in Python.
# ----------------------------------------------------------------------------------------
class OutObject:
  def __init__(self):
    self.arg_value = None

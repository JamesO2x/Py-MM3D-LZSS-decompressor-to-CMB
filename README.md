# Py MM3D LZSS decompressor to CMB
 A python script that removes LZSS compression from Majora's Mask 3D ZSI files. It then also converts the ZSI file to CMB format. Now also works with Ocarina of Time 3D ZSI files.

## About
3D model files for *Majora's Mask 3D* are contained in a `.zsi` file format. Some of these files are also compressed using an algorithm called `LZSS`.

The best tool I've found so far for accurately ripping models from the game is the *Blender 2.79* addon at: [MeltyPlayer/OoT3D-Importer](https://github.com/MeltyPlayer/OoT3D-Importer)

Unfortunately, this addon only supports the loading of decompressed model files in `.cmb` file format. My python tools here will decompress and convert any `.zsi` to a common `.cmb` format, which the Blender addon can read.

---

## Usage Guide
Compiled EXE versions of the script are in the `dist` folder. You can use these instead if you don't have Python installed.

1. Make sure you have backups of your `.zsi` files somewhere safe.
2. Copy any `.zsi` models you want to convert into the `place_zsi_files_here` folder that sits in the same directory as the executable `zsi_conversion.exe`. 
	- This tool crawls down all sub-folders. You can copy every `.zsi` from the game and convert it all in one go, if you wish. And you can sort them into as many subfolders as you wish.
3. Run `zsi_conversion.exe` and follow the instructions.
4. After its done, you'll see `.cmb` and `.zsi_lzs_decomp` files next to all your `.zsi` files.
5. The `.cmb` files are what you want. The `.zsi_lzs_decomp` are temporary files (copies of the `.zsi` after LZSS decompression)
6. You'll also notice a file called `check_head_log.csv` in the directory of the `exe`. This file contains a log of all the files it scanned, and what "header" the file had, in a `csv` file format. You can use this log for further batch conversion in another program if you wish. Its a plain text file, it should open in any text editor or any spreadsheet program.

That's it.

### Optional Step 7
7. You can run `junk_cleanup.exe` in the same directory, which will crawl through all your subfolders and delete any of the `.zsi` and `.zsi_lzs_decomp` and `.zsidecomp` (old format) temporary files, so your folders are now only filled with `.cmb`. Just run that program and follow its instructions.

### Python 
For python instructions, follow above, but use the `.py` versions in the `src` folder instead.

---

## Credits & Thank You's
- Alvare, scurest, Starkium, and other members of [VG-Resource Forums](https://www.vg-resource.com/thread-28564-page-28.html)
- MeltyPlayer - [MeltyPlayer/OoT3D-Importer](https://github.com/MeltyPlayer/OoT3D-Importer) for the addon.
- xdanieldzd and NishaWolfe for: [NishaWolfe/N3DSCmbViewer: Zelda OoT3D & MM3D .cmb model viewer](https://github.com/NishaWolfe/N3DSCmbViewer) - as the basis for my CSharp conversion to Python of LZSS decompressor.
- Also [FinModelUtility/LzssDecompressor.cs](https://github.com/MeltyPlayer/FinModelUtility/blob/792c183a42761cc72f4a93dddff2faf607b9e309/FinModelUtility/UniversalModelExtractor/src/platforms/threeDs/tools/LzssDecompressor.cs) as basis for my Conversion.

---

## Final Notes:
This was only tested with "Scene" files from Majora's Mask 3D and Ocarina of Time 3D. It should in theory work with other Grezzo ZSI files, but I haven't tested it.

I may add the functionality of this python code directly into a fork of [MeltyPlayer/OoT3D-Importer](https://github.com/MeltyPlayer/OoT3D-Importer) some day. But no plans to so at the moment.

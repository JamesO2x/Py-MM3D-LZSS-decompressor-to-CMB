# RESOURCES
A generalized guide on making LZSS in python from scratch:
> [LZSS - The Hitchhiker's Guide to Compression](https://go-compression.github.io/algorithms/lzss/)

# Update 2022.11.02
This folder contains the LZSS C# code copied from `N3DSCmbViewer/LZSS.cs`

> The C# code from the N3DS Cmb Viewer, which already decodes LZSS:  
> [N3DSCmbViewer/LZSS.cs at 3c3f66cf40d9122f8d0ebeab07c4db659b426b8b · xdanieldzd/N3DSCmbViewer](https://github.com/xdanieldzd/N3DSCmbViewer/blob/3c3f66cf40d9122f8d0ebeab07c4db659b426b8b/N3DSCmbViewer/LZSS.cs)

My goal here is to comment every line, and figure out exactly what its doing. Then attempt to convert it to python. I don't know much about C#, so most of what I'm doing here is guesswork, just analyzing the basic logic of the code.

# Update 2022.11.03
Success! I did it. I managed to recreate the LzSS compression in python.

This version of the `.py` file has original *C#* code above each line (commented out) for comparison. It helped me analyze the code and repurpose it on a line-by-line basis.

> NOTE: Try to analyze the "FinModel" vesrion, and see if there's any effeciencies I could glean from it.


```
# ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗
#    ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║
#    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║
#    ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
# ##########################################################
# Read a file, and decompress it
# ##########################################################
```
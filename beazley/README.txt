Code from PyCon India 2019 Keynote Talk
David Beazley (https://www.dabeaz.com)
======================================

This code is presented "as is" and represents what was live-coded
during my closing keynote presentation at PyCon India, Chennai,
October 13, 2009.  I have made no changes to the files.

Requires:  Python 3.6+, numpy, pygame

Also Requires: https://github.com/aochagavia/rocket_wasm/blob/master/html/program.wasm

The final code runs a version of Rocket, which is found at:
https://aochagavia.github.io/blog/rocket---a-rust-game-running-on-wasm/

Rocket is a Rust program compiled to WebAssembly. I made no changes
to this code and used only the published program.wasm file found on
Aochagavia's site.

Here are some interesting links to projects involving WebAssembly and Python

1. The WebAssembly spec:  https://webassembly.github.io/spec/

2. Almar Klein's EuroPython 2018 talk. www.youtube.com/watch?v=u2kKxmb9BWs
   Highly recommended. He does other neat stuff with Rocket.

3. pyodide. (Scientific Stack on Web Assembly) github.com/iodide-project/pyodide

4. Pure Python Compiler Infrastructure (PPCI). https://ppci.readthedocs.io

5. Wasmer (https://wasmer.io)

The "wadze" library that I used to decode Wasm is a creation of mine. The
official source code for that is available at https://github.com/dabeaz/wadze
Wadze is a real project. Feedback welcome!

*** IMPORTANT DISCLAIMER *** 

This code was written/designed specifically for the purposes of giving
a talk and having something "work" in under an hour.  It takes a number
of liberties with the Wasm spec, is incomplete, and is almost
certainly not anything you would ever want to use.  That said: enjoy!

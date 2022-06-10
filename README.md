# Go and WebAssembly

The repostitory contains the source code for my talk about compiling Go applications into WebAssembly (wasm) and how WebAssembly works.

Check out [SLIDES](https://www.canva.com/design/DAFCzup8ZuU/bAdnsADxPAs6t2kJrCBHjA/view) from the talk.

## Wasm internals

The section covers how wasm work internally. It is based on the [A Talk Near the Future of Python](https://youtu.be/r-A78RgMhZU) screencast by David Beazley, and you should watch it. You can find in [beazley](./beazley) directory the code from his screencast cleaned up, actualized, and reformatted by me.

To run the code:

1. Install numpy and pygame.
1. Download [program.wasm](https://github.com/aochagavia/rocket_wasm/blob/master/html/program.wasm) and place it into `beazley` directory.
1. Run `python3 ./beazley/rocket.py`

**Exercise**: Try changing the implementation of sin and cos functions so that `sin` returns cosines, and `cos` returns sines. How does it affect the program?

## Hello world

To run this and all other examples, you'll need [task](http://taskfile.dev/) installed. Also, you'll need the Go compiler. Preferrably, the latest version.

The source code for this section is available in [hello](./hello) directory.

1. Run `task build -- ./hello` to produce the wasm binary and bootstrap code. You can find the output inside [frontend](./frontend) directory.
1. Run `task serve` to serve the content of `frontend` directory. Do it for all other steps too to see the result. Or just leave the server running from now on.
1. Open [localhost:1337](http://localhost:1337/). You should see a blank page.
1. Open Chrome DevTools (press F12). Switch to the "Console" tab. You should see the "oh hi mark" output.

**Exercise**: Try replacing `println` by `fmt.Println`. How does it affect the binary size?

## Calling JS from Go

The source code for this section is available in [js](./hello) directory. Compile and run it in the same way as you did in the previous section, just use `task build -- ./js` to build it.

**Exercise**: Replace `window.Get("document")` by `window.Get("nope")`. What do you see in Chrome Console?

## Using GWeb

[GWeb](https://github.com/life4/gweb) is a type-safe wrapper around Web API (JS calls). The sections shows a basic example of using it. You cna fid the source code for the section in [gweb](./gweb) directory. Do the same steps as before to compile and run it.

You can find more examples at [gweb.orsinium.dev](https://gweb.orsinium.dev/).

**Exercise**: Make the page to show the current time. What time is it? When does it get updated?

## Reducing the binary size using TinyGo

For this section you need to install [TinyGo](https://tinygo.org/). Try running `task install:tinygo`, it might work. If it doesn't, just follow the official installation instructions.

1. Compile the code from the previous section using TinyGo: `task tiny_build -- ./gweb`. Check if it works. Note the new size of the binary. On my machine, it dropped from 1.6M to 198K.
1. Compile the same code without the scheduler: `task tiny_build -- -scheduler=none ./gweb`. Check if it works. Note the new size of the binary. On my machine, it's now 152K.
1. Now, compile the first example without scheduler and with leaky GC (allocates but never frees): `task tiny_build -- -scheduler=none -gc=leaking ./hello`. Check if it works. What's the new size? On my machine, it dropped from 1.2M to 29K.

**Exercise**: Try building with `-gc=none` option. What's the size? Does it work?

## Reducing the binary size using Binaryen

For this section, you'll need [binaryen](https://github.com/WebAssembly/binaryen). Try installing it using `task install:binaryen`. If it doesn't work, manually download the latest release for your OS from Github releases.

1. Build any of the examples from previous sections. For example, build gweb example using tinygo: `task tiny_build -- -scheduler=none ./gweb`.
1. Run `task optimize`. Check if it works. Note the new binary size.

On my machine, the size of `hello` (with leaking GC) drops from 29K to 25K and the size of `gweb` drops from 100K to 89K.

## WASI

The section covers compiling system applications into WASM with [WASI](https://wasi.dev/) system interface using TinyGo. To run the wasm binary from the terminal you need to install [wasmtime](https://wasmtime.dev/). Try running `task install:wasmtime`. If it doesn't work, follow the official installation guide.

1. Build the binary: `task wasi:build`
1. Run it with wasmtine: `task wasi:run`

**Exercise**: Build the same `hello` example targeting `wasm` and `wasi`. Does the file size differ?

## Further reading

1. [WebAssembly guides on MDN](https://developer.mozilla.org/en-US/docs/WebAssembly)
1. [GWeb documentation](https://github.com/life4/gweb)
1. [AssemblyScript language](https://www.assemblyscript.org/)

mkdir -p build
cp frontend/* build/
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" build/runner.js
GOOS=js GOARCH=wasm go build -o build/frontend.wasm .

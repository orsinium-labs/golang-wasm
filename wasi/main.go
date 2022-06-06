package main

import (
	"fmt"
	"io/ioutil"
)

func main() {
	fmt.Println("I'm in the console")
	text := []byte("I'm in the file\n")
	err := ioutil.WriteFile("./log.txt", text, 0644)
	if err != nil {
		panic(err)
	}
}

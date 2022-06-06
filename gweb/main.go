package main

import "github.com/life4/gweb/web"

func main() {
	window := web.GetWindow()
	doc := window.Document()
	doc.SetTitle("Welcome page")
	header := doc.CreateElement("h1")
	header.SetText("oh hi mark")
	body := doc.Body()
	body.Node().AppendChild(header.Node())
}

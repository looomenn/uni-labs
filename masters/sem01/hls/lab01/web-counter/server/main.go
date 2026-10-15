package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
)

// fmt: for formatiing strings and printing to the console
// log: for logging errors and messages
// net/http: for creating the HTTP server and handling requests

type Counter interface {
	Inc() error
	Get() (int64, error)
	Reset() error
}


// var counter Counter: declares a variable with type interface
// MemoryCounter: creates an instance of the MemoryCounter struct with default values.
// &MemoryCounter{}: returns a pointer to the newly created MemoryCounter instance
var counter Counter = &MemoryCounter{}


// w http.ResponseWriter:
//   - used to form the HTTP response to send back to the client
// r *http.Request:
//   - pointer to the struct that contains all the info about the request
//   made by the client
func countHandler(w http.ResponseWriter, r *http.Request) {
	value, err := counter.Get()

	if err != nil {
		http.Error(w, "Failed to get counter", http.StatusInternalServerError)
		return
	}

	fmt.Fprintln(w, value)
}


func incHandler(w http.ResponseWriter, r *http.Request) {
	if err := counter.Inc(); err != nil {
		http.Error(w, "Failed to increment counter", http.StatusInternalServerError)
		return
	}

	fmt.Fprintln(w, "ok")
}


func resetHandler(w http.ResponseWriter, r *http.Request) {
	if err := counter.Reset(); err != nil {
		http.Error(w, "Failed to reset counte", http.StatusInternalServerError)
		return
	}

	fmt.Fprintln(w, "ok")
}


func main(){
	// flag.String() returns *string(), not the value itself
	addr := flag.String("addr", ":8080", "HTTP Server address")
	flag.Parse()

	// register the handler function for the /count endpoint
	http.HandleFunc("GET /count", countHandler)
	http.HandleFunc("GET /inc", incHandler)
	http.HandleFunc("GET /reset", resetHandler)

	log.Printf("Server started on %s", *addr)

	// nil: use the default ServeMux to handle requests
	log.Fatal(http.ListenAndServe(*addr, nil))
}

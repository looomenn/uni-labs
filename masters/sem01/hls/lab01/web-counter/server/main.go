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
// declared the variable without assigning a specific implementation to it.
// starting value = nil
var counter Counter


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
	// cli arguments format: <cli-flag>, <default-value>, <help-text>

	// flag.String() returns *string(), not the value itself
	addr := flag.String("addr", ":8080", "HTTP Server address")
	storage := flag.String("storage", "memory", "Counter storage type")
	filePath := flag.String("file", "counter.dat", "Counter storage file path")
	flag.Parse()

	switch *storage {
	case "memory":
		counter = &MemoryCounter{}
	
	case "disk":
		diskCounter, err := NewDiskCounter(*filePath)
		if err != nil {
			log.Fatalf("Failed to init disk counter: %v", err)
		}
		
		counter = diskCounter
	
	default:
		log.Fatalf("Uknown storage type: %s", *storage)
	}

	// register the handler function for the /count endpoint
	http.HandleFunc("GET /count", countHandler)
	http.HandleFunc("GET /inc", incHandler)
	http.HandleFunc("GET /reset", resetHandler)

	log.Printf("Server started on %s", *addr)

	// nil: use the default ServeMux to handle requests
	log.Fatal(http.ListenAndServe(*addr, nil))
}

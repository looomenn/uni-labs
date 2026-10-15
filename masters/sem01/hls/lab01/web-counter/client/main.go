package main

import (
	"fmt"
	"io"
	"log"
	"flag"
	"net/http"
)

func main() {
	httpClient := &http.Client{}

	requestsPerClient := 5
	failedRequests := 0

	for requestIndex := 0; requestIndex < requestsPerClient; requestIndex++{
		err := sendRequest(httpClient, "http://localhost:8080/inc")

		if err != nil {
			failedRequests++
			log.Printf("Request %d failed: %v", requestIndex+1, err)
		}
	}

	successfulRequest := requestsPerClient - failedRequests

	fmt.Printf("total reqs: %d\n", requestsPerClient)
	fmt.Printf("successful: %d\n", successfulRequest)
	fmt.Printf("failed: %d\n", failedRequests)


	fmt.Println("Request completed successfully")
}

func sendRequest(httpClient *http.Client, url string) error {
	response, err := httpClient.Get(url)
	if err != nil {
		return fmt.Errorf("failed to send request: %w", err)
	}
	defer response.Body.Close()

	_, err = io.Copy(io.Discard, response.Body)
	if err != nil {
		return fmt.Errorf("failed to read response: %w", err)
	}

	if response.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected HTTP status: %s", response.Status)
	}

	return nil
}

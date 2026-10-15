package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"strings"
	"net/http"
	"sync/atomic"
)

func main() {
	requestsPerClient := flag.Int("requests", 10000, "Number of requests per client")
	baseURL := flag.String("url", "http://localhost:8080", "Base URL of the server")
	clients := flag.Int("clients", 1, "Number of clients")
	
	flag.Parse()

	if *requestsPerClient <= 0 {
		log.Fatalf(
			"Number of requests per client must be greater than 0. Got: %d",
			*requestsPerClient,
		)
	}

	if *clients <= 0 {
		log.Fatalf(
			"Number of clients must be greater than 0. Got: %d",
			*clients,
		)
	}

	// future url tests goes here
	// i'm not writing quasi ifs to check if given url has port in it

	httpClient := &http.Client{}
	endpoint := strings.TrimRight(*baseURL, "/") + "/inc"

	var failedRequests atomic.Int64
	runRequests(httpClient, endpoint, *requestsPerClient, &failedRequests)

	successfulRequests := int64(*requestsPerClient) - failedRequests.Load()

	fmt.Printf("total reqs: %d\n", *requestsPerClient)
	fmt.Printf("successful: %d\n", successfulRequests)
	fmt.Printf("failed: %d\n", failedRequests.Load())
}

func runRequests(
	httpClient *http.Client,
	endpoint string,
	requestsPerClient int,
	failedRequests *atomic.Int64,
) {
	for requestIndex := 0; requestIndex < requestsPerClient; requestIndex++ {
		err := sendRequest(httpClient, endpoint)

		if err != nil {
			failedRequests.Add(1)
			log.Printf("Request %d failed: %v", requestIndex+1, err)
		}
	}
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


package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"sync"
	"sync/atomic"
	"time"
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

	// settings for keep-live
	transport := &http.Transport{
		MaxIdleConns: 100,
		MaxIdleConnsPerHost: 100,
	}
	httpClient := &http.Client{
		Transport: transport,
	}
	endpoint := strings.TrimRight(*baseURL, "/") + "/inc"

	var failedRequests atomic.Int64
	var waitGroup sync.WaitGroup
	start := make(chan struct{})

	for clientIndex := 0; clientIndex < *clients; clientIndex++ {
		waitGroup.Add(1)

		go func() {
			defer waitGroup.Done()

			<-start

			runRequests(
				httpClient,
				endpoint,
				*requestsPerClient,
				&failedRequests,
			)
		}()
	}

	startTime := time.Now()

	close(start)
	waitGroup.Wait()

	elapsed := time.Since(startTime)
	totalRequests := int64(*clients) * int64(*requestsPerClient)
	successfulRequests := totalRequests - failedRequests.Load()

	rps := float64(totalRequests) / elapsed.Seconds()

	fmt.Printf("total clients: %d\n", *clients)
	fmt.Printf("total requests: %d\n", totalRequests)
	fmt.Printf("\tsuccessful: %d\n", successfulRequests)
	fmt.Printf("\tfailed: %d\n", failedRequests.Load())
	fmt.Printf("elased: %.4f s\n", elapsed.Seconds())
	fmt.Printf("rps: %.2f s\n", rps)
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

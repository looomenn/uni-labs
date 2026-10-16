package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
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
	serverURL := strings.TrimRight(*baseURL, "/")

	incrementURL := serverURL + "/inc"
	resetURL := serverURL + "/reset"
	countURL := serverURL + "/count"

	var failedRequests atomic.Int64
	var waitGroup sync.WaitGroup
	start := make(chan struct{})

	if err := sendRequest(httpClient, resetURL); err != nil {
		log.Fatalf("Failed to reset counter: %v", err)
	}

	for clientIndex := 0; clientIndex < *clients; clientIndex++ {
		waitGroup.Add(1)

		go func() {
			defer waitGroup.Done()

			<-start

			runRequests(
				httpClient,
				incrementURL,
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
	totalErrors := failedRequests.Load()
	successfulRequests := totalRequests - totalErrors
	rps := float64(totalRequests) / elapsed.Seconds()

	counterValue, err := getCounterValue(httpClient, countURL)
	if err != nil {
		log.Fatalf("failed to get counter value: %v", err)
	}

	fmt.Printf("clients: %d\n", *clients)
	fmt.Printf("requests: %d\n", totalRequests)
	fmt.Printf("\tsuccessful: %d\n", successfulRequests)
	fmt.Printf("\tfailed: %d\n", totalErrors)
	fmt.Printf("elased: %.4f s\n", elapsed.Seconds())
	fmt.Printf("rps: %.2f req/s\n", rps)

	fmt.Printf("counter value: %d (expected %d)\n", counterValue, totalRequests)

	if counterValue != totalRequests {
		log.Fatalf(
			"Counter mismatch: expected %d, got %d",
			totalRequests,
			counterValue,
		)
	}
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

func getCounterValue(
	httpClient *http.Client,
	url string,
) (int64, error) {
	response, err := httpClient.Get(url)
	if err != nil {
		return 0, fmt.Errorf("Failed to send request: %w", err)
	}

	defer response.Body.Close()

	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		return 0, fmt.Errorf("failed to read HTTP body: %w", err)
	}

	if response.StatusCode != http.StatusOK {
		return 0, fmt.Errorf("unexpected HTTP status: %s", response.Status)
	}

	responseText := strings.TrimSpace(string(responseBody))

	value, err := strconv.ParseInt(responseText, 10, 64)
	if err != nil {
		return 0, fmt.Errorf("failed to prase int value: %w", err)
	}

	return value, nil
}

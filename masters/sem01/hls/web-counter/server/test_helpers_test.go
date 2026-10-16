package main

import "testing"

func assertCounterValue(test *testing.T, counter Counter, expected int64) {
	test.Helper()

	actual, err := counter.Get()
	if err != nil {
		test.Fatalf("Failed to read counter: %v", err)
	}

	if actual != expected {
		test.Errorf("Expected counter to be %d, got %d", expected, actual)
	}
}

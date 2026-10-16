package main

import (
	"sync"
	"testing"
)

func TestMemoryCounter(test *testing.T) {
	memoryCounter := &MemoryCounter{}

	assertCounterValue(test, memoryCounter, 0)

	for increment := 0; increment < 5; increment++ {
		if err := memoryCounter.Inc(); err != nil {
			test.Fatalf("Failed to increment counter: %v", err)
		}
	}

	assertCounterValue(test, memoryCounter, 5)

	if err := memoryCounter.Reset(); err != nil {
		test.Fatalf("Failed to reset counter: %v", err)
	}

	assertCounterValue(test, memoryCounter, 0)
}

func TestMemoryCounterConcurrent(test *testing.T) {
	var waitGroup sync.WaitGroup

	memoryCounter := &MemoryCounter{}
	assertCounterValue(test, memoryCounter, 0)

	for workerIndex := 0; workerIndex < 10; workerIndex++ {
		waitGroup.Add(1)

		go func () {
			defer waitGroup.Done()

			for increment := 0; increment < 1000; increment++ {
				if err := memoryCounter.Inc(); err != nil {
					test.Errorf("Failed to increment counter: %v", err)
					return
				}
			}
		} ()
	}

	waitGroup.Wait()

	assertCounterValue(test, memoryCounter, 10000)
}

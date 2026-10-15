package main

import (
	"sync"
	"path/filepath"
	"testing"
)

func TestDiskCounterIncOnNewFile(test *testing.T) {
	filePath := filepath.Join(test.TempDir(), "counter.dat")

	diskCounter, err := NewDiskCounter(filePath)
	if err != nil {
		test.Fatalf("Failed to create disk counter: %v", err)
	}
	defer diskCounter.file.Close()

	err = diskCounter.Inc()
	if err != nil {
		test.Fatalf("Failed to increment counter: %v", err)
	}

	value, err := diskCounter.Get()
	if err != nil {
		test.Fatalf("Failed to read counter: %v", err)
	}

	if value != 1 {
		test.Errorf("Expected counter to be 1, got %d", value)
	}

}

func TestDiskCounterPersistence(test *testing.T) {
	filePath := filepath.Join(test.TempDir(), "counter.dat")

	firstCounter, err := NewDiskCounter(filePath)
	if err != nil {
		test.Fatalf("Failed to create disk counter: %v", err)
	}

	for increment := 0; increment < 2; increment++ {
		if err := firstCounter.Inc(); err != nil {
			firstCounter.file.Close()
			test.Fatalf("Failed to increment counter: %v", err)
		}
	}

	if err := firstCounter.file.Close(); err != nil {
		test.Fatalf("Failed to close counter file: %v", err)
	}

	secondCounter, err := NewDiskCounter(filePath)
	if err != nil {
		test.Fatalf("Failed to reopen counter: %v", err)
	}
	defer secondCounter.file.Close()

	value, err := secondCounter.Get()
	if err != nil {
		test.Fatalf("Failed to read counter: %v", err)
	}

	if value != 2 {
		test.Errorf("Expected counter to be 2, got %d", value)
	}
}

func TestDiskCounterReset(test *testing.T) {
	filePath := filepath.Join(test.TempDir(), "counter.dat")

	diskCounter, err := NewDiskCounter(filePath)
	if err != nil {
		test.Fatalf("Failed to create disk counter: %v", err)
	}
	defer diskCounter.file.Close()

	for increment := 0; increment < 3; increment++ {
		if err := diskCounter.Inc(); err != nil {
			test.Fatalf("Failed to increment counter: %v", err)
		}
	}

	assertCounterValue(test, diskCounter, 3)

	if err := diskCounter.Reset(); err != nil {
		test.Fatalf("Failed to reset counter: %v", err)
	}

	assertCounterValue(test, diskCounter, 0)
}

func TestDiskCounterConcurrent(test *testing.T) {
	var waitGroup sync.WaitGroup

	filePath := filepath.Join(test.TempDir(), "counter.dat")

	diskCounter, err := NewDiskCounter(filePath)
	if err != nil {
		test.Fatalf("Failed to create disk counter: %v", err)
	}

	defer diskCounter.file.Close()

	assertCounterValue(test, diskCounter, 0)
	
	for workerIndex := 0; workerIndex < 4; workerIndex++ {
		waitGroup.Add(1)

		go func () {
			defer waitGroup.Done()

			for increment := 0; increment < 10; increment++ {
				if err := diskCounter.Inc(); err != nil {
					test.Errorf("Failed to increment counter: %v", err)
					return
				}
			}
		} ()
	}

	waitGroup.Wait()
	assertCounterValue(test, diskCounter, 40)
}
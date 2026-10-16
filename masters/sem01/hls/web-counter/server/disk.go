package main

import (
	"os"
	"sync"
	"encoding/binary"
	"io"
	"fmt"
	"math"
)


type DiskCounter struct {
	mutex sync.Mutex
	file *os.File
}


func NewDiskCounter(path string) (*DiskCounter, error) {

	// os.O_RDWR: open for read and write
	// os.O_CREATE: create the file if it doesn't exist 
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0644)
	if err != nil {
		return nil, err
	}

	return &DiskCounter {
		file: f,
	}, nil
}


func (counter *DiskCounter) Get() (int64, error) {
	counter.mutex.Lock()

	// defer postpones the execution of a func call untill the surrouding func returns
	// so, pustpones Unlock() call till the Get() returns
	defer counter.mutex.Unlock()

	var buf [8]byte

	// byf[:]: slice buf[] which refers to all 8 elements in this array;
	//  	   points where to write bytes
	// 0: start from file's 0 byte
	// n: number of total bytes red
	// err: any error while reading
	n, err := counter.file.ReadAt(buf[:], 0)

	if err == io.EOF && n == 0 {
		return 0, nil
	}

	if err != nil {
		return 0, nil
	}

	value := int64(binary.LittleEndian.Uint64(buf[:]))

	return value, nil
}


func (counter *DiskCounter) Inc() error {
	counter.mutex.Lock()
	defer counter.mutex.Unlock()

	var buf [8]byte

	n, err := counter.file.ReadAt(buf[:], 0)

	if err == io.EOF && n == 0 {
		err = nil
	}

	if err != nil {
		return fmt.Errorf("read counter: %w", err)
	}

	value := int64(binary.LittleEndian.Uint64(buf[:]))

	if value == math.MaxInt64 {
		return fmt.Errorf("Counter overflow")
	}

	value++

	binary.LittleEndian.PutUint64(buf[:], uint64(value))

	if _, err := counter.file.WriteAt(buf[:], 0); err != nil {
		return fmt.Errorf("write counter: %w", err)
	}

	if err := counter.file.Sync(); err != nil {
		return fmt.Errorf("sync counter: %w", err)
	}

	return nil
}


func (counter *DiskCounter) Reset() error {
	counter.mutex.Lock()
	defer counter.mutex.Unlock()

	var buf [8]byte

	if _, err := counter.file.WriteAt(buf[:], 0); err != nil {
		return fmt.Errorf("reset counter: %w", err)
	}

	if err := counter.file.Sync(); err != nil {
		return fmt.Errorf("sync counter: %w", err)
	}

	return nil
}
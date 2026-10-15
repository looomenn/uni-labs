package main

import "sync/atomic"
// atomic: contains low-level atomic memory primitives for sync algos

type MemoryCounter struct {
	value atomic.Int64
}


// c *MemoryCounter: receiver of the method, allows access to the MemoryCounter instance
// *MemoryCounter: pointer to the MemoryCounter struct
// Inc: method to increment the counter value atomically
// error: return type indicating that the method may return an error
func (c *MemoryCounter) Inc() error {
	c.value.Add(1)
	return nil
}


func (c *MemoryCounter) Get() (int64, error) {
	return c.value.Load(), nil
}


func (c *MemoryCounter) Reset() error {
	c.value.Store(0)
	return nil
}

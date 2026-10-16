# Web Counter

A small Go HTTP server and load-testing client for comparing in-memory and disk-backed counters under concurrent requests.

## Requirements

- [Go](https://go.dev/dl/) installed and available on `PATH` (use a version supported by `go.mod`)
- Windows: PowerShell 5.1 or later, for `run-benchmarks.ps1`
- macOS / Linux: Bash, for `run-benchmarks.sh`
- No third-party Go packages are required by the benchmark scripts

Check your installation with `go version`.

## Project structure

```text
web-counter/
├── go.mod
├── server/
│   ├── main.go
│   ├── memory.go
│   ├── disk.go
│   └── *_test.go
├── client/
│   └── main.go
├── run-benchmarks.ps1
├── run-benchmarks.sh
└── results/
    ├── benchmarks/        # Generated when scripts run
    └── profiles/          # Optional pprof files
```

## Server

The server exposes the following GET endpoints:

| Endpoint | Action                    |
| -------- | ------------------------- |
| `/inc`   | Increment the counter     |
| `/count` | Read the current value    |
| `/reset` | Reset the counter to zero |

The memory mode uses an atomic integer. The disk mode stores the value in a file, serializes updates with a mutex, and calls `Sync()` after writing.

Run the server from this directory:

```bash
go run ./server -storage=memory -addr=127.0.0.1:8080
```

Or enable disk storage:

```bash
go run ./server -storage=disk -addr=127.0.0.1:8080 -file=counter.dat
```

## Client

In another terminal, run:

```bash
go run ./client -clients=10 -requests=10000 -url=http://127.0.0.1:8080
```

The client resets the counter before the run, sends the specified number of requests per client, measures elapsed time, calculates RPS, and checks the final counter value. The `-requests` value is per client, not the total.

## Run all benchmarks

The scripts build the server and client once, start the server for each storage mode, and run 1, 2, 5, and 10 clients × 10,000 requests per client. They save one text log per scenario, stop the server, and remove temporary executables. Do not leave another server running on port 8080.

**Windows (PowerShell):**

```powershell
.\run-benchmarks.ps1
```

If script execution is blocked by PowerShell policy, use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\run-benchmarks.ps1
```

Change the port or request count if needed:

```powershell
.\run-benchmarks.ps1 -Port 8081 -RequestsPerClient 100
```

**macOS / Linux (Bash):**

```bash
bash ./run-benchmarks.sh
```

Optional overrides:

```bash
PORT=8081 REQUESTS_PER_CLIENT=100 bash ./run-benchmarks.sh
```

Each run creates a directory under `results/benchmarks/` with logs such as `memory-clients-5.txt` and `disk-clients-10.txt`. Both scripts can be invoked from any working directory as long as they remain in the project root.
Note: Disk benchmarks may take several minutes because each increment `calls Sync()`. Benchmark runs do not enable CPU profiling.

## Tests

Run the Go tests:

```bash
go test ./server
```

Optionally use the race detector:

```bash
go test -race ./server
```

The race detector requires a supported C compiler on some platforms, including Windows.

## CPU profiling

The server exposes Go's pprof endpoints under `/debug/pprof/`. With the server running, capture a 10-second CPU profile:

```bash
curl -o memory.pprof 'http://127.0.0.1:8080/debug/pprof/profile?seconds=10'
go tool pprof -http=127.0.0.1:9090 memory.pprof
```

Run the client while the profile is being collected. The memory-mode workload may need more requests to keep the server busy throughout the sampling period. Open View → Flame Graph in the pprof UI. For Windows, use curl.exe rather than the PowerShell alias curl if applicable

# HLS-Lab01: Web Counter

This lab explores how concurrent HTTP requests affect a shared counter, and how the storage method changes server throughput.

The Go implementation, test scripts, and usage instructions are in [web-counter/](../web-counter/).

The experiment compares two storage modes (in-memory and disk-backed) with 1, 2, 5, and 10 clients sending 10,000 requests each. Results are evaluated using requests per second (RPS) and CPU flame graphs.

To run all eight benchmark scenarios, open a terminal in `web-counter/` and follow its README. Go must be installed. The scripts support Windows (PowerShell) and macOS/Linux (Bash).

# Run all WebCounter benchmars on Windows (or at least attempt to do so)

param (
    [int]$Port = 8080,
    [int]$RequestsPerClient = 10000
)

$ErrorActionPreference = 'Stop'

if (-not (Get-Command go -ErrorAction SilentlyContinue)) {
    throw 'Go is required: https://go.dev/dl/'
}

$results = Join-Path $PSScriptRoot ("results/benchmarks/" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$tmp = Join-Path ([IO.Path]::GetTempPath()) ("webcounter-" + [guid]::NewGuid().ToString('N'))
$serverExe = Join-Path $tmp 'server.exe'
$clientExe = Join-Path $tmp 'client.exe'
$server = $null

New-Item -ItemType Directory -Force -Path $results, $tmp | Out-Null
Push-Location $PSScriptRoot

try {
    go build -o $serverExe ./server
    if ($LASTEXITCODE -ne 0) { throw 'Server build failed' }

    go build -o $clientExe ./client
    if ($LASTEXITCODE -ne 0) { throw 'Client build failed' }

    foreach ($mode in 'memory', 'disk') {
        $server = Start-Process -FilePath $serverExe -PassThru -NoNewWindow `
            -ArgumentList "-storage=$mode -file=`"$tmp\counter.dat`" -addr=127.0.0.1:$Port" `
            -RedirectStandardOutput (Join-Path $results "$mode-server.out.log") `
            -RedirectStandardError (Join-Path $results "$mode-server.err.log")

        Start-Sleep -Seconds 1
        if ($server.HasExited) { throw "Server failed. Check $results/$mode-server.err.log" }

        foreach ($clients in 1, 2, 5, 10) {
            Write-Host "`n+----+ ${mode}: $clients client(s) +----+"
            & $clientExe "-clients=$clients" "-requests=$RequestsPerClient" "-url=http://127.0.0.1:$Port" |
                Tee-Object -FilePath (Join-Path $results "$mode-$clients.txt")
            if ($LASTEXITCODE -ne 0) { throw "Benchmark failed: $mode / $clients clients" }
        }

        Stop-Process -Id $server.Id -Force
        $server.WaitForExit()
        $server.Dispose()
        $server = $null
    }

    Write-Host "Done. Results: $results"
}
finally {
    if ($server) {
        if (-not $server.HasExited) { Stop-Process -Id $server.Id -Force }
        $server.Dispose()
    }
    Pop-Location
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}

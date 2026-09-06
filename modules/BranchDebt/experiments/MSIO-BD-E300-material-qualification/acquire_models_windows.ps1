param(
    [Parameter(Mandatory = $true)][string]$Token,
    [string]$Target = 'D:\Temp\ModelStateIO-BranchDebt-E300',
    [string]$Proxy = 'http://127.0.0.1:7897'
)

$ErrorActionPreference = 'Stop'
if ($Token -ne 'ACQUIRE-MSIO-BD-E300') {
    throw 'authorization token mismatch'
}
$expectedTarget = 'D:\Temp\ModelStateIO-BranchDebt-E300'
if ([IO.Path]::GetFullPath($Target) -ne [IO.Path]::GetFullPath($expectedTarget)) {
    throw "target must equal $expectedTarget"
}

$manifest = Join-Path $PSScriptRoot 'MODEL_ACQUISITION.tsv'
$rows = Import-Csv -LiteralPath $manifest -Delimiter "`t"
New-Item -ItemType Directory -Path $Target -Force | Out-Null
$lockPath = Join-Path $Target '.acquire.lock'
$lock = [IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None')
try {
    foreach ($row in $rows) {
        if ($row.model -like 'Qwen2.5-7B-*') {
            $repo = 'Qwen/Qwen2.5-7B-Instruct-GGUF'
        } elseif ($row.model -like 'Qwen2.5-14B-*') {
            $repo = 'Qwen/Qwen2.5-14B-Instruct-GGUF'
        } elseif ($row.model -like 'Qwen2.5-32B-*') {
            $repo = 'Qwen/Qwen2.5-32B-Instruct-GGUF'
        } else {
            throw "unexpected model: $($row.model)"
        }
        $final = Join-Path $Target $row.file
        $partial = "$final.part"
        if (Test-Path -LiteralPath $final) {
            $item = Get-Item -LiteralPath $final
            $digest = (Get-FileHash -LiteralPath $final -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($item.Length -eq [int64]$row.bytes -and $digest -eq $row.sha256) {
                "verified-existing`t$($row.file)`t$($row.bytes)`t$digest"
                continue
            }
            throw "refusing mismatched final file: $final"
        }
        if ((Test-Path -LiteralPath $partial) -and
            (Get-Item -LiteralPath $partial).Length -gt [int64]$row.bytes) {
            throw "oversized partial file: $partial"
        }
        $url = "https://huggingface.co/$repo/resolve/$($row.revision)/$($row.file)"
        "download`t$($row.file)`t$url"
        & curl.exe --fail --location --retry 2 --retry-delay 5 `
            --connect-timeout 20 --max-time 21600 --speed-limit 1024 `
            --speed-time 60 --continue-at - --proxy $Proxy --output $partial $url
        if ($LASTEXITCODE -ne 0) { throw "curl failed with $LASTEXITCODE for $url" }
        $item = Get-Item -LiteralPath $partial
        $digest = (Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($item.Length -ne [int64]$row.bytes -or $digest -ne $row.sha256) {
            throw "identity mismatch for $partial"
        }
        Move-Item -LiteralPath $partial -Destination $final
        "verified-new`t$($row.file)`t$($row.bytes)`t$digest"
    }
    "complete`t$([DateTime]::UtcNow.ToString('o'))"
} finally {
    $lock.Dispose()
}

#!/usr/bin/env powershell

Param(
    [Parameter(Mandatory=$False, Position=0)]
    [String]$Pattern = "*"
)

$ErrorActionPreference = "Stop"

$script:numTests = 0
$script:numFailures = 0

function RunTest($type, $ext) {
    ++$script:numTests
    $expectedFile = Get-Item (Join-Path $filesDir ($child.BaseName + ".$ext"))
    Write-Verbose "Running test on file $($expectedFile.Name)"
    $expected = Get-Content $expectedFile
    $actual = pandoc $child.FullName -t $type --filter linguafilter
    # if $actual is not equal to $expected
    if (Compare-Object $actual $expected) {
        Write-Host "The pandoc output does not match the file." -ForegroundColor Red -BackgroundColor Black
        $actualSpaces = " " * $expectedFile.Name.Length
        Write-Host "Actual:      $actualSpaces$actual" -ForegroundColor Red -BackgroundColor Black
        Write-Host "Expected ($($expectedFile.Name)): $expected" -ForegroundColor Red -BackgroundColor Black
        Write-Host
        ++$script:numFailures
    }
}

$filesDir = Join-Path $PSScriptRoot files
$children = Get-ChildItem (Join-Path $filesDir "$Pattern.md")
foreach ($child in $children) {
    RunTest "html" "html"
    RunTest "latex" "tex"
}

$testsPlural = if ($script:numTests -eq 1) {"test"} else {"tests"}
if ($script:numFailures -gt 0) {
    Write-Host "Ran $script:numTests $testsPlural, $script:numFailures failed." -ForegroundColor Red -BackgroundColor Black
    exit 1
} else {
    Write-Host "$script:numTests $testsPlural passed!" -ForegroundColor Green -BackgroundColor Black
}


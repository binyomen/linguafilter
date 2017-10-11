#!/usr/bin/env powershell

$ErrorActionPreference = "Stop"

$numTests = 0

function RunTest($type, $ext) {
    $actual = pandoc $child.FullName -t $type --filter linguafilter
    $expectedFile = Get-Item (Join-Path $filesDir ($child.BaseName + ".$ext"))
    $expected = Get-Content $expectedFile
    if ($actual -ne $expected) {
        Write-Host "The pandoc output does not match the file." -ForegroundColor Red -BackgroundColor Black
        Write-Host "Actual: $actual" -ForegroundColor Red -BackgroundColor Black
        Write-Host "Expected ($($expectedFile.Name)): $expected" -ForegroundColor Red -BackgroundColor Black
        $testsPlural = if ($numTests -eq 1) {"test"} else {"tests"}
        Write-Host "Ran $numTests $testsPlural." -ForegroundColor Red -BackgroundColor Black
        exit 1
    }
}

$filesDir = Join-Path $PSScriptRoot files
$children = Get-ChildItem (Join-Path $filesDir *.md)
foreach ($child in $children) {
    ++$numTests
    RunTest "html" "html"
    RunTest "latex" "tex"
}

$testsPlural = if ($numTests -eq 1) {"test"} else {"tests"}
Write-Host "$numTests $testsPlural passed!" -ForegroundColor Green -BackgroundColor Black

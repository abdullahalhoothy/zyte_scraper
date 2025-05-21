' Silent PowerShell Script Runner for zyte_scraper sync
' Runs the sync script without any visible windows

Dim objShell
Set objShell = CreateObject("WScript.Shell")

' Run PowerShell script completely hidden
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""F:\git\zyte_scraper\sync_zyte_scraper.ps1""", 0, False

Set objShell = Nothing

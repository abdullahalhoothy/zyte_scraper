# Create Scheduled Task for Zyte Scraper Sync
# This script creates an hourly scheduled task to run the sync script

$ErrorActionPreference = "Stop"

# Task configuration
$taskName = "Zyte Scraper Hourly Sync"
$taskDescription = "Syncs zyte_scraper folder from F: to Google Drive every hour"
$scriptPath = "F:\git\zyte_scraper\sync_zyte_scraper.ps1"

Write-Host "Creating scheduled task: $taskName" -ForegroundColor Green
Write-Host "Script location: $scriptPath" -ForegroundColor Yellow

try {
    # Check if the sync script exists
    if (!(Test-Path $scriptPath)) {
        throw "Sync script not found at: $scriptPath"
    }

    # Check if task already exists and remove it
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    }

    # Calculate start time (2 minutes from now)
    $startTime = (Get-Date).AddMinutes(2).ToString("yyyy-MM-ddTHH:mm:ss")

    # Create the task XML with proper start time
    $taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>$taskDescription</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <Repetition>
        <Interval>PT1H</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>$startTime</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$env:USERNAME</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <RestartOnFailure>
      <Interval>PT10M</Interval>
      <Count>3</Count>
    </RestartOnFailure>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-ExecutionPolicy Bypass -WindowStyle Hidden -File "$scriptPath"</Arguments>
      <WorkingDirectory>F:\git\zyte_scraper</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

    # Register the task using the XML
    Register-ScheduledTask -TaskName $taskName -Xml $taskXml -Force

    Write-Host "`nScheduled task created successfully!" -ForegroundColor Green
    Write-Host "Task details:" -ForegroundColor Cyan
    Write-Host "  Name: $taskName"
    Write-Host "  First run: $((Get-Date).AddMinutes(2).ToString('yyyy-MM-dd HH:mm:ss'))"
    Write-Host "  Frequency: Every 1 hour"
    Write-Host "  Script: $scriptPath"

    # Show the task info
    Start-Sleep -Seconds 2  # Give it a moment to register
    $taskInfo = Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo
    Write-Host "`nTask Status: $($taskInfo.TaskState)" -ForegroundColor Yellow

    Write-Host "`nYou can manage this task using:" -ForegroundColor Cyan
    Write-Host "  Task Scheduler GUI: taskschd.msc"
    Write-Host "  PowerShell commands:"
    Write-Host "    Get-ScheduledTask -TaskName '$taskName'"
    Write-Host "    Start-ScheduledTask -TaskName '$taskName'"
    Write-Host "    Stop-ScheduledTask -TaskName '$taskName'"
    Write-Host "    Disable-ScheduledTask -TaskName '$taskName'"
    Write-Host "    Enable-ScheduledTask -TaskName '$taskName'"
    Write-Host "    Unregister-ScheduledTask -TaskName '$taskName'"

} catch {
    Write-Host "`nError creating scheduled task:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nMake sure you're running PowerShell as Administrator!" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nScheduled task setup complete!" -ForegroundColor Green
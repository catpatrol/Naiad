<#
.SYNOPSIS
  Register (or remove) the THREE session-anchored Naiad brief tasks.
  Amendment 2 §2.3 / §10.

.NOTES
  RETIRED 2026-08-15 (queue 005 M4). DO NOT RUN THIS.

  This is a Windows PowerShell installer for Windows Task Scheduler. The project
  moved to macOS; there is no Task Scheduler on this host and `$python` below
  still points at `C:\venvs\naiad\Scripts\python.exe`, which does not exist. It
  was already classified ALREADY-DEAD by the M3 sweep
  (BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M3-SWEEP.md) and is NOT deleted, because
  it is the only written record of how the three slot-anchored brief triggers
  were specified — including the timezone reasoning below, which is still correct
  and still unimplemented on macOS.

  WHAT REPLACES IT, partially: three launchd agents armed 2026-08-15 —
  `com.naiad.daily` (07:00 daily), `com.naiad.estate` (Sundays 08:00),
  `com.naiad.workflow` (Sundays 08:30). See `exchange/status/CADENCE.md`.

  WHAT IS NOT YET REPLACED, and is the reason this file is kept rather than
  archived: those three agents do NOT cover the per-slot brief triggers this
  script registers. `com.naiad.daily` invokes `daily_routine.py` with **no
  `--slot`**, so the slot-aware jobs in `routine_jobs.json` report SKIPPED by
  design rather than running. Porting the london / ny_am / post_ny triggers to
  launchd -- including the America/New_York anchoring described below, which
  launchd's `StartCalendarInterval` does NOT do natively (it fires on machine
  local wall-clock, exactly like the Windows triggers) -- is OUTSTANDING and
  belongs to the operator's M5 checklist.

.DESCRIPTION
  Reads ops/brief_schedule.yaml and registers one Windows Task Scheduler job per
  slot (london / ny_am / post_ny), each invoking the EXISTING
  scripts/daily_routine.py with --slot. There is no second scheduler: these
  tasks drive the same routine the daily job already uses.

  TIMES ARE HELD IN America/New_York AND RESOLVED THROUGH THE ZONE AT GENERATION
  TIME. A stored UTC offset breaks twice a year; anchoring to the session keeps
  `ny_am` meaning "an hour into the New York morning" all year round.

  Windows Task Scheduler triggers fire on MACHINE local wall-clock time, so the
  resolved New York time is converted into machine-local before registering.
  When the machine is not in the schedule's zone the script says so loudly
  rather than registering a task that is silently an hour out.

  The next four DST transitions are printed so the operator can see exactly when
  the resolved UTC times will move.

  The brief is an OPS artifact. Scheduling it changes nothing about the
  firewall: it still never reads journals, never computes outcome statistics,
  and never becomes study evidence.

.PARAMETER Remove
  Delete the three tasks instead of creating them.

.PARAMETER Force
  Overwrite existing tasks of the same names.

.PARAMETER WhatIfOnly
  Resolve and print everything, register nothing.

.EXAMPLE
  .\scripts\setup_brief_schedule.ps1 -WhatIfOnly
.EXAMPLE
  .\scripts\setup_brief_schedule.ps1 -Force
.EXAMPLE
  .\scripts\setup_brief_schedule.ps1 -Remove
#>
[CmdletBinding()]
param(
    [switch]$Remove,
    [switch]$Force,
    [switch]$WhatIfOnly
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$cfgPath = Join-Path $repo "ops\brief_schedule.yaml"

if (-not (Test-Path $cfgPath)) {
    throw "missing $cfgPath - the schedule is defined there, not in this script"
}

# Minimal targeted YAML read. The file is ours and its shape is fixed, so this is
# honest; a general YAML parser is not a dependency worth adding for three slots.
$zone = $null
$slots = @()
$namePrefix = "NaiadBrief"
# The venv lives outside the repo (off OneDrive); a venv cannot be relocated, so
# this is an absolute path rather than one derived from $repo.
$python = "C:\venvs\naiad\Scripts\python.exe"
$script = "scripts/daily_routine.py"
$logRel = "research_outputs/brief/brief_run.log"

$cur = $null
foreach ($line in Get-Content $cfgPath) {
    $t = $line.Trim()
    if ($t -eq "" -or $t.StartsWith("#")) { continue }
    if ($t -match '^zone:\s*(\S+)')        { $zone = $Matches[1]; continue }
    if ($t -match '^name_prefix:\s*(\S+)') { $namePrefix = $Matches[1]; continue }
    if ($t -match "^python:\s*'(.+)'$")    { $python = $Matches[1]; continue }
    if ($t -match '^script:\s*(\S+)')      { $script = $Matches[1]; continue }
    if ($t -match '^log:\s*(\S+)')         { $logRel = $Matches[1]; continue }
    if ($t -match '^-\s*id:\s*(\S+)') {
        if ($cur) { $slots += $cur }
        $cur = [pscustomobject]@{ id = $Matches[1]; local = $null; why = $null }
        continue
    }
    if ($cur -and $t -match '^local:\s*"([0-9]{2}:[0-9]{2})"') { $cur.local = $Matches[1]; continue }
    if ($cur -and $t -match '^why:\s*"(.+)"$')                 { $cur.why = $Matches[1]; continue }
}
if ($cur) { $slots += $cur }

if (-not $zone) { throw "no zone: key in $cfgPath" }
if ($slots.Count -ne 3) { throw "expected 3 slots in $cfgPath, found $($slots.Count)" }

Write-Host ""
Write-Host "Naiad brief schedule - zone $zone" -ForegroundColor Cyan
Write-Host ("=" * 66)

# ZONE RESOLUTION. Each local time is resolved through the zone TODAY, so the
# printed UTC is a computed fact and never a stored offset (F-B22).
$tz = $null
try { $tz = [System.TimeZoneInfo]::FindSystemTimeZoneById($zone) } catch { $tz = $null }
if ($null -eq $tz) {
    $tz = [System.TimeZoneInfo]::FindSystemTimeZoneById("Eastern Standard Time")
    Write-Host "  note: '$zone' not a Windows zone id; using 'Eastern Standard Time' (same zone)" -ForegroundColor DarkYellow
}

$localTz = [System.TimeZoneInfo]::Local
if ($localTz.Id -ne $tz.Id) {
    Write-Host ""
    Write-Host "  WARNING: this machine is in '$($localTz.Id)', not '$($tz.Id)'." -ForegroundColor Red
    Write-Host "  Task Scheduler fires on MACHINE local time. Trigger times below are" -ForegroundColor Red
    Write-Host "  converted so each slot lands at the intended New York moment today -" -ForegroundColor Red
    Write-Host "  but they will NOT track New York DST on their own." -ForegroundColor Red
    Write-Host "  Re-run this script after each transition printed below." -ForegroundColor Red
}

$today = (Get-Date).Date
$rows = @()
foreach ($s in $slots) {
    $parts = $s.local.Split(":")
    $naive = [datetime]::new($today.Year, $today.Month, $today.Day, [int]$parts[0], [int]$parts[1], 0, [System.DateTimeKind]::Unspecified)
    $utc = [System.TimeZoneInfo]::ConvertTimeToUtc($naive, $tz)
    $machine = [System.TimeZoneInfo]::ConvertTimeFromUtc($utc, $localTz)
    $isDst = $tz.IsDaylightSavingTime($naive)
    $rows += [pscustomobject]@{
        Slot = $s.id
        LocalNY = $s.local
        ResolvedUTC = $utc.ToString("HH:mm")
        MachineLocal = $machine.ToString("HH:mm")
        DST = $(if ($isDst) { "EDT" } else { "EST" })
    }
}
$rows | Format-Table Slot, LocalNY, ResolvedUTC, MachineLocal, DST -AutoSize

Write-Host "Next four DST transitions in ${zone}:" -ForegroundColor Cyan
$found = 0
$probe = $today
$noon0 = [datetime]::new($probe.Year, $probe.Month, $probe.Day, 12, 0, 0, [System.DateTimeKind]::Unspecified)
$prev = $tz.IsDaylightSavingTime($noon0)
while ($found -lt 4 -and $probe -lt $today.AddYears(3)) {
    $probe = $probe.AddDays(1)
    $noon = [datetime]::new($probe.Year, $probe.Month, $probe.Day, 12, 0, 0, [System.DateTimeKind]::Unspecified)
    $isDst = $tz.IsDaylightSavingTime($noon)
    if ($isDst -ne $prev) {
        $to = $(if ($isDst) { "EDT (UTC-4)" } else { "EST (UTC-5)" })
        $shift = $(if ($isDst) { "resolved UTC moves one hour EARLIER" } else { "resolved UTC moves one hour LATER" })
        Write-Host ("  {0}  ->  {1}   {2}" -f $probe.ToString("yyyy-MM-dd"), $to, $shift)
        $prev = $isDst
        $found++
    }
}
Write-Host ""

if ($WhatIfOnly) {
    Write-Host "-WhatIfOnly: nothing registered." -ForegroundColor Yellow
    return
}

if (-not (Test-Path $python)) { throw "venv python not found at $python" }
$scriptPath = Join-Path $repo ($script -replace "/", "\")
if (-not (Test-Path $scriptPath)) { throw "not found: $scriptPath" }

$logPath = Join-Path $repo ($logRel -replace "/", "\")
$logDir = Split-Path -Parent $logPath
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }

foreach ($r in $rows) {
    $taskName = "${namePrefix}_$($r.Slot)"

    if ($Remove) {
        schtasks /Query /TN $taskName *> $null
        if ($LASTEXITCODE -eq 0) {
            schtasks /Delete /TN $taskName /F | Out-Null
            Write-Host "  removed $taskName" -ForegroundColor Yellow
        } else {
            Write-Host "  $taskName not present" -ForegroundColor DarkGray
        }
        continue
    }

    $cmd = "cmd /c cd /d `"$repo`" && `"$python`" `"$scriptPath`" --slot $($r.Slot) >> `"$logPath`" 2>&1"

    schtasks /Query /TN $taskName *> $null
    if ($LASTEXITCODE -eq 0 -and -not $Force) {
        Write-Host "  $taskName already exists (use -Force to overwrite)" -ForegroundColor DarkYellow
        continue
    }

    $taskArgs = @("/Create", "/TN", $taskName, "/TR", $cmd, "/SC", "DAILY",
                  "/ST", $r.MachineLocal, "/RL", "LIMITED")
    if ($Force) { $taskArgs += "/F" }
    schtasks @taskArgs | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host ("  registered {0}  at {1} machine-local  ({2} NY {3}, {4} UTC)" -f `
            $taskName, $r.MachineLocal, $r.LocalNY, $r.DST, $r.ResolvedUTC) -ForegroundColor Green
    } else {
        Write-Host "  FAILED to register $taskName (exit $LASTEXITCODE)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Three tasks drive scripts/daily_routine.py --slot. No second scheduler." -ForegroundColor Cyan

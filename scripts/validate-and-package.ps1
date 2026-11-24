[CmdletBinding()]
param(
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$fullRoot = Join-Path $repoRoot 'distributions/ai-platform/powerpoint-skill'
$addinRoot = Join-Path $repoRoot 'distributions/powerpoint-addin/powerpoint-addin-skill'

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $repoRoot 'dist'
}

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

function Get-SkillFrontmatter {
    param([string]$SkillFile)

    $content = Get-Content -LiteralPath $SkillFile -Raw
    $match = [regex]::Match($content, '\A---\s*\r?\n(?<yaml>.*?)\r?\n---', 'Singleline')
    Assert-True $match.Success "Missing YAML frontmatter in $SkillFile"

    $metadata = @{}
    foreach ($line in ($match.Groups['yaml'].Value -split '\r?\n')) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }

        $field = [regex]::Match($line, '^(?<key>[A-Za-z][A-Za-z0-9_-]*):\s*(?<value>.*)$')
        Assert-True $field.Success "Unsupported frontmatter syntax in ${SkillFile}: $line"
        $metadata[$field.Groups['key'].Value] = $field.Groups['value'].Value.Trim().Trim('"').Trim("'")
    }

    $keys = @($metadata.Keys | Sort-Object)
    Assert-True (($keys -join ',') -eq 'description,name') "Only name and description are allowed in ${SkillFile}; found: $($keys -join ', ')"
    Assert-True (-not [string]::IsNullOrWhiteSpace($metadata['description'])) "Skill description is empty in $SkillFile"
    return $metadata
}

function Get-NormalizedText {
    param([string]$Path)

    return (Get-Content -LiteralPath $Path -Raw).Replace("`r`n", "`n").Replace("`r", "`n")
}

function Get-AllRelativeFiles {
    param([string]$Root)

    return @(Get-ChildItem -LiteralPath $Root -Recurse -File | ForEach-Object {
        $_.FullName.Substring($Root.Length).TrimStart('\', '/').Replace('\', '/')
    } | Sort-Object)
}

function Assert-ZipRoot {
    param(
        [string]$ArchivePath,
        [string]$ExpectedRoot
    )

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [System.IO.Compression.ZipFile]::OpenRead($ArchivePath)
    try {
        $files = @($archive.Entries | Where-Object { -not [string]::IsNullOrEmpty($_.Name) })
        Assert-True ($files.Count -gt 0) "Archive is empty: $ArchivePath"

        foreach ($entry in $files) {
            $normalized = $entry.FullName.Replace('\', '/')
            Assert-True $normalized.StartsWith("$ExpectedRoot/") "Unexpected ZIP root in ${ArchivePath}: $normalized"
        }

        $roots = @($files | ForEach-Object { $_.FullName.Replace('\', '/').Split('/')[0] } | Sort-Object -Unique)
        Assert-True (($roots -join ',') -eq $ExpectedRoot) "Archive must contain exactly one root folder named $ExpectedRoot"
    }
    finally {
        $archive.Dispose()
    }
}

Assert-True (Test-Path -LiteralPath $fullRoot -PathType Container) "Missing AI-platform distribution: $fullRoot"
Assert-True (Test-Path -LiteralPath $addinRoot -PathType Container) "Missing PowerPoint add-in distribution: $addinRoot"

$fullMetadata = Get-SkillFrontmatter (Join-Path $fullRoot 'SKILL.md')
$addinMetadata = Get-SkillFrontmatter (Join-Path $addinRoot 'SKILL.md')

Assert-True ($fullMetadata['name'] -eq 'powerpoint-skill') 'Unexpected AI-platform skill name.'
Assert-True ($addinMetadata['name'] -eq 'powerpoint-addin-skill') 'Unexpected PowerPoint add-in skill name.'
Assert-True ($fullMetadata['name'] -ne $addinMetadata['name']) 'Skill names must be distinct.'
Assert-True ((Split-Path $fullRoot -Leaf) -eq $fullMetadata['name']) 'AI-platform folder name must match its skill name.'
Assert-True ((Split-Path $addinRoot -Leaf) -eq $addinMetadata['name']) 'Add-in folder name must match its skill name.'
Assert-True ($fullMetadata['description'] -match 'bundled template') 'AI-platform description must identify bundled-template behavior.'
Assert-True ($addinMetadata['description'] -match 'currently open PowerPoint') 'Add-in description must identify open-presentation behavior.'

foreach ($skillRoot in @($fullRoot, $addinRoot)) {
    $skillText = Get-NormalizedText (Join-Path $skillRoot 'SKILL.md')
    Assert-True ($skillText.Contains('three simultaneous deliverables')) "Three-deliverable contract missing from $skillRoot/SKILL.md"
    Assert-True ($skillText.Contains('[pptx-basename]-companion-options-report.md')) "Companion Markdown filename contract missing from $skillRoot/SKILL.md"
    Assert-True ($skillText.Contains('substantive_reason')) "Substantive-slide classification fields missing from $skillRoot/SKILL.md"
    Assert-True ($skillText.Contains('Reporting only T1')) "Title-only rejection rule missing from $skillRoot/SKILL.md"
    Assert-True ($skillText.Contains('Use two QA passes')) "Two-pass QA rule missing from $skillRoot/SKILL.md"
    Assert-True ($skillText.Contains('never delete a part automatically') -or $skillText.Contains('never auto-delete')) "Orphan-preservation rule missing from $skillRoot/SKILL.md"
    Assert-True (-not $skillText.Contains('segment the report by section')) "Obsolete segmented-report instruction remains in $skillRoot/SKILL.md"

    $recoveryText = Get-NormalizedText (Join-Path $skillRoot 'references/evidence_qa_and_recovery.md')
    Assert-True (-not $recoveryText.Contains('create section-level report files')) "Obsolete multi-file reporting instruction remains in $skillRoot"
}

$fullTemplate = Join-Path $fullRoot 'assets/Corporate_Template.pptx'
Assert-True (Test-Path -LiteralPath $fullTemplate -PathType Leaf) 'AI-platform distribution must contain assets/Corporate_Template.pptx.'
Assert-True (Test-Path -LiteralPath (Join-Path $fullRoot 'assets/icon.svg') -PathType Leaf) 'AI-platform distribution must contain its icon.'
Assert-True (Test-Path -LiteralPath (Join-Path $fullRoot 'agents/openai.yaml') -PathType Leaf) 'AI-platform distribution must contain its agent metadata.'
Assert-True (Test-Path -LiteralPath (Join-Path $fullRoot 'scripts/validate_pptx.py') -PathType Leaf) 'AI-platform distribution must contain its read-only PPTX validator.'
Assert-True ((Get-NormalizedText (Join-Path $fullRoot 'SKILL.md')).Contains('python scripts/validate_pptx.py')) 'AI-platform skill must invoke its validator.'

Assert-True (-not (Test-Path -LiteralPath (Join-Path $addinRoot 'assets'))) 'Add-in distribution must not contain an assets directory.'
Assert-True (-not (Test-Path -LiteralPath (Join-Path $addinRoot 'agents'))) 'Add-in distribution must not contain agent metadata.'
Assert-True (-not (Test-Path -LiteralPath (Join-Path $addinRoot 'scripts'))) 'Add-in distribution must not contain scripts.'
Assert-True ((Get-ChildItem -LiteralPath $addinRoot -Recurse -File -Filter '*.pptx').Count -eq 0) 'Add-in distribution must not contain PPTX files.'
Assert-True ((Get-ChildItem -LiteralPath $addinRoot -Recurse -File -Filter 'icon.svg').Count -eq 0) 'Add-in distribution must not contain an icon.'
Assert-True ((Get-NormalizedText (Join-Path $addinRoot 'SKILL.md')).Contains('Through PowerPoint')) 'Add-in skill must require native structural checks.'

$intentionalDifferences = @(
    'SKILL.md',
    'examples/deck_spec_example.json',
    'references/template_manifest.json'
)

$fullFiles = Get-AllRelativeFiles $fullRoot
$addinFiles = Get-AllRelativeFiles $addinRoot
$fullOnlyPrefixes = @('agents/', 'assets/', 'scripts/')

foreach ($relativePath in $addinFiles) {
    if ($relativePath -in $intentionalDifferences) {
        continue
    }

    Assert-True ($relativePath -in $fullFiles) "Unexpected add-in-only file: $relativePath"
    $fullText = Get-NormalizedText (Join-Path $fullRoot $relativePath)
    $addinText = Get-NormalizedText (Join-Path $addinRoot $relativePath)
    Assert-True ($fullText -ceq $addinText) "Unintended drift detected in shared file: $relativePath"
}

foreach ($relativePath in $fullFiles) {
    if ($relativePath -in $intentionalDifferences) {
        continue
    }

    $isApprovedFullOnlyFile = $false
    foreach ($prefix in $fullOnlyPrefixes) {
        if ($relativePath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            $isApprovedFullOnlyFile = $true
            break
        }
    }

    Assert-True ($isApprovedFullOnlyFile -or $relativePath -in $addinFiles) "Unexpected AI-platform-only file: $relativePath"
}

$platformPointerFiles = @(
    'SKILL.md',
    'examples/deck_spec_example.json',
    'references/template_manifest.json'
)

foreach ($relativePath in $platformPointerFiles) {
    $fullText = Get-NormalizedText (Join-Path $fullRoot $relativePath)
    $addinText = Get-NormalizedText (Join-Path $addinRoot $relativePath)
    Assert-True ($fullText.Contains('assets/Corporate_Template.pptx')) "AI-platform template pointer missing from $relativePath"
    Assert-True ($addinText.Contains('CURRENT_OPEN_POWERPOINT_PRESENTATION') -or $addinText.Contains('currently open PowerPoint presentation')) "Add-in open-presentation pointer missing from $relativePath"
    Assert-True (-not $addinText.Contains('assets/Corporate_Template.pptx')) "Bundled-template pointer leaked into add-in file: $relativePath"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python3 -ErrorAction SilentlyContinue
}
Assert-True ($null -ne $python) 'Python is required for JSON Schema validation.'

& $python.Source (Join-Path $PSScriptRoot 'validate-json.py') $fullRoot $addinRoot
Assert-True ($LASTEXITCODE -eq 0) 'JSON Schema validation failed.'

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$fullArchive = Join-Path $OutputDirectory 'powerpoint-skill-ai-platform.zip'
$addinArchive = Join-Path $OutputDirectory 'powerpoint-addin-skill.zip'

foreach ($archivePath in @($fullArchive, $addinArchive)) {
    if (Test-Path -LiteralPath $archivePath) {
        Remove-Item -LiteralPath $archivePath -Force
    }
}

Compress-Archive -LiteralPath $fullRoot -DestinationPath $fullArchive -CompressionLevel Optimal
Compress-Archive -LiteralPath $addinRoot -DestinationPath $addinArchive -CompressionLevel Optimal

Assert-ZipRoot $fullArchive 'powerpoint-skill'
Assert-ZipRoot $addinArchive 'powerpoint-addin-skill'

$addinSize = (Get-Item -LiteralPath $addinArchive).Length
$addinLimit = 50KB
Assert-True ($addinSize -le $addinLimit) "Add-in ZIP is $addinSize bytes; limit is $addinLimit bytes."

Write-Host 'Validation passed.'
Write-Host "AI-platform archive: $fullArchive ($((Get-Item -LiteralPath $fullArchive).Length) bytes)"
Write-Host "PowerPoint add-in archive: $addinArchive ($addinSize bytes; limit $addinLimit bytes)"

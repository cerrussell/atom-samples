param(
    [array]$slicetypes = @("usages", "reachables"),
    [array]$langs = @("java", "python", "javascript"),
    [string]$outputdir = ".",
    [string]$repodir = "src_repos",
    [string]$repocsv = "C:\Users\user\PycharmProjects\atom-samples\sources.csv"
)

function build_args
{
    [CmdletBinding()]
    param()

    $parser = New-Object System.Management.Automation.PSObject
    $parser | Add-Member -MemberType NoteProperty -Name "description" -Value "Generate Atom Samples"
    $parser | Add-Member -MemberType NoteProperty -Name "slicetypes" -Value @("usages", "reachables")
    $parser | Add-Member -MemberType NoteProperty -Name "langs" -Value @("java", "python", "javascript")
    $parser | Add-Member -MemberType NoteProperty -Name "outputdir" -Value $outputdir
    $parser | Add-Member -MemberType NoteProperty -Name "repodir" -Value $repodir
    $parser | Add-Member -MemberType NoteProperty -Name "repocsv" -Value $repocsv

    return $parser
}

function generate
{

    $repositories = Import-Csv -Path $repocsv

    foreach ($repo in $repositories)
    {
        if ($repo.language -in $langs) {
            $dir = $repodir + "/" + $repo.language + "/"+ $repo.project
            git clone $repo.link $dir
            if ($repo.pre_build_cmd.Length -gt 0)
            {
                $loc = Get-Location
                Set-Location $dir
                Invoke-Expression $repo.pre_build_cmd
                Set-Location $loc
            }
            if ($repo.build_cmd.Length -gt 0)
            {
                $loc = Get-Location
                Set-Location $dir
                Invoke-Expression $repo.build_cmd
                Set-Location $loc
            }
            if ($repo.post_build_cmd.Length -gt 0)
            {
                $loc = Get-Location
                Set-Location $dir
                Invoke-Expression $repo.post_build_cmd
                Set-Location $loc
            }

            foreach ($stype in $slicetypes)
            {
                $fname = $repo.project + "-" + $stype + ".json"
                Write-Host "Generating "$stype" slice for "$repo.project" at "$outputdir/$repo.language/$fname
                atom $stype -l $repo.language -o $repodir/$repo.language/$repo.project/$repo.project.atom -s $outputdir/$repo.language/$fname $repodir/$repo.language/$repo.project
            }
        }
    }
}

$args = build_args

generate
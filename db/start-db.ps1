Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Get the directory of the script
$BASEDIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# Run docker-compose
docker-compose --file "$BASEDIR/docker-compose.yml" up
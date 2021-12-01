
# python.exe "C:\Program Files (x86)\Eclipse\Sumo\tools\randomTrips.py" -n .\osm.net.xml -e 500000 -o .\osm.passenger.routes.xml --persontrips --trip-attributes modes=public
if (Test-Path 'dist') {
    Get-ChildItem 'dist' | Remove-Item -Recurse -Force
  }

if($PSVersionTable.Platform -eq "Unix")
{
  python ./runner.py

} else{
  python .\runner.py
}

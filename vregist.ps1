#vregistor1.0

#this script is for registor
$usage = "
#dir registor
#.\vregistor.ps1 -dir

#all registor items
#.\vregistor.ps1 -all
"
if($args.count -gt 1)
{
    $usage
    throw "over more args!!!"
}
if($args.count -eq 0)
{
    $usage
    throw "Empty args"
}

try{

if($args[0] -eq "-dir")
{
Get-ChildItem -Path hkcu:\ -force
exit
}

if($args[0] -eq "-all")
{
Get-ChildItem -Path hkcu:\ -Recurse -Force
exit
}
Throw "Bad args"
}
catch{

$usage
throw "Fail to show the registor!!!"

}
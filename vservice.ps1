#vservice1.0

#interface design:


$usage = "
#create a file to show all info of vservice
#.\vservice.ps1 -get-servicebyname xxx
    #plus :  if you want check all service , use `"vservice -get-servicebyname *`"

#get the service which is running
#.\vservice.ps1 -get-runningservice

#get the service which is stopped
#.\vservice.ps1 -get-stoppedservice

#stop/start a service by name
#.\vservice.ps1 -start-servicebyname xxx
#.\vservice.ps1 -stop-servicebyname xxx

"
#limit count of args
if ( $args.count -gt 2)
{
    $usage
    Throw "bad cmd"
}

if ( $args[0] -eq "-get-runningservice")
{
    $i = 0
    Get-Service | foreach{ 
        if ( $_.status -eq "running")
        {
            $_
            $i++
        }
    }
    
    exit
}


if ( $args[0] -eq "-get-stoppedservice")
{
    $i = 0
    Get-Service | foreach{ 
        if ( $_.status -eq "stopped")
        {
            $_
            $i++
        }
    }
    
    exit
}


#.\vservice.ps1 -start-servicebyname xxx
#.\vservice.ps1 -stop-servicebyname xxx

if ( $args[0] -eq "-start-servicebyname")
{
    if($args[1] -eq "")
    {
        $usage
        throw "plz input the name of service!"
    }
    
    try 
    {
        $name = $args[1]
        Get-Service -name $name | foreach{ $_.start()}
        echo "success"
    }catch
    {
        throw "Fail to start the service: $args[1]"
    }
}

if ( $args[0] -eq "-stop-servicebyname")
{
    if($args[1] -eq "")
    {
        $usage
        throw "plz input the name of service!"
    }
    
    try 
    {
        $service = Get-Service -name $arg[1]
        $service.stop()
        echo "success"
    }catch
    {
        throw "Fail to stop the service : $args[1]"
    }
}

if ($args[0] -eq '-get-servicebyname')
{
    try
    {
        $service = Get-Service -Name $args[1]
        echo $service
    }
    catch
    {
        throw "Bad args"
    }
}


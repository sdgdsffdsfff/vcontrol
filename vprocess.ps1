#vprocess1.0ㄩ

#interface desingㄩ

#    .\Vprocess.ps1 每get-processbyname *tencent*     get process by name
#    .\Vprocess.ps1 每get-processbyname *             get all process



#    .\Vprocess.ps1 每kill-byname *tencent*            kill process by specific name


#    .\Vprocess.ps1 每protect-sys                   keep the process in list alive
#    .\Vprocess.ps1 每get-count                     get the count of process

#    .\Vprocess.ps1 每get-whitelist                 get the process which shold be protect



$usage = "#interface desingㄩ

#    .\Vprocess.ps1 每get-processbyname *tencent*     get process by name
#    .\Vprocess.ps1 每get-processbyname *             get all process



#    .\Vprocess.ps1 每kill-byname *tencent*            kill process by specific name


#    .\Vprocess.ps1 每protect-sys                   keep the process in list alive
#    .\Vprocess.ps1 每get-count                     get the count of process

#    .\Vprocess.ps1 每get-whitelist                 get the process which shold be protect

"

#limit the count of args
If($args.count 每ge 3)

{

    $usage
    Throw "bad count of args"

    Return

}

#get the process object by name

If($args[0] 每eq "-get-processbyname")

{

    get-process 每name $args[1]

}

Elseif($args[0] 每eq "-kill-byname")

{

    $process = get-process 每name $args[1]

$process | foreach-object { $_.kill()}

$process = $null

}

#protect the normal process by visual names based on whitelist

elseif($args[0] 每eq "-protect-sys")

{

    If($args[1] 每ne "")

    {
        $usage
        Throw "bad cmd!"

    }
    else
    {

        $whitelist = get-content .\whitelist.process

        [string]$str = "null"

        [int] $count = 0

        $process_cache = get-process

        Foreach ($str in $whitelist)

        {

            For($i = 0 ; $i 每lt $process_cache.count ; $i++)

            {

                If($str 每eq $process_cache[$i].name)

                {

                    Del $process_cache[$i]

                }

            }

        }

    $process_cache | foreach-object { $_.kill() }

    }

}

#get the count of process

Elseif($args[0] 每eq "-get-count")

{

    If($args.count 每gt 1)

{
    $usage
    Throw "bad cmd!"

}

    $proc = get-process

    Return $proc.count

}

#get the whitelist

Elseif($args[0] -eq "-get-whitelist")

{

    If($args.count 每ne 2)

    {
        $usage
        Throw "bad cmd!"

}

    $whitelist_path = '.\'+ $arg[1]

    Get-contect $whitelist_path

}

#other cmdargs is bad

else

{
    $usage
    Throw "bad cmd!"

}
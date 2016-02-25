#vprocess1.0��

#interface desing��

#    .\Vprocess.ps1 �Cget-processbyname *tencent*     get process by name
#    .\Vprocess.ps1 �Cget-processbyname *             get all process



#    .\Vprocess.ps1 �Ckill-byname *tencent*            kill process by specific name


#    .\Vprocess.ps1 �Cprotect-sys                   keep the process in list alive
#    .\Vprocess.ps1 �Cget-count                     get the count of process

#    .\Vprocess.ps1 �Cget-whitelist                 get the process which shold be protect



$usage = "#interface desing��

#    .\Vprocess.ps1 �Cget-processbyname *tencent*     get process by name
#    .\Vprocess.ps1 �Cget-processbyname *             get all process



#    .\Vprocess.ps1 �Ckill-byname *tencent*            kill process by specific name


#    .\Vprocess.ps1 �Cprotect-sys                   keep the process in list alive
#    .\Vprocess.ps1 �Cget-count                     get the count of process

#    .\Vprocess.ps1 �Cget-whitelist                 get the process which shold be protect

"

#limit the count of args
If($args.count �Cge 3)

{

    $usage
    Throw "bad count of args"

    Return

}

#get the process object by name

If($args[0] �Ceq "-get-processbyname")

{

    get-process �Cname $args[1]

}

Elseif($args[0] �Ceq "-kill-byname")

{

    $process = get-process �Cname $args[1]

$process | foreach-object { $_.kill()}

$process = $null

}

#protect the normal process by visual names based on whitelist

elseif($args[0] �Ceq "-protect-sys")

{

    If($args[1] �Cne "")

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

            For($i = 0 ; $i �Clt $process_cache.count ; $i++)

            {

                If($str �Ceq $process_cache[$i].name)

                {

                    Del $process_cache[$i]

                }

            }

        }

    $process_cache | foreach-object { $_.kill() }

    }

}

#get the count of process

Elseif($args[0] �Ceq "-get-count")

{

    If($args.count �Cgt 1)

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

    If($args.count �Cne 2)

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
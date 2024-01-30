use ~/dev/sync/nushell/vars.nu *

export-env {
    $env.WORK_DIRS = ({} 
        | insert arkc $arkc
        | insert core $core
        | insert ets_frontend $ets_frontend
        | insert ets_plugin $ets_plugin
    )
}

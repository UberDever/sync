const arkc = '~/dev' + '/arkcompiler'
const core = $arkc + '/runtime_core/static_core'
const ets_frontend = $arkc + '/ets_frontend'
const ets_plugin = $core + '/plugins/ets'

export-env {
    $env.WORK_DIRS = ({} 
        | insert arkc $arkc
        | insert core $core
        | insert ets_frontend $ets_frontend
        | insert ets_plugin $ets_plugin
    )
}

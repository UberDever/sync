dev_dir=~/dev
arkc_dir="$dev_dir/arkcompiler"
core_dir="$arkc_dir/runtime_core/static_core"
ets_frontend_dir="$dev_dir/arkcompiler/ets_frontend"
ets2panda_dir="$ets_frontend_dir/ets2panda"
ets_plugin_dir="$core_dir/plugins/ets"

sandbox_dir=$dev_dir/sandbox

cmake_arkc() {
    echo "Executing with parameters: " 
    echo "$@"
    cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -DPANDA_CROSS_COMPILER=false "$@"
}

cmake_ets2panda() {
    echo "Executing with parameters: " 
    echo "$@"
    cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -DPANDA_CROSS_COMPILER=false -DPANDA_WITH_TESTS=true -DPANDA_WITH_BENCHMARKS=true "$@"
}

update_repo() {
    if [[ $# -ne 6 ]]; then
        return
    fi
    arkc_origin="${1%%/*}"
    ecma_origin="${2%%/*}"
    ets2_origin="${3%%/*}"
    cd $4 &&
    git fetch $arkc_origin &&
    git rebase $1 --autostash &&
    cd $5 &&
    git fetch $ecma_origin && 
    git rebase $2 --autostash &&
    cd $6 &&
    git fetch $ets2_origin &&
    git rebase $3 --autostash && cd $4
}

update_arkc() {
    arkc_branch="origin/master"
    ecma_branch="origin/master"
    ets2_branch="origin/master"
    update_repo $arkc_branch $ecma_branch $ets2_branch $core_dir $ets_frontend_dir $ets2panda_dir
}

go_arkc() { cd $arkc_dir; }
go_ets() { cd $ets_frontend_dir; }
go_core() { cd $core_dir; }
go_ets_plugin() { cd $ets_plugin_dir; }

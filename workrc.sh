export dev_dir=~/dev
export arkc_dir="$dev_dir/arkcompiler"
export core_dir="$arkc_dir/runtime_core/static_core"
export ets_frontend_dir="$dev_dir/arkcompiler/ets_frontend"
export es2panda_dir="$ets_frontend_dir/ets2panda"
export ets_plugin_dir="$core_dir/plugins/ets"

sandbox_dir=$dev_dir/sandbox

cmake_arkc() {
    echo "Executing with parameters: " 
    echo "$@"
    # -DPANDA_WITH_BENCHMARKS=true \
    cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -DPANDA_CROSS_COMPILER=false "$@"
}

cmake_arkc_default() {
    cmake_arkc $core_dir
}

cmake_es2panda() {
    echo "Executing: " 
    cmd="cmake -GNinja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -DPANDA_CROSS_COMPILER=false -DPANDA_WITH_TESTS=true -DPANDA_WITH_BENCHMARKS=true -DPANDA_ETS_INTEROP_JS=ON -DES2PANDA_PATH="$es2panda_dir" $@"
    echo $cmd
    eval "$cmd"
}

cmake_es2panda_default() {
    cmake_es2panda $core_dir
}

update_repo() {
    if [[ $# -ne 6 ]]; then
        return
    fi
    arkc_origin="${1%%/*}"
    ecma_origin="${2%%/*}"
    es2_origin="${3%%/*}"
    cd $4 &&
    git fetch $arkc_origin &&
    git rebase $1 --autostash &&
    cd $5 &&
    git fetch $ecma_origin && 
    git rebase $2 --autostash &&
    cd $6 &&
    git fetch $es2_origin &&
    git rebase $3 --autostash && cd $4
}

git_rebase_arkc_master() {
    git_rebase_arkc "origin/master"
}

git_rebase_arkc() {
    if [[ $# -ne 1 ]]; then
        echo "Please provide branch to rebase to"
    fi
    arkc_branch="$1"
    ecma_branch="$1"
    es2_branch="$1"
    update_repo $arkc_branch $ecma_branch $es2_branch $core_dir $ets_frontend_dir $es2panda_dir
}

git_switch_arkc() {
    if [[ $# -ne 1 ]]; then
        echo "Please provide branch to switch to"
    fi
    cd_ets
    git switch "$1"
    cd_core
    git switch "$1"
    cd_arkc
}

cd_arkc() { cd $arkc_dir; }
cd_ets() { cd $ets_frontend_dir; }
cd_core() { cd $core_dir; }
cd_ets_plugin() { cd $ets_plugin_dir; }
cd_build() { cd_arkc && cd build; }

es2panda_ets_example() { ./bin/es2panda --output example.abc $@ _.ets; }

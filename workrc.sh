export arkc_dir="$dev_dir/arkcompiler"
export core_dir="$arkc_dir/runtime_core/static_core"
export ets_frontend_dir="$arkc_dir/ets_frontend"
export es2panda_dir="$ets_frontend_dir/ets2panda"
export ets_plugin_dir="$core_dir/plugins/ets"
export ecmascript_dir="$core_dir/plugins/ecmascript"
export used_arkc="arkcompiler"

use_panda() {
    export arkc_dir="$dev_dir/panda"
    export core_dir="$arkc_dir/runtime_core/static_core"
    export ets_frontend_dir="$arkc_dir/ets_frontend"
    export es2panda_dir="$ets_frontend_dir/ets2panda"
    export ets_plugin_dir="$core_dir/plugins/ets"
    export used_arkc="panda"
}

use_arkcompiler() {
    export arkc_dir="$dev_dir/arkcompiler"
    export core_dir="$arkc_dir/runtime_core/static_core"
    export ets_frontend_dir="$arkc_dir/ets_frontend"
    export es2panda_dir="$ets_frontend_dir/ets2panda"
    export ets_plugin_dir="$core_dir/plugins/ets"
    export used_arkc="arkcompiler"
}

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

cd_arkc() { echo "In $used_arkc"; cd $arkc_dir; }
cd_ets() { echo "In $used_arkc"; cd $ets_frontend_dir; }
cd_core() { echo "In $used_arkc"; cd $core_dir; }
cd_ets_plugin() { echo "In $used_arkc"; cd $ets_plugin_dir; }
cd_ecmascript() { echo "In $used_arkc"; cd $ecmascript_dir; }
cd_buildr() { echo "In $used_arkc"; cd_arkc && cd build-release; }
cd_buildd() { echo "In $used_arkc"; cd_arkc && cd build-debug; }
cd_build() { cd_buildd; }

es2panda_ets_example() { ./bin/es2panda --output example.abc $@ _.ets; }

# function errors_json { I=1; cat out.txt | while read line; do if [[ $line == {* ]]; then sed -n ${I}p out.txt | jq | less; break; else I=$[$I +1]; fi done; }
# function gen_stdlib { ./bin/es2panda --gen-stdlib --extension=ets --verifier-errors="ArithmeticOperationValidForAll,ForLoopCorrectlyInitializedForAll,SequenceExpressionHasLastTypeForAll,NodeHasTypeForAll" --output=./plugins/ets/etsstdlib.abc &> out.txt }
function selfcheck { ~/dev/gitee_sync/selfcheck.sh --configure --root-dir=$arkc_dir --build-dir=$arkc_dir/build-debug --build=tests_full --run-func-suite --run-cts --build-clean --es2panda-dir=$es2panda_dir; }

function forall-bz { 
    if [[ $# -lt 1 ]]; then
        echo "Please input command to execute in blue zone repos (ets_frontend, runtime_core, ecmascript)."
        echo "./both <cmd> <arg1> ... <argn>"
        return -1
    fi
    command=$1
    shift
    cd $core_dir &&
    $command "$@"
    cd $ets_frontend_dir &&
    $command "$@"
    if [[ -d $ecmascript_dir ]]; then
        cd $ecmascript_dir
        $command "$@"
    fi
}

function git_fetch_reset_bz {
    origin="origin"
    master="master"
    if [[ $# -lt 2 ]]; then
        echo "Using default origin/master"
    else 
        origin="$1"
        master="$2"
    fi
    forall-bz git switch $master
    forall-bz git fetch $origin
    forall-bz git reset --hard $origin/$master
}

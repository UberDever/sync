dev_dir=~/dev
panda_dir=$dev_dir/panda
ecmascript_dir=$panda_dir/plugins/ecmascript
es2panda_dir=$ecmascript_dir/es2panda

sandbox_dir=$dev_dir/sandbox
asm_dir=$sandbox_dir/asm
# arkts_dir=$sandbox_dir/arkts
arkts_dir=$es2panda_dir/migrator/test/java-mapper/

ark() {
    old_pwd=$(pwd)
    cd $panda_dir/build
    if [ -z $2 ]; then
        entry="ETSGLOBAL::main"
    else
        entry=$2
    fi
    path=$old_pwd/$1 
    echocolor BLUE "entry: $entry"
    echocolor BLUE "path: $path"
    ./bin/ark --log-level=debug --log-components=interpreter --boot-panda-files=plugins/ets/etsstdlib.abc --load-runtimes=ets $path $entry
    # --log-level=debug --log-components=interpreter
    cd $old_pwd
}

ark_disasm() {
    old_pwd=$(pwd)
    cd $panda_dir/build
    base=$(basename $1)
    name=${base%%.*}
    path=$old_pwd/$1 
    out=$asm_dir/$name.cba
    echocolor BLUE "out: $out"
    echocolor BLUE "path: $path"
    ./bin/ark_disasm $path $out
    cd $old_pwd
}

es2panda() {
    old_pwd=$(pwd)
    cd $panda_dir/build
    base=$(basename $1)
    name=${base%%.*}
    out=$asm_dir/$name.abc 
    path=$old_pwd/$1
    echocolor BLUE "out: $out"
    echocolor BLUE "path: $path"
    ./bin/es2panda --stdlib=$panda_dir/plugins/ets/stdlib --extension=ets --output=$out --opt-level=0 $path
    cd $old_pwd
}

migrator () {
    old_pwd=$(pwd)
    cd $es2panda_dir/migrator
    out=$arkts_dir
    path=$old_pwd/$1
    echocolor BLUE "out: $out"
    echocolor BLUE "path: $path"
    java -jar out/migrator-1.0.jar -s --verbose $path -o $out
    cd $old_pwd
}

migrate_compile_run() {
    echocolor LIGHTRED "Migrator"
    migrator java/$1.java
    echocolor LIGHTRED "Es2Panda"
    es2panda arkts/$1.java.sts
    echocolor LIGHTRED "Ark"
    ark asm/$1.abc $1::main
}
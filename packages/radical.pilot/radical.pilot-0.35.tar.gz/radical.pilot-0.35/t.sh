
myprint(){
    echo ===
    echo "$*" | sed -e 's/%/%%/g' | xargs --null printf
    echo ===
}

echo "$@"
echo
myprint "$@"
echo


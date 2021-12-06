#!/bin/sh
answer='WRONG'
echo "\nCHECKING dependencies:"
#python3 -m poetry install
python -m pip list 2>/dev/null | grep -q dnspython
if [ $? -eq 0 ] ; then
    answer="DONE"
    echo "PROPERLY"
    
else
    echo "FOUND breakage!"
    echo "REPAIR ...\n"
    echo "UPGRADE pip:\n"
    python -m pip install --upgrade pip
    echo "\nINSTALLING pymongo[srv]:\n"
    python -m pip install "pymongo[srv]"
    answer="WARNING waiting resolve!"
fi

echo "\nEXTERNAL IPaddr:"
curl ifconfig.me/ip
echo "\n"
echo $answer
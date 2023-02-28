for file in "./easy_ham/*"; do
    mv -f $file "$PWD/test/$file.eml"
done
# rename all the files in the test-out directory to have a .out extension instead of .txt
# Usage: ./temp.sh

for file in test-out/*.txt
do
  mv $file ${file%.txt}.out
done
```
#!/bin/bash
FILE=knn.txt
for i in {1..100}
do
  echo "Running iteration $i..."
  python3 mp6.py --extra --max_iter $i >> $FILE
  echo "------------------------------------" >> $FILE
done

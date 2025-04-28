for x in benchmarks-smt/*/*/*.smt2; do
  echo "Converting $x"
#   echo "rlset reals;" > converted/$x
  python3 smt_to_red.py $x > converted/$x
  echo "Done"
  # break
done
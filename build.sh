cp $1 ./grades.db
docker build -t dashboard .
rm ./grades.db
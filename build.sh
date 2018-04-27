# TODO GENERATE FAKE GRADES IF DEBUG
if [[ $2 == "DEBUG" ]]; then
    python generate_debug_grades.py
else
    cp $1 ./grades.db
fi

docker build -t dashboard .
rm ./grades.db
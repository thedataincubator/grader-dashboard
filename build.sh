if [[ $2 == "DEBUG" ]]; then
    echo "DEBUG"
    python generate_debug_grades.py
else
    cp $1 ./grades.db
    python add_posts.py
fi

docker build -t gcr.io/mooc-hub/dashboard .
rm ./grades.db

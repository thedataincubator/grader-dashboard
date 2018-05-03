Dashboard for our grader.

Right now the sqllite database is put into the container, but eventually we can point it to another database (maybe on AWS)

Currently the application is set up to run either on heroku or on a Kubernetes cluster.

To run on heroku, authenticate your credentials, then run
`heroku container:push web`

To run k8s, push the container to our gcr.io repo and then set the proper image version in the deployment file.  Then update the deployment with 

`kubetcl apply -f <deploy-file> -n <namespace>`

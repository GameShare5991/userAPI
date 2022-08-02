# userAPI

API gateway for performing CRUD operations on GameShare users.

# build image: 
docker build . -t jackjackzhou/user-api

# run image though docker: 
docker run --publish 4000:4000 user-api

# push image:
docker push jackjackzhou/user-api

# kubectl create&run
minikube start
kubectl create -f user-app-deployment.yaml
minikube tunnel
minikube dashboard

# secret
kubectl create secret generic user-app-key --from-file=serviceAccountKey.json

kubectl describe secrets/user-app-key

# clean up
kubectl delete -f user-app-deployment.yaml
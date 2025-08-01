        i own 2835 stocks of nvidia. i bought them 1 year ago for 74 eurs each. what is their current value in euros, and how much profit i made?
        I bought 371 nvidia shares for 138 euros on 6th of january 2023. how much i payed back then and what would be their value in euros now? (check if there was a share split)

docker tag adam_adam-mcp-server:latest europe-west3-docker.pkg.dev/assistant-424508/containers/adam-mcp:1.0
docker push europe-west3-docker.pkg.dev/assistant-424508/containers/adam-mcp:1.0
docker pull us-central1-docker.pkg.dev/assistant-424508/quickstart-docker-repo/quickstart-image:tag1

gcloud run deploy mcp-server \
  --image europe-west3-docker.pkg.dev/assistant-424508/containers/adam-mcp:1.0 \
  --region=europe-west3 \
  --no-allow-unauthenticated

gcloud run services proxy mcp-server --region=europe-west3
# Adam: Trading broker agent

Adam is a versatile trading broker agent designed to assist users with various tasks, including retrieving weather reports and current time information for any city. It provides multiple modes of operation, such as web interface, command-line tools, and server functionality, making it adaptable to different use cases.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/adam.git
   cd adam

2. Install the required dependencies:
    ```bash
    pip install uv
    ```
3. Install dependencies using `uv`:
    ```bash
    uv install
    ```
    4. Set up the `.env` file:
        - Rename `.env.sample` to `.env`
        - Update the variables accordingly

4. Run the MCP Servers:
    - Run the command: 
    ```bash 
    uv run serv.py
    ``` 

5. Run the application:
    - To run via web:
    ```bash
    adk web
    ```
    - To run via command line:
    ```bash
    adk run multi_tool_agent
    ```
    - To run as a server:
    ```bash
    adk api_server
    ```

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
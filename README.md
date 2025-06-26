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
4. Run the application:
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
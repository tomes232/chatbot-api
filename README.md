# Chatbot API

This repository contains a FastAPI application that serves as a chatbot API. The chatbot can answer questions about my resume using two different models: a fine-tuned DistilBERT model from Hugging Face, and the OpenAI Assistant.

## API Routes

The main API route is a POST route at `/models/{model_name}`. The `model_name` parameter can be either `distilbert` or `openai`.

The POST route accepts a JSON body with the following fields:

- `input`: The question being asked about my resume.
- `session_id`: The ID of the chat thread. This field is optional and defaults to `None`.

The response from this route is a JSON object with the following fields:

- `model`: The name of the model used to answer the question.
- `output`: The answer to the question.
- `session_id`: The ID of the chat thread. This is the same as the `session_id` in the request if it was provided.

## Running the API

To run the API, you need to build a Docker image and then run a container from that image. Here are the commands to do this:

```bash
docker build -t chatbot-api:latest .
docker run --name my-chatbot -p 80:80 chatbot-api:latest
```

You also need to provide environment variables for the OpenAI API key and MongoDB username and password. You can do this by adding the `-e` option to the `docker run` command, like this:

```bash
docker run --name my-chatbot -p 80:80 -e OPENAI_API_KEY=your_openai_api_key -e MONGODB_USERNAME=your_mongodb_username -e MONGODB_PASSWORD=your_mongodb_password chatbot-api:latest
```

Please replace `your_openai_api_key`, `your_mongodb_username`, and `your_mongodb_password` with your actual OpenAI API key, MongoDB username, and MongoDB password.
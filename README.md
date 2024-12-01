  Developed RAG-ChatBot Using LLamaindex 


BACKEND🔗🔗:

Getting Started-------------------------------------------------------------
First, setup the environment:

    poetry install
    poetry shell
By default, we use the OpenAI LLM (though you can customize, see app/context.py). As a result you need to specify an OPENAI_API_KEY in an .env file in this directory.

Example .env file:

    OPENAI_API_KEY=<openai_api_key>
Second, generate the embeddings of the documents in the ./data directory (if this folder exists - otherwise, skip this step):

    python app/engine/generate.py
"To genrate Embedding and for more further information about vector search index ---------See https://github.com/run-llama/mongodb-demo/tree/main?tab=readme-ov-file#create-a-vector-search-index

    
Third, run the development server:

    python main.py
Then call the API endpoint /api/chat to see the result:

    curl --location 'localhost:8000/api/chat' \
    --header 'Content-Type: application/json' \
    --data '{ "messages": [{ "role": "user", "content": "Hello" }] }'
    You can start editing the API by modifying app/api/routers/chat.py. The endpoint auto-updates as you save the file.

Open http://localhost:8000/docs with your browser to see the Swagger UI of the API.

The API allows CORS for all origins to simplify development. You can change this behavior by setting the ENVIRONMENT environment variable to prod:

    ENVIRONMENT=prod uvicorn main:app
Learn More
To learn more about LlamaIndex, take a look at the following resources:

LlamaIndex Documentation - learn about LlamaIndex.
You can check out the LlamaIndex GitHub repository - your feedback and contributions are welcome!







Frontend 🔗🔗:


Getting Started----------------------------
First, install the dependencies:

    npm install
Second, run the development server:

    npm run dev
    Open http://localhost:3000 with your browser to see the result.

You can start editing the page by modifying app/page.tsx. The page auto-updates as you edit the file.

This project uses next/font to automatically optimize and load Inter, a custom Google Font.

Learn More
To learn more about LlamaIndex, take a look at the following resources:

LlamaIndex Documentation - learn about LlamaIndex (Python features).
LlamaIndexTS Documentation - learn about LlamaIndex (Typescript features).
You can check out the LlamaIndexTS GitHub repository - your feedback and contributions are welcome!


                         

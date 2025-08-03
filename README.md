# Language bot conversationalist

## Collection and processing of information
1. Unique user ID is saved
2. Chat logs are saved
3. Messages are sent to the OpenAI neural network

## Functional
1. The basic prompt implements the chatbot mechanism
2. The bot does not provide any information without a user request
3. The bot will speak in the target language until asked otherwise.
4. The bot does not provide translations in the native language unless explicitly asked to do so.

## Architecture
1. The logic of the objects is in the file "class_.py"
2. Logs and database are deployed in the "./.user_log" folder in the project directory
3. See the file for DB metadata
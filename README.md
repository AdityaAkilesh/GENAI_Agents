# GenAI Agents – AI-Powered Toolkit (Gemini 1.5 Flash & Streamlit)

## Project Overview

This project is a collection of **9 AI agents** built with **Google's Gemini (Generative AI)** models and **Streamlit**. It provides a web app interface where users can leverage various AI capabilities, from language processing to speech recognition. Each agent is specialized for a particular task, as listed below:

- **Grammar Correction** – Fixes grammar and spelling mistakes in text.
- **Invoice Q&A** – Answers questions based on the content of a single invoice (PDF/text).
- **Multi-Invoice Q&A** – Answers questions using information from multiple invoice PDFs.
- **Sentiment Analysis** – Determines the sentiment of a given text (e.g. positive, negative, neutral).
- **Spam Detection** – Detects whether a given email/text is spam or not.
- **Speech Recognition** – Converts spoken audio (wav/mp3) into text transcription.
- **Summarization** – Generates a concise summary of a longer text document.
- **Text Classification** – Classifies text into predefined categories (e.g. topics or labels).
- **Translation** – Translates text from one language to another (default target is French, can be specified).

All agents harness the power of large language models (via **Google Generative AI Gemini**) or relevant AI services, and return results in a structured JSON-like format for clarity. The Streamlit app ties these agents together under a unified interface for easy interaction.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/yourusername/GenAI_Agents.git
   cd GenAI_Agents
   ``` 

2. **Create a Virtual Environment (Optional but Recommended)**:  
   Use Python 3.x and create a virtual environment to manage dependencies. For example:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   # For Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies**:  
   Install the required Python libraries using pip:  
   ```bash
   pip install -r requirements.txt
   ```  
   This will install all necessary packages, including **Streamlit**, **LangChain**, **Google Generative AI (PaLM)** client, **PyMuPDF** (for PDF processing), **SpeechRecognition**, **Matplotlib**, etc.

4. **Obtain API Credentials**:  
   Acquire a Google Generative AI API key (for the PaLM/Gemini models). You may need to sign up for Google’s PaLM API access and obtain an API key. Once you have the key, set it as an environment variable:  
   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```  
   Replace `"YOUR_API_KEY_HERE"` with your actual API key. The application will load this key to authenticate with the Gemini models. If the key is not set, the app will alert you with an error.

5. **Run the Streamlit App**:  
   Start the web application by running Streamlit:  
   ```bash
   streamlit run mainapp.py
   ```  
   This will launch the app on a local server (by default at **http://localhost:8501**). Keep the terminal running while you use the app.

## Usage

### Running the Streamlit App

Once the Streamlit server is running, open a browser and navigate to the local URL (usually `http://localhost:8501`). You will see the **GenAI Agents** interface. Here’s how to use it:

- **Enter a Query**: Use the text input area to type your request or question. You can ask for any supported operation. For example:
  - *“Correct the grammar of the following sentence: I has a apple.”*
  - *“Translate the sentence 'Good morning' to Spanish.”*
  - *“Summarize the text below:”* (and then paste a paragraph of text)
  - *“Is this email spam or not:”* (and then include the email text)
- **Upload Files if Needed**:  
  For certain agents, you should provide a file:
  - *Invoice Q&A*: Upload a PDF of an invoice and ask a question about it (e.g., "What is the total amount due on the invoice?"). Use the **“Upload PDF Invoices”** file uploader to select one or multiple PDF files.  
  - *Speech Recognition*: Upload an audio file (`.wav` or `.mp3`) containing speech via the **“Upload Audio File”** uploader. You can then ask something like "Transcribe the uploaded audio" in the query box.
- **Submit the Query**: Click the **"Ask AI Agent"** button. The application will process your input. It intelligently decides which AI agent (tool) to use based on your query and the provided files. For example, if you uploaded an invoice PDF and asked a question, it will route the query to the *Invoice Q&A* agent. If you simply asked to translate text, it will use the *Translation* agent.
- **View Results**: The answer or result will be displayed on the page, typically in a structured format. Most outputs are shown as JSON for clarity. For instance, a grammar correction will show the original text and the corrected version in a JSON object.

Behind the scenes, the app uses a LangChain-powered agent that can pick the appropriate tool among the nine based on your request. This means you can interact in a flexible, conversational way without manually selecting which model to use each time. Simply ask naturally, and the system will invoke the right AI module.

### Programmatic Access (API Usage)

While the primary interface is the Streamlit web app, you can also use these AI agents programmatically in your own scripts or integrate them into an API:

- **Direct Python Usage**: Each capability is implemented as a Python function in the `modules/` directory. You can import these in your Python code. For example:  
  ```python
  from modules import grammar_correction, translation
  result = grammar_correction.correct_grammar("Ths is an exampel sentence.")
  print(result)
  # Output: {'original': 'Ths is an exampel sentence.', 'corrected': 'This is an example sentence.'}
  ```  
  Similarly, you can call `translation.translate_text("Hello", target_language="fr")`, `sentiment_analysis.analyze_sentiment(text)`, etc. Each function returns a Python dictionary with the result, which can be easily converted to JSON if you are building a REST API around it.
- **REST API**: If you wish to expose these models via a RESTful API, you could wrap the function calls in a web framework (such as Flask or FastAPI). For example, you might create endpoints like `/correct_grammar` or `/summarize` that accept POST requests with input data and then return the JSON output from the corresponding module. This project doesn't include a pre-built Flask/FastAPI server, but the modular design makes it straightforward to add one if needed.

**Note**: To use the agents programmatically, you will still need to configure the environment with the required API key (`GEMINI_API_KEY`) for any functions that call the Google Gemini models.

## Model Architecture & Technical Details

This project’s architecture combines a web interface with powerful language and speech models:

- **Gemini Models (Google Generative AI)**: Most of the language-focused agents (grammar, Q&A, sentiment, spam, summarization, classification, translation) use Google’s Generative AI via the **PaLM API**. Specifically, they leverage the *Gemini models* (e.g. "gemini-1.5-flash" and "gemini-2.0-flash" variants) for text generation. These are large language models that have been trained on vast textual data by Google, capable of understanding instructions and producing natural language outputs. We use the official `google-generativeai` Python client to interact with these models. The prompts are carefully constructed to guide the model to return a **structured JSON output** for each task. For example, the Invoice Q&A agent prompts the model with: *"Based on this invoice..., answer the query... and return the response as a structured JSON object."* This approach ensures the results are easy to parse and use downstream.
- **LangChain Agent Orchestration**: Instead of treating each capability in isolation, we employ **LangChain** to create an intelligent agent that can decide which tool to use. Each AI agent function is wrapped as a LangChain **Tool** with a name and description. We initialize a LangChain agent (using `ChatGoogleGenerativeAI` as the LLM backbone and a reasoning strategy) with all 9 tools. When a user question comes in, the agent uses a reasoning process (ReAct framework) to select and invoke the correct tool. This enables a seamless experience — the user doesn’t have to manually pick the grammar checker vs. translator; the system figures it out from context. The LangChain agent is configured with a conversational memory as well, allowing it to remember previous interactions within the same session (so it can handle follow-up questions or references to earlier data, if the Streamlit session persists the conversation).
- **Speech Recognition**: The speech-to-text functionality is handled by the **SpeechRecognition** library (which under the hood uses Google’s Speech API for transcription). This is the only agent that does not use the generative LLM. When an audio file is provided, the `speech_recognition.transcribe_audio` function is called to produce text from spoken words. That text can then be fed into other agents if needed (for example, you could transcribe an audio and then ask the summarizer to summarize the transcribed text).
- **PDF Processing for Invoice Q&A**: For the invoice-related Q&A, the system uses **PyMuPDF (fitz)** to parse PDF files. The text content of uploaded invoices is extracted and then passed to the generative model along with the user’s question. The *Multi-Invoice Q&A* agent will concatenate or handle multiple PDFs by extracting text from each and combining relevant information before querying the LLM, enabling cross-document questions (e.g., "Which invoice has the highest total amount?").
- **Structured Outputs**: Each agent function is designed to return a dictionary (JSON-serializable). This makes it easier to display results in the app and for developers to use the output. For example, the translation agent returns `{"translated_text": "Bonjour"}` for an input "Hello" to French, and the sentiment agent might return `{"sentiment": "Positive", "confidence": 0.95}`. Standardizing outputs as JSON helps in maintaining consistency and enables potential integration with other systems.
- **Streamlit Interface**: The front-end is built with Streamlit, which allows for quick development of an interactive UI in pure Python. The app layout consists of input widgets (text area, file uploaders, button) and output display. The Streamlit script orchestrates reading user input, calling the LangChain agent with the appropriate context (including any uploaded files), and then formatting the response for display. The use of Streamlit means the app can be run locally or deployed easily without needing a separate front-end.

No additional training was performed on these models; we rely on the pre-trained capabilities of Google's models and standard libraries. The logic and intelligence of the system come from prompt engineering and the agent’s decision-making flow. This modular and cloud-based approach (using APIs) means you don't need heavy compute power locally – however, an internet connection is required for the generative AI and speech recognition calls.

## Deployment

You have multiple options to deploy this project for wider use, either using containerization or cloud platforms. Below are guidelines for deploying with **Docker**, on **AWS**, and on **Google Cloud Platform (GCP)**. Before deployment, ensure you have properly set your `GEMINI_API_KEY` in the environment where the app will run (for cloud services, you might use environment configuration or secret managers).

### Using Docker

Deploying via Docker allows you to containerize the application and run it consistently anywhere Docker is supported:

1. **Create a Docker Image**: Write a `Dockerfile` in the project root (if not already provided). For example:  
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . /app
   RUN pip install -r requirements.txt
   ENV GEMINI_API_KEY=<YOUR_API_KEY_HERE>
   EXPOSE 8501
   CMD ["streamlit", "run", "mainapp.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```  
   This Dockerfile uses a slim Python base image, installs the requirements, sets the API key (you can also pass it at runtime instead for security), and runs the Streamlit app on container start.

2. **Build the Docker Image**:  
   ```bash
   docker build -t genai-agents:latest .
   ```  
   This will package the application into an image named `genai-agents`.

3. **Run the Docker Container**:  
   ```bash
   docker run -d -p 8501:8501 --name genai_app \
       -e GEMINI_API_KEY="YOUR_API_KEY_HERE" \
       genai-agents:latest
   ```  
   This command starts the container in detached mode, maps port 8501 so the app is accessible, and passes the API key as an environment variable. Adjust the port if needed. Once running, the Streamlit app will be accessible at the host’s address (e.g., `http://<server-ip>:8501`).

Using Docker, you can easily deploy the container to any container hosting service or cloud VM. Just ensure that the environment variable for the API key is set on the container for the app to function.

### Deploying on AWS

There are several ways to deploy this app on **Amazon Web Services**. Here are a couple of common approaches:

- **AWS EC2 (Virtual Machine)**: You can launch an EC2 instance (Amazon’s VM service) with a suitable Amazon Machine Image (AMI) that has Docker or at least Python pre-installed.
  - *Using Docker on EC2*: Build and push the Docker image to a registry (like Docker Hub or AWS ECR), then pull and run it on the EC2 instance. This is convenient because the environment inside the container is consistent. Ensure the EC2 security group allows inbound traffic on the Streamlit port (e.g., 8501).
  - *Manual Setup on EC2*: Alternatively, SSH into the EC2, install Python and required dependencies, set the `GEMINI_API_KEY`, and run `streamlit run mainapp.py` directly. This is less portable than Docker but works for a single VM.
- **AWS Elastic Beanstalk**: Elastic Beanstalk can deploy web apps easily. You can configure it with a Docker deployment (just provide the Dockerfile or Dockerrun configuration) or as a Python application. For a Streamlit app, using Docker is often simpler. Upload the Docker image or configure Beanstalk to use the GitHub repository and your Dockerfile. It will handle creating the EC2 instance, load balancing, etc. Remember to set environment variables (like the API key) in the Beanstalk configuration.
- **AWS ECS/Fargate or EKS**: For a more scalable container deployment, you can use AWS ECS (Elastic Container Service) or Kubernetes (EKS). Build the Docker image and push it to **AWS ECR** (Elastic Container Registry). Then create an ECS service or EKS pod definition that runs the container. For ECS (Fargate), you won’t have to manage servers directly. You will need to specify the container port (8501) and ensure the load balancer or service security allows that port. Again, set the `GEMINI_API_KEY` in your task definition or Kubernetes manifest as an environment variable or secret.

No matter which AWS method you choose, after deployment you should be able to access the Streamlit app via the public DNS or IP of the service. For production use, you might consider placing a reverse proxy (like Nginx) in front of Streamlit or using an AWS Application Load Balancer to route traffic.

### Deploying on Google Cloud Platform (GCP)

On **GCP**, you also have multiple options to host the Streamlit app:

- **Google Compute Engine (GCE)**: This is similar to AWS EC2. Launch a VM instance on GCE, install Docker or the necessary Python environment, then run the application. If using Docker, you can use the same image built earlier. Open the firewall for the port (8501) under your GCP project’s VPC settings or use GCE’s interface to allow HTTP traffic on that port.
- **Google Cloud Run**: Cloud Run is a convenient service for running containers without managing servers. Build your Docker image (as above) and upload it to **Google Container Registry (GCR)** or **Artifact Registry**. Then create a Cloud Run service from that image. Cloud Run can automatically handle scaling. You just need to specify the port (8501) and supply the `GEMINI_API_KEY` as an environment variable in the service settings. Cloud Run will give you a secure URL for your app. One advantage is that Cloud Run can scale down to zero when not in use, possibly saving cost.
- **Google Kubernetes Engine (GKE)**: If you are comfortable with Kubernetes, you can deploy the container on a GKE cluster. This is more complex if you don't already use Kubernetes. Similar to AWS EKS, you’d create a deployment and service for the Streamlit app container.

- **App Engine (Flex)**: Google App Engine Flexible Environment can run custom Docker containers as well. You could deploy the app by writing an `app.yaml` that points to your Dockerfile. However, Cloud Run is generally simpler for containerized apps nowadays.

For any GCP deployment, make sure to store your API key securely. On Cloud Run or App Engine, use environment variables or secrets. On a VM, you’d export it in the shell or use a startup script. Once deployed, you’ll get a URL (or IP) to access the Streamlit interface remotely.

### Note on Streamlit Cloud

Another easy deployment option is **Streamlit Community Cloud** (if this project is open-source). You can share your repo on Streamlit’s hosting (share.streamlit.io) for free, which will run the app in their cloud. You would need to add the `GEMINI_API_KEY` in the app’s settings on Streamlit Cloud. This option is great for quick demos and smaller scale usage without worrying about infrastructure.

## License & Credits

**License**: This project is open-source and available under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the MIT license. (Feel free to check the `LICENSE` file in this repository for the full text.)

*If you use this project in your research or build upon it, please consider acknowledging this repository. And of course, star the project on GitHub if you found it useful!* 

Let's continue to innovate and build great AI solutions together. Happy coding!

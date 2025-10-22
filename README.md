# Naive Retrieval-Augmented Generation (RAG) for Script Writing

**Unleash the film writer in you!**  
This project walks you through building a complete **Retrieval-Augmented Generation (RAG)** pipeline using **LangChain** — designed to generate new movie scenes, dialogues, and creative story twists inspired by real movie scripts.

---

## Overview

The project is a complete end-to-end RAG system that ingests real movie scripts, retrieves relevant scenes, and generates original cinematic content using large language models.  

It includes **data collection → data ingestion → embeddings → retrieval → generation**, learning how to integrate all major RAG components along the way.

---

## Features

- **Script Loading:** Fetch full movie scripts from the Internet Movie Script Database (IMSDb).  
- **Scene Splitting:** Automatically divide scripts into scenes using LangChain text splitters.  
- **Vector Embeddings:** Convert scene chunks into embeddings using Hugging Face models.  
- **Semantic Search:** Use Qdrant as a vector database for efficient similarity-based retrieval.  
- **Query Rewriting:** Automatically refine user queries to improve retrieval accuracy.  
- **Context-Aware Generation:** Combine retrieved scenes with user prompts to create new storylines.  
- **Modular Design:** Clean, stage-based structure for easy understanding and extension.  

---

##  Tools and Frameworks
This project utilizes several tools and libraries to create a complete RAG pipeline:

- **LangChain** - Core RAG pipeline (loading, splitting, retrieval, generation)
- **Hugging Face** - Embedding generation
- **Qdrant** - Vector database for semantic search
- **BeautifulSoup4** - Parsing scripts from IMSDb
- **Requests** - HTTP requests for fetching content
- **ChatGroq** - Language models for text generation

## How to Run
1. **Clone the repository**:

   ```bash
   git https://github.com/Z-Kotliner/Naive-RAG-for-Script-Writing.git
   cd AI-Diet-Meal-Planner


2. **Create a virtual environment (recommended):**

     ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. **Install dependencies:**

     ```bash
    pip install -r requirements.txt


4. **Set environment variables**
Create a .env file:

    ```bash
    GROQ_API_KEY=your_api_key_here
    HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
   
5. **Start Qdrant locally(Docker)**
    
    ```bash
    docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant

6. **Run final stage**

    ```bash
    python main.py

---
## Example Interaction
> Enter a movie title> Mission Impossible

    Loaded script for Mission Impossible from https://imsdb.com/scripts/Mission-Impossible.html.

    Found 129 scenes in the script for Mission Impossible.
    Embedded script for Mission Impossible.

> Enter your query> Create a scene depicting Ethan as the antagonist and living in a cave. It should start with INT. CAVE - DAY

    Rewritten query to: "Find scenes set in a cave during the day featuring Ethan as the main antagonist, starting with the description "INT. CAVE - DAY"."


    Final Answer:

    INT. CAVE - DAY
    The camera pans across the dark, damp interior of the cave, the sound of dripping water echoing off the walls. Ethan, dressed in tattered clothing, emerges from the shadows, his eyes gleaming with a malevolent intensity. He moves with a deliberate slowness, his movements economical and precise.

    As he walks, the camera follows him, capturing the rough, rocky terrain of the cave floor. Ethan's feet are bare, and his toes grip the stone as he navigates the uneven surface. He stops in front of a small, flickering fire, the flames casting eerie shadows on the walls of the cave.

    Ethan's gaze falls upon a small, makeshift computer terminal, cobbled together from scavenged parts. He regards it with a calculating interest, his fingers twitching as he considers his next move. The camera zooms in on his face, capturing the twisted, antagonistic expression that twists his features.

    Suddenly, Ethan's head snaps up, his eyes locking onto something in the distance. He listens intently, his ears straining to pick up the faint sound of footsteps, echoing through the cave. A slow, sinister smile spreads across his face as he realizes he is not alone.

---


This project was done as part of the fulfilment of the core topics of 'Introduction to AI Engineering with Python' HyperSkill course.
#### Learn more at:
https://hyperskill.org/projects/518

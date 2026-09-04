#✈️ TripMate AI — A Multi-Agent Travel Planner

TripMate AI is an open-source, AI-powered travel planner that turns a simple natural-language trip request into a complete travel plan — including flight suggestions, hotel recommendations, and a day-by-day itinerary.

Powered by a multi-agent workflow built with LangGraph, LangChain, and FastAPI, TripMate AI coordinates specialized agents to research, plan, and present your trip in one seamless experience.

##🧠 Why This Project?
Planning a trip usually means jumping between multiple websites, spreadsheets, and tools. TripMate AI brings everything into one intelligent pipeline:

###✈️ A flight-search agent

###🏨 A hotel-research agent

###🗺️ An itinerary-planning agent

###📝 A final response agent

All coordinated through a LangGraph workflow — so you can focus on the journey, not the logistics.


##✨ Features
✈️ Real-time flight research using AviationStack

🏨 Smart hotel suggestions via Tavily search

🧠 Multi-agent orchestration with LangGraph

📝 Structured, human-readable travel itineraries

🌐 FastAPI backend with a clean web interface

💾 Persistent conversation state using PostgreSQL

⚡ Fast, LLM-powered responses with Groq


##🛠️ Tech Stack
Category	Tools & Services
Language	Python 3.10+
Backend	FastAPI, LangGraph, LangChain
Frontend	Jinja2 + HTML/CSS/JavaScript
LLM Provider	Groq
Database	PostgreSQL
APIs	AviationStack, Tavily


##📁 Project Structure
text
.
├── app.py                # FastAPI entry point
├── backend.py            # LangGraph travel workflow
├── requirements.txt      # Python dependencies
├── static/               # Static assets (CSS, JS)
├── templates/            # HTML templates
└── tools/                # Flight & web search integrations

##🚀 Getting Started
###Prerequisites
Python 3.10 or newer

PostgreSQL up and running

API keys for:

Groq

Tavily

AviationStack


##🔐 Environment Variables
Create a .env file in the project root:

env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
DEFAULT_ORIGIN_IATA=DAC   # optional, fallback origin airport

##📦 Installation
bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

##▶️ Running the App
Start the FastAPI server:

bash
python app.py
Then open your browser at:
👉 http://127.0.0.1:8000/


##📡 API Endpoints
Method	Endpoint	Description
GET	/health	Health check
POST	/api/travel	Submit a travel plan request
###Example Request
bash
curl -X POST http://127.0.0.1:8000/api/travel \
  -H "Content-Type: application/json" \
  -d '{"message":"Plan a 3-day trip to Tokyo with a budget of $1200"}'


##🔁 How the Workflow Works
User submits a travel request.

The flight agent gathers flight data.

The hotel agent searches for accommodation.

The itinerary agent builds a practical day-by-day plan.

The final agent compiles everything into a polished, readable response.


##🤝 Contributing
Contributions are welcome! Whether you want to add new travel features, improve the UI, or fix bugs:

Fork the repository

Create a feature branch

Make your changes

Open a pull request


##🙏 Acknowledgments
Built with modern LLM tooling and real-world travel APIs. This project is a practical example of combining LangGraph agents with real-world applications — and a testament to what open-source AI can do.


##📄 License
This project is open-source and available under the MIT License.
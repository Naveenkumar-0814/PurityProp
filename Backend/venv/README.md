# Tamil Nadu Real Estate AI Assistant

A domain-restricted, multilingual AI chatbot for real estate queries specific to Tamil Nadu, India. Built with FastAPI backend and React frontend, powered by Llama 3.1 8B via Groq API.

## Features

✅ **Domain Restricted** - Only answers real estate-related questions  
✅ **Multilingual Support** - Tamil script, Tanglish, and English with strict language matching  
✅ **Tamil Nadu Focused** - Specific to TN laws, regulations, and procedures  
✅ **Comprehensive Knowledge** - Property registration, documents, loans, legal compliance  
✅ **Modern UI** - Premium design with glassmorphism and smooth animations  
✅ **Session Management** - Maintains conversation history  

## Tech Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy (Database ORM)
- Groq API (Llama 3.1 8B)
- SQLite (Development)

**Frontend:**
- React 18
- Vite (Build tool)
- Axios (HTTP client)
- Lucide React (Icons)

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment variables are already 
 in `.env` file with your Groq API key.

5. Run the backend server:
```bash
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## Usage

1. Start both backend and frontend servers
2. Open browser to `http://localhost:5173`
3. Click "New Chat" to start a session
4. Ask real estate questions in:
   - **Tamil Script**: "சென்னையில் வீடு வாங்க என்ன ஆவணங்கள் தேவை?"
   - **Tanglish**: "Chennai la veedu vaanga enna documents venum?"
   - **English**: "What documents are needed to buy a house in Chennai?"

## API Endpoints

- `POST /api/sessions` - Create new chat session
- `POST /api/chat` - Send message and get response
- `GET /api/sessions/{session_id}/messages` - Get conversation history
- `GET /api/health` - Health check

## Project Structure

```
Real Estate/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── domain_validator.py
│   │   │   ├── llm_service.py
│   │   │   └── tn_knowledge_base.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routes.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatMessage.jsx
    │   │   └── ChatInput.jsx
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Key Features Explained

### Domain Restriction
- Keyword-based detection for real estate terms
- Rejects non-real estate queries politely in user's language
- Supports Tamil, Tanglish, and English rejection messages

### Language Matching
- Detects input language automatically
- Responds in the EXACT same language format
- Tamil script → Tamil script response
- Tanglish → Tanglish response
- English → English response

### Tamil Nadu Knowledge Base
- Property registration process
- Required documents (buyer, seller, property)
- Authorities (TNRERA, DTCP, CMDA, Sub-Registrar)
- Stamp duty and registration fees
- Bank loan procedures
- Red flags and warnings

## Legal Disclaimer

⚠️ This application provides informational guidance only, not legal advice. Users should consult legal professionals for specific cases.

## License

MIT License - Free to use and modify

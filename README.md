# arXiv CS Daily Agent

A multi-agent collaborative system that autonomously completes software development from natural language task descriptions. This project demonstrates an AI-driven development workflow where specialized agents collaborate to build a complete "arXiv CS Daily" webpage.

## 🎯 Project Overview

This system implements a multi-agent architecture with three specialized agents working together to generate a functional web application:

- **Project Planning Agent**: Breaks down high-level requirements into executable tasks
- **Code Generation Agent**: Implements code solutions using LLM and file management tools
- **Code Evaluation Agent**: Validates code quality through automated testing

The orchestrator manages task scheduling, agent communication, and state tracking to ensure seamless collaboration.

## 🏗️ System Architecture

### Multi-Agent Components

```
┌─────────────────────────────────────────────────────────┐
│              Multi-Agent Orchestrator                     │
│  • Task Scheduling                                       │
│  • Communication Management                              │
│  • State Management                                      │
└─────────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Planning   │ │   Code Gen   │ │  Evaluation  │
│    Agent     │ │    Agent     │ │    Agent     │
└──────────────┘ └──────────────┘ └──────────────┘
         │              │              │
         └──────────────┴──────────────┘
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
    ┌─────────┐              ┌──────────┐
    │  Tools  │              │   LLM    │
    │  • File │              │  Client  │
    │  • Cmd  │              │          │
    │  • Web  │              └──────────┘
    └─────────┘
```

### Agent Roles

1. **Planning Agent** (`agents/planning_agent.py`)
   - Receives natural language requirements
   - Generates structured task plans with dependencies
   - Defines technical specifications for each task

2. **Code Generation Agent** (`agents/code_generation_agent.py`)
   - Executes development tasks
   - Uses LLM to generate code and data files
   - Manages file operations through FileManager
   - Falls back to scripts if LLM fails

3. **Code Evaluation Agent** (`agents/code_evaluation_agent.py`)
   - Validates code quality
   - Runs automated tests (e.g., `npm run build`)
   - Reports pass/fail status

### Tool Kit

- **FileManager** (`tools/file_manager.py`): File creation, reading, and writing
- **CommandExecutor** (`tools/command_executor.py`): Shell command execution
- **LLMClient** (`tools/llm_client.py`): OpenAI-compatible API integration
- **WebSearch** (`tools/web_search.py`): Placeholder for web search functionality

## 📦 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Git

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd arxiv-cs-daily-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.deepseek.com
   OPENAI_MODEL=deepseek-chat
   ```
   
   **Note**: Remove spaces after `=` signs. Supported LLM providers:
   - DeepSeek: `https://api.deepseek.com`, model: `deepseek-chat`
   - OpenAI: `https://api.openai.com/v1`, model: `gpt-4o-mini`
   - Custom OpenAI-compatible APIs

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

## 🚀 Usage

### Running the Multi-Agent System

1. **Start the backend server** (recommended for daily updates):
   ```bash
   # From project root
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`
   
   **Important**: When the backend server starts, it automatically sets up a daily update scheduler that runs at 02:00 every day to refresh paper data.

2. **Run the agent system manually** (without server):
   ```bash
   # From project root with virtual environment activated
   python -c "from backend.main import orchestrator; orchestrator.bootstrap('build arxiv cs daily'); orchestrator.run(); print(orchestrator.summary())"
   ```

   Or for daily refresh:
   ```bash
   python -c "from backend.main import orchestrator; orchestrator.bootstrap('daily refresh'); orchestrator.run()"
   ```

3. **Start the frontend development server**:
   ```bash
   # From frontend directory
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

### Daily Update Mechanism

The system implements **automatic daily updates** to refresh the paper list:

1. **Automatic Scheduled Updates**:
   - When the backend server starts, it automatically schedules a daily update job
   - The update runs at **02:00 (2 AM) every day**
   - Uses the multi-agent system to generate fresh paper data via LLM

2. **Manual Update via API**:
   ```bash
   # Trigger update immediately via API
   curl -X POST http://127.0.0.1:8000/update
   ```

3. **Check Scheduler Status**:
   ```bash
   # View scheduler status and next run time
   curl http://127.0.0.1:8000/scheduler/status
   ```

4. **Update via Python**:
   ```bash
   python -c "from backend.main import orchestrator; orchestrator.bootstrap('daily refresh'); orchestrator.run()"
   ```

### Example Workflow

1. **Agent Planning Phase**:
   - Planning Agent receives: "build arxiv cs daily"
   - Generates tasks: `plan-frontend`, `plan-data`, `plan-detail-page`, `plan-tests`

2. **Code Generation Phase**:
   - Code Generation Agent executes tasks in dependency order
   - Uses LLM to generate `papers.json` with 15 unique papers
   - Creates React components and frontend structure

3. **Evaluation Phase**:
   - Code Evaluation Agent runs `npm run build` to validate
   - Reports build success/failure

4. **Result**:
   - Complete functional web application
   - Papers data in `frontend/src/data/papers.json`
   - All logs in `logs/agent_YYYYMMDD.log`

## 📁 Project Structure

```
arxiv-cs-daily-agent/
├── agents/                  # Agent implementations
│   ├── base_agent.py       # Base agent class
│   ├── planning_agent.py   # Task planning logic
│   ├── code_generation_agent.py  # Code generation
│   └── code_evaluation_agent.py  # Code validation
├── orchestrator/           # Multi-agent orchestration
│   ├── orchestrator.py    # Main orchestrator
│   └── task_types.py      # Task data structures
├── tools/                  # Agent tools
│   ├── file_manager.py    # File operations
│   ├── command_executor.py # Command execution
│   ├── llm_client.py      # LLM API client
│   └── web_search.py      # Web search (placeholder)
├── backend/                # FastAPI backend
│   └── main.py            # API server and agent setup
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.jsx      # Homepage
│   │   │   ├── CategoryPage.jsx  # Category sub-page
│   │   │   └── DetailPage.jsx   # Paper detail page
│   │   ├── data/
│   │   │   └── papers.json      # Generated paper data
│   │   └── App.jsx              # Router setup
│   └── package.json
├── scripts/                # Utility scripts
│   ├── generate_mock_papers.py  # Fallback data generator
│   └── generate_detail_page.py  # Detail page generator
├── logs/                   # Log files
├── .env                    # Environment variables (create this)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## ✨ Features

### arXiv CS Daily Webpage

The generated application includes:

1. **Domain-Specific Navigation System**
   - Categorized navigation by arXiv CS fields (cs.AI, cs.AR, cs.CV, cs.LG, etc.)
   - Category cards with "Browse Papers" buttons
   - Dedicated category pages (`/category/:categoryId`)

2. **Daily Updated Paper List**
   - **Automatically updates daily** via scheduled task (runs at 02:00)
   - Displays latest papers with essential details
   - Paper title (hyperlinked to detail page)
   - Submission date and arXiv field tags
   - Publication date filter
   - Category filtering
   - Can be manually triggered via `/update` API endpoint

3. **Dedicated Paper Detail Page**
   - Direct PDF link to arXiv
   - Core metadata (title, authors, submission date, categories)
   - Citation generation tools:
     - BibTeX format (one-click copy)
     - Standard academic citation (one-click copy)
   - Accessible via `/paper/:paperId` route

### Routing Structure

- `/` - Homepage with hero section, categories, and paper feed
- `/category/:categoryId` - Category-specific paper list (e.g., `/category/cs.AI`)
- `/paper/:paperId` - Individual paper detail page

## 🔧 Configuration

### LLM Configuration

Edit `.env` to configure your LLM provider:

```env
# DeepSeek Example
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat

# OpenAI Example
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### Logging

Logs are automatically written to `logs/agent_YYYYMMDD.log` with:
- Rotation at 10 MB
- 7-day retention
- DEBUG level logging
- Console output with color formatting

## 📊 Key Execution Examples

### Example 1: Initial Build

```bash
python -c "from backend.main import orchestrator; orchestrator.bootstrap('build arxiv cs daily'); orchestrator.run()"
```

**Expected Output**:
- Tasks: `plan-frontend`, `plan-data`, `plan-detail-page`, `plan-tests`
- Generated: `frontend/src/data/papers.json` (15 papers)
- Build validation: `npm run build` success

### Example 2: Daily Refresh (Manual)

```bash
python -c "from backend.main import orchestrator; orchestrator.bootstrap('daily refresh'); orchestrator.run()"
```

Or via API (if server is running):
```bash
curl -X POST http://127.0.0.1:8000/update
```

**Expected Output**:
- LLM generates new paper data with 2025 dates
- Updates `papers.json` with latest submissions
- Fallback to script if LLM fails

### Example 3: Automatic Daily Update

When the backend server is running, daily updates happen automatically:

```bash
# Start server (scheduler starts automatically)
uvicorn backend.main:app --reload

# Check scheduler status
curl http://127.0.0.1:8000/scheduler/status
```

**Expected Output**:
- Scheduler runs daily at 02:00
- Updates paper data automatically
- Logs written to `logs/agent_YYYYMMDD.log`

### Example 4: Check Daily Update Status

```bash
# Check if papers contain today's date
python scripts/check_daily_update.py
```

**Expected Output**:
- Shows today's date
- Lists papers with today's date
- Warns if no today's papers found

### Example 5: View Logs

```bash
# View today's log
cat logs/agent_$(date +%Y%m%d).log

# On Windows PowerShell
Get-Content logs/agent_$(Get-Date -Format "yyyyMMdd").log
```

## 🔍 Verifying Daily Updates

### How to Check if Daily Update is Working

1. **Check Current Papers**:
   ```bash
   python scripts/check_daily_update.py
   ```
   This will show:
   - Today's date
   - Latest date in papers
   - Number of papers with today's date

2. **Check Scheduler Status** (if server is running):
   ```bash
   curl http://127.0.0.1:8000/scheduler/status
   ```
   Shows:
   - Whether scheduler is running
   - Next scheduled run time

3. **Manual Trigger** (to test immediately):
   ```bash
   # Via API
   curl -X POST http://127.0.0.1:8000/update
   
   # Via Python
   python -c "from backend.main import orchestrator; orchestrator.bootstrap('daily refresh'); orchestrator.run()"
   ```

4. **Check Frontend**:
   - Open the webpage
   - Check if hero section shows today's date
   - Filter by today's date in "Publication Date" dropdown
   - Should see papers with today's date

## 🛠️ Development

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `think()` method
3. Register in `orchestrator.py`

### Adding New Tools

1. Create a tool class with `name` attribute and `run()` method
2. Register tool in agent's `__init__` method
3. Use `dispatch_tool()` to invoke

### Extending Functionality

- **New Task Types**: Add to `planning_agent.py` `_draft_plan()` method
- **New LLM Operations**: Extend `code_generation_agent.py` to handle new operation types
- **New Validation**: Add commands to `code_evaluation_agent.py`

## 🐛 Troubleshooting

### LLM API Errors

- **Permission Denied**: Check API key and base URL in `.env`
- **Rate Limit**: Switch to a different model or adjust limits
- **Model Not Found**: Verify model name matches provider's documentation

**Solution**: System automatically falls back to `scripts/generate_mock_papers.py`

### Frontend Build Errors

- **Module Not Found**: Run `npm install` in `frontend/` directory
- **Port Already in Use**: Change port in `vite.config.js` or kill existing process

### Unicode Errors

- **Windows Encoding Issues**: Already handled with `encoding="utf-8"` in `command_executor.py`

## 📝 Notes

- The system uses a fallback mechanism: if LLM calls fail, scripts are executed instead
- All paper data is generated with 2025 dates for realistic testing
- Logs provide detailed traceability of agent actions and decisions
- The frontend automatically uses local data if the backend is unavailable

## 📄 License

This project is created for educational purposes as part of the COMP7103C course assignment.

## 👥 Authors

Multi-agent system implementation for Code Agent Building project.

---

**For detailed system design, challenges, and results analysis, please refer to the Project Report (PDF).**

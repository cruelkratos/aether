# Aether: Cloud-Native AI Agent with Tool Use and Memory

A production-ready AI agent system that leverages external tools (web search, SQL queries, Python code execution, REST APIs) with persistent memory across sessions.

## 🎯 Features

- **Agent Loop**: Reasoning engine with multi-step tool calling
- **Tool Registry**: 4 integrated tools - web search, SQL executor, Python sandbox, API caller
- **Multi-Layer Memory**:
  - Redis: Short-term session cache (24h)
  - PostgreSQL: Long-term conversation history
  - Qdrant: Vector semantic search for context retrieval
- **Web UI**: Interactive chat frontend
- **REST API**: Session-based agent access
- **Security**: Tool call sandboxing, input validation, whitelist enforcement
- **Monitoring**: Metrics endpoint, logging, performance tracking

## 🚀 Quick Start

### Prerequisites (Install on Your Machine)

**System Tools:**
- Docker Desktop (version 20.10+)
- Docker Compose (version 2.0+)
- Git

**Optional Local Development:**
- Python 3.11+
- pip

**Cloud (AWS) Tools:**
- AWS CLI
- kubectl
- eksctl
- helm (optional)

### Local Deployment (Docker Compose)

```bash
# Clone and navigate
git clone <repo> && cd aether

# Start all services
docker-compose up -d --build

# Initialize database
docker-compose exec api python scripts/init_db.py

# Verify services
docker-compose ps

# Access frontend
open http://localhost:8000
```

All 5 services start in the background:
- **API** (port 8000) - FastAPI with Uvicorn
- **Ollama** (port 11434) - Local LLM service (llama2)
- **PostgreSQL** (port 5432) - Conversation history
- **Redis** (port 6379) - Session cache
- **Qdrant** (port 6333) - Vector DB for semantic search

### Stop Services

```bash
docker-compose down
```

---

## 📊 API Endpoints

### Session Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/create` | Create new session |
| POST | `/sessions/{id}/query` | Send query to agent |
| GET | `/sessions/{id}/history` | Get conversation history |
| POST | `/sessions/{id}/reset` | Clear session memory |
| DELETE | `/sessions/{id}` | Delete session |
| GET | `/health/liveness` | Liveness probe |
| GET | `/health/readiness` | Readiness probe |
| GET | `/metrics` | System metrics |

### Example: Create Session and Query

```bash
# Create session
curl -X POST http://localhost:8000/sessions/create

# Query agent
curl -X POST http://localhost:8000/sessions/{SESSION_ID}/query \
  -H "Content-Type: application/json" \
  -d '{"user_prompt":"What is Python?"}'

# Get history
curl http://localhost:8000/sessions/{SESSION_ID}/history
```

---

## 🔧 Tools Available

### 1. Web Search (DuckDuckGo)
```json
{
  "tool": "web_search",
  "query": "latest AI news"
}
```
Returns: Search results, abstracts, related topics

### 2. SQL Query Executor
```json
{
  "tool": "sql_query",
  "query": "SELECT * FROM users LIMIT 10"
}
```
- Only SELECT queries allowed
- Connected to PostgreSQL
- 10-second timeout

### 3. Python Executor (Sandbox)
```json
{
  "tool": "python_exec",
  "code": "print(sum([1,2,3]))"
}
```
- Whitelisted imports: math, json, re, datetime, collections, etc.
- 30-second timeout
- No file I/O or system commands

### 4. REST API Caller
```json
{
  "tool": "api_call",
  "url": "https://jsonplaceholder.typicode.com/posts/1",
  "method": "GET"
}
```
- HTTP GET/POST/PUT/DELETE/PATCH
- 15-second timeout
- SSRF protection with whitelisting

---

## 🧪 Testing

### Run All Tests
```bash
# Inside container
docker-compose exec api pytest -v

# On host
set PYTHONPATH=%cd%
pytest -v
```

### Test Files
- `tests/test_basic.py` - Health checks
- `tests/test_api.py` - Session API endpoints
- `tests/test_tools.py` - Individual tool functionality
- `tests/test_agent.py` - Agent loop and memory

### Test Coverage
- 15+ API endpoint tests
- 8+ tool execution tests
- Agent loop with memory integration tests
- End-to-end workflow tests

---

## 💾 Architecture

### Request Flow
```
User Query → Session API → Agent Loop → Memory Handler
     ↓
Tool Registry → (Web Search | SQL | Python | API) → Memory Layers
     ↓
Response → Session History → User
```

### Memory Layers
1. **Redis Cache**: Last 20 messages, 24h TTL
2. **PostgreSQL**: Full history, structured queries
3. **Qdrant**: Embeddings for semantic search

### Agent Reasoning
1. Retrieve context from all memory layers
2. Build prompt with available tools
3. Call LLM (Ollama/OpenAI)
4. Parse tool selection from response
5. Execute tool (with safety checks)
6. Update memory with result
7. Repeat until final answer

---

## 🛠️ Configuration

### Environment Variables (`.env`)
```
REDIS_URL=redis://redis:6379
DATABASE_URL=postgresql+asyncpg://aether:aether_pass@postgres:5432/aether_db
QDRANT_URL=http://qdrant:6333
OLLAMA_URL=http://ollama:11434
```

### Docker Compose Override
Edit `docker-compose.yml` to:
- Change Ollama model: Update `ollama` service
- Adjust resource limits: Add `deploy: resources`
- Use external databases: Update environment variables

---

## ☁️ Cloud Deployment (AWS EKS)

### Preparation
1. Install AWS CLI and eksctl
2. Configure AWS credentials
3. Have Docker image pushed to ECR

### Deploy to EKS
```bash
# Create cluster (one-time)
eksctl create cluster --name aether-prod --region us-east-1

# Deploy services
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/postgres-statefulset.yaml
kubectl apply -f k8s/redis-statefulset.yaml
kubectl apply -f k8s/qdrant-deployment.yaml
kubectl apply -f k8s/agent-api-deployment.yaml
kubectl apply -f k8s/ingress.yaml

# Monitor deployment
kubectl get pods -n aether
kubectl logs -n aether deployment/aether-api
```

### Production Changes
- Ollama → OpenAI API (set in config)
- PostgreSQL → AWS RDS
- Redis → AWS ElastiCache
- Qdrant → Keep in-cluster or Pinecone
- Add horizontal autoscaling
- Add ingress/load balancer
- Configure SSL/TLS

---

## 📝 Project Structure

```
aether/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── models.py            # SQLAlchemy models
│   ├── logging_utils.py     # Logging & metrics
│   ├── api/
│   │   ├── session_routes.py
│   │   └── models.py
│   ├── agent/
│   │   ├── agent_loop.py
│   │   ├── tool_registry.py
│   │   ├── llm_interface.py
│   │   └── tools/
│   │       ├── web_search.py
│   │       ├── sql_executor.py
│   │       ├── python_executor.py
│   │       └── api_caller.py
│   ├── memory/
│   │   ├── memory_handler.py
│   │   ├── redis_layer.py
│   │   ├── postgres_layer.py
│   │   └── qdrant_layer.py
│   └── database.py
├── frontend/
│   └── index.html           # Web UI
├── scripts/
│   ├── init_db.py
│   └── seed_db.py
├── tests/
│   ├── test_basic.py
│   ├── test_api.py
│   ├── test_tools.py
│   └── test_agent.py
├── k8s/                     # Kubernetes manifests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔐 Security & Limitations

### Security Measures
- Tool call sandboxing (Python subprocess timeout)
- SQL whitelist (SELECT only, no DDL/DML)
- API whitelist (SSRF protection)
- Input validation on all endpoints
- CORS configured for frontend

### Known Limitations
- Single Ollama instance (no load balancing local)
- In-memory session store (use PostgreSQL in prod)
- Python sandboxing is basic (use Docker/Firecracker in prod)
- No auth on API (implement JWT/API keys in prod)
- Embedding generation is hash-based (use OpenAI/Hugging Face in prod)

---

## 📊 Monitoring

### Health Checks
```bash
curl http://localhost:8000/health/liveness
curl http://localhost:8000/health/readiness
```

### Metrics
```bash
curl http://localhost:8000/metrics
```

Returns:
```json
{
  "queries_total": 42,
  "queries_success": 40,
  "success_rate": 95.2,
  "avg_query_duration": 3.2,
  "active_sessions": 5,
  "tools_total": 15,
  "tools_success": 13
}
```

---

## 🧑‍💻 Development

### Install Dependencies (Host)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Tests on Host
```bash
set PYTHONPATH=%cd%
pytest -v
```

### Run API Directly
```bash
uvicorn app.main:app --reload --port 8000
```

### Add New Tool
1. Create `app/agent/tools/your_tool.py`
2. Implement async function: `async def your_tool(**kwargs) -> dict`
3. Register in `app/agent/tool_registry.py`
4. Add tests in `tests/test_tools.py`

---

## 📈 Performance Tips

- **Increase Ollama replicas** for concurrent requests
- **Use larger LLM model** for better reasoning (llama2-13b)
- **Cache embeddings** in Redis for repeated queries
- **Reduce context window** to speed up LLM calls
- **Use CloudFront** for static frontend assets

---

## 🐛 Troubleshooting

### Container won't start
```bash
docker-compose logs api --tail=50
```

### API connection refused
```bash
# Check if port 8000 is available
netstat -an | grep 8000
# Or just wait for container startup (takes 10-15s)
```

### Ollama timeout
- Model is downloading: `docker exec aether-ollama-1 ollama list`
- Pull model: `docker exec aether-ollama-1 ollama pull llama2`

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose ps postgres
# View logs
docker-compose logs postgres --tail=20
```

---

## 📚 Next Steps

- [ ] Deploy to AWS EKS
- [ ] Integrate OpenAI GPT-4 for better reasoning
- [ ] Add persistent session storage
- [ ] Implement user authentication
- [ ] Add rate limiting
- [ ] Set up monitoring with Prometheus/Grafana
- [ ] Create advanced test scenarios (20+ workflows)
- [ ] Optimize embedding model
- [ ] Add voice input support

---

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create feature branch
3. Add tests
4. Submit PR

---

**Built with ❤️ for the future of AI agents.**

### Running Tests

#### Option 1: Inside Docker (Recommended)
```bash
# Run all tests
docker-compose exec api pytest -v

# Run specific test file
docker-compose exec api pytest tests/test_basic.py -v

# Run with coverage
docker-compose exec api pytest --cov=app --cov-report=html
```

#### Option 2: On Host Machine
```bash
# Install dependencies locally
pip install -r requirements.txt

# Set Python path and run tests
PYTHONPATH=. pytest -v
PYTHONPATH=. pytest tests/test_basic.py -v

# Or use pytest.ini (automatically sets path)
pytest -v
pytest tests/test_basic.py -v
```

#### Option 3: Direct Python execution (not recommended)
```bash
# This requires manual PYTHONPATH setup
PYTHONPATH=. python -m pytest tests/test_basic.py -v
```

# TEN Backend

**The Entrepreneurial Navigator** - A comprehensive platform designed to empower early-stage startups with AI-driven insights, risk evaluation, reputation analysis, investor matching, and strategic guidance.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

## 📚 Documentation

**Live API Documentation:**
- **Interactive Docs (Swagger UI):** [https://ten-be.koyeb.app/docs](https://ten-be.koyeb.app/docs)
- **ReDoc:** [https://ten-be.koyeb.app/redoc](https://ten-be.koyeb.app/redoc)

---

## 🚀 Features

TEN Backend provides 10 comprehensive endpoints for startup ecosystem navigation:

- **Risk Assessment** - Evaluate potential business risks and mitigation strategies
- **Reputation Analysis** - Monitor and analyze brand reputation across digital channels  
- **Investor Matching** - Connect with suitable investors based on startup profile
- **Pitch Feedback** - Get AI-powered feedback on pitch decks and presentations
- **Competitor Radar** - Comprehensive competitive landscape analysis
- **Traction Estimator** - Assess and project business traction metrics
- **Buzz Builder** - Strategic content and marketing recommendations
- **Legal Assistance** - Basic legal guidance for startup operations
- **Exit Strategy** - Strategic planning for business exits and acquisitions
- **Talent Navigator** - Hiring and team building recommendations

---

## 🏗️ Architecture

### Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **AI Engine:** [Google Gemini 1.5 Flash](https://ai.google.dev/) - Advanced AI model for intelligent responses
- **Caching:** [Redis](https://redis.io/) - In-memory caching with 1-hour TTL
- **Deployment:** [Koyeb](https://www.koyeb.com/) - Cloud platform for seamless deployment
- **Containerization:** [Docker](https://www.docker.com/) - Containerized deployment

### External Services

- **Search Integration:** [SerpAPI](https://serpapi.com/) - Real-time search results integration
- **Cache Storage:** [Upstash Redis](https://upstash.com/) - Serverless Redis database

---

## 🛠️ Local Development Setup

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose**
- **Redis**

### 1. Clone Repository

```bash
git clone https://github.com/Afnanksalal/TEN
cd TEN/TEN_BE
```

### 2. Redis Setup

Choose one of the following Redis setup options:

#### Option A: Local Redis Installation

**Install Redis locally:**

```bash
# macOS (using Homebrew)
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server

# Windows (using WSL or download from Redis website)
# Visit: https://redis.io/download
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

#### Option B: Upstash Redis (Cloud-based)

1. **Sign up at [Upstash](https://upstash.com/)**
2. **Create a new Redis database**
3. **Copy the connection string** (format: `rediss://default:password@endpoint:port`)

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
# Redis Configuration (choose one)
# For local Redis:
REDIS_URL="redis://localhost:6379"
# For Upstash Redis:
# REDIS_URL="rediss://default:your_password@your_endpoint.upstash.io:your_port"

# Application Settings
APP_NAME="The Entrepreneurial Navigator"

# API Keys (obtain from respective services)
GOOGLE_API_KEY="your_google_gemini_api_key_here"
SERPAPI_API_KEY="your_serpapi_key_here"

# Authentication (generate secure random strings)
VALID_API_KEYS='["your_api_key_1", "your_api_key_2", "your_api_key_3"]'
```

#### Getting API Keys

**Google Gemini API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the generated key

**SerpAPI Key:**
1. Sign up at [SerpAPI](https://serpapi.com/)
2. Navigate to your dashboard
3. Copy your API key

### 4. Docker Development Setup

#### Using Docker Compose (Recommended)

```bash
# Build and start the development environment
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Manual Docker Build

```bash
# Build the Docker image
docker build -t ten-backend .

# Run the container
docker run -p 8000:8000 --env-file .env ten-backend
```

### 5. Local Python Setup (Alternative)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Access the Application

- **API Base URL:** http://localhost:8000
- **Interactive Documentation:** http://localhost:8000/docs
- **ReDoc Documentation:** http://localhost:8000/redoc

---

## 📦 Dependencies

### Core Framework
- **[fastapi](https://fastapi.tiangolo.com/)** - Modern web framework for building APIs
- **[uvicorn[standard]](https://www.uvicorn.org/)** - ASGI server implementation
- **[pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[pydantic-settings](https://docs.pydantic.dev/latest/usage/settings/)** - Settings management for Pydantic

### AI & External Services
- **[google-generativeai](https://ai.google.dev/)** - Google Gemini AI integration
- **[google-search-results](https://serpapi.com/)** - SerpAPI integration for search functionality
- **[aiohttp](https://docs.aiohttp.org/)** - Asynchronous HTTP client/server

### Caching & Performance
- **[redis](https://redis-py.readthedocs.io/)** - Redis client for Python
- **[fastapi-limiter[redis]](https://github.com/long2ice/fastapi-limiter)** - Rate limiting with Redis backend

### Utilities
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[python-multipart](https://github.com/andrew-d/python-multipart)** - Multipart form data parsing

---

## 🐳 Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose with Local Redis

If using local Redis, update your `docker-compose.yml`:

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
  
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./app:/app/app
      - ./requirements.txt:/app/requirements.txt
    depends_on:
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  redis_data:
```

And update your `.env` file:
```env
REDIS_URL="redis://redis:6379"  # Note: use 'redis' as hostname in Docker Compose
```

---

## 🔧 Configuration Options

### Redis Configuration

The application supports both local and cloud Redis instances:

- **Local Redis:** `redis://localhost:6379`
- **Upstash Redis:** `rediss://default:password@endpoint:port`
- **Docker Compose Redis:** `redis://redis:6379`

### Rate Limiting

API endpoints are rate-limited using Redis. Configure limits in your application settings:

- Default: 100 requests per minute per IP
- Cached responses: 1-hour TTL

---

## 🚦 API Endpoints

All endpoints accept JSON payloads and return structured responses:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/risk-assessment` | POST | Evaluate business risks and mitigation strategies |
| `/reputation-analysis` | POST | Analyze brand reputation across channels |
| `/investor-matching` | POST | Match startups with suitable investors |
| `/pitch-feedback` | POST | AI-powered pitch deck feedback |
| `/competitor-radar` | POST | Competitive landscape analysis |
| `/traction-estimator` | POST | Business traction metrics assessment |
| `/buzz-builder` | POST | Marketing and content strategy |
| `/legal-assistance` | POST | Basic legal guidance for startups |
| `/exit-strategy` | POST | Strategic exit planning |
| `/talent-navigator` | POST | Hiring and team building guidance |

### Authentication

Currently, the API uses simple API key authentication:

```bash
curl -X POST "http://localhost:8000/risk-assessment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{"company_data": "..."}'
```

---

## 🧪 Testing

### Manual Testing

Use the interactive documentation at `http://localhost:8000/docs` to test endpoints directly in your browser.

### Command Line Testing

```bash
# Health check
curl http://localhost:8000/health

# Test endpoint (replace with actual API key)
curl -X POST "http://localhost:8000/risk-assessment" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"startup_info": "AI-powered fintech startup"}'
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the [API documentation](https://ten-be.koyeb.app/docs)
- Review the setup guide above

---

**Built with ❤️ for the startup ecosystem**

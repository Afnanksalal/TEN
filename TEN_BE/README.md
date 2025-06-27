# TEN Backend

This is the backend API for **TEN – The Entrepreneurial Navigator**, a tool that helps early-stage startups with risk evaluation, reputation insights, investor matching, pitch feedback, competitor analysis, and more.

📄 **API Docs:**  
[https://ten-be.koyeb.app/redoc](https://ten-be.koyeb.app/redoc)

---

## 🔹 Tech Overview

- Built with **FastAPI**
- Uses **Gemini 1.5 Flash** for all AI-driven tasks (including sentiment)
- **Redis** for caching responses (1-hour TTL)
- Hosted on **Koyeb**

---

## 🧩 Main Endpoints

Each route takes structured JSON input and returns contextual AI-generated output.

- `/risk-assessment`  
- `/reputation-analysis`  
- `/investor-matching`  
- `/pitch-feedback`  
- `/competitor-radar`  
- `/traction-estimator`  
- `/buzz-builder`  
- `/legal-assistance`  
- `/exit-strategy`  
- `/talent-navigator`

See full request/response formats in the [Redoc docs](https://ten-be.koyeb.app/redoc).

---

## 🔐 Auth

No authentication required (public endpoints). Rate limits and access controls may be added in future versions.


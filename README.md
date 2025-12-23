# JobFlowAI

JobFlowAI is an AI-powered resume comparison, enhancement, and interview assistant. It simplifies the job application process by providing tools to analyze and improve your resume, compare it against job descriptions, and prepare for interviews.

## 🚀 One-Click Deployment

| Frontend (Vercel) | Backend (Render) |
| :---: | :---: |
| [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fshyamsunderprogramer-design%2FJobflowai&project-name=jobflowai-frontend&framework=create-react-app&root-directory=frontend&env=REACT_APP_API_BASE_URL) | [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/shyamsunderprogramer-design/Jobflowai) |

> **Note:** For Vercel, set `REACT_APP_API_BASE_URL` to your Render backend URL after deploying the backend.
> **Note:** For Render, you will be prompted to input `OPENAI_API_KEY`.

## Features

-   **Resume & Cover Letter Generation**: Create professional resumes and cover letters.
-   **Resume Enhancement**: Improve your resume with AI-driven suggestions.
-   **Resume Comparison**: Compare your resume against job descriptions to see how well you match.
-   **Interview Preparation**: Get AI-generated interview questions and feedback.
-   **Job Search**: Find relevant job openings (integrated with job news).
-   **Profile Management**: Manage your professional profile.
-   **Payments & Trials**: Premium features integrated with Stripe.

## Tech Stack

### Backend
-   **Language**: Python
-   **Framework**: FastAPI
-   **Database**: PostgreSQL (SQLAlchemy with Alembic migrations)
-   **Authentication**: JWT (JSON Web Tokens)
-   **AI Integration**: OpenAI (implied by env vars)

### Frontend
-   **Language**: TypeScript / JavaScript
-   **Framework**: React
-   **Styling**: Vanilla CSS / Tailwind (to be confirmed, uses `react-scripts`)
-   **Libraries**: `axios`, `lucide-react`, `react-router-dom`

### Infrastructure
-   **Containerization**: Docker & Docker Compose
-   **Reverse Proxy**: Likely Nginx (if deployed), or direct API access in dev.

## Getting Started

### Prerequisites
-   [Docker](https://www.docker.com/products/docker-desktop) and Docker Compose installed.
-   Or, for local development without Docker:
    -   Python 3.8+
    -   Node.js 14+
    -   PostgreSQL

### Installation (Docker - Recommended)

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd JobFlowAI
    ```

2.  **Environment Setup:**
    -   Create a `.env` file in the `backend/` directory (or root if using docker-compose env file option).
    -   Refer to `backend/main.py` or `backend/config.py` for required environment variables (e.g., `OPENAI_API_KEY`, `DATABASE_URL`, `SECRET_KEY`).

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    -   The backend API will be available at `http://localhost:8000`.
    -   The database will be available on port `5432`.

### Local Development (Manual)

#### Backend
1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    uvicorn main:app --reload
    ```

#### Frontend
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```
    -   The app will run at `http://localhost:3000`.

## Project Structure

```
JobFlowAI/
├── backend/                # FastAPI Backend
│   ├── main.py             # Application entry point
│   ├── routes/             # API Endpoints
│   ├── models.py           # Database Models
│   ├── schemas/            # Pydantic Schemas
│   ├── services/           # Business Logic
│   └── ...
├── frontend/               # React Frontend
│   ├── public/             # Static Assets
│   ├── src/                # Source Code
│   │   ├── components/     # Reusable Components
│   │   ├── pages/          # Application Pages
│   │   └── ...
│   └── package.json        # Frontend Dependencies
├── docker-compose.yml      # Docker Services Configuration
├── requirements.txt        # Backend Dependencies (Root reference)
└── README.md               # Project Documentation
```

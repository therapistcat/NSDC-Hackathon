# 🚀 HR EdTech Platform for Gen Z

An interactive learning platform featuring gamification, micro-learning, community engagement, and AI-powered mentorship. Built for the modern workforce with a focus on Gen Z engagement through badges, streaks, and progressive unlock systems.

## 🌟 Key Features

### **🎮 Gamified Learning System**
- **Reinforcement Learning Quizzes**: Adaptive difficulty based on performance
- **Time-Based Constraints**: Strategic timing with penalties for exceeding limits
- **Tab-Switching Detection**: Anti-cheating mechanism for fair play
- **Comprehensive Badges**: 8+ achievement types (Quiz Master, Interview Ace, Mentorship Master, etc.)
- **Points & Leaderboards**: Competitive ranking system
- **Daily Streaks**: Habit-building through consistent engagement

### **🧠 AI-Powered Micro Learning**
- **Personalized Content Curation**: Tag-based content recommendations
- **Daily Flashcards**: Bite-sized learning modules
- **Learning Roadmaps**: AI-generated career progression paths
- **Streak Tracking**: Visual progress indicators
- **Resource Library**: Videos, articles, and interactive content

### **👥 Community Hub**
- **Semantic Search**: Smart community recommendations based on user interests
- **Discussion Forums**: Real-time post and comment system
- **Specialized Communities**: Topic-based groups for focused learning
- **Networking Features**: Connect with peers and mentors

### **🎯 Interview & Mentorship**
- **Badge-Locked Scheduling**: Mock interviews require earned achievements
- **Skill-Based Matching**: Automatic mentor-student pairing
- **Performance Scoring**: Comprehensive interview evaluation
- **Direct Connect**: Instant mentorship sessions (5+ badges required)
- **Career Exploration**: Unconventional career path recommendations

### **📊 Dual Dashboard System**
- **Student Dashboard**: Gamified learning experience with progress tracking
- **Recruiter Dashboard**: Digital resume system viewing student talent
- **Real-Time Stats**: Points, badges, streaks, and rankings
- **Quick Actions**: One-click access to all features

## 🛠️ Technology Stack

**Backend:**
- **Framework**: FastAPI (async Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT tokens with role-based access
- **Validation**: Pydantic schemas
- **Documentation**: Auto-generated Swagger UI

**Frontend Requirements (To Be Built):**
- **Framework**: React 18+ with Vite
- **Styling**: TailwindCSS + Custom Components
- **Animations**: Framer Motion + Locomotive Scroll
- **3D Elements**: Three.js for interactive components
- **State Management**: Context API or Redux
- **Forms**: React Hook Form with validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- Node.js 16+ (for frontend development)

### Backend Setup

1. **Clone and Navigate**
```bash
git clone <repository-url>
cd nsdc-hackathon/backend
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
Create `.env` file in `backend/` directory:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=nsdc_hackathon
SECRET_KEY=your-super-secret-key-here-generate-new-one
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Start MongoDB**
```bash
# If using local MongoDB
mongod
```

5. **Run Backend Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI.

---

## 📚 API Documentation

### Base URL: `http://localhost:8000/api/v1`

### Authentication
All protected endpoints require Bearer token authentication:
```
Authorization: Bearer <jwt_token>
```

---

## 🔐 Authentication Endpoints

### Student Registration
**POST** `/auth/student/signup`
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password",
  "domains": "Data Science, Machine Learning",
  "skills": "Python, SQL, TensorFlow",
  "interests": "AI, Career Development, Tech Innovation"
}
```
**Response:**
```json
{
  "id": "64f...",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "student",
  "message": "Student registered successfully"
}
```

### Recruiter Registration
**POST** `/auth/recruiter/signup`
```json
{
  "name": "Jane Smith",
  "email": "jane@company.com",
  "password": "secure_password",
  "company": "TechCorp Inc",
  "position": "HR Manager"
}
```

### Mentor Registration
**POST** `/auth/mentor/signup`
```json
{
  "name": "Dr. Bob Wilson",
  "email": "bob@expert.com",
  "password": "secure_password",
  "expertise": "Data Science, Leadership, Career Counseling",
  "experience_years": 15
}
```

### Login
**POST** `/auth/login`
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```
**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user_id": "64f...",
  "role": "student"
}
```

---

## 👤 User Management Endpoints

### Get Dashboard
**GET** `/user/dashboard` (Auth Required)
Returns role-specific dashboard data with gamification stats.

**Student Dashboard Response:**
```json
{
  "user_profile": {
    "name": "John Doe",
    "role": "student",
    "points": 450,
    "badges": ["Quiz Master", "Rising Star"],
    "streak_days": 7,
    "domains": ["Data Science"],
    "skills": ["Python", "SQL"],
    "interests": ["AI", "Career Development"]
  },
  "gamification": {
    "latest_quiz_attempts": [...],
    "earned_badges": ["Quiz Master"],
    "current_streak": 7,
    "points_earned": 450,
    "leaderboard_rank": 15
  },
  "learning": {
    "upcoming_interviews": [],
    "community_memberships": [...],
    "learning_streak": 7
  },
  "quick_actions": ["Take Daily Quiz", "View Learning", ...]
}
```

**Recruiter Dashboard Response:**
```json
{
  "total_students_viewed": 25,
  "top_talent": [
    {
      "id": "64f...",
      "name": "John Doe",
      "points": 450,
      "badges": ["Quiz Master"],
      "domains": ["Data Science"],
      "skills": ["Python", "SQL"],
      "completed_interviews": 2
    }
  ],
  "search_filters": {
    "domains": ["Data Science", "Marketing"],
    "skills": ["Python", "JavaScript"],
    "badge_filter": ["Quiz Master", "Interview Ace"]
  }
}
```

---

## 🎮 Quiz System Endpoints

### Get Available Quizzes
**GET** `/quiz/available?difficulty=easy` (Auth Required)
```json
[
  {
    "id": "64f...",
    "title": "Data Science Fundamentals",
    "difficulty": "easy",
    "questions_count": 10,
    "points": 10,
    "time_limit": 300
  }
]
```

### Submit Quiz Attempt
**POST** `/quiz/attempt` (Auth Required)
```json
{
  "quiz_id": "64f...",
  "answers": [
    {"question_id": 0, "answer": "A"},
    {"question_id": 1, "answer": "B"}
  ],
  "time_taken": 280,
  "tab_switches": 1
}
```
**Response:**
```json
{
  "correct_answers": 8,
  "total_questions": 10,
  "score_percentage": 80.0,
  "final_score": 76.0,
  "points_earned": 76,
  "badges_earned": ["Quiz Master"],
  "next_recommended_difficulty": "hard",
  "message": "Quiz completed! You scored 76.0%"
}
```

### Get Leaderboard
**GET** `/quiz/leaderboard?limit=10` (Auth Required)
```json
[
  {
    "rank": 1,
    "name": "Jane Smith",
    "points": 1250,
    "badges": ["Quiz Master", "Interview Ace"],
    "quiz_attempts": 25
  }
]
```

---

## 🧠 Learning Endpoints

### Get Daily Content
**GET** `/learning/daily-content` (Auth Required)
```json
{
  "daily_content": [
    {
      "_id": "64f...",
      "title": "Machine Learning Basics",
      "content": "...",
      "topic": "AI/ML",
      "summary": "Introduction to ML concepts",
      "flashcards": [
        {
          "question": "What is Machine Learning?",
          "answer": "A subset of AI that enables computers to learn...",
          "difficulty": "easy"
        }
      ]
    }
  ],
  "total_items": 5,
  "message": "AI-curated learning content for today"
}
```

### Get Learning Resources
**GET** `/learning/resources?topic=python&skill_level=beginner` (Auth Required)
```json
{
  "resources": [
    {
      "_id": "64f...",
      "title": "Python for Beginners",
      "resource_type": "video",
      "url": "https://youtube.com/...",
      "skill_level": "beginner",
      "match_score": 85
    }
  ]
}
```

### Create Learning Roadmap
**POST** `/learning/roadmap` (Auth Required)
```json
{
  "career_goal": "Data Scientist",
  "time_commitment": "10 hours/week",
  "current_level": "intermediate"
}
```

---

## 👥 Community Endpoints

### Get Community Recommendations
**GET** `/community/recommend` (Auth Required)
Semantic search based on user tags, returns personalized community suggestions.

### Join Community
**POST** `/community/{community_id}/join` (Auth Required)
```json
{"message": "Successfully joined community"}
```

### Create Community
**POST** `/community/create` (Auth Required)
```json
{
  "name": "Data Science Enthusiasts",
  "description": "Community for data lovers",
  "topic": "Data Science",
  "tags": "python, data, analytics"
}
```

---

## 🎯 Interview Endpoints

### Schedule Interview
**POST** `/interview/schedule` (Auth Required, requires 3+ badges)
```json
{
  "mentor_id": "64f...",
  "scheduled_time": "2025-01-15T14:00:00.000Z",
  "topic": "System Design",
  "difficulty": "medium"
}
```

### Complete Interview
**PUT** `/interview/{interview_id}/complete` (Mentor only)
```json
{
  "score": 85.5,
  "feedback": "Great communication skills...",
  "strengths": "Problem solving approach",
  "improvements": "Technical depth"
}
```

---

## 🤝 Mentor Connect Endpoints

### Direct Mentor Connect
**POST** `/mentor-interviews/connect/{student_id}` (Auth Required, requires 5+ badges)
Instant connection with skill-matched mentor for direct support.

### Get Career Exploration
**GET** `/mentor-interviews/recommend/career-exploration` (Auth Required, requires apex badges)
```json
{
  "unconventional_careers": [
    {
      "title": "AI Ethics Consultant",
      "description": "Guide ethical AI development",
      "required_skills": ["AI", "Ethics", "Policy"],
      "growth_potential": "High",
      "salary_range": "$120K-$180K",
      "match_score": 90
    }
  ]
}
```

---

## 📊 Error Handling

### Standard Error Response Format
```json
{
  "detail": "Error message description",
  "status_code": 400
}
```

### Common HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (invalid/missing token)
- **403**: Forbidden (insufficient permissions/badges)
- **404**: Not Found
- **422**: Validation Error (Pydantic validation)
- **500**: Internal Server Error

### Badge-Requirement Errors
```json
{
  "detail": "You need at least 3 badges for mock interviews. Current: 1",
  "status_code": 403
}
```

---

## 🏗️ Frontend Implementation Guide

### Core Requirements
1. **React Application**: Vite + TypeScript
2. **Styling**: TailwindCSS + Custom components
3. **Animations**: Framer Motion for micro-interactions
4. **State Management**: Context API for user auth & app state
5. **API Client**: Axios or Fetch with interceptor for auth

### Key Components to Implement

#### Authentication Flow
```tsx
// AuthContext for token management
const AuthContext = createContext<AuthContextType>({...});

// Login/Signup forms with validation
// Role-based routing protection
// Auto token refresh mechanism
```

#### Quiz System
```tsx
// QuizPlayer component with timer
// Tab-switch detection (visibilitychange API)
// Real-time score calculation
// Results screen with confetti animations
// Badge unlock celebrations
```

#### Dashboard Components
```tsx
// Role-specific dashboard rendering
// Gamification progress visualization
// Quick action cards
// Real-time stats updates
```

#### Learning Interface
```tsx
// Flashcard swiper component
// Daily content grid
// Learning roadmap visualization
// Streak calendar component
```

### Visual Design Specifications

#### Color Palette
```css
:root {
  --primary: #6366f1;      /* Indigo */
  --secondary: #ec4899;    /* Pink */
  --accent: #06b6d4;      /* Cyan */
  --success: #10b981;     /* Green */
  --warning: #f59e0b;     /* Yellow */
  --error: #ef4444;       /* Red */
  --background: #f8fafc;  /* Light gray */
}
```

#### Typography Scale
- **H1**: 2.25rem (36px) Bold
- **H2**: 1.875rem (30px) Bold
- **H3**: 1.5rem (24px) Bold
- **Body**: 1rem (16px) Regular
- **Small**: 0.875rem (14px) Regular

### Mobile-First Responsive Design
- **Desktop**: 1024px+ (full dashboard)
- **Tablet**: 768-1023px (stacked layout)
- **Mobile**: <768px (single column, bottom navigation)

### Animations & Interactions
- **Page Transitions**: Slide in/out effects
- **Hover States**: Scale transforms, color changes
- **Loading States**: Skeleton screens, spinners
- **Celebration Effects**: Confetti, particle systems
- **Progress Indicators**: Circular progress, animated bars

---

## 🎯 User Journey Examples

### New Student Onboarding
1. **Signup**: Choose domains, skills, interests
2. **Assessment Quiz**: Initial skill evaluation
3. **Daily Learning**: Personalized content delivery
4. **Community Join**: Recommended communities
5. **Goals Setting**: Career roadmap creation

### Quiz Experience
1. **Selection**: Choose difficulty (with recommendation)
2. **Gameplay**: Timer, questions, tab monitoring
3. **Penalties**: Time overage and tab switch deductions
4. **Results**: Score breakdown, badges earned
5. **Progression**: Next difficulty recommendation

### Mentorship Journey
1. **Badge Earning**: Unlock interview scheduling (3+ badges)
2. **Interview Prep**: Schedule with preferred mentor
3. **Practice Session**: Comprehensive interview experience
4. **Direct Connect**: Unlock instant mentor chats (5+ badges)
5. **Career Guidance**: Explore unconventional paths

---

## 📈 Scaling Considerations

### Database Optimization
- **Indexing**: User tags, quiz attempts, community memberships
- **Caching**: Redis for leaderboard data, frequent queries
- **Pagination**: Large result sets (communities, leaderboards)
- **Aggregation**: MongoDB pipelines for analytics

### Performance Enhancements
- **CDN**: Static assets distribution
- **Compression**: Gzip response compression
- **Lazy Loading**: Component/code splitting
- **Image Optimization**: WebP format, lazy loading

### Monitoring & Analytics
- **Usage Tracking**: User engagement metrics
- **Performance Monitoring**: API response times
- **Error Logging**: Sentry integration
- **Business Metrics**: Feature usage, conversion rates

---

## 🔒 Security Features

### Authentication Security
- **JWT Tokens**: Stateless authentication
- **Password Hashing**: bcrypt with salt
- **Rate Limiting**: Prevent brute force attacks
- **Session Management**: Automatic logout on inactivity

### API Security
- **Input Validation**: Pydantic models for all endpoints
- **CORS Configuration**: Frontend domain restriction
- **SQL Injection Prevention**: MongoDB injection protection
- **XSS Protection**: Input sanitization

---

## 🚀 Deployment Guide

### Backend Deployment
1. **Container Setup**: Docker + Uvicorn
2. **Environment Variables**: Production secrets
3. **Database**: MongoDB Atlas or managed instance
4. **Reverse Proxy**: Nginx for static file serving
5. **SSL/TLS**: Let's Encrypt certificates

### Frontend Deployment
1. **Build Process**: `npm run build`
2. **Static Hosting**: Vercel, Netlify, or S3+CloudFront
3. **Environment Config**: Separate API URLs for development/production
4. **CDN**: Global content delivery

### CI/CD Pipeline
1. **Automated Testing**: Unit and integration tests
2. **Code Quality**: ESLint, Prettier, Black formatting
3. **Deployment**: GitHub Actions for automated deployment
4. **Monitoring**: Error tracking and performance alerts

---

This comprehensive documentation provides everything needed to build the complete HR EdTech platform frontend. Each endpoint is documented with request/response examples, and the system architecture supports all Gen Z learning preferences through gamification and progressive engagement features.

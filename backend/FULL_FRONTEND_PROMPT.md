# Complete Frontend Prompt for HR EdTech Platform

## Platform Overview
**HR EdTech Platform for Gen Z** - An interactive learning platform with gamification, micro-learning, community features, and AI-powered mentorship.

## Core Features Implemented ✅

### 1. **Dual Dashboard System**
- **Student Dashboard**: Gamified learning experience
- **Recruiter Dashboard**: Digital resume viewing with student talent pool

### 2. **Authentication & User Management**
- Student, Recruiter, and Mentor signups
- JWT-based authentication
- Profile management with domains, skills, interests

### 3. **Gamified Quiz System**
- **Difficulty Levels**: Easy (10 points), Medium (20 points), Hard (30 points)
- **Time Limits**: Easy (30s/question), Medium (45s/question), Hard (60s/question)
- **Reinforcement Learning**: Adapts difficulty based on performance
- **Penalties**: Time limit penalties, tab-switching detection
- **Badges**: Quiz Master, Perfect Score, Rising Star, Interview Ace, etc.

### 4. **AI-Powered Micro Learning**
- Daily curated content with flashcards
- Video, article, resource recommendations
- Learning streaks and progress tracking
- Personalized roadmaps

### 5. **Community Hub**
- Semantic search community recommendations
- Post creation and discussion forums
- Membership management

### 6. **Mock Interview System**
- Badge-locked scheduling (3+ badges required)
- Mentor evaluation and scoring
- Interview performance tracking

### 7. **Direct Mentor Connect**
- Badge-locked feature (5+ badges required)
- Skill-based mentor matching
- Video/audio/chat sessions

### 8. **Career Exploration**
- Apex badge-locked feature
- Unconventional career recommendations
- Skill-based career suggestions

---

## 🛠️ TECHNICAL STACK
- **Frontend**: React + Vite
- **UI Framework**: Clean, modern design with animations
- **State Management**: Context API or Redux
- **Styling**: TailwindCSS + Custom Components
- **Animations**: Locomotive Scroll + Framer Motion
- **3D Elements**: Three.js for interactive components
- **Backend**: FastAPI + MongoDB

---

## 🎨 UI DESIGN SPECIFICATIONS

### Color Scheme
```javascript
const colors = {
  primary: '#6366f1',     // Indigo
  secondary: '#ec4899',   // Pink
  accent: '#06b6d4',     // Cyan
  success: '#10b981',    // Green
  warning: '#f59e0b',    // Yellow
  error: '#ef4444',      // Red
  background: '#f8fafc', // Light gray
  surface: '#ffffff',
  text: '#1f2937',
  textSecondary: '#64748b'
}
```

### Typography
- **Primary Font**: Poppins (Modern, clean)
- **Secondary Font**: Inter (Highly readable)
- **Headings**: Bold, 2rem+
- **Body**: Regular, 1rem
- **Accent Text**: Semi-bold

### Design Principles
- **Clean UI**: Minimalist design with ample white space
- **Interactive Elements**: Hover effects, micro-animations
- **Gamification Visuals**: Badges, progress bars, streaks
- **Mobile-First**: Responsive design prioritizing mobile experience
- **Accessibility**: High contrast, screen reader support

### Animations & Interactions
- **Locomotive Scroll**: Smooth page scrolling
- **Framer Motion**: Page transitions, button hover effects
- **Three.js**: Interactive 3D elements for gamification
- **Micro-interactions**: Button clicks, form submissions, success states

---

## 🏗️ COMPONENT ARCHITECTURE

### Core Layout Components
```
App/
├── Header (Navigation, User Menu, Notifications)
├── Sidebar (Menu items, Progress indicators)
├── Main Content Area
├── Footer (Links, Version info)
```

### Dashboard Components
```
StudentDashboard/
├── StatsCards (Points, Badges, Streak, Rank)
├── QuizSection (Available Quizzes, Recent Attempts)
├── LearningSection (Daily Content, Flashcards)
├── CommunitySection (My Communities, Recommendations)
├── InterviewSection (Upcoming, History)
├── MentorConnect (Available Mentors, Sessions)
```

### Quiz Components
```
QuizSystem/
├── QuizList (Filter by difficulty, search)
├── QuizPlayer
│   ├── QuestionCard (MCQ with timer)
│   ├── ProgressBar
│   ├── TabSwitchWarning (Modal)
│   ├── SubmitConfirm
├── QuizResults (Score breakdown, badges earned, next difficulty)
```

---

## 📱 SCREEN-BY-SCREEN BREAKDOWN

### 1. Landing/Auth Screens
```
1.1 Welcome Screen
- Animated hero section with Three.js elements
- Sign up options (Student/Recruiter/Mentor)
- Feature highlights with icons

1.2 Signup Forms
- Student: Name, Email, Domains, Skills, Interests
- Recruiter: Name, Email, Company, Position
- Mentor: Name, Email, Expertise, Experience

1.3 Login Screen
- Email/password OAuth form
- Forgot password link
- Social login options
```

### 2. Student Dashboard
```
2.1 Main Dashboard
├── Stats Overview
│   ├── Points & Rank
│   ├── Badges Earned
│   ├── Current Streak
│   ├── Upcoming Events
├── Quick Actions Grid (4x2)
│   ├── Take Daily Quiz
│   ├── View Learning
│   ├── Join Community
│   ├── Schedule Interview
│   ├── Connect Mentor
│   ├── Explore Careers
│   ├── View Progress
│   └── Settings

2.2 Gamification Section
├── Badge Collection (Grid layout with tooltips)
├── Leaderboard (Animated rank changes)
├── Achievement Notifications
├── Streak Calendar (Heat map style)
```

### 3. Quiz Interface
```
3.1 Quiz Selection
├── Filter by difficulty (tabs)
├── Recommended difficulty badge
├── Quiz cards with preview

3.2 Quiz Gameplay
├── Question Counter (1/10 with progress bar)
├── Timer countdown with color change
├── Tab switch warning modal
├── Answer options with hover effects
├── Submit button with loading state

3.3 Results Screen
├── Score animation (confetti effect)
├── Detailed breakdown (correct/incorrect)
├── Points earned
├── Badges unlocked (celebration animation)
├── Next recommended difficulty
├── Share results option
```

### 4. Micro Learning
```
4.1 Daily Content Feed
├── Content cards with animated reveals
├── Flashcard swiper
├── Mark as completed
├── Save for later

4.2 Learning Resources
├── Video player with controls
├── Article reader
├── Resource library (filterable)
├── Download/bookmark options

4.3 Progress Dashboard
├── Streak visualizer
├── Topics heatmap
├── Weekly reports
├── Goal setting
```

### 5. Community Hub
```
5.1 Community Discovery
├── Recommended communities (match score badges)
├── Search with filters
├── Categories grid

5.2 Community Detail
├── Header with member count
├── Post feed
├── Create post modal
├── Member management

5.3 Discussion Threads
├── Post with replies
├── Like/upvote system
├── Attachment support
├── Real-time updates (WebSockets ready)
```

### 6. Interview & Mentorship
```
6.1 Interview Scheduling
├── Mentor selection
├── Calendar/time picker
├── Topic selection
├── Badge requirement check

6.2 Mentor Connect
├── Available mentors grid
├── Skill match visualization
├── One-click connect
├── Call interface (video/audio/chat)

6.3 Career Exploration
├── Career cards with 3D effects
├── Skill requirements
├── Salary/growth data
├── Application links
```

---

## 🚀 FRONTEND PROMPT FOR LOVABLE

Create a beautiful, interactive React application for an HR EdTech platform targeting Gen Z with the following specifications:

### Build Requirements:
1. **Create a modern React app** using Vite
2. **Implement clean, professional UI** with TailwindCSS
3. **Add smooth animations** using Framer Motion
4. **Include 3D interactive elements** using Three.js
5. **Implement smooth scrolling** with Locomotive Scroll
6. **Mobile-first responsive design**
7. **Accessible components** (ARIA labels, keyboard navigation)

### Key Features to Implement:
- Dual dashboard system (Student & Recruiter)
- Gamified quiz system with time constraints and penalties
- Community features with semantic search
- Interview scheduling with badge-based unlocking
- Mentor connect system with skill matching
- Career exploration with unconventional paths

### Technical Implementation:

1. **State Management**: Use Context API for authentication state, quiz state, user data
2. **API Integration**: Connect to FastAPI backend with comprehensive error handling
3. **Real-time Features**: WebSocket readiness for live chat/chats
4. **Progressive Web App**: Service worker, offline capability
5. **Performance**: Lazy loading, code splitting, image optimization

### Authentication Flow:
- JWT token management with automatic refresh
- Protected routes for different user roles
- Password reset functionality
- Profile completion wizard for new users

### Gamification Design:
- Animated badge unlocks with celebratory effects
- Progressive difficulty visualization
- Streak tracking with fire animations
- Leaderboard with rank animations

### Custom Components Needed:
- BadgeDisplay, QuizTimer, ProgressRing, Flashcard, CommunityCard, InterviewCard, CareerCard
- Modals: ConfirmAction, TabSwitchWarning, BadgeUnlocked, InterviewScheduled
- Forms: QuizCreationForm, CommunityPostForm, InterviewBookingForm

### Animation Guidelines:
- Micro-interactions on hover/click
- Page transitions using Framer Motion
- Loading states with skeleton screens
- Success/error state animations
- 3D elements for gamification components

### API Endpoints to Integrate:
- `/api/v1/auth/*` - Authentication
- `/api/v1/user/dashboard` - Dashboard data
- `/api/v1/quiz/*` - Quiz functionality
- `/api/v1/learning/*` - Micro learning
- `/api/v1/community/*` - Community features
- `/api/v1/interview/*` - Interview system
- `/api/v1/mentor-interviews/*` - Mentor connect

Please create an engaging, visually appealing interface that will captivate Gen Z users and make HR learning both fun and effective!

---

## 🔗 BACKEND INTEGRATION DETAILS

### API Base URL: `http://localhost:8000/api/v1`

### Authentication Headers:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### Key API Endpoints:

**Authentication:**
- `POST /auth/student/signup` - Student registration
- `POST /auth/recruiter/signup` - Recruiter registration
- `POST /auth/mentor/signup` - Mentor registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

**Dashboard:**
- `GET /user/dashboard` - Role-specific dashboard

**Quiz System:**
- `GET /quiz/available` - Get available quizzes
- `POST /quiz/attempt` - Submit quiz attempt
- `GET /quiz/leaderboard` - Get leaderboard
- `GET /quiz/attempts/history` - Quiz history

**Learning:**
- `GET /learning/daily-content` - Daily curated content
- `GET /learning/resources` - Learning resources
- `POST /learning/roadmap` - Create learning roadmap

**Community:**
- `GET /community/recommend` - Recommended communities
- `POST /community/join/{id}` - Join community
- `GET /community/{id}/posts` - Community posts

**Interviews:**
- `POST /interview/schedule` - Schedule interview
- `GET /interview/my-interviews` - Get user's interviews
- `PUT /interview/{id}/complete` - Complete interview

**Mentor Connect:**
- `POST /mentor-interviews/connect/{id}` - Direct mentor connect
- `GET /mentor-interviews/available-mentors` - Get available mentors
- `GET /mentor-interviews/recommend/career-exploration` - Career recommendations

### Error Handling:
- 400: Validation errors
- 401: Unauthorized
- 403: Forbidden (badge requirements not met)
- 404: Resource not found
- 500: Server error

### Response Format:
```json
{
  "data": {...},
  "message": "Success message",
  "error": null | "Error message"
}
```

This comprehensive backend implementation provides all the functionality needed to build an engaging HR EdTech platform for Gen Z!

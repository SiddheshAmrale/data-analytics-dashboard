# 📋 Task Management App

A collaborative task management application with real-time updates, drag-and-drop functionality, and team collaboration features. Built with React, TypeScript, and Tailwind CSS.

## ✨ Features

- **Real-time Collaboration**: Live updates across team members
- **Drag & Drop**: Intuitive task organization with beautiful animations
- **Task Categories**: Organize tasks by status (To Do, In Progress, Done)
- **Team Management**: Add team members and assign tasks
- **Due Dates**: Set and track task deadlines
- **Priority Levels**: Mark tasks as high, medium, or low priority
- **Comments**: Add comments and discussions to tasks
- **Search & Filter**: Find tasks quickly with advanced filtering
- **Responsive Design**: Works perfectly on all devices
- **Dark/Light Mode**: Toggle between themes

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Beautiful DnD** - Drag and drop functionality
- **React Router** - Navigation
- **React Hook Form** - Form handling
- **Axios** - HTTP client
- **Socket.io Client** - Real-time communication
- **Date-fns** - Date manipulation
- **Lucide React** - Beautiful icons

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Socket.io** - Real-time communication
- **MongoDB** - Database
- **JWT** - Authentication

## 🚀 Installation

### Prerequisites
- Node.js (v16 or higher)
- MongoDB

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siddheshamrale/task-management-app.git
   cd task-management-app
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Environment variables**
   Create `.env` file in the root directory:
   ```env
   REACT_APP_API_URL=http://localhost:5000
   REACT_APP_SOCKET_URL=http://localhost:5000
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

## 📁 Project Structure

```
task-management-app/
├── src/
│   ├── components/         # Reusable components
│   │   ├── Board/         # Kanban board components
│   │   ├── Task/          # Task-related components
│   │   ├── UI/            # UI components
│   │   └── Layout/        # Layout components
│   ├── pages/             # Page components
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API services
│   ├── utils/             # Utility functions
│   ├── types/             # TypeScript type definitions
│   └── styles/            # Global styles
├── server/                # Backend server
│   ├── controllers/       # Route controllers
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   └── socket/           # Socket.io handlers
└── public/               # Static files
```

## 🎨 Features Demo

### Task Management
- Create, edit, and delete tasks
- Drag tasks between columns (To Do → In Progress → Done)
- Set task priority and due dates
- Add comments and attachments

### Team Collaboration
- Invite team members
- Assign tasks to team members
- Real-time updates across all users
- Activity feed and notifications

### Board Organization
- Customize board columns
- Filter tasks by assignee, priority, or due date
- Search tasks by title or description
- Export board data

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PUT /api/tasks/:id/move` - Move task to different column

### Boards
- `GET /api/boards` - Get user boards
- `POST /api/boards` - Create new board
- `PUT /api/boards/:id` - Update board
- `DELETE /api/boards/:id` - Delete board

### Comments
- `GET /api/tasks/:id/comments` - Get task comments
- `POST /api/tasks/:id/comments` - Add comment
- `DELETE /api/comments/:id` - Delete comment

## 🎯 Key Features

### Real-time Updates
- Live task updates across all team members
- Instant notifications for task changes
- Collaborative editing with conflict resolution

### Drag & Drop
- Smooth drag and drop between columns
- Visual feedback during drag operations
- Keyboard accessibility support

### Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Adaptive layouts for different screen sizes

## 🔒 Security Features

- JWT authentication
- Input validation
- XSS protection
- CORS configuration
- Rate limiting

## 🧪 Testing

```bash
# Run frontend tests
npm test

# Run backend tests
cd server && npm test
```

## 📦 Deployment

### Frontend (Netlify/Vercel)
```bash
npm run build
```

### Backend (Heroku/Railway)
```bash
cd server
git push heroku main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Siddhesh Amrale**
- GitHub: [@siddheshamrale](https://github.com/siddheshamrale)
- LinkedIn: [Siddhesh Amrale](https://linkedin.com/in/siddhesh-amrale)

## 🙏 Acknowledgments

- React Beautiful DnD for drag and drop
- Framer Motion for animations
- Tailwind CSS for styling
- Socket.io for real-time features 
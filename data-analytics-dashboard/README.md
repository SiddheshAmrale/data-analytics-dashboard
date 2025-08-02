# 📊 Data Analytics Dashboard

A real-time data visualization dashboard with interactive charts and analytics tools for business intelligence. Built with React frontend, Python backend, and PostgreSQL database.

## ✨ Features

- **Real-time Data Visualization**: Live charts and graphs
- **Interactive Dashboards**: Customizable widget layouts
- **Multiple Chart Types**: Line, bar, pie, scatter, and area charts
- **Data Filtering**: Advanced filtering and search capabilities
- **Export Functionality**: Export reports as PDF, CSV, or Excel
- **User Authentication**: Secure login and role-based access
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Toggle between themes
- **Data Import**: Support for CSV, Excel, and JSON files
- **Scheduled Reports**: Automated report generation

## 🛠️ Tech Stack

### Frontend
- **React** - UI framework
- **TypeScript** - Type safety
- **Chart.js** - Chart library
- **React Chart.js 2** - React wrapper for Chart.js
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **Axios** - HTTP client
- **Socket.io Client** - Real-time updates

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Python** - Data processing
- **PostgreSQL** - Database
- **Sequelize** - ORM
- **Socket.io** - Real-time communication
- **Node-cron** - Scheduled tasks

### Data Processing
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Matplotlib** - Plotting
- **Scikit-learn** - Machine learning

## 🚀 Installation

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- PostgreSQL
- Redis (optional, for caching)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siddheshamrale/data-analytics-dashboard.git
   cd data-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create `.env` file:
   ```env
   NODE_ENV=development
   PORT=5000
   DATABASE_URL=postgresql://username:password@localhost:5432/analytics
   REDIS_URL=redis://localhost:6379
   JWT_SECRET=your_jwt_secret
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb analytics
   
   # Run migrations
   npm run migrate
   ```

6. **Start development server**
   ```bash
   npm run dev
   ```

## 📁 Project Structure

```
data-analytics-dashboard/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   │   ├── Charts/   # Chart components
│   │   │   ├── Dashboard/ # Dashboard components
│   │   │   └── UI/       # UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom hooks
│   │   └── utils/        # Utility functions
│   └── public/
├── server/                # Node.js backend
│   ├── controllers/      # Route controllers
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── python/               # Python data processing
│   ├── scripts/         # Data processing scripts
│   ├── models/          # ML models
│   └── utils/           # Python utilities
└── docs/                # Documentation
```

## 🎨 Dashboard Features

### Chart Types
- **Line Charts**: Time series data visualization
- **Bar Charts**: Categorical data comparison
- **Pie Charts**: Proportional data representation
- **Scatter Plots**: Correlation analysis
- **Area Charts**: Cumulative data visualization
- **Heatmaps**: Matrix data visualization

### Interactive Features
- **Zoom & Pan**: Interactive chart navigation
- **Tooltips**: Detailed data on hover
- **Legend**: Toggle data series visibility
- **Responsive**: Charts adapt to screen size
- **Export**: Save charts as images

### Data Management
- **Data Import**: Upload CSV, Excel, JSON files
- **Data Validation**: Automatic data type detection
- **Data Cleaning**: Remove duplicates and outliers
- **Data Transformation**: Aggregation and filtering

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile

### Dashboards
- `GET /api/dashboards` - Get user dashboards
- `POST /api/dashboards` - Create dashboard
- `PUT /api/dashboards/:id` - Update dashboard
- `DELETE /api/dashboards/:id` - Delete dashboard

### Data Sources
- `GET /api/data-sources` - Get data sources
- `POST /api/data-sources` - Add data source
- `PUT /api/data-sources/:id` - Update data source
- `DELETE /api/data-sources/:id` - Delete data source

### Charts
- `GET /api/charts` - Get charts
- `POST /api/charts` - Create chart
- `PUT /api/charts/:id` - Update chart
- `DELETE /api/charts/:id` - Delete chart

### Reports
- `GET /api/reports` - Get reports
- `POST /api/reports` - Generate report
- `GET /api/reports/:id/export` - Export report

## 📊 Analytics Features

### Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, standard deviation
- **Correlation Analysis**: Pearson, Spearman correlations
- **Trend Analysis**: Time series decomposition
- **Outlier Detection**: Statistical outlier identification

### Machine Learning
- **Clustering**: K-means, hierarchical clustering
- **Classification**: Random Forest, SVM, Logistic Regression
- **Regression**: Linear, polynomial regression
- **Time Series**: ARIMA, exponential smoothing

### Business Intelligence
- **KPIs**: Key Performance Indicators
- **Goal Tracking**: Progress towards targets
- **Forecasting**: Future trend predictions
- **Alerting**: Automated notifications

## 🔒 Security Features

- JWT authentication
- Role-based access control
- Data encryption
- Input validation
- SQL injection prevention
- XSS protection

## 📈 Performance Optimization

- **Caching**: Redis-based response caching
- **Compression**: Response compression
- **Lazy Loading**: Load charts on demand
- **Virtual Scrolling**: Handle large datasets
- **CDN**: Static asset delivery

## 🧪 Testing

```bash
# Run frontend tests
cd client && npm test

# Run backend tests
npm test

# Run Python tests
cd python && python -m pytest
```

## 📦 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Production Deployment
```bash
# Build frontend
npm run build

# Start production server
npm start
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

- Chart.js for charting library
- React Chart.js 2 for React integration
- PostgreSQL for database
- Python data science ecosystem 
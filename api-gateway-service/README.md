# 🌐 API Gateway Service

A microservices API gateway built with Node.js and Express, featuring rate limiting, authentication, and request routing. Designed to handle high-traffic applications with security and performance in mind.

## ✨ Features

- **Request Routing**: Route requests to appropriate microservices
- **Rate Limiting**: Prevent API abuse with configurable limits
- **Authentication**: JWT-based authentication and authorization
- **Request Validation**: Validate incoming requests
- **Caching**: Redis-based response caching
- **Load Balancing**: Distribute traffic across multiple services
- **Monitoring**: Request logging and metrics
- **API Documentation**: Auto-generated Swagger documentation
- **Security**: CORS, Helmet, and other security headers
- **Compression**: Response compression for better performance

## 🛠️ Tech Stack

### Core
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **Redis** - Caching and session storage
- **JWT** - Authentication tokens

### Security & Performance
- **Helmet** - Security headers
- **CORS** - Cross-origin resource sharing
- **Rate Limiting** - API abuse prevention
- **Compression** - Response compression
- **Winston** - Logging

### Documentation & Testing
- **Swagger** - API documentation
- **Jest** - Testing framework
- **ESLint** - Code linting

## 🚀 Installation

### Prerequisites
- Node.js (v16 or higher)
- Redis server
- Docker (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siddheshamrale/api-gateway-service.git
   cd api-gateway-service
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment variables**
   Create `.env` file:
   ```env
   NODE_ENV=development
   PORT=3000
   REDIS_URL=redis://localhost:6379
   JWT_SECRET=your_jwt_secret_key
   RATE_LIMIT_WINDOW_MS=900000
   RATE_LIMIT_MAX_REQUESTS=100
   ```

4. **Start Redis server**
   ```bash
   # Using Docker
   docker run -d -p 6379:6379 redis:alpine
   
   # Or install Redis locally
   redis-server
   ```

5. **Start the gateway**
   ```bash
   npm run dev
   ```

## 📁 Project Structure

```
api-gateway-service/
├── src/
│   ├── config/           # Configuration files
│   ├── middleware/       # Custom middleware
│   │   ├── auth.js      # Authentication middleware
│   │   ├── rateLimit.js # Rate limiting
│   │   ├── validation.js # Request validation
│   │   └── cache.js     # Caching middleware
│   ├── routes/          # Route definitions
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   └── index.js         # Main application file
├── tests/               # Test files
├── docs/                # Documentation
└── docker/              # Docker configuration
```

## 🔧 Configuration

### Service Routes
Configure microservice endpoints in `src/config/services.js`:

```javascript
const services = {
  userService: {
    url: process.env.USER_SERVICE_URL || 'http://localhost:3001',
    timeout: 5000
  },
  productService: {
    url: process.env.PRODUCT_SERVICE_URL || 'http://localhost:3002',
    timeout: 5000
  },
  orderService: {
    url: process.env.ORDER_SERVICE_URL || 'http://localhost:3003',
    timeout: 5000
  }
};
```

### Rate Limiting
Configure rate limits in `src/config/rateLimit.js`:

```javascript
const rateLimitConfig = {
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
};
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

### User Service
- `GET /api/users` - Get all users
- `GET /api/users/:id` - Get user by ID
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

### Product Service
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product by ID
- `POST /api/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Order Service
- `GET /api/orders` - Get all orders
- `GET /api/orders/:id` - Get order by ID
- `POST /api/orders` - Create order
- `PUT /api/orders/:id` - Update order

## 🛡️ Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control
- Token refresh mechanism
- Secure password hashing

### Rate Limiting
- IP-based rate limiting
- User-based rate limiting
- Burst protection
- Configurable limits

### Request Validation
- Input sanitization
- Schema validation
- SQL injection prevention
- XSS protection

## 📊 Monitoring & Logging

### Request Logging
- Request/response logging
- Error tracking
- Performance metrics
- Audit trails

### Health Checks
- Service health monitoring
- Database connectivity checks
- Redis connectivity checks
- Load balancer integration

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run specific test file
npm test -- tests/auth.test.js
```

## 📦 Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t api-gateway .

# Run container
docker run -p 3000:3000 api-gateway
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: api-gateway:latest
        ports:
        - containerPort: 3000
```

## 🔍 API Documentation

Access Swagger documentation at:
```
http://localhost:3000/api-docs
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

- Express.js community
- Redis for caching
- Winston for logging
- Swagger for documentation 
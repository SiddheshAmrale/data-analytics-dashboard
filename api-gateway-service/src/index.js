const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const jwt = require('jsonwebtoken');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Logging
app.use(morgan('combined'));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use(limiter);

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Access token required' });
  }

  jwt.verify(token, process.env.JWT_SECRET || 'your-secret-key', (err, user) => {
    if (err) {
      return res.status(403).json({ message: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};

// Service discovery and routing
const services = {
  auth: process.env.AUTH_SERVICE_URL || 'http://localhost:3001',
  users: process.env.USERS_SERVICE_URL || 'http://localhost:3002',
  products: process.env.PRODUCTS_SERVICE_URL || 'http://localhost:3003',
  orders: process.env.ORDERS_SERVICE_URL || 'http://localhost:3004'
};

// Route handlers
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'API Gateway is running',
    timestamp: new Date().toISOString()
  });
});

// Authentication routes
app.post('/api/auth/login', async (req, res) => {
  try {
    const response = await axios.post(`${services.auth}/login`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Authentication service error'
    });
  }
});

app.post('/api/auth/register', async (req, res) => {
  try {
    const response = await axios.post(`${services.auth}/register`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Authentication service error'
    });
  }
});

// User routes (protected)
app.get('/api/users/profile', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${services.users}/profile`, {
      headers: { Authorization: req.headers.authorization }
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'User service error'
    });
  }
});

app.put('/api/users/profile', authenticateToken, async (req, res) => {
  try {
    const response = await axios.put(`${services.users}/profile`, req.body, {
      headers: { Authorization: req.headers.authorization }
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'User service error'
    });
  }
});

// Product routes (protected)
app.get('/api/products', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${services.products}`, {
      headers: { Authorization: req.headers.authorization },
      params: req.query
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Product service error'
    });
  }
});

app.get('/api/products/:id', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${services.products}/${req.params.id}`, {
      headers: { Authorization: req.headers.authorization }
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Product service error'
    });
  }
});

// Order routes (protected)
app.post('/api/orders', authenticateToken, async (req, res) => {
  try {
    const response = await axios.post(`${services.orders}`, req.body, {
      headers: { Authorization: req.headers.authorization }
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Order service error'
    });
  }
});

app.get('/api/orders', authenticateToken, async (req, res) => {
  try {
    const response = await axios.get(`${services.orders}`, {
      headers: { Authorization: req.headers.authorization },
      params: req.query
    });
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.message || 'Order service error'
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
  console.log('Available services:');
  Object.entries(services).forEach(([name, url]) => {
    console.log(`  ${name}: ${url}`);
  });
});

module.exports = app; 
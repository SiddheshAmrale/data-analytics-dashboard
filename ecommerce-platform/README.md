# 🛒 E-Commerce Platform

A full-stack e-commerce platform built with React frontend, Node.js backend, and MongoDB database. Features include user authentication, product management, shopping cart, and payment integration.

## ✨ Features

- **User Authentication**: Secure login/register with JWT tokens
- **Product Management**: CRUD operations for products with image upload
- **Shopping Cart**: Add/remove items with quantity management
- **Payment Integration**: Stripe payment processing
- **Order Management**: Track order status and history
- **Admin Dashboard**: Manage products, orders, and users
- **Responsive Design**: Mobile-friendly interface
- **Search & Filter**: Find products easily
- **Reviews & Ratings**: User feedback system

## 🛠️ Tech Stack

### Frontend
- **React** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Redux Toolkit** - State management
- **React Router** - Navigation
- **Axios** - HTTP client

### Backend
- **Node.js** - Runtime environment
- **Express.js** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM
- **JWT** - Authentication
- **Stripe** - Payment processing
- **Multer** - File uploads

## 🚀 Installation

### Prerequisites
- Node.js (v16 or higher)
- MongoDB
- Stripe account

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siddheshamrale/ecommerce-platform.git
   cd ecommerce-platform
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Environment variables**
   Create `.env` file in the root directory:
   ```env
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_jwt_secret
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   PORT=5000
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

## 📁 Project Structure

```
ecommerce-platform/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── store/         # Redux store
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   └── public/
├── server/                 # Node.js backend
│   ├── controllers/        # Route controllers
│   ├── models/            # MongoDB models
│   ├── routes/            # API routes
│   ├── middleware/        # Custom middleware
│   └── utils/             # Utility functions
├── uploads/               # Product images
└── docs/                  # Documentation
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Create product (admin)
- `PUT /api/products/:id` - Update product (admin)
- `DELETE /api/products/:id` - Delete product (admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user orders
- `GET /api/orders/:id` - Get order details

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item
- `DELETE /api/cart/remove/:id` - Remove item from cart

## 🎨 Features Demo

### User Features
- Browse products with search and filters
- Add items to shopping cart
- Secure checkout with Stripe
- Track order status
- Leave product reviews

### Admin Features
- Manage product inventory
- Process orders
- View sales analytics
- Manage user accounts

## 🔒 Security Features

- JWT authentication
- Password hashing with bcrypt
- Input validation
- Rate limiting
- CORS protection
- Helmet security headers

## 🧪 Testing

```bash
# Run backend tests
npm test

# Run frontend tests
cd client && npm test
```

## 📦 Deployment

### Backend (Heroku)
```bash
git push heroku main
```

### Frontend (Netlify/Vercel)
```bash
npm run build
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

- Stripe for payment processing
- MongoDB for database
- React and Node.js communities 
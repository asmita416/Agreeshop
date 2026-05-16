# AgriShop - Enhanced E-Commerce Platform

## Features Implemented

### 1. **Category Navigation System**
- **View:** Navigate categories from the navbar dropdown menu
- **Route:** `/category/<category_id>`
- **Features:**
  - Browse products by category
  - Filter view by agriculture type
  - Breadcrumb navigation
  - Category-specific product display

### 2. **Wishlist System**
- **Add to Wishlist:** Click heart icon on any product
- **Routes:**
  - `/add_to_wishlist/<product_id>` - Add product to wishlist
  - `/remove_from_wishlist/<product_id>` - Remove from wishlist
  - `/wishlist` - View all wishlist items
- **Features:**
  - Save products for later
  - Add from wishlist to cart
  - View all saved items in one place

### 3. **Enhanced Cart System**
- **Route:** `/cart`
- **Features:**
  - Quantity management (increase/decrease)
  - Update quantities on-the-fly
  - Real-time total calculation
  - Delivery charges calculation
  - Multiple payment options

### 4. **User Profile Management**
- **Route:** `/profile`
- **Features:**
  - Edit personal information
  - Update delivery address
  - Store phone and email
  - View account creation date
  - Quick links to orders and wishlist

### 5. **Checkout System**
- **Route:** `/checkout`
- **Features:**
  - Review delivery address
  - Confirm order items
  - Calculate final total
  - Generate order ID
  - Create delivery record

### 6. **Online Payment Integration**
- **Route:** `/payment/<order_id>`
- **Payment Methods:**
  - **Online Payment:** Razorpay Integration (Debit/Credit Card, UPI, Net Banking)
  - **Cash on Delivery:** Pay at delivery
- **Features:**
  - Secure payment gateway
  - Multiple payment methods
  - Transaction ID tracking
  - Payment confirmation

### 7. **Order Management System**
- **Routes:**
  - `/my-orders` - View all user orders
  - `/order/<order_id>` - View detailed order info
  - `/order-confirmation/<order_id>` - View after purchase

- **Features:**
  - Order status tracking
  - Timeline view (Pending → Confirmed → Shipped → Delivered)
  - Order history
  - Payment status
  - Delivery information

### 8. **Delivery System**
- **Features:**
  - Estimated delivery time (3-5 business days)
  - Delivery status tracking
  - Order notes
  - Delivery updates

### 9. **Database Schema**

#### Users Table (Enhanced)
```
- id, username, password, email, phone, address, city, pincode, created_at
```

#### Wishlist Table
```
- id, user_id, product_id, added_at
```

#### Orders Table
```
- id, user_id, total_amount, order_date, status, payment_status, payment_id
```

#### Order Items Table
```
- id, order_id, product_id, quantity, price
```

#### Delivery Table
```
- id, order_id, status, estimated_date, delivery_date, notes, updated_at
```

#### Payments Table
```
- id, order_id, amount, payment_method, status, transaction_id, created_at
```

---

## Navigation Flow

### For Customers:
1. **Home** → Browse products by category
2. **Add to Cart/Wishlist** → Save products
3. **View Cart** → Manage quantities
4. **Checkout** → Enter delivery details
5. **Payment** → Choose payment method
6. **Order Confirmation** → View order details
7. **My Orders** → Track delivery status

### For Admin:
1. **Login** → Access admin panel
2. **Add Products** → Upload new products
3. **Manage Categories** → Edit categories
4. **View Orders** → Monitor deliveries (future feature)

---

## API Routes

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout

### Products & Categories
- `GET /` - Home page (all products)
- `GET /category/<cat_id>` - View category

### Cart
- `GET /add_to_cart/<product_id>` - Add product
- `GET /update_cart/<product_id>/<quantity>` - Update quantity
- `GET /remove_from_cart/<product_id>` - Remove product
- `GET /cart` - View cart

### Wishlist
- `GET /add_to_wishlist/<product_id>` - Add to wishlist
- `GET /remove_from_wishlist/<product_id>` - Remove from wishlist
- `GET /wishlist` - View wishlist

### Orders & Checkout
- `GET /checkout` - Checkout page
- `POST /checkout` - Create order
- `GET /payment/<order_id>` - Payment page
- `POST /payment/<order_id>` - Process payment
- `GET /order-confirmation/<order_id>` - Order confirmation
- `GET /my-orders` - View all orders
- `GET /order/<order_id>` - View order details

### User Account
- `GET /profile` - View/edit profile
- `POST /profile` - Update profile

---

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python app.py
```

### 3. Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Demo Credentials

### Admin Account
- **Username:** admin
- **Password:** admin

### Test User
- **Username:** user1
- **Password:** user1

---

## Payment Methods Supported

### 1. Online Payment (Razorpay)
- Debit Card
- Credit Card
- UPI
- Net Banking
- Wallet

### 2. Cash on Delivery
- Pay when order arrives
- Available for all locations

---

## Future Enhancements

1. **Email Notifications** - Order confirmations, shipping updates
2. **SMS Alerts** - Real-time delivery updates
3. **Admin Dashboard** - Analytics and reports
4. **Review & Ratings** - Customer product reviews
5. **Coupon System** - Discount codes
6. **Inventory Management** - Stock tracking
7. **Return/Exchange** - Order modifications
8. **Live Chat Support** - Customer service
9. **Mobile App** - iOS/Android application
10. **Multi-language Support** - Regional languages

---

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection ready
- Secure payment gateway integration
- SQL injection prevention with parameterized queries

---

## Performance Optimization

- Database indexing on foreign keys
- Session management for cart
- Image optimization using URLs
- Bootstrap CDN for frontend

---

## Troubleshooting

### Cart not saving?
- Clear browser cookies and try again
- Ensure session is enabled

### Payment not working?
- Use demo card: 4111 1111 1111 1111
- Check payment gateway configuration

### Order not appearing?
- Refresh the page
- Check user login session

---

## Support

For issues or questions:
- Email: support@agrshop.com
- Phone: 1-800-AGRI-SHOP

---

**Version:** 2.0  
**Last Updated:** May 2024  
**Status:** Production Ready

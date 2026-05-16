# 🧪 TESTING GUIDE - AgriShop Features

## Quick Test Checklist

### Prerequisites
- [ ] Python installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Browser ready (Chrome/Firefox recommended)

---

## 🚀 Getting Started

### 1. Start the Application
```bash
python app.py
```
Expected output:
```
Running on http://127.0.0.1:5000
```

### 2. Open Browser
Navigate to: `http://localhost:5000`

---

## 📋 Feature Testing

### Test 1: Home Page & Navigation ✅
**Steps:**
1. Load home page
2. Click different navbar items
3. Check responsive menu on mobile view

**Expected Results:**
- ✓ Page loads with all products
- ✓ Categories dropdown works
- ✓ All links functional
- ✓ Navigation responsive on mobile

---

### Test 2: Category Browsing ✅
**Steps:**
1. Click "Categories" dropdown in navbar
2. Select "🌱 Seeds"
3. Verify you see only seed products
4. Click breadcrumb to go back

**Expected Results:**
- ✓ Category page loads
- ✓ Only seed products shown
- ✓ Category title displayed
- ✓ Breadcrumb working

---

### Test 3: User Registration & Login ✅
**Steps:**
1. Click "Register" in navbar
2. Create new account:
   - Username: `testuser123`
   - Password: `password123`
   - Email: `test@example.com`
   - Phone: `9876543210`
3. Click Register
4. You should be redirected to login
5. Log in with new credentials

**Expected Results:**
- ✓ Registration form accepts input
- ✓ Account created successfully
- ✓ Redirected to login
- ✓ Login works with new credentials
- ✓ Session created (cart initialized)

---

### Test 4: Add to Wishlist ❤️
**Steps:**
1. Make sure you're logged in
2. Find any product card
3. Click heart icon in top-right of product image
4. Heart should change color
5. Click wishlist in navbar
6. Verify product is in wishlist

**Expected Results:**
- ✓ Heart icon visible for logged-in users
- ✓ Product added to wishlist
- ✓ Wishlist page shows saved items
- ✓ Can remove from wishlist
- ✓ Can add wishlist items to cart

---

### Test 5: Shopping Cart ✅
**Steps:**
1. Click on any product card
2. Click "Add to Cart" button
3. Add 2-3 different products
4. Click "Cart" in navbar
5. Increase quantity of one item
6. Decrease quantity of another
7. Remove one item

**Expected Results:**
- ✓ Products added to cart
- ✓ Cart counter updates in navbar
- ✓ Cart page shows all items
- ✓ Quantity can be increased/decreased
- ✓ Price updates automatically
- ✓ Total amount calculated correctly
- ✓ Delivery charges shown (₹50)
- ✓ Items can be removed
- ✓ Empty cart shows helpful message

---

### Test 6: User Profile Management 👤
**Steps:**
1. Click on username in navbar dropdown
2. Select "Profile"
3. Fill in:
   - Email: `test@example.com`
   - Phone: `9876543210`
   - Address: `123 Farm Lane, Village`
   - City: `Springfield`
   - Pincode: `123456`
4. Click "Save Changes"
5. Refresh and verify data persists

**Expected Results:**
- ✓ Profile page loads
- ✓ Form fields are editable
- ✓ Data saved successfully
- ✓ Data persists after refresh
- ✓ Links to orders and wishlist available

---

### Test 7: Complete Purchase Flow 🛒
**Steps:**

#### Step 7A: Checkout
1. Add 2-3 products to cart
2. Click "Proceed to Checkout"
3. Review delivery address
4. Verify order items display
5. Check order summary

**Expected Results:**
- ✓ Checkout page loads
- ✓ Delivery address shown
- ✓ Order items listed
- ✓ Total amount calculated
- ✓ Delivery charges included

#### Step 7B: Payment
1. Click "Proceed to Payment"
2. Select payment method (Online or COD)
3. For online: Select payment method details shown
4. For COD: Select Cash on Delivery
5. Click "Confirm Payment"

**Expected Results:**
- ✓ Payment page loads
- ✓ Order ID displayed
- ✓ Payment options shown
- ✓ Can select different methods
- ✓ Demo card details visible for testing

#### Step 7C: Order Confirmation
1. After payment, you should see confirmation page
2. Verify:
   - Order number displayed
   - Order date shown
   - Items listed
   - Delivery information shown
   - Delivery status: "Processing"

**Expected Results:**
- ✓ Confirmation page loads
- ✓ Order details correct
- ✓ Delivery info displayed
- ✓ Links to continue shopping or view orders

---

### Test 8: Order Tracking 📦
**Steps:**
1. Click on username → "My Orders"
2. View all your orders
3. Click on an order to see details
4. Verify order timeline

**Expected Results:**
- ✓ My Orders page shows all orders
- ✓ Each order shows status badge
- ✓ Progress bar visible
- ✓ Order details page loads
- ✓ Timeline shows order progression
- ✓ Estimated delivery date shown
- ✓ Payment details visible

---

### Test 9: Mobile Responsiveness 📱
**Steps:**
1. Open app in browser
2. Press F12 (Developer Tools)
3. Click device toggle (mobile view)
4. Test different screen sizes:
   - iPhone (375px)
   - Tablet (768px)
   - Desktop (1200px)
5. Test all features on mobile

**Expected Results:**
- ✓ Layout adjusts to screen size
- ✓ Navigation collapses to hamburger menu
- ✓ Cart buttons visible and clickable
- ✓ Product cards stack properly
- ✓ Forms are mobile-friendly
- ✓ No horizontal scroll needed

---

### Test 10: Admin Panel ⚙️
**Steps:**
1. Make sure logged-in user is "admin"
2. Click username dropdown
3. Select "Admin Panel"
4. Fill in product form:
   - Name: `Test Product`
   - Price: `100`
   - Image URL: `https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=400`
   - Category: Select any category
   - Description: `Test product description`
5. Click "Add Product"
6. Go back to home and verify product appears

**Expected Results:**
- ✓ Admin panel accessible
- ✓ Form accepts input
- ✓ Product added successfully
- ✓ New product visible on home page
- ✓ Product appears in correct category

---

### Test 11: Wishlist → Cart Flow ❤️ → 🛒
**Steps:**
1. Add products to wishlist
2. Go to wishlist
3. Click "Add to Cart" on wishlist product
4. Verify product now in cart
5. Go to cart and confirm

**Expected Results:**
- ✓ Wishlist to cart transfer works
- ✓ Product appears in cart
- ✓ Quantity defaults to 1
- ✓ Can modify in cart afterwards

---

### Test 12: Session Persistence 🔄
**Steps:**
1. Add products to cart
2. Add items to wishlist
3. Log out
4. Log back in
5. Check cart status
6. Check wishlist status

**Expected Results:**
- ✓ Cart cleared after logout (session behavior)
- ✓ Wishlist persists (database)
- ✓ Profile info saved
- ✓ Orders still visible

---

## 🧪 Advanced Testing

### Test 13: Empty States ❌
**Steps:**
1. Start fresh (clear cart, no wishlist items)
2. Go to cart with empty cart
3. Go to wishlist with no items
4. Check My Orders with no orders

**Expected Results:**
- ✓ Helpful empty messages shown
- ✓ Call-to-action buttons present
- ✓ No errors or blank pages

---

### Test 14: Database Integrity 🗄️
**Steps:**
1. Open `database.db` with SQLite client
2. Verify tables exist:
   - users, categories, products
   - wishlist, orders, order_items
   - delivery, payments
3. Verify data for:
   - Created users
   - Created orders
   - Wishlist entries
   - Payment records

**Expected Results:**
- ✓ All tables present
- ✓ Data properly stored
- ✓ Foreign keys working
- ✓ No corrupted data

---

### Test 15: Performance ⚡
**Steps:**
1. Add 5-10 items to cart
2. Add 5-10 items to wishlist
3. Create 5 test orders
4. Check page load times
5. Monitor memory usage

**Expected Results:**
- ✓ Pages load within 2 seconds
- ✓ No significant lag
- ✓ Database queries efficient
- ✓ Memory usage reasonable

---

## 🔍 Browser Compatibility Testing

### Test on Multiple Browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

**Expected Results:**
- ✓ All features work same across browsers
- ✓ No JavaScript errors
- ✓ CSS renders correctly
- ✓ Forms function properly

---

## 🆘 Troubleshooting During Testing

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>
```

### Issue: "Database locked" error
**Solution:**
- Close any open database connections
- Delete `database.db` to start fresh
- Run `python app.py` to reinitialize

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Products not showing
**Solution:**
- Delete `database.db`
- Run `python app.py`
- Sample products will be auto-added

### Issue: Cart not persisting
**Solution:**
- This is expected - session clears on logout
- Wishlist is database-backed and persists

---

## ✅ Test Completion Checklist

- [ ] All 15 tests passed
- [ ] No errors in browser console
- [ ] No errors in terminal
- [ ] Mobile view tested
- [ ] All browsers tested
- [ ] Database integrity verified
- [ ] Performance acceptable
- [ ] All features working as expected

---

## 📊 Test Results Template

Copy this to document your testing:

```
Date: ________________
Tester: ________________
Browser: ________________
OS: ________________

Test Results:
- Home Page: PASS / FAIL
- Categories: PASS / FAIL
- Registration: PASS / FAIL
- Login: PASS / FAIL
- Wishlist: PASS / FAIL
- Cart: PASS / FAIL
- Profile: PASS / FAIL
- Checkout: PASS / FAIL
- Payment: PASS / FAIL
- Orders: PASS / FAIL
- Mobile: PASS / FAIL
- Admin: PASS / FAIL

Issues Found:
1. ________________
2. ________________

Notes:
________________
```

---

## 🎯 Sign-Off

Once all tests pass, the application is ready for:
✅ Production deployment
✅ User acceptance testing
✅ Live launch

---

## 📞 Test Support

If tests fail:
1. Check browser console (F12)
2. Check terminal for errors
3. Review SETUP_GUIDE.md
4. Check database.db exists
5. Verify all dependencies installed

---

**Test Guide Version:** 2.0
**Last Updated:** May 2024
**Status:** Ready for Testing

Good luck with testing! 🚀


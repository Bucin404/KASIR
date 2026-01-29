# KASIR Modern - Kotlin Edition 🍽️

A modern Point of Sale (POS) system built with Kotlin and Ktor, featuring authentication, role-based access control, real-time notifications, and Bluetooth receipt printing.

## 🎯 Features

### Core Features (Ported from Flask)
- ✅ Modern, responsive UI with blue-green premium theme
- ✅ Menu management with categories (Food, Drinks, Desserts)
- ✅ Shopping cart functionality
- ✅ Transaction processing with tax calculation
- ✅ Real-time statistics dashboard
- ✅ Transaction history tracking
- ✅ SQLite database persistence

### New Features
- 🔐 **Authentication System**: JWT-based login and registration
- 👥 **Role-Based Access Control**: Admin, Cashier, and Manager roles
- 🔔 **Real-Time Notifications**: WebSocket-based notification system
- 🖨️ **Bluetooth Receipt Printing**: Connect to Bluetooth receipt printers and print transaction receipts
- 🛠️ **Admin Management**: Add, edit, and delete menu items with pricing
- 📊 **Enhanced Analytics**: User-attributed transactions and detailed statistics

## 🏗️ Architecture

### Backend Stack
- **Language**: Kotlin (JVM)
- **Framework**: Ktor 2.3.7
- **Database**: SQLite with Exposed ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: BCrypt password hashing
- **Real-time**: WebSockets for notifications
- **Printing**: ESC/POS printer support via Bluetooth

### Frontend
- **UI**: HTML5, CSS3, JavaScript (preserved from original Flask app)
- **Theme**: Blue-Green Modern Premium design
- **Layout**: Responsive, mobile-friendly
- **Features**: Dynamic menu loading, cart management, checkout flow

## 🚀 Getting Started

### Prerequisites
- JDK 11 or higher
- Gradle (included via wrapper)
- Bluetooth adapter (for printer functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Bucin404/KASIR.git
   cd KASIR
   ```

2. **Build the project**
   ```bash
   ./gradlew build
   ```

3. **Run the application**
   ```bash
   ./gradlew run
   ```

   The server will start on `http://localhost:8000`

### Default Credentials
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: ADMIN

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
  ```json
  {
    "username": "user",
    "email": "user@example.com",
    "password": "password",
    "role": "CASHIER"
  }
  ```

- `POST /api/auth/login` - Login
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

### Menu Management
- `GET /api/menu` - Get all menu items
- `POST /api/menu` - Add menu item (Admin only)
- `PUT /api/menu/:id` - Update menu item (Admin only)
- `DELETE /api/menu/:id` - Delete menu item (Admin only)

### Transactions
- `POST /api/checkout` - Process transaction
  ```json
  {
    "items": [
      {
        "id": 1,
        "name": "Nasi Goreng Spesial",
        "price": 25000,
        "quantity": 2
      }
    ],
    "payment": 60000
  }
  ```

- `GET /api/stats` - Get today's statistics
- `GET /api/transactions/today` - Get today's transactions
- `GET /api/transactions/recent` - Get recent transactions

### Notifications
- `GET /api/notifications/:userId` - Get user notifications
- `WS /ws/notifications` - Real-time notification stream

### Bluetooth Printing
- `GET /api/printer/discover` - Discover available Bluetooth printers
- `POST /api/printer/connect` - Connect to a printer
  ```json
  {
    "deviceName": "Printer Name",
    "deviceAddress": "00:11:22:33:44:55"
  }
  ```
- `POST /api/printer/disconnect` - Disconnect from printer
- `POST /api/printer/print` - Print receipt
  ```json
  {
    "transactionId": "TRX20240129123456",
    "date": "29/01/2024 12:34:56",
    ...
  }
  ```

## 👥 User Roles

### Admin
- Full access to all features
- Can manage menu items (add, edit, delete)
- Can view all transactions
- Can manage user accounts

### Manager
- Can view statistics and reports
- Can process transactions
- Cannot modify menu items

### Cashier
- Can process transactions
- Can view own transaction history
- Limited access to statistics

## 🖨️ Bluetooth Printer Setup

### Supported Printers
- ESC/POS compatible thermal receipt printers
- Bluetooth-enabled printers

### Setup Instructions
1. Pair your Bluetooth printer with the system
2. Use the `/api/printer/discover` endpoint to find available printers
3. Connect to your printer using `/api/printer/connect`
4. Print receipts after transactions using `/api/printer/print`

### Receipt Format
The receipt includes:
- Store header
- Transaction ID and date
- Cashier name
- Itemized list with quantities and prices
- Subtotal, tax (10%), and total
- Payment and change amounts
- Thank you message

## 🗄️ Database Schema

### Users
- id, username, email, password_hash, role, created_at

### MenuItems
- id, name, price, category, image, description, popular

### Transactions
- id, transaction_id, date, date_iso, subtotal, tax, total, payment, change_amount, cashier, user_id

### TransactionItems
- id, transaction_id (FK), item_id, item_name, price, quantity

### Notifications
- id, message, type, timestamp, user_id, read

## 🎨 UI/UX Design

The application maintains the original Flask app's beautiful UI design:
- **Color Scheme**: Blue-Green Modern Premium theme
- **Typography**: Poppins and Inter fonts
- **Layout**: Split-screen with scrollable menu and fixed cart
- **Animations**: Smooth transitions and hover effects
- **Responsive**: Mobile-friendly design
- **Images**: High-quality food photography from Unsplash

## 🔒 Security Features

- Password hashing with BCrypt
- JWT-based authentication
- Role-based authorization
- Secure token validation
- Input validation on all endpoints
- SQL injection prevention via ORM

## 🧪 Testing

Run the test suite:
```bash
./gradlew test
```

## 📦 Deployment

### Building for Production
```bash
./gradlew build
```

The application JAR will be created in `build/libs/`

### Running in Production
```bash
java -jar build/libs/kasir-kotlin-all.jar
```

### Environment Variables
- `PORT` - Server port (default: 8000)
- `JWT_SECRET` - Secret key for JWT signing (change in production!)

## 🔄 Migration from Flask

This Kotlin implementation provides:
1. ✅ **Feature Parity**: All original Flask features are preserved
2. ✅ **Same UI/UX**: Identical visual design and user experience
3. ✅ **Enhanced Features**: Added authentication, roles, notifications, and printing
4. ✅ **Better Performance**: Compiled Kotlin code with async/await support
5. ✅ **Type Safety**: Strong typing prevents runtime errors
6. ✅ **Scalability**: Better suited for production deployment

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Kotlin and Ktor**

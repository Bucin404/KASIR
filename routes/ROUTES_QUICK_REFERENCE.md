# KASIR Routes Quick Reference

## Authentication Routes (`/auth`)
```
POST   /auth/login              - User login
GET    /auth/logout             - User logout
GET    /auth/register           - Registration form
POST   /auth/register           - Process registration
GET    /auth/check-session      - Check session (API)
```

## Admin Routes (`/admin`)
```
GET    /admin/dashboard                    - Admin dashboard
GET    /admin/users                        - List users
GET    /admin/users/add                    - Add user form
POST   /admin/users/add                    - Process add user
GET    /admin/users/edit/<id>              - Edit user form
POST   /admin/users/edit/<id>              - Process edit user
POST   /admin/users/delete/<id>            - Delete user
POST   /admin/users/<id>/toggle-status     - Toggle user status
GET    /admin/stats/summary                - Statistics (API)
```

## Cashier Routes (`/cashier`)
```
GET    /cashier/                           - POS interface
GET    /cashier/transactions               - Transaction history
GET    /cashier/transaction/<id>           - Transaction detail
POST   /cashier/process-transaction        - Process transaction (API)
GET    /cashier/print-receipt/<id>         - Print receipt
POST   /cashier/cancel-transaction/<id>    - Cancel transaction (API)
GET    /cashier/products/search            - Search products (API)
```

## Finance Routes (`/finance`)
```
GET    /finance/dashboard                  - Finance dashboard
GET    /finance/records                    - List financial records
GET    /finance/records/add                - Add record form
POST   /finance/records/add                - Process add record
GET    /finance/records/edit/<id>          - Edit record form
POST   /finance/records/edit/<id>          - Process edit record
POST   /finance/records/delete/<id>        - Delete record
GET    /finance/reports                    - Financial reports
GET    /finance/api/summary                - Summary (API)
```

## Order Routes (`/order`)
```
GET    /order/menu                         - Public menu (QR ordering)
POST   /order/place-order                  - Place order (API)
GET    /order/payment/<order_id>           - Payment page
POST   /order/payment-callback             - Midtrans callback (API)
GET    /order/status/<order_id>            - Order status
GET    /order/manage                       - Manage orders (staff)
POST   /order/update-status/<id>           - Update status (API)
GET    /order/qr-generate                  - Generate QR code
GET    /order/api/orders                   - List orders (API)
```

## API Routes (`/api`)

### Products
```
GET    /api/products                       - List products
GET    /api/products/<id>                  - Get product
GET    /api/products/categories            - List categories
```

### Transactions
```
GET    /api/transactions                   - List transactions
GET    /api/transactions/<id>              - Get transaction
GET    /api/transactions/search            - Search transactions
```

### Statistics
```
GET    /api/stats/dashboard                - Dashboard stats
GET    /api/stats/sales                    - Sales statistics
GET    /api/stats/top-products             - Top products
```

### Users
```
GET    /api/users                          - List users
```

### Orders
```
GET    /api/orders                         - List orders
GET    /api/orders/<order_id>              - Get order (limited info)
```

### Finance
```
GET    /api/finance/summary                - Financial summary
```

### System
```
GET    /api/health                         - Health check
```

## Access Control

| Role    | Access Level                           |
|---------|----------------------------------------|
| admin   | Full access to all routes              |
| pemilik | Admin + Finance routes                 |
| kasir   | Cashier routes + view transactions     |
| public  | Order menu, place order, check status  |

## Common Query Parameters

### Pagination
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20, max: 100)

### Filters
- `status` - Filter by status
- `date` - Filter by date (YYYY-MM-DD)
- `category` - Filter by category
- `search` / `q` - Search query

### API Parameters
- `limit` - Limit results (max: 100)
- `period` - Time period (today, week, month, year)

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description"
}
```

## HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

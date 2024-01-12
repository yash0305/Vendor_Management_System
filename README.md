<h1 align="center">Vendor Management System with Performance Metrics</h1>

<p align="center">
  <em>This Vendor Management System (VMS) is a Django-based application designed to handle vendor profiles, track purchase orders, and calculate vendor performance metrics.</em>
</p>

## Objective

The objective of this project is to develop a comprehensive Vendor Management System using Django and Django REST Framework, enabling efficient vendor profile management, purchase order tracking, and vendor performance evaluation.

## Core Features

### 1. Vendor Profile Management
- **Model Design:** Includes fields for vendor information like name, contact details, address, and a unique vendor code.
- **API Endpoints:**
  - `POST /api/vendors/`: Create a new vendor.
  - `GET /api/vendors/`: List all vendors.
  - `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
  - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
  - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

### 2. Purchase Order Tracking
- **Model Design:** Tracks purchase orders with fields like PO number, vendor reference, order date, items, quantity, and status.
- **API Endpoints:**
  - `POST /api/purchase_orders/`: Create a purchase order.
  - `GET /api/purchase_orders/`: List all purchase orders with an option to filter by vendor.
  - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
  - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
  - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

### 3. Vendor Performance Evaluation
- **Metrics:** Calculates various performance metrics like On-Time Delivery Rate, Quality Rating, Response Time, and Fulfilment Rate.
- **API Endpoints:**
  - `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.
## Data Models

### 1. Vendor Model
- Stores essential information about vendors and their performance metrics.
- Includes fields for name, contact details, address, vendor code, and performance metrics.

### 2. Purchase Order (PO) Model
- Captures details of each purchase order and is used to calculate performance metrics.
- Contains fields such as PO number, vendor link, order date, delivery date, items, quantity, status, and performance-related fields.

### 3. Historical Performance Model
- Optionally stores historical data on vendor performance, allowing trend analysis.
- Includes fields for vendor link, date, and historical performance metrics.


## Backend Logic for Performance Metrics
- **On-Time Delivery Rate:** Calculated upon PO status change to 'completed'.
- **Quality Rating Average:** Updated upon completion of each PO where a quality_rating is provided.
- **Average Response Time:** Calculated upon vendor acknowledgment of a PO.
- **Fulfilment Rate:** Calculated upon any change in PO status.

## API Endpoint Implementation
- **Vendor Performance Endpoint (`GET /api/vendors/{vendor_id}/performance`):** Retrieves calculated performance metrics for a specific vendor.
- **Update Acknowledgment Endpoint (`POST /api/purchase_orders/{po_id}/acknowledge`):** Allows vendors to acknowledge POs, triggering acknowledgment_date update and average_response_time recalculation.

## Additional Technical Considerations
- **Efficient Calculation:** Optimized logic for handling large datasets efficiently.
- **Data Integrity:** Checks to handle scenarios like missing data or division by zero in calculations.
- **Real-time Updates:** Consideration of Django signals for triggering real-time metric updates.

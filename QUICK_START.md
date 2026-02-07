# Quick Start Guide

## Backend Server Status
✅ **Backend is running on http://localhost:3000**

## To Open the Frontend:

### Option 1: Direct File Open
1. Open your web browser (Chrome, Firefox, or Edge)
2. Press `Ctrl+O` (or `Cmd+O` on Mac)
3. Navigate to: `f:\CEE-port_visualization\port-visualization-frontend\index.html`
4. Click "Open"

### Option 2: Drag and Drop
1. Open Windows Explorer
2. Navigate to: `f:\CEE-port_visualization\port-visualization-frontend\`
3. Drag `index.html` into your browser window

### Option 3: Using a Local Server (Recommended)
```bash
# Install a simple HTTP server globally (one time only)
npm install -g http-server

# Navigate to frontend directory
cd f:\CEE-port_visualization\port-visualization-frontend

# Start the server
http-server -p 8080

# Then open: http://localhost:8080
```

## Important: MongoDB Requirement

⚠️ **MongoDB must be running for the backend to work!**

### To start MongoDB:
```bash
# If MongoDB is installed, run:
mongod --dbpath ./data/db

# Or if using MongoDB as a service:
net start MongoDB
```

If MongoDB is not installed, download it from: https://www.mongodb.com/try/download/community

## Testing the Application

Once you have both the frontend open and MongoDB running:

1. **Add a Port**: Click the "+ Add Port" button
2. **Click on the map** to set coordinates
3. **Fill in the form** with port details
4. **Save** to create your first port
5. **Test Export**: Click "Export" to download GeoJSON
6. **Test Import**: Click "Import" to upload a GeoJSON file

## Current Status

✅ Backend API Server: Running on port 3000
⏳ MongoDB: Please start manually
⏳ Frontend: Open manually using one of the options above

## API Endpoints Available

- GET http://localhost:3000/api/ports - List all ports
- POST http://localhost:3000/api/ports - Create port
- GET http://localhost:3000/api/geojson/ports - Get GeoJSON
- GET http://localhost:3000/health - Health check

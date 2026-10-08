# Intelligent Fleet Management System

A web-based fleet-management prototype for maintaining vehicles, drivers, trips, fuel, maintenance, and related records.

## Project Structure

```
fleet-management/
├── backend/                          # Django REST API
│   ├── config/                       # Django settings & URL config
│   ├── apps/                         # Django applications
│   │   ├── users/                   # User authentication & management
│   │   ├── vehicles/                # Vehicle management
│   │   ├── drivers/                 # Driver management
│   │   ├── trips/                   # Trip tracking
│   │   ├── routes/                  # Route optimization
│   │   ├── fuel/                    # Fuel management
│   │   ├── maintenance/             # Maintenance tracking
│   │   ├── notifications/           # Notification system
│   │   ├── reports/                 # Report generation
│   │   └── dashboard/               # Analytics dashboard
│   ├── static/                       # Static files
│   ├── media/                        # User uploads
│   └── requirements.txt              # Python dependencies
├── frontend/                          # HTML/CSS/JavaScript UI
│   ├── pages/                        # HTML pages
│   ├── css/                          # Stylesheets
│   └── js/                           # JavaScript files
├── docker/                            # Docker configuration
│   ├── Dockerfile                   # Backend container
│   ├── docker-compose.yml           # Multi-container setup
│   └── nginx.conf                   # Reverse proxy config
├── docs/                              # Documentation
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
└── requirements.txt                   # Python dependencies
```

## Technology Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL / SQLite (default)
- **Cache**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT (SimpleJWT)
- **APIs**: Python requests for external integrations

### Frontend
- **HTML5** / **CSS3** / **Vanilla JavaScript**
- **Bootstrap 5** - Responsive UI framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client (optional)

### DevOps
- **Docker** & **Docker Compose**
- **Nginx** - Reverse proxy & static file serving
- **Gunicorn** - WSGI server

## Features by Module

### 1. User Management
- User registration & login
- Admin-only role assignment and audit-log access
- Fleet APIs restricted to staff, admins, and fleet managers
- Customer accounts are limited to their own profile and account data

### 2. Vehicle Management
- Add/Edit/Delete vehicles
- Track vehicle status, location, and mileage
- Service history tracking
- Insurance and registration management

### 3. Driver Management
- Driver registration and licensing
- Experience tracking
- Performance ratings
- Assignment to vehicles

### 4. Trip Management
- Create and update scheduled trip records
- Manually managed trip statuses and actual distance
- No live GPS tracking or automatic delay detection

### 5. Route Optimization
- Store route records, delivery points, sequences, and estimates
- Route order, distance, and cost are entered as data; no route-solving engine is implemented

### 6. Fuel Management
- Record fuel consumption
- Cost tracking
- Aggregate dashboard fuel totals
- No automatic monthly fuel analytics generation

### 7. Maintenance Management
- Maintenance records and schedules
- Service history
- Cost tracking
- No predictive maintenance alerts are generated automatically

### 8. Notifications
- In-app notification records and preferences
- Password-reset emails use configured SMTP; general email/SMS notifications are not implemented

### 9. Reports
- Store report requests and their selected format/date range
- PDF, Excel, and CSV file generation/downloads are not implemented

### 10. Dashboard
- Aggregated fleet statistics and charts
- Vehicle map uses manually stored coordinates; it is not live tracking
- Fuel and maintenance totals are all-time aggregates

## Installation & Setup

### Prerequisites
- Python 3.11 or 3.12 (Django 4.2 support range)
- PostgreSQL 13+ (or SQLite for development)
- Redis 6+
- Node.js 16+ (optional, for frontend tooling)

### Quick Start (Local Development)

1. **Clone the repository**
   ```bash
   cd c:\Users\dhruv\OneDrive\Desktop\app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   copy backend\.env.example backend\.env
   # Edit backend/.env with your settings
   ```

5. **Run migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Frontend: http://localhost:8000
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

### Run Tests

From the `backend` directory, run the Django test suite:

```bash
python manage.py test
```

The default local email backend prints password-reset emails in the development server console. Configure SMTP environment variables to deliver reset links by email.

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   cd docker
   docker-compose up -d
   ```

2. **Run migrations in Docker**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

3. **Create superuser in Docker**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. **Access services**
   - Frontend: http://localhost
   - API: http://localhost/api/
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## API Endpoints

Protected endpoints require JWT authentication. Include header:
```
Authorization: Bearer <your_access_token>
```

### Users
- `POST /api/token/` - Obtain JWT access and refresh tokens
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `GET /api/users/me/` - Get current user profile

### Vehicles
- `GET /api/vehicles/` - List vehicles
- `POST /api/vehicles/` - Create vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle
- `DELETE /api/vehicles/{id}/` - Delete vehicle
- `POST /api/vehicles/{id}/update_location/` - Update vehicle location

### Drivers
- `GET /api/drivers/` - List drivers
- `POST /api/drivers/` - Create driver
- `GET /api/drivers/{id}/` - Get driver details

### Trips
- `GET /api/trips/` - List trips
- `POST /api/trips/` - Create trip
- `GET /api/trips/{id}/` - Get trip details
- `PUT /api/trips/{id}/` - Update trip

### Routes
- `GET /api/routes/` - List routes
- `POST /api/routes/` - Create optimized route

### Fuel
- `GET /api/fuel/entries/` - List fuel entries
- `POST /api/fuel/entries/` - Create fuel entry
- `GET /api/fuel/analytics/` - Fuel analytics

### Maintenance
- `GET /api/maintenance/records/` - List maintenance records
- `POST /api/maintenance/records/` - Create maintenance record
- `GET /api/maintenance/schedule/` - Get maintenance schedule

### Dashboard
- `GET /api/dashboard/` - Get dashboard statistics

### Reports
- `GET /api/reports/` - List reports
- `POST /api/reports/` - Generate report

## Configuration

### Environment Variables (.env)
```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
MONGO_DB_NAME=fleet_management
MONGO_HOST=localhost
MONGO_PORT=27017

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_HOURS=24

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Development Workflow

### Create New Feature
1. Create Django app: `python manage.py startapp app_name`
2. Define models in `models.py`
3. Create serializers in `serializers.py`
4. Create viewsets in `views.py`
5. Register routes in `urls.py`
6. Add to `INSTALLED_APPS` in settings
7. Run migrations: `python manage.py makemigrations && migrate`

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.vehicles

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Setup PostgreSQL database
- [ ] Setup Redis cache
- [ ] Configure email backend
- [ ] Setup Celery workers
- [ ] Use environment-specific settings
- [ ] Setup SSL/TLS certificates
- [ ] Configure CORS properly
- [ ] Setup logging and monitoring
- [ ] Run security checks: `python manage.py check --deploy`

### Deployment Options
- **Heroku**: Use `Procfile` and `runtime.txt`
- **Railway**: Use `docker-compose.yml`
- **AWS**: Use EC2 + RDS + ElastiCache
- **DigitalOcean**: Use App Platform or Droplets

## Troubleshooting

### Database Issues
```bash
# Reset database
python manage.py flush

# Check migrations
python manage.py showmigrations

# Create migrations
python manage.py makemigrations
```

### Static Files Issues
```bash
# Collect static files
python manage.py collectstatic --clear --noinput
```

### Cache Issues
```bash
# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Contributing

1. Create a new branch: `git checkout -b feature/new-feature`
2. Make your changes
3. Commit: `git commit -m 'Add new feature'`
4. Push: `git push origin feature/new-feature`
5. Create Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, feature requests, or questions:
- Create an issue in the repository
- Contact: support@fleetmanagement.com

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time GPS tracking with WebSocket
- [ ] Advanced analytics with ML predictions
- [ ] Integration with Google Maps API
- [ ] SMS notifications
- [ ] Multi-language support
- [ ] Dark mode UI
- [ ] Advanced reporting with Pivot tables
- [ ] Integration with IoT devices
- [ ] Blockchain for audit trails

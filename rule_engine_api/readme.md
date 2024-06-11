# Rule Engine API

The **Rule Engine API** is a FastAPI-based web service designed to evaluate transactions against predefined rules and provide an approval status based on the evaluation results. It includes endpoints for checking transactions, saving transactions to a database, managing rules, and more.

## Features

- **Transaction Evaluation**: Evaluate transactions against predefined rules to determine approval or rejection.
- **Database Interaction**: Save transactions to a PostgreSQL database and retrieve rules from the database.
- **Rule Management**: Create, read, update, and delete rules dynamically through API endpoints.
- **Logging**: Use logging to track transaction evaluations and database interactions.
- **Initial Data Setup**: Automatically populate the database with initial rules upon startup.
- **Docker Support**: Deploy the application as a Docker container for easy portability and scalability.

## Project Structure

The project follows a structured layout for easy navigation:

```
.
├── app                   # Main application directory
│   ├── main.py           # Main FastAPI application
│   ├── api               # API-related files
│   │   └── v0            # API versioning directory
│   │       └── endpoints # Endpoint implementations
│   │           ├── rules.py         # Rules API endpoints
│   │           └── transaction.py   # Transaction API endpoints
│   ├── core              # Core configuration files
│   │   └── config.py     # Application configuration
│   ├── db                # Database related files
│   │   ├── crud.py       # CRUD operations for database
│   │   ├── models.py     # SQLAlchemy models
│   │   └── session.py    # Database session setup
│   ├── initial_data      # Initial data setup files
│   │   ├── initial_rules.json    # Initial rules data
│   │   └── insert_rules.py       # Script to insert initial rules
│   ├── schemas           # Pydantic schemas
│   │   ├── responses.py  # Response models
│   │   ├── rule.py       # Rule schemas
│   │   └── transaction.py    # Transaction schemas
│   └── services          # Additional services
│       └── rule_engine.py     # Rule evaluation logic
├── docker-compose.yml   # Docker Compose configuration
├── readme.md            # Project readme file
├── requirements.txt     # Python dependencies
├── scripts              # Utility scripts
│   └── api_load.py      # Script for API load testing
└── tests                # Test cases
    └── test_transactions.py   # Transaction test cases
```

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.x and pip (if not using Docker)

### Running the Application

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd rule-engine-api
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Access the API at `http://localhost:8000/v0/`.

### Debugging

To debug the application:

1. Set breakpoints in your code where you want to pause execution.
2. Run the Docker containers in debug mode:

    ```bash
    docker-compose -f docker-compose.yml -f docker-compose.debug.yml up --build
    ```

3. Use your preferred debugger (e.g., VS Code, PyCharm) to attach to the running container.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for your own projects.

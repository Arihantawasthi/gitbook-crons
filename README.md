# GitBook Crons

**Automated background jobs for the GitBook platform.**  
This service collects repository statistics and syncs commit data on a scheduled basis. It interacts directly with the [`gitbook`](https://github.com/your-org/gitbook) backend service to keep the database and metadata up-to-date.

---

## 🧠 What It Does

GitBook Crons is the invisible engine of the GitBook ecosystem. It runs periodically to:

- Calculate statistics for each repository
- Sync last commit information
- Update global stats (commits, lines, files, etc.)
- Submit this data to the backend via HTTP APIs

> It’s your personal Git janitor, but with better hygiene and no complaints.

---

## 🛠 Tech Stack

- **Python 3.x**
- Uses standard libraries (`subprocess`, `os`, `json`, etc.)
- Communicates with the GitBook backend via `requests`
- Schedulable via `cron`, `systemd`, or CI runners

---

## ⚙️ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-org/gitbook-crons.git
cd gitbook-crons
```

### 2. Install dependencies
It's recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure and run the job
All environment configuration is handled via `runserver.sh`. Create this file with:
```bash
#!/bin/zsh

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: ./runserver.sh <task>"
  echo "Available commands: update_stats, insert_metadata"
  exit 1
fi

export GIT_DIR=/path/to/bare/git/directory/
export DB_NAME=gitbook
export DB_USER=yourusername
export DB_PASS=yourpassword
export DB_HOST=localhost
export DB_PORT=5432

python main.py "$1"
```

Make it executable:
```chmod +x runserver.sh```

Then simple run it:
```source runserver.sh```

You can also schedule it using cron or another job runner.

## 📬 Backend API Dependency
This service requires a running instance of the [`gitbook backend`](https://github.com/Arihantawasthi/gitbook.git). It uses the following endpoints:
| Method      | Endpoint                     | Description
| :---        | :---                         | :---
| `GET`       | `/api/v1/repos`              | List all tracked repositories
| `POST`      | `/api/v1/update-last-commit` | Manually trigger update of last commit data
| `GET`       | `/api/v1/stats`              | Fetch overall repositories statistics (repos, commits, lines, etc.)

---

## 🧪 Development Notes
- The stats calculation ignores common bloat directories like `node_modules`, `.git`, `.venv`, etc.
- All data flows back to the backend through clean HTTP POSTs
- Failures are logged to stdout for now (extend with better logging if needed)

---

## 📅 Scheduling Example
Use a crontab to run this periodically
```*/15 * * * * /absolute/path/to/gitbook-crons/runserver.sh```


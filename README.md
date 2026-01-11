# Kafka Email Event-Driven Architecture

A simple event-driven system using Apache Kafka where a **Producer** generates email update events and a **Consumer** processes them in real-time.

## 🛠️ Tech Stack

- **Apache Kafka** (via Docker)
- **Python 3.13+**
- **kafka-python-ng** library

## 📁 Project Structure

```
kafka-email/
├── docker-compose.yml   # Kafka server (single-node, KRaft mode)
├── requirements.txt     # Python dependencies
├── README.md
└── src/
    ├── producer.py      # Generates email update events
    └── consumer.py      # Processes events in real-time
```

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Python 3.13+

### 1. Start Kafka

```bash
docker-compose up -d
```

Wait ~30 seconds for Kafka to initialize. Verify it's running:

```bash
docker-compose logs kafka
```

Look for: `Kafka Server started`

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Consumer (Terminal 1)

```bash
python src/consumer.py
```

### 4. Run the Producer (Terminal 2)

```bash
python src/producer.py
```

### 5. Watch Events Flow! 🎉

The producer sends email events every 2 seconds. The consumer displays them with action icons:

| Icon | Action |
|------|--------|
| 📤 | sent |
| 📬 | delivered |
| 👁️ | opened |
| 🔗 | clicked |
| ⚠️ | bounced |
| 🚫 | unsubscribed |

### Cleanup

```bash
docker-compose down
```

## 📨 Event Format

```json
{
  "event_id": "uuid",
  "event_type": "email_update",
  "timestamp": "2026-01-11T23:30:00",
  "email_id": "abc123",
  "action": "sent|delivered|opened|clicked|bounced|unsubscribed",
  "details": {
    "sender": "newsletter@company.com",
    "recipient": "user@gmail.com",
    "subject": "Sample Email #1234"
  }
}
```

## 🔧 Configuration

Edit these constants in `producer.py` and `consumer.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker address |
| `TOPIC_NAME` | `email-updates` | Kafka topic name |
| `CONSUMER_GROUP` | `email-processor-group` | Consumer group ID |


"""
Email Update Event Producer
Generates email update events and sends them to Kafka topic 'email-updates'
"""

import json
import time
import random
import uuid
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'email-updates'

# Sample data for generating realistic events
EMAIL_ACTIONS = ['sent', 'delivered', 'opened', 'clicked', 'bounced', 'unsubscribed']
SAMPLE_EMAILS = [
    'newsletter@company.com',
    'promo@shop.com', 
    'updates@service.com',
    'alerts@platform.com'
]
SAMPLE_RECIPIENTS = [
    'john.doe@gmail.com',
    'jane.smith@yahoo.com',
    'bob.wilson@outlook.com',
    'alice.chen@mail.com'
]


def create_email_event():
    """Generate a random email update event"""
    action = random.choice(EMAIL_ACTIONS)
    
    event = {
        'event_id': str(uuid.uuid4()),
        'event_type': 'email_update',
        'timestamp': datetime.now().isoformat(),
        'email_id': str(uuid.uuid4())[:8],
        'action': action,
        'details': {
            'sender': random.choice(SAMPLE_EMAILS),
            'recipient': random.choice(SAMPLE_RECIPIENTS),
            'subject': f'Sample Email #{random.randint(1000, 9999)}'
        }
    }
    
    # Add action-specific details
    if action == 'clicked':
        event['details']['link_url'] = 'https://example.com/offer'
    elif action == 'bounced':
        event['details']['bounce_reason'] = random.choice(['invalid_address', 'mailbox_full', 'server_error'])
    
    return event


def main():
    print("=" * 50)
    print("📧 Email Update Event Producer")
    print("=" * 50)
    print(f"Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    
    # Create Kafka producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        print("✅ Connected to Kafka successfully!\n")
    except KafkaError as e:
        print(f"❌ Failed to connect to Kafka: {e}")
        print("Make sure Kafka is running: docker-compose up -d")
        return

    print(f"Sending events to topic: '{TOPIC_NAME}'")
    print("Press Ctrl+C to stop\n")
    print("-" * 50)
    
    event_count = 0
    
    try:
        while True:
            # Create and send event
            event = create_email_event()
            
            # Use email_id as the key for partitioning
            future = producer.send(
                TOPIC_NAME,
                key=event['email_id'],
                value=event
            )
            
            # Wait for confirmation
            try:
                record_metadata = future.get(timeout=10)
                event_count += 1
                print(f"[{event_count}] Sent: {event['action'].upper():12} | "
                      f"Email: {event['email_id']} | "
                      f"To: {event['details']['recipient']}")
            except KafkaError as e:
                print(f"❌ Failed to send event: {e}")
            
            # Wait before sending next event
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print(f"🛑 Producer stopped. Total events sent: {event_count}")
    finally:
        producer.close()


if __name__ == '__main__':
    main()

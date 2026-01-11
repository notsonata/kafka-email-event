"""
Email Update Event Consumer
Subscribes to Kafka topic 'email-updates' and processes events in real-time
"""

import json
import sys
from kafka import KafkaConsumer
from kafka.errors import KafkaError

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'email-updates'
CONSUMER_GROUP = 'email-processor-group'


def process_email_event(event):
    """Process an email update event"""
    action = event.get('action', 'unknown')
    email_id = event.get('email_id', 'N/A')
    details = event.get('details', {})
    recipient = details.get('recipient', 'unknown')
    subject = details.get('subject', 'No subject')
    
    # Format output based on action type
    action_icons = {
        'sent': '📤',
        'delivered': '📬',
        'opened': '👁️ ',
        'clicked': '🔗',
        'bounced': '⚠️ ',
        'unsubscribed': '🚫'
    }
    
    icon = action_icons.get(action, '📧')
    
    print(f"{icon} [{action.upper():12}] Email: {email_id} | To: {recipient}")
    print(f"   Subject: {subject}")
    
    # Show additional details for specific actions
    if action == 'clicked' and 'link_url' in details:
        print(f"   Link: {details['link_url']}")
    elif action == 'bounced' and 'bounce_reason' in details:
        print(f"   Reason: {details['bounce_reason']}")
    
    print()


def main():
    print("=" * 50)
    print("📧 Email Update Event Consumer")
    print("=" * 50)
    print(f"Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    
    # Create Kafka consumer
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id=CONSUMER_GROUP,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        print("✅ Connected to Kafka successfully!")
        print(f"✅ Subscribed to topic: '{TOPIC_NAME}'")
        print(f"✅ Consumer group: '{CONSUMER_GROUP}'\n")
    except KafkaError as e:
        print(f"❌ Failed to connect to Kafka: {e}")
        print("Make sure Kafka is running: docker-compose up -d")
        return

    print("Waiting for email events...")
    print("Press Ctrl+C to stop\n")
    print("-" * 50)
    
    event_count = 0
    
    try:
        for message in consumer:
            event = message.value
            event_count += 1
            
            print(f"--- Event #{event_count} (Partition: {message.partition}, Offset: {message.offset}) ---")
            process_email_event(event)
                
    except KeyboardInterrupt:
        print("\n🛑 Shutdown signal received...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("-" * 50)
        print(f"📊 Total events processed: {event_count}")
        consumer.close()
        print("👋 Consumer closed. Goodbye!")


if __name__ == '__main__':
    main()

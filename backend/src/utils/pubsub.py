import base64
import json
from typing import Any, Dict

from fastapi import HTTPException, Request
from google.cloud import pubsub_v1  # type: ignore

from src.constants import DOCKER, PROD, PROJECT_ID, PUBSUB_TOKEN

"""
EMULATOR FUNTIONS
"""


def create_topic(project_id: str, topic_id: str) -> None:
    """Create a new Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)  # type: ignore
    topic = publisher.create_topic(request={"name": topic_path})  # type: ignore
    print(f"Created topic: {topic.name}")  # type: ignore


def create_push_subscription(
    project_id: str, topic_id: str, subscription_id: str, endpoint: str
) -> None:
    """Create a new push subscription on the given topic."""
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, topic_id)  # type: ignore
    sub_path = subscriber.subscription_path(project_id, subscription_id)  # type: ignore
    push_config = pubsub_v1.types.PushConfig(push_endpoint=endpoint)  # type: ignore

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        request = {"name": sub_path, "topic": topic_path, "push_config": push_config}  # type: ignore
        subscription = subscriber.create_subscription(request=request)  # type: ignore

    print(f"Push subscription created: {subscription}.")
    print(f"Endpoint for subscription is: {endpoint}")


"""
APPLICATION FUNTIONS
"""

publisher = pubsub_v1.PublisherClient()


def publish_to_topic(topic: str, message: Dict[str, Any]) -> None:
    # Encode data
    data = json.dumps(message).encode("utf-8")

    if PROD or DOCKER:
        # Write to PubSub or emulator
        topic_path: str = publisher.topic_path(PROJECT_ID, topic)  # type: ignore
        publisher.publish(topic_path, data=data)  # type: ignore
    else:
        raise HTTPException(400, "Must be in production or docker")


async def parse_request(token: str, request: Request) -> Dict[str, Any]:
    if token != PUBSUB_TOKEN:
        raise HTTPException(400, "Invalid token")

    data = await request.json()
    if PROD or DOCKER:
        data = json.loads(base64.b64decode(data["message"]["data"]))

    return data

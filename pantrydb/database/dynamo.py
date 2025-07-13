from typing import List

import boto3
import structlog
from botocore.exceptions import ClientError

from pantrydb.database.abstract import PantryDatabase
from pantrydb.items import PantryItem

logger = structlog.get_logger()


class DynamoPantryDatabase(PantryDatabase):
    """DynamoDB implementation of the PantryDatabase abstract class."""

    TABLE_NAME = "pantry_items"

    @classmethod
    def from_env_vars(cls) -> "DynamoPantryDatabase":
        """Create a DynamoPantryDatabase instance from environment variables."""
        return cls()

    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.TABLE_NAME)
        self.client = boto3.client("dynamodb")
        logger.info("DynamoPantryDatabase initialized", table_name=self.TABLE_NAME)

    def list_items(self) -> List[PantryItem]:
        logger.info("Listing items in dynamo")
        try:
            response = self.table.scan()
            items = response.get("Items", [])
            return [
                PantryItem(name=item["item_name"], amount=item["amount"])
                for item in items
            ]
        except ClientError:
            return []

    def add_item(self, item: PantryItem) -> bool:
        logger.info("Adding item to dynamo")
        try:
            # Try to update the amount if item exists, else put new item
            self.table.update_item(
                Key={"item_name": item.name},
                UpdateExpression="SET amount = if_not_exists(amount, :zero) + :inc",
                ExpressionAttributeValues={":inc": item.amount, ":zero": 0},
                ReturnValues="UPDATED_NEW",
            )
            logger.info("Added item to dynamo")
            return True
        except ClientError:
            return False

    def remove_item(self, item: PantryItem) -> bool:
        logger.info("Removing item from dynamo")
        try:
            get_response = self.table.get_item(Key={"item_name": item.name})
            current_item = get_response.get("Item")

            if not current_item:
                logger.warning("Item not found")
                return False

            current_amount = current_item.get("amount", 0)

            if current_amount < item.amount:
                logger.warning("Trying to remove more items than are present")
                return False

            if current_amount == item.amount:
                # Remove the entire item
                self.table.delete_item(
                    Key={"item_name": item.name},
                    ConditionExpression="amount <= :dec",
                    ExpressionAttributeValues={":dec": item.amount},
                )
            else:
                # Decrement the amount
                self.table.update_item(
                    Key={"item_name": item.name},
                    UpdateExpression="SET amount = amount - :dec",
                    ConditionExpression="amount >= :dec",
                    ExpressionAttributeValues={":dec": item.amount},
                )

            logger.info("Removed item from dynamo")
            return True
        except ClientError as e:
            logger.error("Failed to remove item", exc_info=e)
            return False

import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Books')


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    print(event)  # debugging

    method = event.get("httpMethod")

    # ✅ GET ALL BOOKS
    if method == "GET":
        result = table.scan()
        return response(200, result["Items"])

    # ✅ ADD BOOK
    elif method == "POST":

        body = json.loads(event.get("body", "{}"))

        item = {
            "bookId": str(uuid.uuid4()),   # FIXED name
            "title": body["title"],
            "author": body["author"],
            "price": body["price"]
        }

        table.put_item(Item=item)

        return response(200, item)

    # ✅ DELETE BOOK
    elif method == "DELETE":

        query = event.get("queryStringParameters")

        if not query or "bookId" not in query:
            return response(400, {"error": "bookId required"})

        table.delete_item(
            Key={"bookId": query["bookId"]}
        )

        return response(200, {"message": "Book deleted"})

    return response(400, {"error": "Unsupported method"})
import json
import boto3
import random
import string

# Initialisation du client DynamoDB
dynamodb = boto3.client("dynamodb")
TABLE_NAME = "URLShortener" # Remplacez par le nom de votre table DynamoDB

def generate_short_id(length=6):
    """Génère un short_id aléatoire de la longueur spécifiée."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def lambda_handler(event, context):
    print("🔍 Événement reçu:", json.dumps(event))

    try:
        http_method = event.get("httpMethod")

        # 📌 Gestion des requêtes OPTIONS (CORS)
        if http_method == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"message": "CORS OK"})
            }

        # 📌 Gestion des requêtes POST (Création d'un lien court)
        if http_method == "POST":
            body = json.loads(event["body"]) if "body" in event and event["body"] else {}

            long_url = body.get("url")
            if not long_url:
                return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},
                        "body": json.dumps({"error": "URL manquante"})}

            short_id = generate_short_id()

            # Enregistrer dans DynamoDB
            dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    "short_id": {"S": short_id},
                    "long_url": {"S": long_url}
                }
            )

            print(f"✅ Lien raccourci créé : {short_id} → {long_url}")

            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "message": "URL raccourcie avec succès",
                    "short_id": short_id,
                    "long_url": long_url,
                    "short_url": f"api_gateway_url/prod/shorten/{short_id}" # Remplacez par l'URL de votre API Gateway
                })
            }

        # 📌 Gestion des requêtes GET (Récupération et redirection)
        elif http_method == "GET":
            path_params = event.get("pathParameters", {})
            short_id = path_params.get("short_id")

            if not short_id:
                return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},
                        "body": json.dumps({"error": "short_id manquant"})}

            print(f"🔍 Recherche de l'URL pour short_id: {short_id}")

            response = dynamodb.get_item(
                TableName=TABLE_NAME,
                Key={"short_id": {"S": short_id}}
            )

            if "Item" not in response:
                return {"statusCode": 404, "headers": {"Access-Control-Allow-Origin": "*"},
                        "body": json.dumps({"error": "URL non trouvée"})}

            long_url = response["Item"]["long_url"]["S"]
            print(f"✅ URL trouvée : {long_url}")

            return {
                "statusCode": 301,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Location": long_url,
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Redirection", "url": long_url})
            }

        return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Requête non valide"})}

    except Exception as e:
        print("🔥 ERREUR CRITIQUE :", str(e))
        return {"statusCode": 500, "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": str(e)})}

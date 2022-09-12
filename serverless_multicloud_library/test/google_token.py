import google.oauth2.id_token
import google.auth.transport.requests

request = google.auth.transport.requests.Request("../../credential/google_cloud.json")
audience = 'https://europe-west2-amiable-bridge-342803.cloudfunctions.net/function-2a'

id_token = google.oauth2.id_token.fetch_id_token(request, audience)
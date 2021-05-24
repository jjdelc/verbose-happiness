import json
from urllib.parse import urlparse, urlunsplit
from urllib.request import Request, urlopen

TIKTOK_VM = "https://vm.tiktok.com"

def follow_url(url):
    request = Request(url)
    response = urlopen(request)
    ugly = response.geturl()
    return ugly


def resolve_tiktok(url):
    html_url = follow_url(url)
    parsed = urlparse(html_url)
    html_url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    ugly = follow_url(html_url)
    return ugly


def response(status, body):
    return {
        'statusCode': status,
        "headers": {"Content-Type": "application/json"},
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    status = 400
    try:
        url = event["queryStringParameters"]["url"]
    except KeyError:
        return response(400, "Invalid Tiktok URL")

    if not url.startswith(TIKTOK_VM):
        return response(400, "Invalid Tiktok URL")

    safe_url = resolve_tiktok(url)
    return response(200, safe_url)

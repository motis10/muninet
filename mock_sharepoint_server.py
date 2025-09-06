from flask import Flask, request, make_response


app = Flask(__name__)


@app.route("/_layouts/15/NetanyaMuni/incidents.ashx", methods=["POST"])
def create_new_incident():
    """
    Mock endpoint for method=CreateNewIncident using multipart/form-data with a 'json' field.
    Always returns the provided static response regardless of input.
    """
    method = request.args.get("method")
    if method != "CreateNewIncident":
        response = make_response({"error": "Unsupported method"}, 400)
        return response

    # Build the exact JSON body specified by the user
    body = {
        "ResultCode": 200,
        "ErrorDescription": "CreateIncident ==> DoCreate => SUCCESS!!! Entity Guid = e1ec2e3c-4063-f011-bec2-7c1e52885535 ==> File Upload Response = [{\"FileName\":null,\"Status\":\"FAILD\",\"Error\":\"System.Exception: The FilesContents Is Missing!\\r\\n   at AC.NTN.FilesManager.API.Controllers.FileController.FileUpload(RequestFilesUpload request) in C:\\\\Users\\\\nadav\\\\Source\\\\Repos\\\\Applicationcare-IL\\\\AC.NTN.FilesManager.API\\\\Controllers\\\\FileController.cs:line 43\"}]",
        "ResultStatus": "SUCCESS CREATE",
        "ResultData": {
            "incidentGuid": "e1ec2e3c-4063-f011-bec2-7c1e52885535",
            "incidentNumber": "116717",
        },
        "data": "116717",
    }

    resp = make_response(body, 200)

    # Set headers to match as closely as possible
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Cache-Control"] = "private"
    resp.headers["X-Sharepointhealthscore"] = "0"
    resp.headers["X-Aspnet-Version"] = "4.0.30319"
    resp.headers["Sprequestguid"] = "4dbeb2a1-4a19-f05f-9402-8c4b269f16a1"
    resp.headers["Request-Id"] = "4dbeb2a1-4a19-f05f-9402-8c4b269f16a1"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["Content-Security-Policy"] = (
        "frame-ancestors 'self' teams.microsoft.com *.teams.microsoft.com *.skype.com *.teams.microsoft.us "
        "local.teams.office.com *.powerapps.com *.yammer.com *.officeapps.live.com *.office.com *.stream.azure-test.net "
        "*.microsoftstream.com *.dynamics.com *.microsoft.com onedrive.live.com *.onedrive.live.com;"
    )
    resp.headers["Sprequestduration"] = "15262"
    resp.headers["Spiislatency"] = "0"
    resp.headers["X-Powered-By"] = "ASP.NET"
    resp.headers["Microsoftsharepointteamservices"] = "16.0.0.16731"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Ms-Invokeapp"] = "1; RequireReadOnly"
    resp.headers["Cf-Cache-Status"] = "DYNAMIC"
    resp.headers["Report-To"] = (
        '{"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v4?s=I5anWvQ8l%2BVkWDjIJzpfuaqv5V4BUB70OqyA7Yc%2Bl%2F4VxTZYzHnYc6QlUUPsM%2BlPaSSHQf%2FCLLIbSCEWt%2FdAlgn61MG3Nq8QoOUiYoEtKdd0Ee8kYLKYbZfFOFqzw8v71Kt5ZLU%3D"}],"group":"cf-nel","max_age":604800}'
    )
    resp.headers["Nel"] = '{"success_fraction":0,"report_to":"cf-nel","max_age":604800}'
    resp.headers["Set-Cookie"] = (
        "__cflb=04dToW8zEWux7w3HXKfKJrvAb1JtzxW77LHmJrJBV5; SameSite=None; Secure; path=/; "
        "expires=Thu, 17-Jul-25 20:00:18 GMT; HttpOnly"
    )
    resp.headers["Strict-Transport-Security"] = "max-age=15552000; includeSubDomains; preload"
    resp.headers["Server"] = "cloudflare"
    resp.headers["Cf-Ray"] = "960bfadec889c088-TLV"
    resp.headers["Server-Timing"] = (
        'cfL4;desc="?proto=TCP&rtt=15549&min_rtt=12115&rtt_var=4452&sent=10&recv=17&lost=0&retrans=0&sent_bytes=3730&recv_bytes=1917&delivery_rate=268425&cwnd=255&unsent_bytes=0&cid=41b093c74022792e&ts=15325&x=0"'
    )

    return resp


if __name__ == "__main__":
    # Bind to all interfaces so it can be reached externally if needed
    app.run(host="0.0.0.0", port=9090, debug=True)



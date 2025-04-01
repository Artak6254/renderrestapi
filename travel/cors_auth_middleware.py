from django.http import JsonResponse

class CustomCORSAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Ստուգում ենք՝ օգտատերը մուտք գործած է թե ոչ
        if request.user.is_authenticated:
            response["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        else:
            response["Access-Control-Allow-Origin"] = "null"  # Չթույլատրել ոչ login արածներին
        
        return response

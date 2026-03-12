import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def analyze_url(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            url = data.get('url')
            
            if not url:
                return JsonResponse({'error': 'URL is required'}, status=400)
            
            # Ensure the URL is properly formatted
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # Fetch headers from the URL
            response = requests.head(url, timeout=10, allow_redirects=True)
            headers = response.headers
            
            # Security headers to analyze
            security_headers_to_check = {
                'Content-Security-Policy': {
                    'description': 'Helps prevent XSS attacks and data injection.'
                },
                'Strict-Transport-Security': {
                    'description': 'Enforces secure (HTTP over SSL/TLS) connections.'
                },
                'X-Frame-Options': {
                    'description': 'Protects against clickjacking vulnerabilities.'
                },
                'X-Content-Type-Options': {
                    'description': 'Prevents MIME-sniffing attacks.'
                },
                'Referrer-Policy': {
                    'description': 'Controls how much referrer information is included with requests.'
                },
                'Permissions-Policy': {
                    'description': 'Controls which web features and APIs can be used.'
                }
            }
            
            # Analyze present/missing headers
            results = []
            for header_name, info in security_headers_to_check.items():
                is_present = header_name in headers
                status = "Present" if is_present else "Missing"
                
                # Determine security level
                if is_present:
                    security_level = "Good"
                else:
                    # Treat CSP and HSTS as high Risk if missing, others as Warnings
                    if header_name in ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Frame-Options']:
                        security_level = "Risk"
                    else:
                        security_level = "Warning"
                
                results.append({
                    "header_name": header_name,
                    "status": status,
                    "security_level": security_level,
                    "explanation": info['description']
                })
                
            # Return JSON payload
            return JsonResponse({'url': url, 'analysis': results})
            
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Failed to reach the target URL. ({str(e)})'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid request payload format.'}, status=400)
            
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

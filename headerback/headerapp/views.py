from .models import ReportedURL, VoteRecord
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from headerapp.utils import analyze_headers
from django.db.models import Q
import json
import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return HttpResponse("This is HomePage")

@csrf_exempt
def analyze_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
        except json.JSONDecodeError:
            url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'URL is required'}, status=400)
            
        # Add scheme if missing
        original_input = url
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        try:
            # Check if reported and get votes
            report = ReportedURL.objects.filter(url__contains=original_input).first()

            # Standard User-Agent to avoid being blocked
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 HeaderShield/1.0'
            }
            
            # Use HEAD request for efficiency and compatibility
            # verify=False can be used if SSL issues are common, but better to keep it True by default
            response = requests.head(url, headers=request_headers, timeout=10, allow_redirects=True)
            
            # If HEAD fails or is not allowed, try GET but only for headers
            if response.status_code == 405 or response.status_code == 403:
                response = requests.get(url, headers=request_headers, timeout=10, stream=True)
            
            headers = response.headers
            
            # Use utility for analysis and fixes
            analysis_results, total_score = analyze_headers(headers)

            result = {
                'url': url,
                'status_code': response.status_code,
                'security_score': total_score,
                'max_score': 100,
                'headers_analyzed': analysis_results,
                'reported_warning': report is not None
            }

            if report:
                result['report_details'] = {
                    'ups': report.ups,
                    'downs': report.downs
                }

            return JsonResponse(result)

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'Scan timed out. The server took too long to respond.'}, status=408)
        except requests.exceptions.SSLError:
            return JsonResponse({'error': 'SSL Verification failed. The target site might have an invalid certificate.'}, status=400)
        except requests.exceptions.ConnectionError:
            return JsonResponse({'error': 'Connection failed. Could not reach the target server.'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'Failed to fetch the URL: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def report_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url')
            description = data.get('description')
        except json.JSONDecodeError:
            url = request.POST.get('url')
            description = request.POST.get('description')

        if not url or not description:
            return JsonResponse({'error': 'URL and Description are required'}, status=400)

        report, created = ReportedURL.objects.get_or_create(url=url, defaults={'description': description})
        if not created:
            return JsonResponse({'message': 'URL already reported', 'already_exists': True})
        
        return JsonResponse({'message': 'Report Accepted', 'already_exists': False})

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

def search_reports(request):
    query = request.GET.get('url', '')
    if not query:
        return JsonResponse({'results': []})
    
    reports = ReportedURL.objects.filter(url__icontains=query)
    results = []
    for r in reports:
        results.append({
            'id': r.id,
            'url': r.url,
            'description': r.description,
            'ups': r.ups,
            'downs': r.downs
        })
    return JsonResponse({'results': results})

@csrf_exempt
def vote_report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report_id = data.get('id')
            vote_type = data.get('vote') # 'up' or 'down'
        except json.JSONDecodeError:
            report_id = request.POST.get('id')
            vote_type = request.POST.get('vote')

        ip = get_client_ip(request)

        try:
            report = ReportedURL.objects.get(id=report_id)
            
            # Check if this IP already voted on THIS report
            existing_vote = VoteRecord.objects.filter(report=report, ip_address=ip).first()
            if existing_vote:
                return JsonResponse({'error': 'You have already voted on this report'}, status=403)

            if vote_type == 'up':
                report.ups += 1
            elif vote_type == 'down':
                report.downs += 1
            
            # Save the vote record
            VoteRecord.objects.create(report=report, ip_address=ip, vote_type=vote_type)
            report.save()
            return JsonResponse({'status': 'success', 'ups': report.ups, 'downs': report.downs})
        except ReportedURL.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def remove_vote(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            report_id = data.get('id')
        except json.JSONDecodeError:
            report_id = request.POST.get('id')

        ip = get_client_ip(request)

        try:
            report = ReportedURL.objects.get(id=report_id)
            vote_record = VoteRecord.objects.filter(report=report, ip_address=ip).first()
            
            if not vote_record:
                return JsonResponse({'error': 'You have not voted on this report'}, status=400)

            # Update report counts
            if vote_record.vote_type == 'up':
                report.ups = max(0, report.ups - 1)
            elif vote_record.vote_type == 'down':
                report.downs = max(0, report.downs - 1)
            
            report.save()
            vote_record.delete()
            
            return JsonResponse({'status': 'success', 'ups': report.ups, 'downs': report.downs})
        except ReportedURL.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

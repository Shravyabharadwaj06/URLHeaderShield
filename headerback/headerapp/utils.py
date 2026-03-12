def get_security_headers_config():
    return {
        'X-Frame-Options': {
            'fix': "X-Frame-Options: DENY"
        },
        'Content-Security-Policy': {
            'fix': "Content-Security-Policy: default-src 'self';"
        },
        'Strict-Transport-Security': {
            'fix': "Strict-Transport-Security: max-age=31536000; includeSubDomains"
        },
        'X-Content-Type-Options': {
            'fix': "X-Content-Type-Options: nosniff"
        },
        'Referrer-Policy': {
            'fix': "Referrer-Policy: no-referrer-when-downgrade"
        },
        'X-XSS-Protection': {
            'fix': "X-XSS-Protection: 1; mode=block"
        },
        'Permissions-Policy': {
            'fix': "Permissions-Policy: camera=(), microphone=(), geolocation=()"
        },
        'Cross-Origin-Opener-Policy': {
            'fix': "Cross-Origin-Opener-Policy: same-origin"
        },
        'Cross-Origin-Embedder-Policy': {
            'fix': "Cross-Origin-Embedder-Policy: require-corp"
        },
        'Cross-Origin-Resource-Policy': {
            'fix': "Cross-Origin-Resource-Policy: same-origin"
        }
    }

def analyze_headers(headers):
    config = get_security_headers_config()
    analysis_results = []
    num_headers = len(config)
    points_per_header = 100 / num_headers
    total_score = 0

    for header, info in config.items():
        # Check both original and lowercase
        header_value = headers.get(header) or headers.get(header.lower())
        
        if header_value:
            total_score += points_per_header
            analysis_results.append({
                'header': header,
                'status': 'Present',
                'value': header_value
            })
        else:
            analysis_results.append({
                'header': header,
                'status': 'Missing',
                'suggested_fix': info['fix']
            })
            
    return analysis_results, round(total_score)

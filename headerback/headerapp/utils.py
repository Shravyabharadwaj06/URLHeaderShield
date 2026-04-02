def get_security_headers_config():
    return {
        'X-Frame-Options': {
            'fixes': {
                'raw': "X-Frame-Options: DENY",
                'nginx': "add_header X-Frame-Options \"DENY\" always;",
                'apache': "Header set X-Frame-Options \"DENY\""
            }
        },
        'Content-Security-Policy': {
            'fixes': {
                'raw': "Content-Security-Policy: default-src 'self';",
                'nginx': "add_header Content-Security-Policy \"default-src 'self';\" always;",
                'apache': "Header set Content-Security-Policy \"default-src 'self';\""
            }
        },
        'Strict-Transport-Security': {
            'fixes': {
                'raw': "Strict-Transport-Security: max-age=31536000; includeSubDomains",
                'nginx': "add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains\" always;",
                'apache': "Header set Strict-Transport-Security \"max-age=31536000; includeSubDomains\""
            }
        },
        'X-Content-Type-Options': {
            'fixes': {
                'raw': "X-Content-Type-Options: nosniff",
                'nginx': "add_header X-Content-Type-Options \"nosniff\" always;",
                'apache': "Header set X-Content-Type-Options \"nosniff\""
            }
        },
        'Referrer-Policy': {
            'fixes': {
                'raw': "Referrer-Policy: no-referrer-when-downgrade",
                'nginx': "add_header Referrer-Policy \"no-referrer-when-downgrade\" always;",
                'apache': "Header set Referrer-Policy \"no-referrer-when-downgrade\""
            }
        },
        'X-XSS-Protection': {
            'fixes': {
                'raw': "X-XSS-Protection: 1; mode=block",
                'nginx': "add_header X-XSS-Protection \"1; mode=block\" always;",
                'apache': "Header set X-XSS-Protection \"1; mode=block\""
            }
        },
        'Permissions-Policy': {
            'fixes': {
                'raw': "Permissions-Policy: camera=(), microphone=(), geolocation=()",
                'nginx': "add_header Permissions-Policy \"camera=(), microphone=(), geolocation=()\" always;",
                'apache': "Header set Permissions-Policy \"camera=(), microphone=(), geolocation=()\""
            }
        },
        'Cross-Origin-Opener-Policy': {
            'fixes': {
                'raw': "Cross-Origin-Opener-Policy: same-origin",
                'nginx': "add_header Cross-Origin-Opener-Policy \"same-origin\" always;",
                'apache': "Header set Cross-Origin-Opener-Policy \"same-origin\""
            }
        },
        'Cross-Origin-Embedder-Policy': {
            'fixes': {
                'raw': "Cross-Origin-Embedder-Policy: require-corp",
                'nginx': "add_header Cross-Origin-Embedder-Policy \"require-corp\" always;",
                'apache': "Header set Cross-Origin-Embedder-Policy \"require-corp\""
            }
        },
        'Cross-Origin-Resource-Policy': {
            'fixes': {
                'raw': "Cross-Origin-Resource-Policy: same-origin",
                'nginx': "add_header Cross-Origin-Resource-Policy \"same-origin\" always;",
                'apache': "Header set Cross-Origin-Resource-Policy \"same-origin\""
            }
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
                'suggested_fixes': info['fixes']
            })
            
    return analysis_results, round(total_score)

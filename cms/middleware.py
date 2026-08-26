class SecurityHeadersMiddleware:
    """
    Middleware to inject enterprise-grade security headers requested by
    Burp Suite Vulnerability Scanner & SecurityHeaders.com (A+ Rating).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 1. HTTP Strict Transport Security (HSTS)
        # Instructs browsers to communicate exclusively over HTTPS for 1 year + subdomains
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        # 2. Content-Security-Policy (CSP)
        # Protects against XSS, clickjacking, and unauthorized data injection
        # Allows self, Google Fonts, FontAwesome CDN, and inline styles used by UI
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com",
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com data:",
            "img-src 'self' data: https: http:",
            "connect-src 'self'",
            "frame-ancestors 'self'",
            "form-action 'self'",
            "base-uri 'self'",
            "object-src 'none'",
        ]
        response.headers['Content-Security-Policy'] = "; ".join(csp_directives)

        # 3. Permissions-Policy
        # Restricts sensitive device APIs (geolocation, microphone, camera, etc.)
        permissions_policy = [
            "camera=()",
            "microphone=()",
            "geolocation=()",
            "payment=()",
            "usb=()",
            "screen-wake-lock=()",
            "accelerometer=()",
            "gyroscope=()",
            "magnetometer=()",
        ]
        response.headers['Permissions-Policy'] = ", ".join(permissions_policy)

        # 4. Additional High-Impact Security Headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'

        return response

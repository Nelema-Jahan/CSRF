from flask import Flask, request, render_template_string, session
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Track requests for statistics
request_stats = {'valid': 0, 'invalid': 0}

HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSRF Protection Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar-custom {
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(10px);
        }
        .hero-section {
            text-align: center;
            color: white;
            padding: 40px 0;
        }
        .hero-section h1 {
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .hero-section p {
            font-size: 1.1rem;
            opacity: 0.95;
        }
        .card-demo {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 25px;
        }
        .card-demo:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
        .card-header-custom {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px 15px 0 0 !important;
            padding: 20px;
            border: none;
        }
        .stats-card {
            text-align: center;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stats-number {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 10px 0;
        }
        .stats-label {
            color: #666;
            font-size: 0.95rem;
        }
        .valid-stat { color: #28a745; }
        .invalid-stat { color: #dc3545; }
        .btn-demo {
            padding: 12px 30px;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
            border: none;
        }
        .btn-secure {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }
        .btn-secure:hover {
            background: linear-gradient(135deg, #20c997 0%, #28a745 100%);
            color: white;
            transform: scale(1.05);
        }
        .btn-attack {
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
        }
        .btn-attack:hover {
            background: linear-gradient(135deg, #fd7e14 0%, #dc3545 100%);
            color: white;
            transform: scale(1.05);
        }
        .form-control-custom {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 12px;
            transition: border-color 0.3s ease;
        }
        .form-control-custom:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        .icon-box {
            font-size: 2.5rem;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        .section-title {
            font-weight: 700;
            color: white;
            margin-bottom: 30px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="bi bi-shield-lock"></i> CSRF Security Lab
            </a>
            <span class="navbar-text text-white ms-auto">
                <i class="bi bi-info-circle"></i> Cross-Site Request Forgery Protection Demo
            </span>
        </div>
    </nav>

    <div class="hero-section">
        <div class="container">
            <h1><i class="bi bi-shield-check"></i> CSRF Protection Demonstration</h1>
            <p>Learn how CSRF tokens protect your web applications from unauthorized requests</p>
        </div>
    </div>

    <div class="container py-5">
        <!-- Statistics Section -->
        <div class="row mb-5">
            <div class="col-md-6">
                <div class="stats-card">
                    <i class="bi bi-check-circle valid-stat" style="font-size: 2rem;"></i>
                    <div class="stats-number valid-stat">{{ valid_count }}</div>
                    <div class="stats-label">Valid Requests</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="stats-card">
                    <i class="bi bi-x-circle invalid-stat" style="font-size: 2rem;"></i>
                    <div class="stats-number invalid-stat">{{ invalid_count }}</div>
                    <div class="stats-label">Blocked Requests</div>
                </div>
            </div>
        </div>

        <!-- Demo Section -->
        <h2 class="section-title mb-5">
            <i class="bi bi-play-circle"></i> Try It Now
        </h2>

        <div class="row">
            <!-- Secure Request Demo -->
            <div class="col-lg-6">
                <div class="card card-demo">
                    <div class="card-header-custom">
                        <i class="bi bi-shield-check"></i> Secure Request (WITH Token)
                    </div>
                    <div class="card-body" style="padding: 30px;">
                        <div class="icon-box text-success">
                            <i class="bi bi-check-circle-fill"></i>
                        </div>
                        <h5 class="card-title">Legitimate Request</h5>
                        <p class="card-text text-muted">
                            This form includes a valid CSRF token. The server will accept and process this request.
                        </p>
                        <form method="post" action="/action" class="mt-4">
                            <input type="hidden" name="csrf_token" value="valid_token">
                            <button type="submit" class="btn btn-demo btn-secure w-100">
                                <i class="bi bi-check-lg"></i> Submit Secure Request
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Attack Demo -->
            <div class="col-lg-6">
                <div class="card card-demo">
                    <div class="card-header-custom">
                        <i class="bi bi-shield-x"></i> Attack Request (WITHOUT Token)
                    </div>
                    <div class="card-body" style="padding: 30px;">
                        <div class="icon-box text-danger">
                            <i class="bi bi-exclamation-triangle-fill"></i>
                        </div>
                        <h5 class="card-title">Attack Attempt</h5>
                        <p class="card-text text-muted">
                            This form is missing the CSRF token. The server will reject this request.
                        </p>
                        <form method="post" action="/action" class="mt-4">
                            <input type="hidden" name="csrf_token" value="">
                            <button type="submit" class="btn btn-demo btn-attack w-100">
                                <i class="bi bi-x-lg"></i> Submit Attack Request
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Info Section -->
        <div class="row mt-5">
            <div class="col-lg-12">
                <div class="card card-demo">
                    <div class="card-header-custom">
                        <i class="bi bi-info-circle"></i> How CSRF Protection Works
                    </div>
                    <div class="card-body" style="padding: 30px;">
                        <div class="row">
                            <div class="col-md-6">
                                <h6 class="mb-3"><i class="bi bi-1-circle-fill" style="color: #667eea;"></i> Token Generation</h6>
                                <p class="text-muted">A unique token is generated for each session and embedded in forms.</p>
                            </div>
                            <div class="col-md-6">
                                <h6 class="mb-3"><i class="bi bi-2-circle-fill" style="color: #667eea;"></i> Request Submission</h6>
                                <p class="text-muted">When a form is submitted, the token is sent along with the request.</p>
                            </div>
                            <div class="col-md-6">
                                <h6 class="mb-3"><i class="bi bi-3-circle-fill" style="color: #667eea;"></i> Token Validation</h6>
                                <p class="text-muted">The server verifies that the token matches the expected value.</p>
                            </div>
                            <div class="col-md-6">
                                <h6 class="mb-3"><i class="bi bi-4-circle-fill" style="color: #667eea;"></i> Request Processing</h6>
                                <p class="text-muted">Only valid requests with correct tokens are processed by the server.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="text-center text-white py-4 mt-5" style="background: rgba(0, 0, 0, 0.2);">
        <div class="container">
            <p class="mb-0"><i class="bi bi-github"></i> Software Security Lab | CSRF Protection Demo</p>
            <small>Timestamp: {{ timestamp }}</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Accepted</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .result-card {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            animation: slideIn 0.5s ease;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .success-icon {
            font-size: 80px;
            color: #28a745;
            margin-bottom: 20px;
            animation: bounce 0.6s ease;
        }
        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        .result-title {
            font-size: 2rem;
            font-weight: 700;
            color: #28a745;
            margin-bottom: 10px;
        }
        .result-subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
        }
        .btn-back {
            padding: 12px 40px;
            font-weight: 600;
            border-radius: 8px;
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            text-decoration: none;
            border: none;
            transition: all 0.3s ease;
            display: inline-block;
        }
        .btn-back:hover {
            background: linear-gradient(135deg, #20c997 0%, #28a745 100%);
            color: white;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="result-card">
        <div class="success-icon">
            <i class="bi bi-check-circle-fill"></i>
        </div>
        <div class="result-title">✓ Request Accepted</div>
        <div class="result-subtitle">Valid CSRF Token Detected</div>
        <p class="text-muted mb-4">Your request has been successfully validated and processed by the server.</p>
        <a href="/" class="btn-back"><i class="bi bi-arrow-left"></i> Return to Demo</a>
    </div>
</body>
</html>
"""

ERROR_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Blocked</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .result-card {
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            animation: shake 0.5s ease;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        .error-icon {
            font-size: 80px;
            color: #dc3545;
            margin-bottom: 20px;
        }
        .result-title {
            font-size: 2rem;
            font-weight: 700;
            color: #dc3545;
            margin-bottom: 10px;
        }
        .result-subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 30px;
        }
        .btn-back {
            padding: 12px 40px;
            font-weight: 600;
            border-radius: 8px;
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
            text-decoration: none;
            border: none;
            transition: all 0.3s ease;
            display: inline-block;
        }
        .btn-back:hover {
            background: linear-gradient(135deg, #fd7e14 0%, #dc3545 100%);
            color: white;
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    <div class="result-card">
        <div class="error-icon">
            <i class="bi bi-x-circle-fill"></i>
        </div>
        <div class="result-title">✗ Request Blocked</div>
        <div class="result-subtitle">Invalid CSRF Token</div>
        <p class="text-muted mb-4">Your request was rejected due to an invalid or missing CSRF token. This is a security feature to protect against cross-site request forgery attacks.</p>
        <a href="/" class="btn-back"><i class="bi bi-arrow-left"></i> Return to Demo</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    from datetime import datetime
    return render_template_string(
        HTML_HOME,
        valid_count=request_stats['valid'],
        invalid_count=request_stats['invalid'],
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/action', methods=['POST'])
def action():
    token = request.form.get('csrf_token')

    if token == "valid_token":
        request_stats['valid'] += 1
        return render_template_string(SUCCESS_PAGE)

    request_stats['invalid'] += 1
    return render_template_string(ERROR_PAGE), 403

if __name__ == "__main__":
    app.run(debug=True)
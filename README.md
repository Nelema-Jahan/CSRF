# CSRF Protection Demo 🛡️

A modern, interactive web application demonstrating Cross-Site Request Forgery (CSRF) protection mechanisms. This educational project showcases how tokens can prevent unauthorized requests.

## Features ✨

- **Interactive Demo Interface** - Beautiful gradient UI with real-time interaction
- **Token Validation** - Demonstrates secure vs. insecure request handling
- **Request Statistics** - Live tracking of valid and blocked requests
- **Educational Content** - Step-by-step explanation of CSRF protection
- **Responsive Design** - Works seamlessly on desktop and mobile devices
- **Visual Feedback** - Animated success and error pages

## Tech Stack 🚀

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Styling**: Custom CSS with animations and gradients
- **Security**: CSRF Token Validation

## Installation 📦

1. **Clone or extract the project**
   ```bash
   cd CSRF
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## How It Works 🔐

### CSRF Protection Flow

1. **Token Generation** - A unique token is created for each session
2. **Token Embedding** - The token is included in all forms
3. **Request Submission** - User submits form with the token
4. **Server Validation** - Server verifies token authenticity
5. **Request Processing** - Only valid requests are executed

## Try The Demo 🎮

### Secure Request
- Submit the form with a **valid CSRF token**
- The server accepts and processes the request ✓
- See real-time statistics update

### Attack Request
- Submit the form with an **invalid/missing CSRF token**
- The server rejects the request ✗
- Learn why this protection is critical

## Features Explained 📚

- **Statistics Dashboard** - Track valid and blocked requests in real-time
- **Side-by-side Comparison** - See both secure and attack scenarios
- **Educational Content** - Understand each step of CSRF protection
- **Visual Hierarchy** - Clear, organized interface with intuitive navigation
- **Modern Design** - Gradient backgrounds, smooth animations, and responsive cards

## Security Notes 🔒

This is an educational demo. In production:
- Use framework-provided CSRF protection (Flask-WTF, Django, etc.)
- Store tokens securely in sessions
- Use HTTPOnly and Secure cookies
- Implement SameSite cookie attributes
- Validate tokens server-side on every state-changing request

## Learning Outcomes 🎓

- Understand CSRF attacks and vulnerabilities
- Learn how tokens prevent CSRF attacks
- Implement basic token validation
- Recognize secure vs. insecure request patterns
- Appreciate the importance of security headers

## Project Structure 📁

```
CSRF/
├── app.py          # Flask application with CSRF demo
├── README.md       # This file
└── requirements.txt # Python dependencies (optional)
```

## Browser Compatibility 🌐

- Chrome/Chromium
- Firefox
- Safari
- Edge
- Mobile browsers

## Future Enhancements 🔮

- [ ] SameSite cookie implementation
- [ ] HTTPOnly flag demonstration
- [ ] Multiple attack scenarios
- [ ] Token expiration demo
- [ ] Advanced security headers showcase

## License 📄

Educational use only. For security research and learning purposes.

---


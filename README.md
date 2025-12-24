### Bachelor of Science in Computer Science (Dec 2024)

Please check out my [portfolio](https://matthew-pool.github.io) for a more streamlined and interactive experience and to check out my new app "Flick".


# Matthew Pool - Portfolio Website

A modern, interactive portfolio website showcasing software development projects and technical expertise across mobile, web, and data science domains.

![Portfolio Banner](assets/images/flick/banner.png)

## 🌟 Live Demo

Visit the live portfolio: [matthew-pool.github.io](https://matthew-pool.github.io)

## 📋 Overview

This portfolio website features a clean, professional design with three main sections:

- **Home**: Showcases Flick, a vertical video streaming Android app with intelligent recommendation algorithms
- **Projects**: Displays a diverse collection of software development projects spanning multiple technologies
- **Refactor**: Demonstrates software engineering skills through program enhancement and optimization

## ✨ Key Features

### Interactive Elements
- **Animated Bird**: A delightful cardinal animation that flies from the navigation to introduce featured projects
- **Dark Mode Toggle**: Smooth theme switching with shimmer animation and persistent preference storage
- **Responsive Design**: Fully optimized for desktop, tablet, and mobile viewing
- **Tab Navigation**: Sticky tab bar for seamless content exploration

### Portfolio Highlights
- Comprehensive project documentation with screenshots and demos
- Live project links and GitHub repository access
- Detailed technical stack breakdowns
- CI/CD pipeline demonstrations
- Interactive external projects (The Existence Paradox)

## 🛠️ Technologies Used

### Frontend
- **HTML5**: Semantic markup and accessibility
- **CSS3**: Custom animations, gradients, flexbox, and grid layouts
- **JavaScript (ES6+)**: Interactive features and smooth animations
- **LocalStorage**: Theme preference persistence

### Design Features
- Custom glassmorphism effects
- Gradient animations with glow effects
- ANSI-inspired metallic UI elements
- Responsive image galleries
- Embedded video content

### Projects Showcased
- **Mobile**: Kotlin, Android SDK, Jetpack Compose, MVVM Architecture
- **Web**: TypeScript, React, Angular, Node.js, Express, HTML/CSS
- **Backend**: Python, Java, MongoDB, MySQL, Firebase
- **Graphics**: C++, OpenGL, GLSL, GLFW
- **Data Science**: Python, Pandas, NumPy, Matplotlib, Machine Learning

## 📁 Project Structure

```
matthew-pool.github.io/
├── aac-dashboard/          # Python/MongoDB dashboard for Austin Animal Center
├── assets/                 # Project screenshots, images, and PDF documentation
├── data-analysis/          # Python data analysis and machine learning projects
├── existence-paradox/      # TypeScript/React philosophical exploration app
├── inventory-buddy/        # Android inventory management demo app
├── java-enhancements/      # Refactored Java rescue animal tracking system
├── super-mario-bros/       # C++ OpenGL recreation of classic Nintendo scene
├── travel-web-app/         # MEAN stack travel website with admin SPA
├── index.html              # Main portfolio webpage
├── script.js               # Interactive animations and bird flight logic
├── styles.css              # Responsive styling with dark mode support
└── README.md               # This file
```

## 🚀 Getting Started

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/matthew-pool/matthew-pool.github.io.git
   cd matthew-pool.github.io
   ```

2. **Open in browser**
   - Simply open `index.html` in your web browser
   - Or use a local server for best results:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx http-server
   ```

3. **View the site**
   - Navigate to `http://localhost:8000` in your browser

### Deployment

This site is designed for GitHub Pages deployment:

1. Push to the `main` branch
2. Enable GitHub Pages in repository settings
3. Select `main` branch as source
4. Site will be live at `https://matthew-pool.github.io`

## 🎨 Customization

### Changing Theme Colors

Edit the gradient colors in `styles.css`:

```css
.contact-card {
    background: linear-gradient(135deg, #667eea, #764ba2, #f093fb, #4facfe, #667eea);
}
```

### Modifying the Bird Animation

Adjust bird flight parameters in `script.js`:

```javascript
const duration = 2500; // Flight duration in milliseconds
endTop = flickRect.top + window.scrollY - 43; // Landing position
```

### Dark Mode Colors

Update dark mode styles in `styles.css`:

```css
body.dark-mode {
    background-color: #1a1a1a;
    color: #e0e0e0;
}
```

## 📱 Featured Project: Flick

**Flick** is a vertical video streaming Android app featuring:
- Intelligent recommendation engine using cosine similarity
- Archive.org integration for vintage content
- Firebase Firestore backend
- Smooth video prebuffering
- Interactive gestures and visual feedback
- Comprehensive test coverage with JUnit and Espresso

[Try Flick on Google Play Test Track](https://groups.google.com/g/appbuddy-flick)

## 🤝 Contributing

While this is a personal portfolio, suggestions and feedback are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/suggestion`)
3. Commit your changes (`git commit -m 'Add suggestion'`)
4. Push to the branch (`git push origin feature/suggestion`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

**Matthew Pool**
- Email: mathyou.me@gmail.com
- Portfolio: [matthew-pool.github.io](https://matthew-pool.github.io)

## 🙏 Acknowledgments

- Inspired by modern web design trends
- Cardinal bird animation created with SVG
- Google Play badge from Google Brand Resources
- Font: Roboto from Google Fonts

---

**Note**: This portfolio showcases real projects developed during my Computer Science degree program and personal development journey. Each project demonstrates specific technical skills and problem-solving abilities. Feel free to explore the individual project repositories for detailed documentation and source code.

*Made with ❤️ by Matthew Pool*

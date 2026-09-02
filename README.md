# Matthew Pool - Portfolio Website

![B.S. Computer Science](https://img.shields.io/badge/B.S._Computer_Science-005A9C?style=for-the-badge&logo=googlescholar&logoColor=white)
![Summa Cum Laude](https://img.shields.io/badge/Summa_Cum_Laude-FFD700?style=for-the-badge&logo=googlescholar&logoColor=black)
![WCAG 2.2 AA](https://img.shields.io/badge/WCAG_2.2_AA-005A9C?style=for-the-badge&logo=w3c&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

A modern, interactive portfolio website showcasing my work as a Software Engineer & Technical Solutions Specialist, highlighting technical expertise across B2B/B2C mobile, web, systems, and data science domains.

## 🌟 Portfolio

Visit my portfolio website for a more streamlined experience and a deeper dive into my projects: [matthew-pool.github.io](https://matthew-pool.github.io)

## 📋 Overview

This portfolio website features a clean, professional design that reflects my academic foundation and professional journey. Building on an Associate of Arts with an information technology focus from Tyler Junior College, I graduated Summa Cum Laude with a Bachelor of Science in Computer Science from Southern New Hampshire University, achieving a 3.99 GPA with an official degree conferral date of January 1, 2025.

The work showcased here stems from rigorous academic study and my independent software development venture, **App.Buddy** (established January 2025). The site is divided into three main sections:

*   **Home**: Showcases featured applications, contact information, and an overview narrative detailing my complete product lifecycle management.
*   **Projects**: Displays a diverse, filterable collection of software development projects spanning Web, Graphics & Games, UI/UX Design, Data & ML, and Systems.
*   **Legacy Refactor**: Demonstrates software engineering skills through the modernization of a legacy Java command-line rescue animal tracking system utilizing Maven, JUnit, MapDB, and optimized time-complexity algorithms.

## ✨ Key Features & Architecture

*   **Zero Dependencies**: Built entirely from scratch without any frontend framework—utilizing pure HTML5, CSS3, and Vanilla JavaScript for maximum performance and maintainability.
*   **Animated SVG Bird**: A custom animated cardinal perches on the shelf and flies to the Flick logo on scroll, using a cubic Bézier curve path calculated in JS via `requestAnimationFrame`.
*   **Design System & Accessibility**: Fully themeable light and dark mode using CSS custom properties with preferences persisted in `localStorage`. The site enforces strict semantic HTML, ARIA roles, and keyboard-navigable interactive elements to ensure WCAG 2.2 AA compliance.
*   **Custom Components**: Engineered a custom project-detail modal popup system and a full lightbox image viewer with keyboard navigation.
*   **CI/CD Pipeline**: Deployed automatically to GitHub Pages via GitHub Actions on every push to `main`.

## 🚀 Featured Projects & Portfolio Highlights

Below is a comprehensive list of the major projects and disciplines featured on the portfolio:

### Mobile & Web Engineering
*   **(This) Portfolio**: A fully hand-coded, zero-dependency responsive portfolio featuring persistent themes and JS-driven SVG animations.
*   **Flick**: A native Android vertical video streaming app featuring a custom Machine Learning recommendation engine (using cosine similarity), MVVM architecture, and Archive.org API integration.
*   **The Existence Paradox**: A high-fidelity interactive SPA built with React, TypeScript, Tailwind CSS, and Vite, featuring complex state hooks and decision-tree navigation.
*   **Full-Stack Travel Platform**: A dual-interface web app featuring a cloud-secured admin SPA, RESTful APIs via LoopBack, and a database migration to AWS DynamoDB orchestrated via Docker.
*   **InventoryBuddy**: An Android inventory management application featuring an SMS notification system for low-stock alerts and local SQLite data persistence.

### Graphics, Games & Level Design
*   **Super Mario Maker ("The Greatest Players of All Time")**: An elite level design achievement securing an All-Time #39 Global and #6 Regional ranking under the alias "CheezSauce". The profile amassed over 164,851 stars, with this specific breakout hit earning 133,630 stars and a feature on the Nintendo Thumb YouTube channel.
*   **Wormhole**: A terminal-based sci-fi text adventure game built with a custom Python OOP engine, featuring multithreading for asynchronous UI updates and event-driven state management.
*   **Super Mario Bros. Recreation**: A classic Nintendo scene recreated using C++, custom OpenGL shaders, GLM, and hand-coded 3D meshes utilizing a Phong lighting model.

### Data Science, Machine Learning & Analytics
*   **Machine Learning**: Explored neural networks, developing a Deep Q-Learning Network (DQN) for pathfinding optimization, a Convolutional Neural Network (CNN) for image recognition, and a Markov Decision Process (MDP).
*   **Austin Animal Center Dashboard**: An interactive data dashboard built with Python, MongoDB, Dash, and Pandas to visualize and analyze shelter data with geolocation mapping.
*   **Statistical & Data Analysis**: Conducted regression modeling on NBA Elo data using Python and SciPy, analyzed NASA climate data utilizing Pandas and Matplotlib, and visualized historical economic indicators.

### Systems, Security & Software Architecture
*   **Financial Security Audit & Remediation**: Conducted vulnerability assessments using OWASP ZAP and refactored a Java Spring Boot API to implement AES-256 encryption and SHA-256 hashing.
*   **System Design & UML**: Authored comprehensive System Design Documents (SDD) mapping out UML activity and sequence diagrams.
*   **Algorithmic Optimization**: Implemented a manual, recursive Merge Sort in C++ to optimize sorting performance from $O(n^2)$ to $O(n \log n)$.
*   **Unit Testing**: Engineered a defensive JUnit 5 test suite in Java utilizing Test-Driven Development (TDD) principles to achieve 100% code coverage.
*   **Database Case Study**: Performed MySQL database administration and Entity Relationship Diagram (ERD) design.
*   **Agile & Scrum Leadership**: Acted as Scrum Master, utilizing Jira for backlog refinement, tracking sprint velocity, and managing SDLC transitions.
*   **Product Design (UI/UX)**: Designed cross-platform low-fidelity wireframes and high-fidelity mockups for "Eat Right!" and "Kiva MoneyMobile", backed by user interviews and personas.

## 📁 Project Structure

```text
matthew-pool.github.io/
├─ aac-dashboard/            # Python/MongoDB dashboard for Austin Animal Center
├─ agile-scrum/              # Agile methodology documentation and project artifacts
├─ algorithmic-optimization/ # Data structures and algorithm performance tuning
├─ assets/                   # Project screenshots, images, and PDF documentation
├─ data-analysis/            # Python data analysis of global temperature deviations
├─ database-administration/  # MySQL database administration, data analysis, and ERD design
├─ economic-analysis/        # Data analysis and modeling of economic indicators
├─ existence-paradox/        # TypeScript/React philosophical exploration app
├─ inventory-buddy/          # Android inventory management demo app
├─ java-refactor/            # Refactored Java rescue animal tracking system
├─ machine-learning/         # ML model training, testing, and analyses
├─ product-design/           # UI/UX designs and architectural specifications
├─ service-tests/            # Automated software testing and quality assurance suites
├─ software-security/        # Java REST API security audit and encryption implementation
├─ statistical-analysis/     # Regression modeling to predict regular-season wins
├─ super-mario-bros/         # C++ OpenGL recreation of classic Nintendo scene
├─ travel-web-app/           # MEAN stack travel booking website with admin SPA
├─ index.html                # Main portfolio webpage
├─ script.js                 # Interactive animations, modals, and bird flight logic
├─ styles.css                # Responsive styling with light/dark mode variables
└─ README.md                 # This file
```

## Copyright & License

© 2026 Matthew Pool. All Rights Reserved.

This repository and its contents are provided for portfolio viewing and employment evaluation purposes only. The code, design, and assets (including all App.Buddy branding and project materials) may not be copied, cloned, or reused without express written permission.
# The Existence Paradox

*An interactive philosophical & scientific exploration of why the universe exists at all.*

![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwindcss&logoColor=white)

## Overview

**The Existence Paradox** is a single-page web app built around one of the oldest questions in philosophy and cosmology: *why is there something rather than nothing?*

Instead of arguing for a single answer, the app treats the question as genuinely unresolved. Visitors stake out a starting position, work through the strongest arguments and counterarguments for each major possibility, and land on a personalized reflection — with the option to change their mind along the way. It's built to be intellectually rigorous without taking itself too seriously; the closing screen even admits, "it sure is fun to think about."

## The Experience

The app moves through three screens, all driven by a single component's internal state — no routing required.

**1. The Question** — Visitors choose a starting position on how the universe came to be: *Created* (by a deity or other cause), *Infinite Past* (no beginning), *Finite Past* (began without a cause), *Something Else*, or *No One Knows*. Each option carries its own accent color that follows through to the results screen.

**2. The Arguments** — A 13-step guided walkthrough with a progress bar and Previous/Continue navigation:
- **Created Universe** runs into the *Creator Regress Problem* — what created the creator? — countered by the classical "necessary being outside time" argument.
- **Infinite Past** runs into the *Infinite Traversal Problem* — how could an infinite stretch of time ever be crossed to reach today? — countered by how mathematicians actually define infinity.
- **Finite Past Without Cause** runs into the *"From Nothing" Problem*, countered by quantum vacuum fluctuations and zero-point energy.
- **The Singularity and Modern Physics** grounds the discussion in the Big Bang and General Relativity.
- A **Process of Elimination** checkpoint asks visitors, directly, whether they accept that none of the three possibilities can be definitively proven or ruled out — yes, no, or unsure, with no wrong answer.
- Closing reflections cover the **Necessity of Existence**, **Alternative Possibilities** (cyclic universes, the multiverse, simulation theory, mathematical platonism, and more), **The Software Analogy** (comparing perceived reality to a UI abstraction layered over a deeper quantum "hardware"), **The Limits of Understanding**, and a **Final Reflection** on why the question resists a clean answer.

**3. The Results** — A personalized takeaway based on the visitor's original answer ("What this means" and "Deeper insight"), followed by a closing reflection and the choice to keep their answer, change it, or admit they're still thinking — before starting over.

## Features

- Fully interactive, branching experience managed entirely in React state
- 13-step argument sequence, each claim paired with a counterpoint where one exists, for critical engagement rather than a one-sided case
- Answer-aware results screen with unique explanation/insight copy for all five starting positions
- Progress bar and step counter through the argument sequence
- Smooth-scroll transitions on selection and screen changes
- Reset flow to revisit the experience from a different starting position
- Fully self-contained dark, cosmic-themed visual design

## Tech Stack

- **React** + **TypeScript**
- **Vite** — build tooling and dev server
- **Tailwind CSS** — project-level styling foundation
- **lucide-react** — icons (`ChevronRight`, `RotateCcw`, `ArrowLeft`)
- **Google Fonts** — Cormorant Garamond (serif, headings & quotes) and Jost (sans-serif, UI text)

> **Note:** The `ExistenceParadox` component ships with its own scoped CSS, injected via a `<style>` tag using custom properties and classes (prefixed `ep-`), rather than Tailwind utility classes. This keeps the component fully self-contained and portable, independent of the app's global Tailwind setup.

## Getting Started

### Prerequisites
- Node.js 18+
- npm (or yarn / pnpm)

### Installation
```bash
git clone <your-repo-url>
cd existence-paradox
npm install
```

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
npm run preview
```

## Project Structure

A standard Vite + React + TypeScript layout — adjust to match your actual repo:

```
existence-paradox/
├── src/
│   ├── components/
│   │   └── ExistenceParadox.tsx   # Question, argument, and results screens
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── tailwind.config.js
├── vite.config.ts
└── package.json
```

## Design Notes

- **Palette:** near-black background (`#070711`) with soft violet/blue nebula gradients
- **Typography:** Cormorant Garamond for the italicized central question and reflective copy, Jost for labels, options, and navigation
- **Color coding:** each of the five starting positions carries its own accent color (violet, blue, green, orange, pink) through to its results screen

## Author

Built by Matt — [matthew-pool.github.io](https://matthew-pool.github.io)

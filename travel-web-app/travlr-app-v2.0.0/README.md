# README: Full-Stack Travel Platform (v2)

## Table of Contents
- [Architecture](#architecture)
- [Functionality](#functionality)
- [Testing](#testing)
- [Reflection](#reflection)

## Architecture

**Introduction**
The admin site for the travel platform consists of a client-based single-page application (SPA) web page that uses [Bootstrap CSS](https://getbootstrap.com/) and [Angular](https://angular.dev/) to provide reusable UI components and presentation logic. For version 2, the backend architecture was heavily modernized to improve scalability, developer experience, and deployment consistency.

**Frontend: Angular SPA**
The Angular-based admin-facing website utilizes a modular architecture containing routes, modules, services, and components. Components consist of HTML, CSS, and [TypeScript](https://www.typescriptlang.org/). TypeScript acts as a JavaScript superset that enforces strict type safety, catching data type errors at compile time and making the frontend codebase highly maintainable. 

**Backend: LoopBack API Framework**

Moving away from standard Express.js routing, this version implements the [LoopBack](https://loopback.io/) API framework. LoopBack allows for the rapid generation of RESTful APIs with minimal boilerplate. It separates the business logic from the routing layer and provides built-in API exploration tools (like Swagger UI), making the backend highly structured and easier to consume from the Angular client.

**Database: AWS DynamoDB**

The data layer was migrated from MongoDB to [AWS DynamoDB](https://aws.amazon.com/dynamodb/). DynamoDB is a fully managed, serverless, NoSQL database designed to run high-performance applications at any scale. This shift provides single-digit millisecond performance and horizontal scalability, handling the app's CRUD (Create, Read, Update, Delete) operations with high efficiency and reduced manual database administration.

**Infrastructure: Docker Containerization**
To eliminate the "it works on my machine" problem, the application environment is orchestrated using [Docker](https://www.docker.com/). Containerizing the application ensures that the Angular frontend, the LoopBack backend, and any local database emulation run consistently across all development, testing, and production environments.

## Functionality

**JSON & Data Interchange**
[JSON](https://en.wikipedia.org/wiki/JSON) (JavaScript Object Notation) remains the primary data interchange format between the LoopBack backend and the Angular frontend. JSON’s lightweight, language-independent structure uses key-value pairs to transmit data efficiently. The user’s web browser sends secure HTTP requests to the server, and the state is managed seamlessly via stateless, scalable REST APIs.

**Component Modularization & Clean Architecture**
Refactorization and modularization were central to the v2 development process. On the frontend, Angular’s component-based structure ensures that repetitive UI elements (like headers, footers, and travel cards) are built once and reused. On the backend, LoopBack enforces a clean separation of concerns, ensuring that models, controllers, and data sources are isolated. This modularity prevents code duplication and makes future feature integrations significantly faster.

## Testing

**API Testing with Postman**
Methods for request and retrieval require comprehensive testing of the new LoopBack endpoints. [Postman](https://www.postman.com/) is utilized to assess the RESTful APIs using HTTP methods like POST, GET, PUT, and DELETE. By submitting requests to the LoopBack server, we can verify status codes, validate the JSON payloads interacting with DynamoDB, and measure response times.

**Testing & Security Best Practices**
Security remains a top priority. The API layer relies on secure token-based authentication ([JWT](https://jwt.io/)) to ensure only authorized users access administrative endpoints. Data at rest and in transit are protected using modern hashing algorithms and [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) encryption for network connections. Transitioning to AWS also allows us to leverage enterprise-grade security configurations. We continuously test for common vulnerabilities outlined by [OWASP](https://owasp.org/) (such as broken access controls and injection risks) to maintain robust application security.

## Reflection

Developing version 2 of this platform answered a lot of advanced questions regarding full-stack software architecture and infrastructure. Migrating the backend to the LoopBack API framework and AWS DynamoDB provided hands-on experience in scaling cloud-native databases and structuring RESTful APIs efficiently. Furthermore, orchestrating the environment with Docker containerization reinforced the importance of modern DevOps practices in the software development lifecycle. It has been incredibly satisfying to see this application evolve from its initial foundation into a robust, containerized, and scalable product. Keep coding!

Matthew Pool
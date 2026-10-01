import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.interview import JobRole, InterviewCategory, DifficultyLevel, Question

QUESTIONS_DATA = [
    # ==================== FRONTEND DEVELOPER ====================
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between let, const, and var in modern JavaScript?",
        "keywords": ["scope", "block scope", "hoisting", "temporal dead zone", "reassignment", "mutable"],
        "sample": "var is function-scoped and hoisted with undefined value. let and const are block-scoped and live in a temporal dead zone prior to declaration. const prevents variable re-assignment, while let permits reassignment."
    },
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Beginner",
        "text": "Explain the CSS Box Model and how box-sizing: border-box changes it.",
        "keywords": ["content", "padding", "border", "margin", "box-sizing", "border-box", "width"],
        "sample": "The CSS Box Model consists of content, padding, border, and margin. By default (content-box), width specifies content only. With border-box, padding and border are included within the specified element width."
    },
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How does React's Virtual DOM work, and how does reconciliation optimize rendering?",
        "keywords": ["virtual dom", "reconciliation", "diffing algorithm", "keys", "rerender", "fiber"],
        "sample": "React maintains a lightweight in-memory representation of the DOM. When state changes, a new tree is created and compared with the previous snapshot using a heuristic O(n) diffing algorithm. Only mutated DOM nodes are updated in the real browser DOM."
    },
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "What are React Hooks and what rules must be followed when using them?",
        "keywords": ["hooks", "useState", "useEffect", "top level", "call order", "custom hooks"],
        "sample": "Hooks allow functional components to use state and lifecycle methods. Key rules: call hooks only at the top level (never in loops or conditions) and call them only from React functional components or custom hooks."
    },
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you optimize Core Web Vitals (LCP, FID/INP, and CLS) in a high-traffic React application?",
        "keywords": ["core web vitals", "lcp", "inp", "cls", "code splitting", "lazy loading", "ssr", "image optimization", "cdn"],
        "sample": "To optimize LCP, optimize critical rendering path, use SSR/SSG, preload hero images, and cache via CDN. For INP, minimize long tasks by offloading CPU-heavy work to web workers and debouncing. For CLS, assign explicit dimensions to media and avoid inserting dynamic content above the fold."
    },
    {
        "role": "Frontend Developer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a situation where a designer provided an impractical UI mock. How did you resolve it?",
        "keywords": ["designer", "collaboration", "compromise", "technical constraint", "accessibility", "alternative"],
        "sample": "I scheduled an interactive walk-through with the UI designer, explained the mobile viewport and accessibility performance constraints, and proposed an alternative interactive pattern that preserved the design essence while maintaining 60fps responsiveness."
    },
    {
        "role": "Frontend Developer", "cat": "HR", "diff": "Beginner",
        "text": "Why do you want to specialize in Frontend Development rather than Backend?",
        "keywords": ["passion", "visual impact", "user experience", "immediate feedback", "empathy", "frontend"],
        "sample": "I am passionate about creating accessible, intuitive user experiences where code immediately translates to user empowerment. The intersection of design precision, engineering rigor, and instant user impact drives my focus."
    },
    {
        "role": "Frontend Developer", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you handle cross-browser compatibility and responsive design across varying mobile devices?",
        "keywords": ["media queries", "css grid", "flexbox", "can i use", "autoprefixer", "testing", "browserstack"],
        "sample": "I follow mobile-first responsive principles using CSS Flexbox and Grid, run automated viewport tests across WebKit and Chromium engines, and utilize PostCSS autoprefixer alongside feature queries like @supports."
    },
    {
        "role": "Frontend Developer", "cat": "Technical", "diff": "Advanced",
        "text": "Explain State Management strategies in large React applications. When would you choose Zustand over Redux Toolkit or Context API?",
        "keywords": ["state management", "zustand", "redux", "context api", "re-renders", "boilerplate", "selectors"],
        "sample": "Context API is suitable for low-frequency global values like theme or auth. Redux Toolkit provides strict predictability for immense teams. Zustand offers minimal boilerplate, excellent selector-based render optimization without provider wrapping, and zero technical debt for fast-scaling apps."
    },
    {
        "role": "Frontend Developer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time you had to refactor a legacy frontend codebase with no automated tests.",
        "keywords": ["refactoring", "legacy code", "regression", "end-to-end testing", "incremental", "cypress"],
        "sample": "I first established a safety net by authoring high-level integration/E2E tests with Playwright. Then I broke monolithic components into decoupled dumb UI and smart hooks incrementally without disrupting production delivery."
    },
    {
        "role": "Frontend Developer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you stay up-to-date with rapidly evolving web standards and frameworks?",
        "keywords": ["continuous learning", "w3c", "tc39", "blogs", "github", "open source", "podcasts"],
        "sample": "I follow TC39 stage proposals, Chrome DevRel updates, read GitHub release notes, and build weekend experiments with newly standardized CSS/JS features to evaluate real-world developer experience."
    },

    # ==================== BACKEND DEVELOPER ====================
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Beginner",
        "text": "Explain the difference between synchronous and asynchronous programming in Python or Node.js.",
        "keywords": ["synchronous", "asynchronous", "blocking", "event loop", "asyncio", "concurrency", "await"],
        "sample": "Synchronous code blocks thread execution until an operation finishes. Asynchronous code registers callbacks or promises with an event loop, allowing the runtime to handle other I/O tasks while awaiting network or disk responses."
    },
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Beginner",
        "text": "What are RESTful API constraints and standard HTTP methods?",
        "keywords": ["rest", "stateless", "client-server", "cacheable", "get", "post", "put", "delete", "status codes"],
        "sample": "REST relies on statelessness, uniform interface, client-server separation, and cacheability. Standard verbs include GET for retrieval, POST for creation, PUT/PATCH for mutation, and DELETE for removal, mapped to standard status codes."
    },
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do database indexes work, and what are the trade-offs of adding too many indexes?",
        "keywords": ["b-tree", "index", "lookup", "write overhead", "storage", "query planner", "composite index"],
        "sample": "Indexes build B-tree data structures allowing O(log N) lookups instead of full table scans. The trade-off is increased disk space and slower INSERT/UPDATE/DELETE queries, because each index must be recomputed on write."
    },
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you implement secure authentication using JWT with Access and Refresh tokens?",
        "keywords": ["jwt", "access token", "refresh token", "rotation", "expiry", "http-only", "signature", "revocation"],
        "sample": "The client receives a short-lived access token and a long-lived refresh token. On expiry, the client hits a refresh endpoint where the refresh token is verified, checked against a revocation database, and rotated."
    },
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Advanced",
        "text": "How would you design a distributed rate limiter that handles 100,000 requests per second across multiple API instances?",
        "keywords": ["redis", "token bucket", "sliding window", "distributed", "concurrency", "lua scripts", "rate limit"],
        "sample": "I would implement a sliding window log or token bucket algorithm in Redis using atomic Lua scripts. Using Redis clusters ensures sub-millisecond execution and horizontal scalability across all load-balanced application instances."
    },
    {
        "role": "Backend Developer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a production outage or critical bug you caused or resolved. What was your mitigation process?",
        "keywords": ["incident response", "post-mortem", "root cause", "monitoring", "rollback", "fix"],
        "sample": "A database connection leak during high traffic exhausted the pool. I rolled back the bad migration immediately to restore service, diagnosed the unclosed connection context, added automated connection pool metrics, and documented a post-mortem."
    },
    {
        "role": "Backend Developer", "cat": "HR", "diff": "Beginner",
        "text": "What appeals to you most about backend engineering and systems programming?",
        "keywords": ["architecture", "data integrity", "scalability", "algorithms", "performance", "backend"],
        "sample": "I appreciate the foundational nature of backend systems: ensuring high availability, bulletproof security, clean data architecture, and designing scalable APIs that support diverse clients reliably."
    },
    {
        "role": "Backend Developer", "cat": "Mixed", "diff": "Intermediate",
        "text": "When would you choose a NoSQL database (like MongoDB or Redis) over a Relational database (like PostgreSQL)?",
        "keywords": ["acid", "schema", "relational", "nosql", "scalability", "unstructured", "caching", "foreign keys"],
        "sample": "PostgreSQL is preferred for structured relational data demanding ACID transactions and complex joins. NoSQL like MongoDB fits evolving document models, while Redis is chosen for high-throughput, low-latency in-memory caching."
    },
    {
        "role": "Backend Developer", "cat": "Technical", "diff": "Advanced",
        "text": "Explain database transaction isolation levels and phenomena like Dirty Reads and Phantom Reads.",
        "keywords": ["acid", "isolation levels", "read uncommitted", "read committed", "repeatable read", "serializable", "mvcc"],
        "sample": "Isolation levels manage concurrent anomalies. Read Uncommitted allows dirty reads; Read Committed avoids dirty reads; Repeatable Read prevents non-repeatable reads; Serializable prevents phantom reads using MVCC or range locks."
    },
    {
        "role": "Backend Developer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time you had to push back on a product requirement due to technical debt or scalability concerns.",
        "keywords": ["pushback", "technical debt", "product manager", "compromise", "data-driven", "sla"],
        "sample": "Product requested real-time aggregate reports on millions of records without caching. I demonstrated benchmark data showing database CPU saturation, then designed an asynchronous event-driven materialized view that satisfied product needs while safeguarding DB SLAs."
    },
    {
        "role": "Backend Developer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you approach writing documentation for internal and public-facing APIs?",
        "keywords": ["openapi", "swagger", "examples", "clarity", "developer experience", "documentation"],
        "sample": "I leverage OpenAPI/Swagger annotations directly from code schemas to guarantee docs never drift. I supplement this with real-world authentication tutorials, error codes, and copy-pasteable curl examples."
    },

    # ==================== FULL STACK DEVELOPER ====================
    {
        "role": "Full Stack Developer", "cat": "Technical", "diff": "Beginner",
        "text": "How does client-server communication work from the browser clicking Submit to the database saving data?",
        "keywords": ["http request", "dns", "tcp handshake", "fastapi", "orm", "database transaction", "json response"],
        "sample": "The browser triggers an HTTP POST request. DNS resolves the host, establishing a TCP/TLS connection. The backend router deserializes and validates the payload, executes business logic, persists records via ORM transactions, and returns a JSON response."
    },
    {
        "role": "Full Stack Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you prevent common web vulnerabilities like XSS, CSRF, and SQL Injection in a full-stack stack?",
        "keywords": ["xss", "csrf", "sql injection", "cors", "parameterized queries", "content security policy", "sanitization"],
        "sample": "Use parameterized ORM queries to eliminate SQL injection. Use modern UI frameworks (React) that auto-escape strings, alongside strict Content Security Policy for XSS. For CSRF, utilize SameSite cookies or anti-CSRF bearer tokens."
    },
    {
        "role": "Full Stack Developer", "cat": "Technical", "diff": "Advanced",
        "text": "Design an end-to-end real-time notification system supporting millions of concurrent connected users.",
        "keywords": ["websockets", "sse", "redis pub/sub", "load balancer", "connection pooling", "horizontal scaling"],
        "sample": "Clients establish authenticated WebSocket or SSE connections terminated at an edge gateway. Multiple backend instances communicate via Redis Pub/Sub channels to broadcast targeted user messages across nodes efficiently."
    },
    {
        "role": "Full Stack Developer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "How do you prioritize your time when you have both frontend bugs and backend performance issues during a sprint?",
        "keywords": ["prioritization", "impact analysis", "triage", "communication", "blocker", "severity"],
        "sample": "I triage based on severity and user impact. If a backend issue threatens data integrity or blocks entire user workflows, it takes precedence. I communicate adjusted timelines transparently with stakeholders."
    },
    {
        "role": "Full Stack Developer", "cat": "HR", "diff": "Intermediate",
        "text": "What do you enjoy about working across the full stack rather than specializing in one domain?",
        "keywords": ["big picture", "versatility", "ownership", "end to end", "seamless integration", "full stack"],
        "sample": "Being full-stack gives me end-to-end ownership. I understand how frontend data requirements influence database design and how backend API contracts shape user interface responsiveness."
    },
    {
        "role": "Full Stack Developer", "cat": "Mixed", "diff": "Advanced",
        "text": "Explain how you would migrate a monolith application into modular microservices with minimal downtime.",
        "keywords": ["strangler fig pattern", "migration", "database decoupling", "api gateway", "downtime", "canary"],
        "sample": "I apply the Strangler Fig pattern: introduce an API Gateway in front of the monolith, extract one bounded context into a microservice with its own database, route traffic via canary deployments, and iterate until the monolith is retired."
    },
    {
        "role": "Full Stack Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you manage database migrations across team members and automated CI/CD deployment pipelines?",
        "keywords": ["alembic", "migrations", "ci/cd", "backward compatibility", "zero downtime", "schema"],
        "sample": "We version control migration scripts using Alembic. In CI/CD, migrations run before application deployment, following expand-and-contract patterns so that old and new code versions can run simultaneously."
    },
    {
        "role": "Full Stack Developer", "cat": "Behavioral", "diff": "Beginner",
        "text": "Tell me about a feature you built from scratch from user story to production release.",
        "keywords": ["user story", "design", "implementation", "testing", "ci/cd", "monitoring", "feedback"],
        "sample": "I designed and deployed an automated invoice export system. I mapped DB schemas, wrote FastAPI export endpoints with streaming responses, built a React download drawer with progress toasts, and verified with automated integration tests."
    },
    {
        "role": "Full Stack Developer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you optimize an application that is experiencing both slow frontend rendering and slow backend database queries?",
        "keywords": ["profiling", "chrome devtools", "query explain", "indexing", "memoization", "caching", "virtualization"],
        "sample": "Profile the full request lifecycle. For backend, analyze slow queries using EXPLAIN ANALYZE, add appropriate indexes, and cache hot data in Redis. For frontend, use React DevTools Profiler to eliminate unnecessary re-renders and virtualize long lists."
    },
    {
        "role": "Full Stack Developer", "cat": "HR", "diff": "Advanced",
        "text": "How do you mentor junior developers across both frontend and backend concepts?",
        "keywords": ["mentorship", "code reviews", "pair programming", "documentation", "empathy", "growth"],
        "sample": "I focus on pair programming and constructive code reviews where I explain the 'why' behind architectural choices, encouraging junior engineers to reason through system trade-offs."
    },

    # ==================== SOFTWARE ENGINEER ====================
    {
        "role": "Software Engineer", "cat": "Technical", "diff": "Beginner",
        "text": "Explain the four core principles of Object-Oriented Programming (OOP) with examples.",
        "keywords": ["encapsulation", "abstraction", "inheritance", "polymorphism", "oop", "classes"],
        "sample": "Encapsulation bundles data and methods while hiding internal state. Abstraction presents a simplified interface. Inheritance allows subclasses to reuse logic. Polymorphism enables uniform interfaces across varying types."
    },
    {
        "role": "Software Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain SOLID design principles and why they matter in maintainable software systems.",
        "keywords": ["solid", "single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion"],
        "sample": "SOLID stands for Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion. They prevent tight coupling, making software extensible, testable, and resilient to refactoring."
    },
    {
        "role": "Software Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "What is the time and space complexity of common sorting algorithms (QuickSort, MergeSort, HeapSort)?",
        "keywords": ["big o", "quicksort", "mergesort", "heapsort", "time complexity", "space complexity", "stability"],
        "sample": "MergeSort is O(N log N) in all cases with O(N) space. QuickSort averages O(N log N) with O(log N) space, but O(N^2) worst case. HeapSort is O(N log N) in-place with O(1) auxiliary space."
    },
    {
        "role": "Software Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "Explain the CAP theorem and PACELC theorem in distributed systems.",
        "keywords": ["cap theorem", "consistency", "availability", "partition tolerance", "pacelc", "latency"],
        "sample": "CAP states that in the event of a network partition (P), a distributed system must choose between Consistency (C) and Availability (A). PACELC extends this: Else (when no partition), the trade-off is between Latency (L) and Consistency (C)."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a scenario where you disagreed with a senior engineer's architectural choice. How did you handle it?",
        "keywords": ["disagreement", "data-driven", "respect", "benchmarks", "compromise", "alignment"],
        "sample": "I built a quick proof-of-concept benchmark demonstrating memory utilization differences under high load. By grounding my argument in objective data rather than opinion, we aligned on a hybrid solution respectfully."
    },
    {
        "role": "Software Engineer", "cat": "HR", "diff": "Beginner",
        "text": "What motivates you to solve challenging computer science problems?",
        "keywords": ["curiosity", "problem solving", "impact", "continuous learning", "engineering"],
        "sample": "I am motivated by decomposing complex, messy problems into elegant, predictable algorithmic components that make tangible positive differences for end users."
    },
    {
        "role": "Software Engineer", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you decide between a microservices architecture versus a well-structured modular monolith?",
        "keywords": ["microservices", "modular monolith", "team size", "deployment complexity", "domain boundaries", "trade-offs"],
        "sample": "For early-to-mid stage products, a modular monolith minimizes network latency, operational overhead, and distributed transaction headaches. Microservices are warranted when distinct domains require independent scaling and dedicated team ownership."
    },
    {
        "role": "Software Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "How would you design a distributed cache invalidation strategy to maintain cache consistency?",
        "keywords": ["cache invalidation", "write-through", "cache-aside", "eventual consistency", "ttl", "cdc", "kafka"],
        "sample": "I favor the Cache-Aside pattern combined with change-data-capture (CDC via Debezium/Kafka) that automatically invalidates or updates Redis keys upon database commits, supplemented with conservative TTLs."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time you had to deliver a critical project under an aggressive deadline.",
        "keywords": ["deadline", "scope management", "mvp", "risk mitigation", "focus", "delivery"],
        "sample": "I aligned with the product manager to trim non-essential features, focused exclusively on the core MVP path, automated integration tests to avoid regression spirals, and delivered on schedule."
    },
    {
        "role": "Software Engineer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you handle constructive criticism received during peer code reviews?",
        "keywords": ["code review", "humility", "growth mindset", "learning", "team standards"],
        "sample": "I view code reviews as opportunities for collective code ownership and personal growth. I separate my ego from my code and appreciate feedback that improves system resilience."
    },

    # ==================== QA ENGINEER ====================
    {
        "role": "QA Engineer", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between black-box, white-box, and grey-box testing?",
        "keywords": ["black-box", "white-box", "grey-box", "source code", "functional testing", "test cases"],
        "sample": "Black-box tests functionality without knowledge of internal code. White-box tests internal structures and paths with full code access. Grey-box combines knowledge of internal data structures with functional testing."
    },
    {
        "role": "QA Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain the Testing Pyramid and the ideal distribution between Unit, Integration, and E2E tests.",
        "keywords": ["testing pyramid", "unit tests", "integration tests", "e2e tests", "speed", "cost", "maintenance"],
        "sample": "The testing pyramid recommends a wide base of fast, cheap unit tests, a middle layer of integration tests verifying API and database interactions, and a thin top layer of end-to-end tests validating user journeys."
    },
    {
        "role": "QA Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you design a robust CI/CD automated test pipeline that prevents flaky tests from blocking deployments?",
        "keywords": ["flaky tests", "ci/cd", "parallelization", "retry mechanism", "quarantine", "docker", "test containers"],
        "sample": "Use Docker test containers for deterministic environments, parallelize suites by feature, eliminate hard-coded sleeps in favor of explicit element polling, and automatically quarantine chronically flaky tests while notifying owners."
    },
    {
        "role": "QA Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "How do you handle a situation where a developer says 'it works on my machine' regarding a bug you reported?",
        "keywords": ["reproduction steps", "environment differences", "collaboration", "logs", "empathy"],
        "sample": "I provide detailed reproduction steps, video recordings, browser versions, and network logs. I invite the developer to pair on my reproduction environment to pinpoint configuration or race-condition variances."
    },
    {
        "role": "QA Engineer", "cat": "HR", "diff": "Beginner",
        "text": "What makes a great QA Engineer stand out from an average tester?",
        "keywords": ["attention to detail", "user advocacy", "automation", "critical thinking", "communication"],
        "sample": "A great QA engineer thinks like both an end user and an adversarial hacker, proactively automates repetitive regression testing, and champions quality culture across the entire engineering lifecycle."
    },
    {
        "role": "QA Engineer", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you balance automated test coverage versus manual exploratory testing when release time is tight?",
        "keywords": ["risk-based testing", "automation", "exploratory", "critical paths", "regression"],
        "sample": "Automate repetitive critical paths and smoke tests in CI. Allocate manual effort toward exploratory testing of newly introduced features and edge-case boundary conditions where automated coverage is not yet mature."
    },
    {
        "role": "QA Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "What tools and strategies do you use for API load and stress testing?",
        "keywords": ["load testing", "stress testing", "k6", "jmeter", "locust", "throughput", "latency", "saturation"],
        "sample": "I author test scripts using k6 or Locust to simulate traffic spikes, measuring p95 and p99 response latencies, error rates, and system resource saturation to uncover connection pool or memory limits."
    },
    {
        "role": "QA Engineer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Describe a time when a critical bug escaped to production on your watch. How did you respond?",
        "keywords": ["root cause analysis", "production incident", "test gap", "regression suite", "accountability"],
        "sample": "A timezone edge case escaped during daylight savings transition. I owned the gap, created a reproduction regression test immediately, and updated our test matrix to systematically include boundary timezone scenarios."
    },
    {
        "role": "QA Engineer", "cat": "Technical", "diff": "Beginner",
        "text": "What are boundary value analysis and equivalence partitioning in test design?",
        "keywords": ["boundary value", "equivalence partitioning", "test cases", "inputs", "valid", "invalid"],
        "sample": "Equivalence partitioning divides inputs into valid and invalid groups where any value yields similar behavior. Boundary value analysis tests edges (min, min+1, max-1, max) where software defects statistically cluster."
    },
    {
        "role": "QA Engineer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you communicate bug severity and priority effectively to product managers?",
        "keywords": ["severity", "priority", "business impact", "clarity", "user journey", "risk"],
        "sample": "I separate severity (technical impact, e.g. data loss or crash) from priority (urgency to the business). I translate technical defects into user friction and financial risk so PMs can make informed release decisions."
    },

    # ==================== DATA ANALYST ====================
    {
        "role": "Data Analyst", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN in SQL?",
        "keywords": ["inner join", "left join", "right join", "full outer join", "nulls", "sql", "keys"],
        "sample": "INNER JOIN returns matching records from both tables. LEFT JOIN returns all rows from the left table and matched rows from the right (or NULL). FULL OUTER JOIN returns all rows when there is a match in either table."
    },
    {
        "role": "Data Analyst", "cat": "Technical", "diff": "Intermediate",
        "text": "What are SQL window functions (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG) and how do they differ from GROUP BY?",
        "keywords": ["window functions", "over partition by", "row_number", "rank", "dense_rank", "group by", "aggregation"],
        "sample": "GROUP BY collapses rows into a single aggregated summary. Window functions compute aggregates across a specified partition or window while preserving the individual identity of each row."
    },
    {
        "role": "Data Analyst", "cat": "Technical", "diff": "Advanced",
        "text": "How do you handle missing, skewed, or outlier data in a large analytical dataset?",
        "keywords": ["imputation", "outliers", "iqr", "z-score", "skewness", "log transform", "median"],
        "sample": "Assess missingness mechanisms (MCAR, MAR, MNAR). For skewed distributions, use median or IQR imputation and log transforms rather than mean/standard deviation. Evaluate whether outliers represent fraud or measurement error before filtering."
    },
    {
        "role": "Data Analyst", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Tell me about a time when your data analysis disproved a widely held assumption by executive leadership.",
        "keywords": ["data storytelling", "executive", "objective", "visualization", "diplomacy", "impact"],
        "sample": "Leadership assumed a churn increase was caused by pricing changes. My cohort retention analysis revealed churn spiked specifically after a buggy mobile release, leading them to prioritize mobile engineering over price rollbacks."
    },
    {
        "role": "Data Analyst", "cat": "HR", "diff": "Beginner",
        "text": "Why do you want to work as a Data Analyst, and how do you explain complex numbers to non-technical stakeholders?",
        "keywords": ["storytelling", "business acumen", "visualization", "clarity", "data-driven decisions"],
        "sample": "I enjoy turning raw numbers into strategic clarity. I explain metrics using business narratives and clear visual analogies rather than technical jargon so stakeholders can act with confidence."
    },
    {
        "role": "Data Analyst", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you design an effective A/B test, determine sample size, and evaluate statistical significance?",
        "keywords": ["a/b testing", "sample size", "p-value", "statistical significance", "type i error", "type ii error", "power"],
        "sample": "Formulate null/alternative hypotheses, establish minimum detectable effect (MDE) and statistical power (typically 80% with alpha 0.05) to compute required sample size, avoid peeking, and test with two-tailed t-test or chi-square."
    },
    {
        "role": "Data Analyst", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between correlation and causation, and how do confounding variables impact findings?",
        "keywords": ["correlation", "causation", "confounding variable", "spurious", "experimentation"],
        "sample": "Correlation signifies that two variables move together, but does not prove one causes the other. Confounding variables influence both factors, creating spurious relationships that only controlled experiments can untangle."
    },
    {
        "role": "Data Analyst", "cat": "Behavioral", "diff": "Advanced",
        "text": "Describe a project where you had to clean messy data from multiple conflicting sources.",
        "keywords": ["data cleaning", "etl", "deduplication", "data dictionary", "pandas", "validation"],
        "sample": "I unified customer records from three legacy CRM databases. I authored automated fuzzy-matching and deduplication pipelines in Pandas, built a unified data dictionary, and flagged ambiguous conflicts for manual human review."
    },
    {
        "role": "Data Analyst", "cat": "Technical", "diff": "Advanced",
        "text": "How do you write performant SQL queries when querying multi-billion-row data warehouses like Snowflake or BigQuery?",
        "keywords": ["partitioning", "clustering", "columnar storage", "predicate pushdown", "materialized views"],
        "sample": "Filter on partitioned and clustered columns first to prune unnecessary partitions, avoid SELECT *, leverage columnar projections, pre-aggregate data in materialized views, and avoid non-sargable functions in WHERE clauses."
    },
    {
        "role": "Data Analyst", "cat": "HR", "diff": "Intermediate",
        "text": "How do you prioritize multiple urgent data analysis requests from different departments?",
        "keywords": ["stakeholder management", "business value", "impact vs effort", "transparency", "roadmap"],
        "sample": "I evaluate requests by business impact and decision urgency. I establish clear turnaround expectations, maintain a transparent request queue, and provide self-service dashboards for recurrent operational questions."
    },

    # ==================== CYBERSECURITY ANALYST ====================
    {
        "role": "Cybersecurity Analyst", "cat": "Technical", "diff": "Beginner",
        "text": "What is the CIA Triad in information security?",
        "keywords": ["confidentiality", "integrity", "availability", "cia triad", "encryption", "hashing"],
        "sample": "Confidentiality ensures data is accessed only by authorized parties (encryption/RBAC). Integrity guarantees data is accurate and untampered (checksums/signatures). Availability ensures systems are operational when needed (redundancy/DDoS defense)."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain the difference between Symmetric and Asymmetric encryption, and how TLS uses both.",
        "keywords": ["symmetric", "asymmetric", "aes", "rsa", "tls handshake", "private key", "public key"],
        "sample": "Symmetric uses a shared secret for fast bulk data encryption (e.g. AES). Asymmetric uses public/private key pairs for secure key exchange (e.g. RSA/ECC). TLS uses asymmetric encryption to exchange a session key, then switches to symmetric encryption for speed."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Technical", "diff": "Advanced",
        "text": "How do you respond to a live Ransomware infection detected across corporate endpoints?",
        "keywords": ["incident response", "containment", "isolation", "forensics", "backup restoration", "eradication"],
        "sample": "Follow SANS/NIST Incident Response: immediately isolate affected segments and endpoints from the network, capture volatile memory for forensics, verify offline clean backup integrity, eradicate attacker persistence, and recover systems incrementally."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a time you discovered an employee violating security policy (e.g. phishing test failure or unauthorized software).",
        "keywords": ["security awareness", "empathy", "non-punitive", "education", "policy enforcement"],
        "sample": "I approached the incident educationally rather than punitively. I conducted a one-on-one session explaining the real threat vector and helped them adopt authorized enterprise tools safely."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "HR", "diff": "Beginner",
        "text": "Why did you choose a career in cybersecurity, and how do you stay motivated in high-stress environments?",
        "keywords": ["defense", "integrity", "problem solving", "adversary", "protection", "cybersecurity"],
        "sample": "I am motivated by defending digital infrastructure and protecting people's privacy. I maintain discipline through structured incident playbooks and continuous training that keeps panic out of critical security operations."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Mixed", "diff": "Intermediate",
        "text": "What is Zero Trust Architecture and what are its core tenets?",
        "keywords": ["zero trust", "never trust always verify", "least privilege", "micro-segmentation", "mfa"],
        "sample": "Zero Trust assumes breach and operates under 'never trust, always verify'. Core principles include explicit identity and device verification, least privilege access control, and network micro-segmentation."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain the OWASP Top 10 vulnerabilities and how to mitigate Broken Object Level Authorization (BOLA/IDOR).",
        "keywords": ["owasp", "bola", "idor", "access control", "authorization checks", "guid"],
        "sample": "BOLA/IDOR occurs when an API endpoint uses user-supplied IDs without verifying ownership. Mitigation requires validating session user ID against resource ownership in every query rather than relying on unguessable IDs alone."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a vulnerability assessment or penetration test where you discovered a critical zero-day or high-risk flaw.",
        "keywords": ["penetration testing", "vulnerability disclosure", "cvss", "remediation", "proof of concept"],
        "sample": "During an internal audit, I discovered an unauthenticated SSRF flaw in a PDF generator service that could query cloud metadata endpoints. I generated a proof of concept, assigned a CVSS score, and coordinated a patch within 24 hours."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "Technical", "diff": "Advanced",
        "text": "How do SIEM and SOC analysts differentiate between genuine advanced persistent threats (APTs) and false positive alerts?",
        "keywords": ["siem", "soc", "false positive", "correlation rules", "threat intelligence", "ioc", "mitre att&ck"],
        "sample": "We cross-reference alerts against the MITRE ATT&CK framework, correlate multi-source endpoint, network, and identity telemetry, enrich with threat intelligence feeds, and tune correlation rules to reduce alarm fatigue."
    },
    {
        "role": "Cybersecurity Analyst", "cat": "HR", "diff": "Intermediate",
        "text": "How do you balance strict security compliance with developer agility and productivity?",
        "keywords": ["devsecops", "shift left", "developer experience", "guardrails", "collaboration"],
        "sample": "I champion DevSecOps: embedding security guardrails directly into CI/CD pipelines (SAST, DAST, dependency scanning) so security becomes an automated enabler rather than an external roadblock."
    },

    # ==================== MOBILE APP DEVELOPER ====================
    {
        "role": "Mobile App Developer", "cat": "Technical", "diff": "Beginner",
        "text": "Explain the mobile application lifecycle in Android and iOS.",
        "keywords": ["lifecycle", "oncreate", "onresume", "onpause", "ondestroy", "background", "foreground"],
        "sample": "Activities and Views transition through creation, foreground/visible, paused, background, and destroyed states. Developers must preserve state and pause expensive location or audio listeners when moving to background."
    },
    {
        "role": "Mobile App Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you handle offline-first architecture, local caching, and data synchronization on mobile devices?",
        "keywords": ["offline first", "sqlite", "room", "core data", "sync queue", "conflict resolution", "retry"],
        "sample": "Write-first to local storage (Room/SQLite), optimistic UI updates, and queue mutation jobs with exponential backoff via WorkManager or background tasks. When connectivity returns, sync with the server using timestamp or CRDT conflict resolution."
    },
    {
        "role": "Mobile App Developer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you achieve 60fps/120fps UI performance and eliminate jank in Flutter or React Native?",
        "keywords": ["jank", "frame drop", "60fps", "bridge", "skia", "memoization", "recycler view", "flatlist"],
        "sample": "Profile with frame analyzers. Avoid blocking the JS or UI threads with heavy computation, use list virtualization (FlatList with windowSize), memoize render items, avoid anonymous functions in loops, and offload CPU tasks to native modules."
    },
    {
        "role": "Mobile App Developer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a scenario where Apple App Store or Google Play Store rejected your app submission. How did you resolve it?",
        "keywords": ["store rejection", "guidelines", "compliance", "privacy policy", "permissions", "appeal"],
        "sample": "Apple rejected an app for requesting background location permissions without adequate user-facing justification. I created an in-app permission onboarding screen explaining the feature, resubmitted with an updated demonstration video, and received approval."
    },
    {
        "role": "Mobile App Developer", "cat": "HR", "diff": "Beginner",
        "text": "What do you find most rewarding about developing mobile applications?",
        "keywords": ["ubiquity", "hardware interaction", "mobile", "tactile", "user delight"],
        "sample": "Mobile devices are the most personal computing devices people own. Building tactile, responsive apps that leverage hardware sensors, cameras, and instant push notifications to solve daily problems is immensely rewarding."
    },
    {
        "role": "Mobile App Developer", "cat": "Mixed", "diff": "Intermediate",
        "text": "When would you build a native app (Kotlin/Swift) versus cross-platform (React Native/Flutter)?",
        "keywords": ["native", "cross platform", "flutter", "react native", "performance", "time to market", "hardware"],
        "sample": "Cross-platform delivers fast time-to-market and shared codebases for business and content apps. Pure native is preferred when deep OS hardware integration (ARKit, Bluetooth Low Energy, high-end 3D graphics) or day-one SDK support is non-negotiable."
    },
    {
        "role": "Mobile App Developer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you manage deep linking and universal links across mobile platforms?",
        "keywords": ["deep linking", "universal links", "app links", "assetlinks", "apple-app-site-association", "routing"],
        "sample": "Configure assetlinks.json on Android and apple-app-site-association on iOS to establish domain ownership. The OS intercepts web URLs and routes directly into specific in-app navigation routes seamlessly."
    },
    {
        "role": "Mobile App Developer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time you optimized an app's battery consumption and memory footprint.",
        "keywords": ["battery drain", "memory leak", "profiling", "location updates", "wakelocks", "leakcanary"],
        "sample": "An app was flagged for excessive battery drain. Using Android Studio Profiler and LeakCanary, I identified continuous GPS polling. I switched to geofencing and fused location providers, reducing background battery impact by 85%."
    },
    {
        "role": "Mobile App Developer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you secure API keys and user credentials stored on mobile devices?",
        "keywords": ["keystore", "keychain", "encryption", "obfuscation", "biometrics", "secure storage"],
        "sample": "Never hardcode API secrets in client code. Store user tokens in Android KeyStore or iOS Keychain encrypted with biometric authentication, and use mobile app attestation (Play Integrity / DeviceCheck) to detect tampered devices."
    },
    {
        "role": "Mobile App Developer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you keep up with annual iOS and Android OS updates and breaking changes?",
        "keywords": ["wwdc", "google i/o", "beta testing", "deprecations", "continuous update"],
        "sample": "I track WWDC and Google I/O sessions, test against developer preview betas early in the summer, and allocate tech debt sprints to address deprecated APIs before consumer OS updates roll out."
    },

    # ==================== DEVOPS ENGINEER ====================
    {
        "role": "DevOps Engineer", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between Continuous Integration (CI) and Continuous Deployment (CD)?",
        "keywords": ["ci", "cd", "continuous integration", "continuous delivery", "automated testing", "deployment"],
        "sample": "CI automates merging code and running automated test suites on every commit. CD extends this by automatically deploying passing builds to staging or production environments without manual gatekeeping."
    },
    {
        "role": "DevOps Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain Kubernetes core primitives: Pods, Deployments, Services, and Ingress.",
        "keywords": ["kubernetes", "pod", "deployment", "service", "ingress", "cluster", "networking"],
        "sample": "A Pod is the smallest deployable unit running containers. A Deployment manages replica sets and zero-downtime rolling updates. A Service provides internal load balancing and stable DNS. An Ingress routes external HTTP/S traffic to internal services."
    },
    {
        "role": "DevOps Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you design a GitOps workflow using tools like ArgoCD or Flux?",
        "keywords": ["gitops", "argocd", "flux", "declarative", "desired state", "drift detection", "reconciliation"],
        "sample": "Git serves as the single source of truth for declarative infrastructure. An in-cluster operator (ArgoCD) monitors repository manifests, detects drift between actual cluster state and Git, and reconciles differences automatically."
    },
    {
        "role": "DevOps Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a production rollback you had to execute. What went wrong and how was it contained?",
        "keywords": ["rollback", "canary", "monitoring", "prometheus", "automated rollback", "blameless"],
        "sample": "A new release caused memory leaks triggering 502 errors. Automated Canary analysis detected error threshold breaches in Prometheus, aborted the deployment, and rolled back to the previous stable revision within 60 seconds."
    },
    {
        "role": "DevOps Engineer", "cat": "HR", "diff": "Beginner",
        "text": "What does 'Infrastructure as Code' (IaC) mean to you and why is it essential?",
        "keywords": ["iac", "terraform", "repeatability", "version control", "auditability", "disaster recovery"],
        "sample": "IaC defines computing infrastructure through code (Terraform, CloudFormation) instead of manual dashboard clicks. It enables repeatability, version-controlled auditing, rapid disaster recovery, and eliminates configuration drift."
    },
    {
        "role": "DevOps Engineer", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you implement Blue-Green versus Canary deployment strategies, and what are their trade-offs?",
        "keywords": ["blue-green", "canary", "traffic shifting", "cost", "risk", "zero downtime"],
        "sample": "Blue-Green runs two identical production environments, switching traffic instantaneously at the router, requiring double infrastructure capacity. Canary deploys to a small percentage of users (e.g. 5%) first, monitoring health before gradual rollout."
    },
    {
        "role": "DevOps Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "What metrics do you monitor using Prometheus and Grafana for backend services (USE and RED methods)?",
        "keywords": ["prometheus", "grafana", "red method", "rate", "errors", "duration", "saturation", "use method"],
        "sample": "For services, use the RED method: Rate (requests/sec), Errors (failed requests/sec), and Duration (latency distribution). For infrastructure, use the USE method: Utilization (% busy), Saturation (queue depth), and Errors."
    },
    {
        "role": "DevOps Engineer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about how you established a blameless post-mortem culture following a major system outage.",
        "keywords": ["blameless post-mortem", "systemic failure", "learning", "action items", "culture"],
        "sample": "I led a post-mortem focusing on systemic failure modes rather than individual human error. We investigated why safeguards failed, authored measurable action items, and shared findings openly across the engineering department."
    },
    {
        "role": "DevOps Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you secure container images and Kubernetes clusters against runtime exploits?",
        "keywords": ["container security", "trivy", "distroless", "rbac", "network policies", "seccomp", "least privilege"],
        "sample": "Scan images with Trivy in CI, utilize minimal distroless base images, run non-root containers with read-only root filesystems, enforce strict Kubernetes RBAC, and apply Network Policies to restrict pod-to-pod lateral communication."
    },
    {
        "role": "DevOps Engineer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you handle on-call rotations and mitigate alert fatigue for your engineering team?",
        "keywords": ["on call", "alert fatigue", "slo", "sli", "actionable alerts", "runbooks"],
        "sample": "I ensure every alerting metric maps to user-facing SLOs and includes an updated runbook. If an alert does not require immediate human action at 2 AM, it is downgraded to a ticket to protect engineer well-being."
    },

    # ==================== AI/ML ENGINEER ====================
    {
        "role": "AI/ML Engineer", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between Supervised, Unsupervised, and Reinforcement Learning?",
        "keywords": ["supervised", "unsupervised", "reinforcement learning", "labels", "clustering", "reward", "policy"],
        "sample": "Supervised learning trains on labeled input-output pairs. Unsupervised learning identifies hidden patterns or clusters in unlabeled data. Reinforcement learning trains agents to maximize cumulative reward through environment interaction."
    },
    {
        "role": "AI/ML Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "Explain the Transformer architecture and how the Multi-Head Self-Attention mechanism works.",
        "keywords": ["transformer", "self-attention", "query", "key", "value", "multi-head", "positional encoding"],
        "sample": "Transformers process sequences in parallel using self-attention. Tokens project into Query, Key, and Value matrices. Softmax((QK^T)/sqrt(d_k))V computes token contextual relevance across multiple parallel attention heads."
    },
    {
        "role": "AI/ML Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "How do you design a Retrieval-Augmented Generation (RAG) system with hybrid search, re-ranking, and hallucination guardrails?",
        "keywords": ["rag", "vector search", "bm25", "hybrid search", "cross-encoder", "re-ranking", "guardrails", "evals"],
        "sample": "Combine sparse keyword search (BM25) with dense vector search (HNSW). Pass top results through a cross-encoder re-ranker. Feed pruned context to the LLM with strict attribution prompts, and evaluate faithfulness using RAGAS metrics."
    },
    {
        "role": "AI/ML Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a model development project where your model performed great in validation but failed in production.",
        "keywords": ["data drift", "concept drift", "train-test contamination", "production monitoring", "retraining"],
        "sample": "A fraud model degraded in production due to concept drift in user transaction behavior. I established production drift monitoring using evidently.ai and automated weekly retraining pipelines to maintain accuracy."
    },
    {
        "role": "AI/ML Engineer", "cat": "HR", "diff": "Beginner",
        "text": "What excites you most about the recent breakthroughs in Generative AI and Large Language Models?",
        "keywords": ["generative ai", "multimodal", "reasoning", "automation", "impact", "frontier"],
        "sample": "The shift from narrow task classifiers to versatile multimodal reasoning engines that understand speech, vision, and text simultaneously unlocks completely new categories of assistive software like this mock interview platform."
    },
    {
        "role": "AI/ML Engineer", "cat": "Mixed", "diff": "Intermediate",
        "text": "When would you fine-tune an open-source LLM versus using Prompt Engineering or RAG with a frontier API?",
        "keywords": ["fine-tuning", "rag", "prompt engineering", "cost", "latency", "domain adaptation", "style"],
        "sample": "Prompt engineering and RAG are best for injecting dynamic factual knowledge with zero training cost. Fine-tuning (LoRA/QLoRA) is justified for specialized output styling, proprietary syntax, or reducing latency/cost on high-volume tasks."
    },
    {
        "role": "AI/ML Engineer", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you evaluate generative AI applications where traditional accuracy metrics (F1/Precision) do not apply?",
        "keywords": ["llm as a judge", "bertscore", "bleu", "rouge", "human evaluation", "ragas", "faithfulness"],
        "sample": "We use a multi-tiered evaluation strategy: deterministic checks (JSON schema validation, regex), semantic metrics (BERTScore), automated LLM-as-a-judge rubrics evaluating faithfulness and relevance, and periodic human-in-the-loop spot checks."
    },
    {
        "role": "AI/ML Engineer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time you optimized an ML pipeline for low-latency real-time inference.",
        "keywords": ["quantization", "onnx", "tensorrt", "latency", "batching", "vllm", "pruning"],
        "sample": "A transcription and emotion analysis pipeline took 8 seconds per answer. I converted models to ONNX and applied 8-bit quantization (INT8), reducing inference latency to under 1.2 seconds without measurable degradation in accuracy."
    },
    {
        "role": "AI/ML Engineer", "cat": "Technical", "diff": "Advanced",
        "text": "Explain parameter-efficient fine-tuning (PEFT) and how LoRA (Low-Rank Adaptation) works mathematically.",
        "keywords": ["peft", "lora", "low rank", "matrix decomposition", "adapters", "frozen weights"],
        "sample": "LoRA freezes pre-trained weight matrices W and models updates as the product of two low-rank matrices: Delta W = B * A, where B is d x r and A is r x k with rank r << min(d, k). This reduces trainable parameters by over 99%."
    },
    {
        "role": "AI/ML Engineer", "cat": "HR", "diff": "Intermediate",
        "text": "How do you navigate ethical concerns, bias mitigation, and safety guardrails in AI model deployments?",
        "keywords": ["ai ethics", "fairness", "bias mitigation", "safety guardrails", "red teaming", "transparency"],
        "sample": "I conduct rigorous dataset diversity audits, author system prompts with explicit safety guardrails, perform adversarial red-teaming, and ensure user-facing AI systems clearly communicate limitations and confidence."
    },

    # ==================== BUSINESS ANALYST ====================
    {
        "role": "Business Analyst", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between functional requirements and non-functional requirements?",
        "keywords": ["functional requirements", "non-functional requirements", "features", "performance", "security", "scalability"],
        "sample": "Functional requirements define what the system must do (e.g. 'user can upload resume'). Non-functional requirements specify how well the system performs (e.g. 'page must load in under 2 seconds', 99.9% uptime)."
    },
    {
        "role": "Business Analyst", "cat": "Technical", "diff": "Intermediate",
        "text": "How do you author clear User Stories and Acceptance Criteria using the INVEST and Gherkin (Given-When-Then) frameworks?",
        "keywords": ["invest", "user stories", "acceptance criteria", "gherkin", "given when then", "scrum"],
        "sample": "Stories follow INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable). Acceptance criteria use Gherkin: Given (preconditions), When (user action), Then (expected observable outcome)."
    },
    {
        "role": "Business Analyst", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Describe a situation where two senior executives had conflicting requirements for a key software release. How did you reconcile them?",
        "keywords": ["conflict resolution", "prioritization", "stakeholder alignment", "data-driven", "roi", "compromise"],
        "sample": "I mapped both requirements against overarching company strategic KPIs and projected ROI. By presenting the trade-offs visually, we reached consensus on a phased rollout delivering executive A's critical need in Phase 1 and B's in Phase 2."
    },
    {
        "role": "Business Analyst", "cat": "HR", "diff": "Beginner",
        "text": "What role does a Business Analyst play in bridging the gap between business stakeholders and technical engineers?",
        "keywords": ["translator", "communication", "empathy", "clarity", "bridge", "scope management"],
        "sample": "A BA acts as a bilingual translator: converting ambiguous business desires into precise, actionable technical specifications while translating engineering constraints into understandable business impacts."
    },
    {
        "role": "Business Analyst", "cat": "Mixed", "diff": "Intermediate",
        "text": "How do you manage scope creep during an active agile sprint?",
        "keywords": ["scope creep", "change management", "backlog", "impact assessment", "sprint goal"],
        "sample": "Acknowledge the request, assess impact on sprint commitment, and defer non-critical changes to the product backlog for prioritization in the subsequent sprint planning session."
    },
    {
        "role": "Business Analyst", "cat": "Technical", "diff": "Advanced",
        "text": "What modeling techniques (BPMN, UML Activity Diagrams, Use Case Diagrams) do you use to map complex business workflows?",
        "keywords": ["bpmn", "uml", "swimlanes", "activity diagram", "use case", "workflow"],
        "sample": "I utilize BPMN 2.0 with swimlanes to clearly differentiate departmental actor responsibilities, decision gateways, handoffs, and error states, ensuring both business and engineering align on workflow boundaries."
    },
    {
        "role": "Business Analyst", "cat": "Behavioral", "diff": "Advanced",
        "text": "Tell me about a time a project was failing to achieve user adoption after launch. How did you diagnose and fix it?",
        "keywords": ["user adoption", "analytics", "user interviews", "funnel analysis", "onboarding", "ux feedback"],
        "sample": "I analyzed funnel drop-off analytics and conducted 10 user interviews. We discovered users were overwhelmed by a complex initial form. We redesigned it into a progressive multi-step wizard, increasing completion by 65%."
    },
    {
        "role": "Business Analyst", "cat": "HR", "diff": "Intermediate",
        "text": "How do you maintain requirement traceability throughout the development lifecycle?",
        "keywords": ["traceability matrix", "jira", "user stories", "test cases", "deliverables", "verification"],
        "sample": "I maintain a Requirements Traceability Matrix linking business goals to epics, user stories, engineering pull requests, and QA test cases to verify complete coverage at every gate."
    },
    {
        "role": "Business Analyst", "cat": "Technical", "diff": "Beginner",
        "text": "What is the difference between a Product Backlog and a Sprint Backlog?",
        "keywords": ["product backlog", "sprint backlog", "prioritization", "scrum", "sprint goal", "estimation"],
        "sample": "The Product Backlog is an evolving, prioritized list of all desired features and fixes for the product. The Sprint Backlog is the subset of items committed by the development team for completion in the current sprint."
    },
    {
        "role": "Business Analyst", "cat": "HR", "diff": "Advanced",
        "text": "How do you foster trust with engineering teams who may be skeptical of requirements from business analysts?",
        "keywords": ["trust", "technical comprehension", "humility", "active listening", "respect", "engineers"],
        "sample": "I demonstrate respect for engineering realities, listen actively to architectural feedback, and write specifications with enough technical rigor that developers feel empowered rather than constrained."
    },

    # ==================== GENERAL HR & BEHAVIORAL QUESTIONS ====================
    {
        "role": "Software Engineer", "cat": "HR", "diff": "Beginner",
        "text": "Tell me about yourself, your background in computer science, and your career aspirations.",
        "keywords": ["education", "passion", "projects", "strengths", "aspirations", "software engineering"],
        "sample": "I graduated with a degree in Software Engineering where I focused on full-stack development and distributed systems. I have built production-ready applications and aspire to grow into a senior architect building reliable, impactful software."
    },
    {
        "role": "Software Engineer", "cat": "HR", "diff": "Beginner",
        "text": "What are your greatest professional strengths, and what is one area you are actively working to improve?",
        "keywords": ["strengths", "weakness", "growth mindset", "problem solving", "self-awareness", "continuous improvement"],
        "sample": "My strength is deep analytical persistence when troubleshooting complex architectural problems. An area I am improving is delegating tasks earlier in project lifecycles to avoid becoming a bottleneck."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Tell me about a time you made a significant mistake on the job. How did you handle it and what did you learn?",
        "keywords": ["mistake", "accountability", "ownership", "correction", "retrospective", "growth"],
        "sample": "I pushed an untested database script that dropped an index during peak hours. I immediately owned the error in Slack, restored the index to alleviate latency, and implemented a mandatory peer-review policy for all production DDL scripts."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Advanced",
        "text": "Describe a situation where you had to adapt quickly to sudden changes in company priorities or technology direction.",
        "keywords": ["adaptability", "resilience", "pivot", "learning agility", "team support"],
        "sample": "Our core client pivoted from an on-premise relational database to cloud serverless. I ramped up on cloud architectures over a single sprint, authored migration blueprints, and helped lead the team through the transition smoothly."
    },
    {
        "role": "Software Engineer", "cat": "HR", "diff": "Intermediate",
        "text": "Where do you see yourself professionally in three to five years?",
        "keywords": ["career growth", "leadership", "technical mastery", "mentorship", "impact", "long-term vision"],
        "sample": "In three to five years, I see myself taking technical lead responsibility, guiding system architecture, mentoring junior engineers, and driving cross-functional engineering initiatives that deliver measurable business value."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Beginner",
        "text": "Describe how you prioritize multiple competing tasks when everything feels urgent.",
        "keywords": ["prioritization", "eisenhower matrix", "communication", "focus", "time management"],
        "sample": "I evaluate tasks based on true impact versus urgency using the Eisenhower matrix. I communicate transparently with stakeholders to set realistic expectations and execute high-priority items sequentially with deep focus."
    },
    {
        "role": "Software Engineer", "cat": "Mixed", "diff": "Beginner",
        "text": "How do you handle working with team members who have very different communication styles than your own?",
        "keywords": ["communication", "empathy", "active listening", "flexibility", "teamwork"],
        "sample": "I adapt my communication to match what works best for them: using concise bulleted summaries for asynchronous communicators and scheduling short face-to-face syncs for collaborative thinkers."
    },
    {
        "role": "Software Engineer", "cat": "Behavioral", "diff": "Intermediate",
        "text": "Tell me about a project you are most proud of having completed. What was your contribution?",
        "keywords": ["pride", "accomplishment", "star method", "leadership", "technical contribution", "results"],
        "sample": "I built an automated mock interview analysis platform integrating speech-to-text, facial expression analysis, and LLM rubric grading. I designed the resilient asynchronous pipeline that processed multi-gigabyte video interviews reliably within seconds."
    }
]

def seed_questions(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        # Build lookup maps
        roles = {r.name: r.id for r in db.query(JobRole).all()}
        cats = {c.name: c.id for c in db.query(InterviewCategory).all()}
        diffs = {d.name: d.id for d in db.query(DifficultyLevel).all()}

        seeded_count = 0
        for q_data in QUESTIONS_DATA:
            role_id = roles.get(q_data["role"])
            cat_id = cats.get(q_data["cat"])
            diff_id = diffs.get(q_data["diff"])

            if not role_id or not cat_id or not diff_id:
                continue

            existing = db.query(Question).filter(Question.text == q_data["text"]).first()
            if not existing:
                q = Question(
                    text=q_data["text"],
                    job_role_id=role_id,
                    category_id=cat_id,
                    difficulty_id=diff_id,
                    expected_keywords=q_data["keywords"],
                    sample_answer=q_data["sample"],
                    is_active=True
                )
                db.add(q)
                seeded_count += 1

        db.commit()
        total_questions = db.query(Question).count()
        print(f"Questions seeded: {seeded_count} new questions added. Total in database: {total_questions}.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding questions: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_questions()

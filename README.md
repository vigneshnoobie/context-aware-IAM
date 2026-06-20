# Context-Aware Identity and Access Management with Behavioral Risk Detection and Adaptive Trust Scoring

This project presents a Context-Aware Identity and Access Management (IAM) system developed as part of a postgraduate research initiative in cybersecurity. The system integrates behavioral analytics, contextual awareness, adaptive trust computation, and decentralized identity storage to enhance authentication and access control mechanisms in modern digital environments.

## Project Overview

Traditional IAM solutions often rely on static access policies and predefined roles, which are insufficient in today’s dynamic and distributed environments. This hybrid IAM system introduces real-time behavioral risk detection, machine learning–based trust evaluation, and dynamic access decisions that evolve over a session.

The system combines centralized access control with decentralized identity storage (via IPFS) to achieve a balance between usability, privacy, and scalability. It is built as a functional prototype with a modular backend, responsive frontend, and real-time integrations for SIEM logging and decentralized identity management.

## Key Features

- Passwordless login using typing behavior and contextual signals such as IP address, device type, and access time
- Real-time risk scoring using trained machine learning models (Decision Trees)
- Adaptive Trust Flow Engine (ATFE) that adjusts user trust levels based on behavioral patterns and contextual factors
- Decentralized identity storage using IPFS for secure verifiable credential (VC) handling
- Dynamic access decisions that allow, challenge, or deny users based on risk and trust scores
- Real-time SIEM log forwarding to external monitoring platforms such as Splunk
- Admin dashboard for visualizing login activity, trust levels, and behavioral anomalies

## Architecture Overview

- **Backend:** Python (Flask framework)
- **Frontend:** HTML, CSS, JavaScript with Jinja2 templating
- **Machine Learning:** scikit-learn (risk scoring and behavior analysis)
- **Identity Storage:** IPFS (for decentralized verifiable credentials)
- **Logging and Monitoring:** Integration with Splunk using HTTP Event Collector
- **Session Management:** Token-based access control with behavioral triggers for session revocation

2. Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate       
venv\Scripts\activate  

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

python app.py

The application will be available locally at:
http://localhost:5000
http://localhost:5000//admin
http://localhost:5000/auth/login

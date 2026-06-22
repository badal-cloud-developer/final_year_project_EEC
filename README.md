# Demand-Driven Waste Management Platform

**For Efficient Collection and Community Engagement**

A web-based platform that connects households, waste collectors, drivers, and municipal authorities through a real-time, demand-driven waste collection system — built to replace Nepal's static, fixed-schedule waste collection model with a dynamic, community-powered alternative.

> Major Project submitted in partial fulfillment of the requirements for the degree of **Bachelor in Computer Engineering**, Pokhara University, Nepal.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Route Optimization Approach](#route-optimization-approach)
- [Simulation & Results](#simulation--results)
- [Security & Privacy](#security--privacy)
- [Project Team](#project-team)
- [Future Work](#future-work)
- [References](#references)

---

## Overview

Waste management in Nepal's urban and semi-urban areas suffers from rigid, fixed-day collection schedules that ignore actual waste generation patterns — leading to overflowing bins, delayed pickups, and illegal dumping. This project proposes a **Python Django–based platform** that lets households report waste on demand, matches those reports with nearby collectors, and optimizes collection routes in real time.

The system layers **gamification** (points, badges, leaderboards) on top of core waste-reporting functionality to drive sustained community participation, and integrates **WhatsApp notifications** via Twilio for accessible, low-friction communication across all user roles.

## Problem Statement

Traditional municipal waste collection in Nepal typically follows a static schedule (e.g., pickup on fixed days regardless of actual waste volume), resulting in:

- Delayed pickups and overflowing bins
- Illegal dumping and poor segregation
- Little to no real-time coordination between households, collectors, and authorities
- Low public engagement in sustainable waste practices

This project investigates whether a **community-driven, gamified digital platform** can meaningfully improve participation, coordination, and collection efficiency compared to the traditional static model.

## Objectives

To design and implement an integrated waste management platform that:

1. Enables real-time, demand-based waste reporting and collection (replacing fixed schedules)
2. Encourages responsible disposal behavior through gamification and direct communication
3. Optimizes collection routes using mapping APIs and vehicle routing algorithms
4. Provides municipal authorities with oversight and analytics for data-driven decision-making

## Key Features

| Feature | Description |
|---|---|
| **Role-based access** | Separate portals for Waste Generators (households), Waste Receivers (collectors/recyclers), Drivers, and Metro Authorities |
| **Real-time waste reporting** | Households report waste by category (Degradable, Non-Degradable, E-waste) with location and optional details |
| **Anonymous illegal dumping reports** | Users can report dumping incidents anonymously with photo evidence |
| **Gamification engine** | Points, badges, and leaderboards reward reporting, segregation, and timely collection |
| **WhatsApp notifications** | Real-time alerts for request acceptance, pickup status, and emergencies via Twilio API |
| **Route optimization** | Clustering and routing algorithms generate efficient, capacity-aware collection routes |
| **Dynamic vehicle allocation** | Unaccepted requests are automatically reassigned to municipal vehicles |
| **Metro dashboard & analytics** | Authorities monitor waste trends, collection performance, and cost metrics city-wide |
| **Driver execution flow** | Drivers receive optimized stop-by-stop routes with in-app verification at each pickup |

## System Architecture

The platform is organized around four core user-flow modules:

1. **User Registration & Authentication** — Role-based sign-up and login (households, receivers, drivers, metro authorities)
2. **Waste Reporting & Social Engagement** — Households submit reports, engage with community posts, and earn points
3. **Waste Collection & Management** — Receivers view and accept matching requests, coordinate pickup, and earn rewards
4. **Metro Oversight & Analytics** — Authorities monitor activity, manage drivers/vehicles, and handle unaccepted requests

Each module is backed by Django's built-in authentication and ORM, with role-based permissions controlling access to views and data.

## Tech Stack

**Frontend**
- HTML, CSS, JavaScript
- Django Templates

**Backend**
- Python Django (MVC architecture, ORM, built-in authentication)

**Database**
- SQLite (development) — with PostgreSQL recommended for production deployment

**Mapping & Routing**
- Google Maps API / Distance Matrix API
- Google OR-Tools
- Leaflet.js (route and cluster visualization)

**Messaging**
- Twilio WhatsApp API

**Design & Prototyping**
- Figma (wireframing and UI prototypes)

## Route Optimization Approach

Collection routing was developed iteratively across several algorithmic approaches:

1. **K-means Clustering** *(initial attempt)* — grouped points by proximity but ignored vehicle capacity, producing infeasible clusters
2. **KDTree Clustering** — enabled efficient spatial partitioning and balanced, capacity-aware clusters
3. **Clarke-Wright Savings Algorithm** — merged clusters into routes based on distance savings
4. **TSP (Greedy Approach) & Google OR-Tools** — optimized visit sequence within each route
5. **Hungarian Algorithm** (via `scipy.optimize.linear_sum_assignment`) — matched cluster centroids to the nearest of 29 ward collection centers

This hybrid pipeline balances route efficiency with real-world constraints like vehicle capacity and dispatch-point proximity.

## Simulation & Results

As the platform has not yet been piloted in a live municipal setting, it was evaluated using a **120-day simulation** built with SimPy and Simulated Annealing, modeling 1,000 synthetic waste-generation points against 29 fixed ward dispatch centers.

| Metric | Result |
|---|---|
| Community participation | Increased by an estimated **30–40%** under the gamified system |
| Travel distance & fuel usage | Reduced by roughly **25–30%** through optimized routing |
| Average pickup time | Reduced from 3–4 days (static model) to **under 2 days** on demand |
| User motivation | ~2/3 of simulated users cited points/leaderboards as a key driver of continued participation |
| Estimated emissions reduction | **25–30%** reduction in fuel-related emissions from shorter routes |

Stakeholder interviews with ward officials and municipal staff supported these findings, citing improved transparency and coordination, while also flagging digital access and long-term engagement as open challenges.

> **Note:** All results are based on simulated data and synthetic scenarios. Real-world deployment would be required to validate these findings under live operating conditions.

## Security & Privacy

- **Anonymous reporting** for illegal dumping incidents, with no personal identifiers in public posts
- **Data minimization** — only location data necessary for collection is retained
- **User consent** obtained for location data collection per platform privacy policy
- **Role-based access control** enforced through Django's authentication and permissions system
- **No public shaming/scoring** — gamification is designed around positive reinforcement only
- Data collected is used **exclusively** for waste management improvement, not monetized or shared with third parties

## Project Team

| Name | Roll Number |
|---|---|
| Ashish Raj Poudel | 21070197 |
| Badal Khanal | 21070201 |
| Mahendra Oli | 21070216 |
| Sujina Pandey | 21070256 |

**Supervised by:** Prof. Dr. Shailesh Bahadur Pandey
**Institution:** Everest Engineering College, Faculty of Science and Technology, Pokhara University, Nepal
**Submission:** July 2025

## Future Work

- Field pilot deployment in Kathmandu to validate simulated results
- Migration from SQLite to PostgreSQL for production scalability
- IoT-integrated smart bin sensors for proactive route triggering
- SMS or alternative interfaces to bridge the digital access gap (~50% internet penetration in Nepal)
- Expansion to additional waste streams and city-wide scaling
- Refined, evolving incentive structures to sustain long-term user engagement

## References

A full list of academic and industry references — covering global waste management research, gamification studies, and routing optimization literature — is available in the complete project report.

---

*This README summarizes the academic project report. For full methodology, diagrams, literature review, and detailed analysis, refer to the complete report document.*

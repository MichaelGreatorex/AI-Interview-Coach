# Infrastructure

This directory contains active Terraform configuration for the deployed runtime of AI Interview Coach.

## Implemented AWS Components

- Networking
	- VPC
	- Public and private subnets
	- Internet gateway and NAT routing

- Compute and delivery
	- ECS cluster
	- Frontend ECS service and task definition
	- Backend ECS service and task definition
	- Application Load Balancer with path-based routing

- Data and registries
	- PostgreSQL RDS instance
	- DB subnet group
	- ECR repositories for frontend and backend images

- Operations
	- CloudWatch log group for ECS containers
	- IAM task execution role and policy attachments

## Runtime Topology

- ALB receives HTTP traffic.
- Frontend and backend run on ECS Fargate in private subnets.
- ALB routes API paths to backend target group.
- RDS is private and accessed only from backend security group.

## Secure by Design

1. Least-privilege network paths
- Why: Limit blast radius and isolate services.
- How: Security groups only allow frontend and backend ingress from ALB; RDS ingress is limited to backend security group.
- Effect: Direct internet access to backend containers and database is blocked.

2. Private runtime placement
- Why: Reduce direct exposure of application and data tiers.
- How: ECS services run in private subnets with no public IP assignment.
- Effect: Access is mediated through ALB and controlled routing.

3. Secret material not hardcoded in task definitions
- Why: Prevent long-lived credential exposure in plain environment config.
- How: Backend task consumes database password through secret reference and IAM access policy.
- Effect: Lower operational risk and improved secret rotation posture.

4. Encryption at rest for persistence
- Why: Protect data if underlying storage is accessed outside normal controls.
- How: RDS storage encryption is enabled.
- Effect: Persistent interview data is encrypted at rest.

## Local Development Runtime

Local containers are defined in the repository root docker-compose file.

- Start local stack: docker compose up --build
- Stop local stack: docker compose down
- Reset local volumes: docker compose down -v

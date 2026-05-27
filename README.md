# Dental Appointment Management System

The Dental Appointment Management System is an AI-powered conversational application designed to simplify and automate the process of managing dental appointments through natural language interactions. Instead of using traditional appointment booking systems, users can communicate with the system in plain English just like speaking with a real receptionist.

The project is built using modern AI engineering frameworks such as LangGraph and LangChain, while the conversational intelligence is powered by the GPT-OSS-120B model served through Groq high-speed inference infrastructure.

This project demonstrates how multiple AI agents can work together inside a coordinated workflow to perform different appointment-related tasks efficiently and intelligently.

---

# Project Objective

The main objective of this project is to build an intelligent dental appointment assistant capable of:

* Understanding human language
* Detecting user intent automatically
* Routing requests to specialized AI agents
* Managing appointment workflows
* Maintaining conversational memory
* Performing real-time booking operations

The system acts as a virtual AI receptionist for a dental clinic.

---

# Main Features

The application provides several important features for patients and clinic administrators.

---

# 1. Appointment Slot Inquiry

Users can ask the system to display available appointment slots for specific doctors or dental specializations.

Example:

```text id="grvlm2"
User:
Show available slots for an orthodontist
```

The system searches the database and displays matching available appointment timings.

---

# 2. Appointment Booking

Patients can book appointments through natural language conversation.

The system collects:

* Patient ID
* Doctor name
* Specialization
* Preferred date and time

Before confirming the appointment, the system always checks whether the requested slot is available.

---

# 3. Appointment Cancellation

Users can cancel previously booked appointments.

The system:

* verifies appointment details
* removes the booking
* confirms cancellation

---

# 4. Appointment Rescheduling

Patients can modify existing appointments by selecting a new time slot.

The system:

* validates the old appointment
* checks the new slot availability
* updates the booking information

---

# 5. Doctor & Patient Information Lookup

The system can also:

* display doctor schedules
* retrieve patient appointments
* show specialization-based availability
* search appointment history

---

# System Architecture

The project follows a **Multi-Agent Architecture**.

Instead of using one large AI system to perform every task, the application divides responsibilities among multiple specialized AI agents.

Each agent is designed for a specific purpose.

This architecture improves:

* scalability
* maintainability
* modularity
* reasoning quality
* workflow organization

---

# Overall Workflow Architecture

```text id="4u1wgs"
                    ┌──────────────┐
                    │  Supervisor  │
                    │    Agent     │
                    └──────┬───────┘
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼

┌─────────────┐    ┌─────────────┐    ┌──────────────┐
│ Info Agent │    │ Booking     │    │ Cancellation │
│             │    │ Agent       │    │ Agent        │
└─────────────┘    └─────────────┘    └──────────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │ Reschedule     │
                   │ Agent          │
                   └────────────────┘
```

---

# Detailed Explanation of Each Agent

---

# 1. Supervisor Agent

The Supervisor Agent acts as the central controller of the entire system.

Responsibilities include:

* reading user messages
* understanding user intent
* deciding which specialized agent should handle the request
* routing workflow execution

The Supervisor performs **Intent Classification**.

Example:

| User Request            | Detected Intent | Assigned Agent     |
| ----------------------- | --------------- | ------------------ |
| "Book an appointment"   | `book`          | Booking Agent      |
| "Cancel my appointment" | `cancel`        | Cancellation Agent |
| "Show available slots"  | `get_info`      | Info Agent         |

The Supervisor Agent is responsible for intelligent workflow routing.

---

# 2. Info Agent

The Info Agent handles all informational queries.

Responsibilities:

* check available slots
* display doctor schedules
* retrieve patient appointments
* search appointment details

This agent performs only read operations and cannot modify appointment data.

---

# 3. Booking Agent

The Booking Agent manages the complete booking workflow.

Responsibilities include:

* collecting patient details
* validating required information
* checking slot availability
* booking appointments
* confirming successful bookings

The Booking Agent always verifies slot availability before creating an appointment.

---

# 4. Cancellation Agent

The Cancellation Agent removes existing appointments.

Responsibilities:

* verify booking information
* identify appointments
* cancel bookings
* confirm cancellation

---

# 5. Reschedule Agent

The Reschedule Agent handles appointment modifications.

Responsibilities:

* verify current appointment
* check new slot availability
* update appointment timing
* confirm rescheduling

---

# Technologies Used

The project integrates multiple modern AI and Python technologies.

| Technology   | Purpose                                          |
| ------------ | ------------------------------------------------ |
| LangGraph    | Multi-agent workflow orchestration               |
| LangChain    | LLM integration and tool calling                 |
| GPT-OSS-120B | Conversational reasoning and response generation |
| Groq         | High-speed LLM inference infrastructure          |
| Pandas       | CSV file management                              |
| Pydantic     | Structured data validation                       |
| Python       | Core programming language                        |

---

# Project Directory Structure

```text id="h8x3if"
dental_agent_project/

├── main.py
├── doctor_availability.csv
├── requirements.txt

├── dental_agent/

│   ├── agent.py
│   ├── config/
│   │   └── settings.py

│   ├── models/
│   │   └── state.py

│   ├── tools/
│   │   ├── csv_reader.py
│   │   └── csv_writer.py

│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── info_agent.py
│   │   ├── booking_agent.py
│   │   ├── cancellation_agent.py
│   │   └── rescheduling_agent.py

│   └── workflows/
│       └── graph.py
```

---

# File-by-File Explanation

---

# `main.py`

This is the entry point of the application.

Responsibilities:

* starts the chatbot
* initializes workflow
* handles user interaction

---

# `doctor_availability.csv`

Acts as the appointment database.

Stores:

* doctor schedules
* appointment slots
* booking information
* availability status

---

# `requirements.txt`

Contains all Python dependencies required for the project.

Example:

* LangChain
* LangGraph
* Pandas
* Pydantic
* Groq SDK

---

# `settings.py`

Stores configuration variables such as:

* API keys
* model name
* temperature values

Example:

```env id="m5t4do"
MODEL_NAME=openai/gpt-oss-120b
```

---

# `state.py`

Defines the shared conversation state structure used by LangGraph.

The state stores:

* conversation history
* intent information
* collected parameters
* tool outputs
* final responses

---

# `csv_reader.py`

Contains tools for reading appointment data.

Examples:

* get available slots
* check slot availability
* fetch patient appointments

---

# `csv_writer.py`

Contains tools for modifying appointment data.

Examples:

* book appointments
* cancel appointments
* update schedules

---

# `graph.py`

Defines the complete workflow graph.

Controls:

* agent routing
* workflow transitions
* tool execution flow
* conditional edges

---

# Installation Process

---

# Step 1 — Create Virtual Environment

```bash id="k44rzv"
python -m venv venv
```

---

# Step 2 — Activate Environment

### Windows

```bash id="djilnx"
venv\Scripts\activate
```

### Linux/Mac

```bash id="gm5hyo"
source venv/bin/activate
```

---

# Step 3 — Install Dependencies

```bash id="8y6dv0"
pip install -r requirements.txt
```

---

# Step 4 — Configure Environment Variables

Create a `.env` file in the project root.

```env id="39khvc"
GROQ_API_KEY=your_api_key_here
MODEL_NAME=openai/gpt-oss-120b
TEMPERATURE=0
```

---

# Running the Application

Start the chatbot system using:

```bash id="jlwmwm"
python main.py
```

The system will launch an interactive terminal-based AI assistant.

---

# Example Conversations

---

# Example 1 — Checking Available Slots

```text id="d4od5k"
User:
Show available slots for an orthodontist

Agent:
Available slots:
1. 5/10/2026 9:00 - Dr. Emily Johnson
2. 5/10/2026 10:00 - Dr. Emily Johnson
```

---

# Example 2 — Booking Appointment

```text id="r0twie"
User:
Book patient 1000082 with Dr. Emily Johnson on 5/10/2026 9:00

Agent:
Checking slot availability...

The slot is available.

Appointment booked successfully.
```

---

# Example 3 — Cancelling Appointment

```text id="06ygam"
User:
Cancel appointment for patient 1000082

Agent:
Appointment cancelled successfully.
```

---

# Example 4 — Rescheduling Appointment

```text id="p0kvml"
User:
Reschedule patient 1000082 to 5/12/2026 10:00

Agent:
Checking new slot availability...

The slot is available.

Appointment rescheduled successfully.
```

---

# Supported Dental Specializations

The system currently supports:

* General Dentist
* Oral Surgeon
* Orthodontist
* Cosmetic Dentist
* Prosthodontist
* Pediatric Dentist
* Emergency Dentist

---

# CSV Data Structure

Appointment data is stored inside:

```text id="znbrwz"
doctor_availability.csv
```

---

# CSV Fields

| Field               | Description               |
| ------------------- | ------------------------- |
| `date_slot`         | Appointment date and time |
| `specialization`    | Type of dentist           |
| `doctor_name`       | Dentist name              |
| `is_available`      | Slot availability         |
| `patient_to_attend` | Patient ID                |

---

# How the AI Workflow Operates

---

# 1. Intent Classification

The Supervisor Agent reads the user message and determines the request type.

Example:

```text id="4h0l1k"
"I want to reschedule my appointment"
```

Detected intent:

```python id="hy2t4f"
intent = "reschedule"
```

The request is then routed to the Reschedule Agent.

---

# 2. Tool Calling

Agents interact with external tools to:

* read appointment data
* update bookings
* verify slot availability

This concept is called **Tool Calling** in AI systems.

---

# 3. State Management

LangGraph maintains conversation state throughout the workflow.

The state includes:

* user messages
* collected booking information
* tool results
* workflow decisions
* responses

This enables memory-aware conversations.

---

# 4. Conditional Routing

The workflow dynamically decides:

* which agent runs next
* whether tools should execute
* when the workflow should terminate

---

# 5. Data Abstraction Layer

Agents never directly manipulate CSV files.

Instead:

* tools manage all data operations
* agents focus only on reasoning and communication

This design improves:

* modularity
* maintainability
* scalability

Future upgrades become easier.

Example:

* CSV → MySQL
* CSV → PostgreSQL
* CSV → MongoDB

without changing agent logic.

---

# AI Engineering Concepts Demonstrated

This project demonstrates several important modern AI engineering concepts:

* Multi-Agent Systems
* Agentic AI
* Tool Calling
* Prompt Engineering
* Workflow Orchestration
* Intent Detection
* Structured Outputs
* Conversational AI
* State Management
* LLM-Based Automation

---

# Educational Importance

This project is highly valuable for learning:

* AI agent development
* real-world LLM workflows
* modular AI architectures
* LangGraph workflows
* LangChain integrations
* conversational automation systems

It provides hands-on experience with practical AI engineering concepts used in modern intelligent applications.

---

# Conclusion

The Dental Appointment Management System is a complete AI-powered multi-agent application that demonstrates how intelligent agents can collaborate to automate real-world workflows through natural language conversations.

By combining LangGraph, LangChain, GPT-OSS-120B, and Groq, the project showcases a scalable and modular architecture for building modern conversational AI systems.


summrize this and add to the post

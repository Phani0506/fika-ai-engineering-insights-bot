# AI-Powered Dev Insights Bot

This project is an MVP implementation of a chat-first, AI-powered view of engineering performance, delivered inside Slack. It uses LangGraph to orchestrate agents that fetch, analyze, and narrate development metrics based on mock data.

---

## 🏛️ Architecture

The system follows an agentic, multi-step process orchestrated by LangGraph. A user's command in Slack triggers a chain of agents that pass state to one another, culminating in a report posted back to the user.

```mermaid
graph TD
    A[User in Slack] -- /dev-report --> B[Slack Bot (slack_bot.py)];
    B --> C{LangGraph Workflow (graph.py)};
    C -- 1. Invoke w/ period --> D[Node: DataHarvester];
    D -- Fetches from --> E[(SQLite DB)];
    D -- Raw Data --> F[Node: DiffAnalyst];
    F -- Analyzed Metrics --> G[Node: InsightNarrator];
    G -- AI-Generated Narrative --> H[Final Report];
    F -- Metrics --> I[Chart Generator (utils.py)];
    I -- Chart Image --> H;
    H --> B;
    B -- Posts Message & Chart --> A;
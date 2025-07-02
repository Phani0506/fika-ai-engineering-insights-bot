import os
import json
from langchain_groq import ChatGroq
from app.data_store import get_session, Commit, PullRequest
import datetime
import pandas as pd

# Initialize the LLM using Groq.
llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

def data_harvester_node(state):
    print("---AGENT: DataHarvester---")
    period = state['period']
    days = {'weekly': 7, 'monthly': 30}.get(period, 7)
    session = get_session()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    commits = session.query(Commit).filter(Commit.timestamp.between(start_date, end_date)).all()
    prs = session.query(PullRequest).filter(PullRequest.merged_at.between(start_date, end_date)).all()
    session.close()
    state['raw_data'] = {
        "commits": [c.__dict__ for c in commits],
        "prs": [p.__dict__ for p in prs]
    }
    return state

def diff_analyst_node(state):
    print("---AGENT: DiffAnalyst---")
    raw_commits = state['raw_data']['commits']
    raw_prs = state['raw_data']['prs']
    pr_df = pd.DataFrame(raw_prs)
    commit_df = pd.DataFrame(raw_commits)
    deploy_frequency = len(pr_df)
    avg_cycle_time = pr_df['cycle_time_hours'].mean() if not pr_df.empty else 0
    total_additions = commit_df['additions'].sum() if not commit_df.empty else 0
    total_deletions = commit_df['deletions'].sum() if not commit_df.empty else 0
    state['analyzed_data'] = {
        "period": state['period'],
        "dora_metrics": {
            "lead_time_for_changes_hours": round(avg_cycle_time, 2),
            "deployment_frequency": deploy_frequency,
            "change_failure_rate": "0%",
            "mttr_hours": 0
        },
        "code_churn": {
            "total_additions": int(total_additions),
            "total_deletions": int(total_deletions),
            "net_churn": int(total_additions - total_deletions)
        }
    }
    return state

def insight_narrator_node(state):
    print("---AGENT: InsightNarrator---")
    analyzed_data = state['analyzed_data']
    prompt = f"""You are a helpful engineering manager AI assistant. Based on the following JSON data for the past {analyzed_data['period']}, write a concise, data-driven summary for the development team in Slack markdown format.
- Start with a high-level overview.
- Use the DORA metrics (Lead Time, Deployment Frequency) to comment on team velocity and efficiency.
- Comment on the total code churn (additions and deletions).
- Keep the tone neutral, professional, and encouraging. Do not invent data not present in the JSON.
Data:
{json.dumps(analyzed_data, indent=2)}"""
    response = llm.invoke(prompt)
    narrative = response.content
    state['narrative'] = narrative
    with open("data/prompt_log.txt", "a") as f:
        f.write(f"---PROMPT---\n{prompt}\n\n---RESPONSE---\n{narrative}\n\n{'='*20}\n\n")
    return state
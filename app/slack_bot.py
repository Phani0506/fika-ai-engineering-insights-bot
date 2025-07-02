import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from app.graph import graph
from app.utils import create_summary_chart

# Load environment variables from your .env file
load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# Initializes your app
app = App(token=SLACK_BOT_TOKEN)

@app.command("/dev-report")
def handle_dev_report(ack, body, say, client, logger):
    ack()
    channel_id = body['channel_id']
    user_id = body['user_id']
    period = body.get('text', 'weekly').strip().lower()
    if period not in ['weekly', 'monthly']:
        say(text=f"Hi <@{user_id}>, I only support `weekly` or `monthly` reports. Please try again, e.g., `/dev-report weekly`.")
        return
    try:
        # Step 1: Post a temporary "working on it" message
        initial_msg_response = say(text=f"🤖 Roger that, <@{user_id}>! Generating the *{period}* developer insights report. This might take a moment...")
        
        # Step 2: Run the entire LangGraph workflow
        inputs = {"period": period}
        result = graph.invoke(inputs)

        # Step 3: Generate the chart image
        chart_path = create_summary_chart(result['analyzed_data'])

        # ==============================================================================
        # =========================== THE FINAL CODE FIX ===============================
        # ==============================================================================
        
        # Step 4: Post the AI narrative as its own message.
        client.chat_postMessage(
            channel=channel_id,
            text=result['narrative']
        )
        
        # Step 5: Upload the chart file with a simple comment.
        # This is more reliable than using image blocks.
        client.files_upload_v2(
            channel=channel_id,
            file=chart_path,
            initial_comment="Here are the key metrics:",
            title=f"{period.capitalize()} Dev Report Chart"
        )
        
        # Step 6: Delete the original "working on it" message
        client.chat_delete(
            channel=channel_id,
            ts=initial_msg_response['ts']
        )

        # ==============================================================================
        # ========================== END OF FINAL CODE FIX =============================
        # ==============================================================================
        
    except Exception as e:
        logger.error(f"Error handling /dev-report: {e}")
        say(text="😥 Uh oh, something went wrong while generating the report. Please check the application logs.")

if __name__ == "__main__":
    print("⚡️ Dev Insights Bot is running!")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
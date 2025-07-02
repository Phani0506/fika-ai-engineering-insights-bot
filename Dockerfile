FROM python:3.10-slim

WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY ./app /code/app

# The seeder script creates the DB file in the data volume
# So we run it on startup before the bot
CMD sh -c "python -m app.seeder && python -m app.slack_bot"
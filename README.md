# Natural Language (AI) SQL Project - Chatbot Memory Broker

CS 452 - Natural language interface to a database using GPT.

**Domain**: A multi-agent communication broker. Agents write messages and memory entries to a shared database; users query it in plain language to retrieve context and history.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OpenAI**
   - Copy `config.json.example` to `config.json`
   - Add your OpenAI API key to `config.json` (never commit this file!)

3. **Initialize database**
   - Run `setup.sql` and `setupData.sql` (or use the app which does this automatically)

4. **Run the app**
   ```bash
   python db_bot.py
   ```

## Project Structure

- `config.json` - API keys (do not share!)
- `setup.sql` - Database schema
- `setupData.sql` - Sample data
- `db_bot.py` - Main app: natural language → SQL → query → friendly response

## Paper Reference

Read the prompting strategies: https://arxiv.org/abs/2305.11853

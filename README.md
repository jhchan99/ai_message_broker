# Natural Language (AI) SQL Project - Chatbot Memory Broker

CS 452 - Natural language interface to a database using GPT.

**Domain**: A multi-agent communication broker. Agents write messages and memory entries to a shared database; users query it in plain language to retrieve context and history.

## Setup

1. **Create a virtual environment** (recommended on Linux/WSL to avoid externally-managed-environment errors)
   ```bash
   # On WSL/Debian/Ubuntu, install venv first if needed:
   sudo apt install python3.12-venv

   python3 -m venv venv
   source venv/bin/activate   # Linux/WSL
   # or: venv\Scripts\activate   # Windows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenAI**
   - Copy `config.json.example` to `config.json`
   - Add your OpenAI API key to `config.json` (never commit this file!)

4. **Initialize database**
   - Run `setup.sql` and `setupData.sql` (or use the app which does this automatically)

5. **Run the app**
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

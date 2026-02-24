"""
Natural Language SQL Bot - CS 452
Chatbot Memory Broker: multi-agent communication database.
Takes user questions, sends to GPT for SQL, queries DB, returns friendly answer.
"""

import json
import os
import sqlite3
from time import time
from openai import OpenAI

# Paths
FDIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(FDIR, "aidb.sqlite")
SETUP_SQL = os.path.join(FDIR, "setup.sql")
SETUP_DATA_SQL = os.path.join(FDIR, "setupData.sql")
CONFIG_PATH = os.path.join(FDIR, "config.json")
RESPONSES_DIR = os.path.join(FDIR, "response")

SQL_ONLY_REQUEST = (
    " Give me a sqlite select statement that answers the question. "
    "Only respond with sqlite syntax. If there is an error do not explain it!"
)


def init_db():
    """Create/reset database from setup files."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    with open(SETUP_SQL) as f:
        cur.executescript(f.read())
    with open(SETUP_DATA_SQL) as f:
        cur.executescript(f.read())
    return con, cur


def run_sql(cur, query):
    """Execute SQL and return results."""
    return cur.execute(query).fetchall()


def get_openai_client():
    """Load config and create OpenAI client."""
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return OpenAI(api_key=config["openaiKey"])


def sanitize_sql(value):
    """Extract SQL from GPT response (handles ```sql ... ``` blocks)."""
    if "```" in value:
        parts = value.split("```", 2)
        if len(parts) >= 2:
            sql_block = parts[1]
            if "\n" in sql_block:
                sql_block = sql_block.split("\n", 1)[1]
            if "```" in sql_block:
                sql_block = sql_block.split("```")[0]
            return sql_block.strip()
    return value.strip()


def get_chat_response(client, content, model="gpt-4o"):
    """Call GPT and return the response text."""
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    parts = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            parts.append(chunk.choices[0].delta.content)
    return "".join(parts)


def build_strategies(setup_sql):
    """Build prompting strategies (zero-shot, single-domain)."""
    single_domain_example = (
        " Which agent has sent the most messages? "
        "\nSELECT a.name, COUNT(m.message_id) as msg_count "
        "\nFROM agent a JOIN message m ON a.agent_id = m.agent_id "
        "\nGROUP BY a.agent_id ORDER BY msg_count DESC LIMIT 1;\n "
    )
    return {
        "zero_shot": setup_sql + SQL_ONLY_REQUEST,
        "single_domain_double_shot": setup_sql + single_domain_example + SQL_ONLY_REQUEST,
    }


def process_question(client, cur, question, strategy_prompt, schema_sql):
    """Full pipeline: question -> GPT (SQL) -> query -> GPT (friendly answer)."""
    prompt = strategy_prompt + " " + question
    sql_response = get_chat_response(client, prompt)
    sql_query = sanitize_sql(sql_response)

    try:
        raw_results = run_sql(cur, sql_query)
        raw_str = str(raw_results)
    except Exception as e:
        return {
            "question": question,
            "sql": sql_query,
            "queryRawResponse": None,
            "friendlyResponse": f"SQL error: {e}",
            "error": str(e),
        }

    # Improved friendly prompt: include schema context so GPT can interpret IDs
    friendly_prompt = (
        f'Database schema (for reference):\n{schema_sql}\n\n'
        f'I asked: "{question}"\n'
        f'The SQL query returned: {raw_str}\n\n'
        "Give a concise, friendly answer in plain English. "
        "If the result contains IDs, resolve them to names/readable values using the schema. "
        "Do not suggest alternatives or add extra chatter."
    )
    friendly_response = get_chat_response(client, friendly_prompt)

    return {
        "question": question,
        "sql": sql_query,
        "queryRawResponse": raw_str,
        "friendlyResponse": friendly_response,
        "error": "None",
    }


def main():
    print("Natural Language SQL Bot - Chatbot Memory Broker")
    con, cur = init_db()
    print("Database initialized.")
    os.makedirs(RESPONSES_DIR, exist_ok=True)

    with open(SETUP_SQL) as f:
        setup_sql = f.read()

    with open(CONFIG_PATH) as f:
        config = json.load(f)
    client = OpenAI(api_key=config["openaiKey"])

    strategies = build_strategies(setup_sql)
    questions = [
        "Which agent has sent the most messages?",
        "What memory entries does MemoryKeeper have?",
        "What did the Assistant say in the task_delegation conversation?",
        "Which conversations have more than 2 messages?",
        "What is stored under the key 'deadline' in memory?",
        "List all agents and their roles.",
    ]

    for strategy_name, strategy_prompt in strategies.items():
        print("\n" + "=" * 60)
        print(f"Strategy: {strategy_name}")
        results = []
        for q in questions:
            print("\n---")
            print("Question:", q)
            r = process_question(client, cur, q, strategy_prompt, setup_sql)
            print("SQL:", r["sql"])
            print("Raw:", r["queryRawResponse"])
            print("Friendly:", r["friendlyResponse"])
            if r["error"] != "None":
                print("Error:", r["error"])
            results.append(r)

        out = {
            "strategy": strategy_name,
            "prompt_prefix": strategy_prompt,
            "questionResults": results,
        }
        out_path = os.path.join(RESPONSES_DIR, f"response_{strategy_name}_{int(time())}.json")
        with open(out_path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nSaved to {out_path}")

    cur.close()
    con.close()
    print("\nDone!")


if __name__ == "__main__":
    main()

# Chatbot Memory Broker

A database that serves as shared memory and message passing for multiple chatbot agents. Agents write facts and messages to the DB; users query it in natural language to retrieve context and history.

## Schema

- **agent** – Agents that can read/write (id, name, role)
- **conversation** – Threads or sessions (id, topic, created_at)
- **message** – Messages between agents (agent_id, conversation_id, content, created_at)
- **memory_entry** – Key-value facts agents store for recall (agent_id, key, value, created_at)

*(Add schema.png here after generating with drawSQL.app or schemacrawler)*

---

## Query that worked well

**Question**: Which agent has sent the most messages?

**GPT SQL Response**:
```sql
SELECT a.name, COUNT(m.message_id) as msg_count
FROM agent a JOIN message m ON a.agent_id = m.agent_id
GROUP BY a.agent_id ORDER BY msg_count DESC LIMIT 1;
```

**Friendly Response**: The agent who has sent the most messages is "Assistant," with a total of 3 messages.

---

## Query that tripped up

**Question**: What did the Assistant say in the task_delegation conversation?

**Zero-shot SQL** (correct – filters by agent):
```sql
SELECT m.content FROM message m
JOIN conversation c ON m.conversation_id = c.conversation_id
JOIN agent a ON m.agent_id = a.agent_id
WHERE c.topic = 'task_delegation' AND a.name = 'Assistant';
```
**Result**: "I will remind you before the deadline." (correct – only Assistant's message)

**Single-domain SQL** (wrong – returned all messages in conversation):
```sql
SELECT m.content FROM message m
JOIN conversation c ON m.conversation_id = c.conversation_id
WHERE c.topic = 'task_delegation' AND c.conversation_id = m.conversation_id;
```
**Result**: Returned 4 messages from Router, MemoryKeeper, Assistant, Summarizer – not just Assistant.

**What went wrong**: The single-domain example (about "which agent has most messages") didn't teach the model to filter by agent when asking "what did X say." The zero-shot version correctly added the `JOIN agent` and `a.name = 'Assistant'` filter.

---

## Prompting strategies

- **Zero-shot**: Schema + "give SQLite SELECT only" + question. No examples.
- **Single-domain double-shot**: Schema + one (question, SQL) example from the same domain + question.

**Observations**: Zero-shot worked better on "what did Assistant say" because it correctly inferred the need to filter by agent. Single-domain sometimes produced more readable output (e.g., including topic names instead of IDs) but could miss filters when the example didn't cover that pattern.

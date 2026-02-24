# Example Questions (6+)

| # | Question | SQL | Response |
|---|----------|-----|----------|
| 1 | Which agent has sent the most messages? | `SELECT a.name, COUNT(m.message_id) ... GROUP BY a.agent_id ORDER BY msg_count DESC LIMIT 1` | Assistant has sent the most messages (3). |
| 2 | What memory entries does MemoryKeeper have? | `SELECT key, value FROM memory_entry JOIN agent ... WHERE agent.name = 'MemoryKeeper'` | theme: dark, layout: compact, deadline: Friday 5pm, project: Natural Language SQL |
| 3 | What did the Assistant say in the task_delegation conversation? | `SELECT m.content FROM message m JOIN conversation c ... JOIN agent a ... WHERE c.topic = 'task_delegation' AND a.name = 'Assistant'` | "I will remind you before the deadline." |
| 4 | Which conversations have more than 2 messages? | `SELECT c.topic FROM conversation c JOIN message m ... GROUP BY c.conversation_id HAVING COUNT(m.message_id) > 2` | task_delegation has more than 2 messages. |
| 5 | What is stored under the key 'deadline' in memory? | `SELECT value FROM memory_entry WHERE key = 'deadline'` | Friday 5pm |
| 6 | List all agents and their roles. | `SELECT name, role FROM agent` | Assistant: helper, Summarizer: summarizer, Router: router, MemoryKeeper: memory |
| 7 | *(Add your own question)* | | |
| 8 | *(Add your own question)* | | |

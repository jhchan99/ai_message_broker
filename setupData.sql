-- Sample data for chatbot memory broker

INSERT INTO agent (agent_id, name, role) VALUES
(1, 'Assistant', 'helper'),
(2, 'Summarizer', 'summarizer'),
(3, 'Router', 'router'),
(4, 'MemoryKeeper', 'memory');

INSERT INTO conversation (conversation_id, topic, created_at) VALUES
(1, 'user_preferences', '2026-02-20 10:00:00'),
(2, 'task_delegation', '2026-02-21 14:30:00'),
(3, 'context_recall', '2026-02-22 09:15:00');

INSERT INTO message (message_id, agent_id, conversation_id, content, created_at) VALUES
(1, 1, 1, 'The user prefers dark mode and compact layouts.', '2026-02-20 10:01:00'),
(2, 2, 1, 'Noted: dark mode, compact layouts.', '2026-02-20 10:02:00'),
(3, 3, 2, 'Routing task to MemoryKeeper for storage.', '2026-02-21 14:31:00'),
(4, 4, 2, 'Stored: deadline is Friday 5pm.', '2026-02-21 14:32:00'),
(5, 1, 2, 'I will remind you before the deadline.', '2026-02-21 14:33:00'),
(6, 1, 3, 'Recalling user preferences from memory.', '2026-02-22 09:16:00'),
(7, 4, 3, 'Retrieved: dark mode, compact, deadline Friday 5pm.', '2026-02-22 09:17:00'),
(8, 2, 2, 'Summary: task delegated, deadline stored.', '2026-02-21 14:35:00');

INSERT INTO memory_entry (memory_id, agent_id, key, value, created_at) VALUES
(1, 4, 'theme', 'dark', '2026-02-20 10:02:00'),
(2, 4, 'layout', 'compact', '2026-02-20 10:02:00'),
(3, 4, 'deadline', 'Friday 5pm', '2026-02-21 14:32:00'),
(4, 4, 'project', 'Natural Language SQL', '2026-02-22 09:00:00'),
(5, 2, 'last_summary', 'User prefs and deadline stored.', '2026-02-21 14:35:00');

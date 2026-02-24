-- Chatbot Memory Broker: multi-agent communication database
-- Agents write messages and memory entries; shared DB enables passing information between agents

create table agent (
  agent_id integer primary key,
  name varchar(50) not null,
  role varchar(50)
);

create table conversation (
  conversation_id integer primary key,
  topic varchar(100),
  created_at datetime default current_timestamp
);

create table message (
  message_id integer primary key,
  agent_id integer not null,
  conversation_id integer not null,
  content text not null,
  created_at datetime default current_timestamp,
  foreign key (agent_id) references agent (agent_id),
  foreign key (conversation_id) references conversation (conversation_id)
);

create table memory_entry (
  memory_id integer primary key,
  agent_id integer not null,
  key varchar(100) not null,
  value text,
  created_at datetime default current_timestamp,
  foreign key (agent_id) references agent (agent_id)
);

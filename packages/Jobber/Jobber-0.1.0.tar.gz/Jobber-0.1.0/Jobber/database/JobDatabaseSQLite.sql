CREATE TABLE IF NOT EXISTS t_jobs(
	id INTEGER,
  parent_id INTEGER,
	name VARCHAR(255),
	description VARCHAR(500),
	drmaa_id VARCHAR(100),
	status VARCHAR(10) NOT NULL,
	job_command VARCHAR(5000),
  error VARCHAR(500),
	is_unique CHAR(1) NOT NULL,
	unique_key VARCHAR(5000),
	is_group_job CHAR(1) NOT NULL,
	max_parallel_nr INTEGER NOT NULL,
	max_nr_of_restarts INTEGER NOT NULL,
	current_run INTEGER NOT NULL,
	start_submit_date TIMESTAMP DEFAULT 0,
	end_submit_date TIMESTAMP DEFAULT 0,
  start_run_date TIMESTAMP DEFAULT 0,
  end_run_date TIMESTAMP DEFAULT 0,
	delete_time BIGINT,
	who_create VARCHAR(200),
	who_update VARCHAR(200),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  executer VARCHAR(20),
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS t_jobs_parent_status ON t_jobs (parent_id, status);
CREATE INDEX IF NOT EXISTS t_jobs_status_name ON t_jobs(status, name);

CREATE TABLE IF NOT EXISTS t_job_options(
	id INTEGER,
	t_job_id INTEGER NOT NULL,
	option_name VARCHAR(100),
	option_value VARCHAR(500),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS t_job_dependencies(
	t_job_id INTEGER NOT NULL,
	t_job_dependency_id INTEGER NOT NULL,
	dependency_job_status VARCHAR(10) NOT NULL,
	PRIMARY KEY(t_job_id, t_job_dependency_id, dependency_job_status)
);

CREATE TABLE IF NOT EXISTS t_job_messages (
  id INTEGER,
  t_job_id INTEGER,
  transaction_id VARCHAR(300),
  type VARCHAR(20) NOT NULL,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  message VARCHAR(1000),
  response_id VARCHAR(50),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS t_job_responses (
  id VARCHAR(50),
  message VARCHAR(1000),
  success TINYINT,
  create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);
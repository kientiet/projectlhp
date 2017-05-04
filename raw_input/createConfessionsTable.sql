use lhpconfessions;
create table confessions (
id INT AUTO_INCREMENT,
status_id varchar(50),
status_type text,
status_message text,
link_name text,
status_published date,
num_reactions int,
num_comments int,
num_shares int,
num_likes int,
num_loves int,
num_wows int,
num_hahas int,
num_sads int,
num_angrys int,
from_school text,
primary key (id)
)
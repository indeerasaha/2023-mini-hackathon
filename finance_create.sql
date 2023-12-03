create table user
	(username		varchar(20),
    password        varchar(20),
    balance         numeric(7,2),
    card_number     numeric(16,0),
    cvv             numeric(3,0),
    exp_date        date,
    credit_score    numeric(3,0),
	 primary key (username)
	);

create table loan_application
    (username       varchar(20),
    application_id  numeric(7,0),
    bio             varchar(300), -- 300 char limit
    total_amount    numeric(5,2), -- 99,999 limit
    lender_username varchar(20),
    primary key(username, application_id),
    foreign key(username) references user(username)
    );
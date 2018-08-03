-- load this file with
--
-- psql -U isdb -d score -f load_beta.sql



DROP TABLE IF EXISTS beta_values CASCADE;
CREATE TABLE beta_values (
    stakeholder    text,
    donation_type  integer,
    size           real,
    access         real,
    income         real,       -- <--- replace with enumerated type
    poverty        real,
    last_donation      real,       -- <--- replace with enumerated type
    distance         real,
    same_donation  real,
    different_donation  real,        -- <--- replace with enumerated type
    pid text
);

\copy beta_values FROM 'csv/betas.csv' csv header;

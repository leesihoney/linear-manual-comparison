-- load this file with
--
-- psql -U isdb -d score -f load_beta.sql



DROP TABLE IF EXISTS beta_values CASCADE;
CREATE TABLE beta_values (
    stakeholder    text,
    donation_type  text,
    size           decimal,
    access         decimal,
    income         decimal,       -- <--- replace with enumerated type
    poverty        decimal,
    last_donation      decimal,       -- <--- replace with enumerated type
    distance         decimal,
    same_donation  decimal,
    different_donation  decimal,        -- <--- replace with enumerated type
    pid text
);

\copy beta_values FROM 'csv/betas.csv' csv header;

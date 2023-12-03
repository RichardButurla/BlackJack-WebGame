-- Create user_game_statistics table
--Holds individual game related data

create table user_game_statistics (
    user varchar(32) not null,
    outcomes varchar(9) not null,
);

-- Create user_statistics table
--Holds overall game related data
create table user_statistics (
    user varchar(32) not null,
    win_rate decimal(2,2) not null,
    bust_rate decimal(2,2) not null,
    highest_win_streak int,
);
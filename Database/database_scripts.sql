/* This file can be run to create the necessary objects for
    a Dao game database */

/* Create the Database */
CREATE DATABASE DAOdb;
GO

/* Create database objects schemas */
USE DAOdb;
GO
CREATE SCHEMA game
CREATE SCHEMA plyr
CREATE SCHEMA fun
;

/* Create tables for game data */
USE DAOdb;
GO
CREATE TABLE [game].[history_log] (
    gameID int PRIMARY KEY,
    black_player_id int FOREIGN KEY,
    white_player_id int FOREIGN KEY,
    start_game SMALLDATETIME not null,
    end_game SMALLDATETIME,
    duration int,
    game_result_id int FOREIGN KEY,
    black_score decimal(1,1),
    white_score decimal(1,1),
    winning_position_id int FOREIGN KEY
);

/* Create dimensions for game data */
USE DAOdb;
GO
CREATE TABLE [game].[game_results] (
    game_result_id int PRIMARY KEY,
    result_desc varchar(10)
);
        INSERT INTO [game].[game_results] (game_result_id, result_desc)
        VALUES ( (1, "Win"), (5, "Draw"), (9, "Incomplete") );

CREATE TABLE [game].[win_positions] (
    winning_position_id int PRIMARY KEY,
    win_positon_desc varchar(50)
);
        INSERT INTO [game].[win_positions] (winning_position_id, win_positon_desc)
        VALUES ( (1, "Line"), (2, "Square"), (4, "4 Corners"), (13, "Smothered"), (666, "Concede") );

/* Create dimensions for player data */
USE DAOdb;
GO
CREATE TABLE [plyr].[players] (
    player_id int PRIMARY KEY,
    player_name varchar(25)
);
        INSERT INTO [plyr].[players] (player_id, player_name)
        VALUES ( (1, "Blapo"), (2,"donny"), (69, "zaser") );

/* Create tables for other game statistics */
USE DAOdb;
GO
CREATE TABLE [fun].[fun_positions] (
    fun_position_id int PRIMARY KEY,
    fun_position_desc varchar(50)
);
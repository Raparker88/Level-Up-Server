

SELECT
    g.id,
                        g.title,
                        g.maker,
                        g.gametype_id,
                        g.number_of_players,
                        g.skill_level,
                        u.id user_id,
                        u.first_name || ' ' || u.last_name AS full_name
                    FROM
                        levelupapi_game g
                    JOIN
                        levelupapi_gamer gr ON g.gamer_id = gr.id
                    JOIN
                        auth_user u ON gr.user_id = u.id
                    ;

SELECT * FROM levelupapi_event;
SELECT * FROM levelupapi_eventgamer;



SELECT 
    e.id,
    e.day,
    e.time,
    g.title,
    u.first_name || " " || u.last_name full_name,
    eg.gamer_id

FROM levelupapi_event e
JOIN levelupapi_game g ON e.game_id = g.id
JOIN levelupapi_eventgamer eg ON eg.event_id = e.id
JOIN levelupapi_gamer gr ON eg.gamer_id = gr.id
JOIN auth_user u ON u.id = gr.user_id

;
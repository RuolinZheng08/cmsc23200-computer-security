CREATE DATABASE hw5_db;
USE hw5_db;

CREATE TABLE problem4 (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    page VARCHAR(255),
    cookie VARCHAR(255),
    ip VARCHAR(255),
    window_width INT,
    window_height INT,
    user_agent VARCHAR(255),
    enable_cookie VARCHAR(255),
    do_not_track VARCHAR(255),
    enable_popup VARCHAR(255),
    fonts VARCHAR(255)
);

SELECT page FROM (
    SELECT cookie, ip, window_width, window_height, user_agent, enable_cookie, do_not_track, enable_popup, fonts, JSON_ARRAYAGG(page) AS page FROM problem4 GROUP BY cookie, ip, window_width, window_height, user_agent, enable_cookie, do_not_track, enable_popup, fonts
    ) as T;
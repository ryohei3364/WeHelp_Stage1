# Task 2:

- ## Create a new database named website.
  ```
  CREATE DATABASE website;
  ```
  <p align='left'><img src='./screenshots/task2_01.png#pic_right' width='45%'/></p>

- ## Create a new table named member, in the website database.
  ```
  CREATE TABLE member(	
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
  );

  DESC member;
  ```
  <p align='left'><img src='./screenshots/task2_03.png#pic_right' /></p>


# Task 3:

- ## INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
  ```
  INSERT INTO member(name, username, password) VALUES('test', 'test', 'test');
  INSERT INTO member(name, username, password) VALUES('玉婷', 'YU', '0000');
  INSERT INTO member(name, username, password) VALUES('小王', 'wang', '1234');
  INSERT INTO member(name, username, password) VALUES('Jay Chen', 'jay', 'aaaa');
  INSERT INTO member(name, username, password) VALUES('劉大明', 'ming', 'ccdd');
  ```
  <p align='left'><img src='./screenshots/task3_01.png#pic_right' /></p>
  
- ## SELECT all rows from the member table.
  ```
  SELECT * FROM member;
  ```
  <p align='left'><img src='./screenshots/task3_02.png#pic_right' /></p>
  
- ## SELECT all rows from the member table, in descending order of time.
  ```
  SELECT * FROM member
  ORDER BY time DESC;
  ```
  <p align='left'><img src='./screenshots/task3_03.png#pic_right' /></p>

- ## SELECT total 3 rows, second to fourth, from the member table, in descending order of time.
  ```
  SELECT * FROM member
  ORDER BY time DESC
  LIMIT 3 OFFSET 1;
  ```
  <p align='left'><img src='./screenshots/task3_04.png#pic_right' /></p>

- ## SELECT rows where username equals to test.
  ```
  SELECT * FROM member WHERE username='test';
  ```
  <p align='left'><img src='./screenshots/task3_05.png#pic_right' /></p>

- ## SELECT rows where name includes the es keyword.
  ```
  SELECT * FROM member WHERE name LIKE '%es%';
  ```
  <p align='left'><img src='./screenshots/task3_06.png#pic_right' /></p>

- ## SELECT rows where both username and password equal to test.
  ```
  SELECT * FROM member WHERE username='test' AND password='test';
  ```
  <p align='left'><img src='./screenshots/task3_07.png#pic_right' /></p>

- ## UPDATE data in name column to test2 where username equals to test.
  ```
  UPDATE member SET name='test2' WHERE username='test';
  ```
  <p align='left'><img src='./screenshots/task3_08.png#pic_right' /></p>
  

# Task 4:

- ## SELECT how many rows from the member table.
  ```
  SELECT COUNT(id) FROM member;
  ```
  <p align='left'><img src='./screenshots/task4_01.png#pic_right' width='50%'/></p>

- ## SELECT the sum of follower_count of all the rows from the member table.

  ### Since my default setting is all users with 0 follower count, I update the data first as below for further calculation.
  ```
  UPDATE member SET follower_count=300 WHERE id=1;
  UPDATE member SET follower_count=50 WHERE id=2;
  UPDATE member SET follower_count=500 WHERE id=3;
  UPDATE member SET follower_count=10 WHERE id=4;
  UPDATE member SET follower_count=200 WHERE id=5;

  SELECT * FROM member;
  ```
  <p align='left'><img src='./screenshots/task4_02.png#pic_right'/></p>

  ```
  SELECT SUM(follower_count) FROM member;
  ```
  <p align='left'><img src='./screenshots/task4_03.png#pic_right' width='65%'/></p>

- ## SELECT the average of follower_count of all the rows from the member table.
  ```
  SELECT AVG(follower_count) FROM member;
  ```
  <p align='left'><img src='./screenshots/task4_04.png#pic_right' width='65%'/></p>

- ## SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
  ```
  SELECT AVG(follower_count)
  FROM (
    SELECT follower_count FROM member
    ORDER BY follower_count DESC
    LIMIT 2
  ) AS top_members;
  ```
  <p align='left'><img src='./screenshots/task4_05.png#pic_right' width='60%'/></p>


# Task 5:

- ## Create a new table named message, in the website database.
  ```
  CREATE TABLE message(	
    id BIGINT AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    content VARCHAR(255) NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(member_id) REFERENCES member(id)
  );
  ```
  <p align='left'><img src='./screenshots/task5_01.png#pic_right'/></p>

- ## SELECT all messages, including sender names. We have to JOIN the member table to get that.

  ### First, I insert data into message table.
  ```
  INSERT INTO message(member_id, content, like_count)
  VALUES
  (1, '第一次加入新手村，請大家多多指教', 58),
  (2, '興趣是耍廢耍懶耍自閉', 15),
  (3, '沒啥特別理由', 3),
  (4, '新北金城武報到', 45),
  (5, '安安我是大明', 39);
  ```
  ### Then, select sender names from member table and join data into message table.

  ```
  SELECT * FROM member INNER JOIN message ON member.id=message.member_id;
  ```
  <p align='left'><img src='./screenshots/task5_02.png#pic_right'/></p>

- ## SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
  ```
  SELECT * FROM member INNER JOIN message 
  ON member.id=message.member_id 
  WHERE member.username='test';
  ```
  <p align='left'><img src='./screenshots/task5_03.png#pic_right'/></p>

- ## Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
  ```
  SELECT member.username, AVG(like_count) FROM message INNER JOIN member
  ON member.id=message.member_id
  WHERE member.username='test';
  ```
  <p align='left'><img src='./screenshots/task5_04.png#pic_right'/></p>

- ## Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
  ```
  SELECT member.username, AVG(like_count) FROM message INNER JOIN member
  ON member.id=message.member_id
  GROUP BY member.username;
  ```
  <p align='left'><img src='./screenshots/task5_05.png#pic_right'/></p>


use homies;
CREATE TABLE Properties (`property_id` int auto_increment primary key ,`seller_type` text, `bedroom` int, `layout_type` text,
 `property_type` text, `locality` text, `price` text, `area` int, `furnish_type` text, 
 `bathroom` int, `status` text,`city` text);
CREATE TABLE Users (`user_id` int auto_increment primary key,`user_name` text, `email` text, `phone number` text, `password` text);
select * from properties;
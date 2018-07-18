
create table recipe
  (
    id serial PRIMARY KEY,
    name text,
    creator text,
    description text,
    insert_date timestamp DEFAULT now(),
    create_date timestamp,
    suspend_date timestamp,
    cooking_time integer, --seconds
    isactive boolean default True,
  UNIQUE(name, creator)
  );

create table ingredient
  (
    id serial PRIMARY KEY,
    name text,
    description text,
    insert_date timestamp DEFAULT now(),
    UNIQUE(name)
  );

create table measurements
  (
    id serial PRIMARY KEY,
    measurement decimal,
    unit text,
    UNIQUE(measurement,unit)
  );

create table recipe_ingredient_map
  (
    id serial PRIMARY KEY,
    ingredient_id integer REFERENCES ingredient (id),
    recipe_id integer REFERENCES recipe (id),
    measurements_id integer REFERENCES measurements (id),
    UNIQUE(ingredient_id,recipe_id, measurements_id)
  );

create table users
  (
    id serial PRIMARY KEY,
    insert_date timestamp DEFAULT now(),
    create_date timestamp,
    suspend_date timestamp,
    first_name text,
    last_name text,
    sex text,
    address text,
    phone text,
    isactive boolean DEFAULT True,
    UNIQUE(first_name,last_name,address)
  );

create table user_diet_preference_map
  (
    id serial PRIMARY KEY,
    insert_date timestamp DEFAULT now(),
    create_date timestamp,
    ingredient_id integer REFERENCES ingredient (id),
    user_id integer REFERENCES users (id),
    isactive boolean DEFAULT True,
    UNIQUE(ingredient_id,user_id)
  );

create table review
  (
    id serial PRIMARY KEY,
    insert_date timestamp DEFAULT now(),
    review_date timestamp,
    user_id integer REFERENCES users (id),
    recipe_id integer REFERENCES recipe (id),
    review text,
    rating smallint, -- (1-5)
    UNIQUE(user_id,recipe_id,rating)
 );

create table cooking_preferrence
  (
    id serial PRIMARY KEY,
    preferrence text,
    insert_date timestamp DEFAULT now(),
    UNIQUE(preferrence)
  );

create table cooking_preferrence_map
  (
    id serial PRIMARY KEY,
    user_id integer REFERENCES users (id),
    recipe_id integer REFERENCES recipe (id),
    ingredient_id integer REFERENCES ingredient (id),
    preferrence_id integer REFERENCES cooking_preferrence (id),
    UNIQUE(user_id,recipe_id,ingredient_id,preferrence_id)
  );

  -- There the QR code will be combination of
  -- user_id, recipe_id, order_preferrence, id, food_expire_date, food_prepare_date

CREATE TYPE order_status AS ENUM ('ordered', 'kitchen_syn', 'kitchen_ack','preparation','shipped', 'received');

create table order_details
  (
    id serial PRIMARY KEY,
    insert_date timestamp DEFAULT now(),
    order_date timestamp,
    status order_status,
    order_preferrence jsonb, -- cooking_preferrence, user_diet_preference
    order_status_timestamp jsonb, -- ordered, kitchen_syn, kitchen_ack, preparation, shipped, received
    kitchen_order_number integer,
    kitchen_vendor text,
    shipping_vendor text,
    shipping_order_number integer,
    user_id integer REFERENCES users (id),
    recipe_id integer REFERENCES recipe (id),
    quantity integer,
    food_prepare_date timestamp,
    food_expire_date timestamp
  );




-------------------------------------------Robot -------------------------------
--Actions
--'user_scanned', 'powering_on', 'powered_on','idle', 'loaded', 'cooking', 'done', 'powering_off','powered_off', 'user_notify','interrupt', 'cleaning','started_video_capture', 'stopped_video_capture', 'saved_video_disc'

create table robot_action
  (
    id serial PRIMARY KEY,
    action text,
    insert_date timestamp DEFAULT now(),
    create_date timestamp,
    UNIQUE(action)
  );

--User_Notifications
--'Food is stale', 'Pan is Missing', 'New Update Available', 'Connect To Wifi' 'Cooking Interrupted', 'Critical Error', 'Cleaning'

create table notification
  (
    id serial PRIMARY KEY,
    notification text,
    insert_date timestamp DEFAULT now(),
    create_date timestamp,
    UNIQUE(notification)
  );


create table scan
  (
    id serial PRIMARY KEY,
    order_id integer,
    order_detail jsonb, -- cooking_preferrence, user_diet_preference, user, recipe
    insert_date timestamp DEFAULT now(),
    scan_date timestamp,
    UNIQUE(order_detail)
  );

create table notify_audit_log
  (
    id serial PRIMARY KEY,
    notification_id integer REFERENCES notification (id),
    robot_action_id integer REFERENCES robot_action (id),
    scan_id integer REFERENCES scan (id),
    insert_date timestamp DEFAULT now(),
    UNIQUE(notification_id,robot_action_id,scan_id)
  );

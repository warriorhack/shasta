--db_data = (first_name,last_name,sex,address,phone,user_create_date,ingredient,ing_create_date)
CREATE OR REPLACE FUNCTION public.sp_insert_user(
  t_first_name text,
  t_last_name text,
  sex text,
  t_address text,
  phone text,
  user_create_date timestamp,
  ingredient text,
  ing_create_date timestamp
)
  RETURNS integer AS
  $BODY$
DECLARE
  user_val integer;
  ingre_val integer;
  user_pref_val integer;
BEGIN
  SELECT id INTO user_val FROM users WHERE first_name = t_first_name and last_name = t_last_name and address = t_address;
  IF user_val IS NULL THEN
    INSERT INTO users (first_name, last_name, sex, address, phone,create_date) values (t_first_name,t_last_name,sex, t_address, phone, user_create_date) RETURNING id INTO user_val;
  END IF;
  SELECT id INTO ingre_val FROM ingredient WHERE name = ing_name;
  IF ingre_val IS NULL THEN
    INSERT INTO ingredient (name, description) values (ing_name, ing_description) RETURNING id INTO ingre_val;
  END IF;
  SELECT id INTO user_pref_val FROM user_diet_preference_map WHERE ingredient_id = ingre_val and user_id = user_val;
  IF user_pref_val IS NULL THEN
    INSERT INTO user_diet_preference_map (ingredient_id, user_id, create_date) values (ingre_val, user_val, ing_create_date) RETURNING id into user_pref_val;
  END IF;

  return user_pref_val;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

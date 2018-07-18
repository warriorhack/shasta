--db_data = (recipe_name,creator,description,create_date,cooking_time,ing_name,ing_description,ing_measurement,ing_unit)
CREATE OR REPLACE FUNCTION public.sp_insert_recipe(
  recipe_name text,
  recipe_creator text,
  description text,
  create_date timestamp,
  cooking_time integer,
  ing_name text,
  ing_description text,
  ing_measurement decimal,
  ing_unit text
)
  RETURNS integer AS
  $BODY$
DECLARE
  recipe_val integer;
  ingre_val integer;
  mes_val integer;
  rec_ing_val integer;
BEGIN
  SELECT id INTO recipe_val FROM recipe WHERE name = recipe_name and creator = recipe_creator;
  IF recipe_val IS NULL THEN
    INSERT INTO recipe (name, creator, description, create_date, cooking_time) values (recipe_name,recipe_creator,description, create_date, cooking_time) RETURNING id INTO recipe_val;
  END IF;
  SELECT id INTO ingre_val FROM ingredient WHERE name = ing_name;
  IF ingre_val IS NULL THEN
    INSERT INTO ingredient (name, description) values (ing_name, ing_description) RETURNING id INTO ingre_val;
  END IF;
  SELECT id INTO mes_val FROM measurements WHERE measurement = ing_measurement and unit = ing_unit;
  IF mes_val IS NULL THEN
    INSERT INTO measurements (measurement, unit) values (ing_measurement, ing_unit) RETURNING id into mes_val;
  END IF;
  SELECT id INTO rec_ing_val FROM recipe_ingredient_map WHERE ingredient_id = ingre_val and recipe_id = recipe_val and measurements_id = mes_val;
  IF rec_ing_val IS NULL THEN
    INSERT INTO recipe_ingredient_map (ingredient_id, recipe_id, measurements_id) values (ingre_val, recipe_val, mes_val) RETURNING id INTO rec_ing_val;
  END IF;
  return rec_ing_val;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

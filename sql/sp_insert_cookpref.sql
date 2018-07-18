--db_data = (user_id,recipe,ingredient,preferrence)
CREATE OR REPLACE FUNCTION public.sp_insert_cookpref(
  user_id integer,
  recipe text,
  ingredient text,
  prefer text
)
  RETURNS integer AS
  $BODY$
DECLARE
  user_val integer;
  recipe_val integer;
  ingre_val integer;
  pref_val integer;
  cook_pref_val integer;
BEGIN
  SELECT id INTO user_val FROM users WHERE id = user_id;
  IF NOT user_val IS NULL THEN
    SELECT id INTO recipe_val FROM recipe WHERE name = recipe;
    IF NOT recipe_val IS NULL THEN
      SELECT id INTO ingre_val FROM ingredient WHERE name = ingredient;
      IF NOT ingre_val IS NULL THEN
        SELECT id INTO pref_val FROM cooking_preferrence WHERE preferrence = prefer;
        IF pref_val IS NULL THEN
          INSERT INTO cooking_preferrence (preferrence) values (prefer) RETURNING id INTO pref_val;
        END IF;
        SELECT id INTO cook_pref_val FROM cooking_preferrence_map WHERE user_id = user_val AND recipe_id = recipe_val AND ingredient_id = ingre_val AND preferrence_id = pref_val;
        IF cook_pref_val IS NULL THEN
          INSERT INTO cooking_preferrence_map (user_id,recipe_id,ingredient_id,preferrence_id) values (user_val, recipe_val, ingre_val, pref_val) RETURNING id INTO cook_pref_val;
        END IF;
      END IF;
    END IF;
  END IF;
  return cook_pref_val;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

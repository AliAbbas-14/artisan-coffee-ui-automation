from behave import given, then

@given('test data is loaded from Excel sheet "{sheet_name}" for scenario "{scenario_id}"')
def step_load_excel_data(context, sheet_name, scenario_id):
    records = context.data_mgr.excel.read_sheet_as_dicts(sheet_name)
    matched = next((r for r in records if r.get("scenario_id") == scenario_id), None)
    assert matched is not None, f"Scenario ID '{scenario_id}' not found in sheet '{sheet_name}'"
    context.test_record = matched

@then('the UI menu should feature the coffee item specified in the Excel dataset')
def step_assert_excel_item_in_menu(context):
    product_name = context.test_record.get("product_name")
    assert context.menu_page.has_product(product_name), f"Excel product '{product_name}' not displayed in menu"

@given('test records are queried from the SQLite database table "{table_name}"')
def step_query_sqlite_records(context, table_name):
    query = f"SELECT name, price, origin FROM {table_name} LIMIT 3"
    records = context.data_mgr.db.execute_query(query)
    assert len(records) > 0, f"No records returned from table '{table_name}'"
    context.db_records = records

@then('the UI menu should display the products fetched from the database')
def step_assert_db_products_in_menu(context):
    for rec in context.db_records:
        name = rec["name"]
        assert context.menu_page.has_product(name), f"Database product '{name}' not found on UI menu"

@given('test criteria is fetched from Redis cache key "{cache_key}"')
def step_fetch_redis_cache(context, cache_key):
    cached_data = context.data_mgr.redis.get_json(cache_key)
    assert cached_data is not None and len(cached_data) > 0, f"No cached data for key '{cache_key}'"
    context.cached_items = cached_data

@then('the UI menu should display the cached coffee items')
def step_assert_cached_items_in_menu(context):
    for item in context.cached_items:
        name = item["name"]
        assert context.menu_page.has_product(name), f"Cached product '{name}' not found on UI menu"

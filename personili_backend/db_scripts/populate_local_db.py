from psycopg2 import connect
import os
from faker import Faker


faker = Faker()

def connect_to_database():
    # Connect to the database
    db = connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT")
    )
    return db

def insert_static_data(db):
    """
    Insert data into static tables that shouldn't be modified by the user
    - Category table
    - Theme table
    - Delivery methods
    - Personalizables
    - Personalizable zones
    - Options
    - Option values
    - Personalizable options
    - Personalization types
    - Personalization methods
    - Organizations
    - Organization profiles
    - Workshops
    - Inventories
    - Inventory items
    - Accounts
    """
    # CATEGORY TABLE
    # Prepare the data
    category_data = [
        # Home decor
        ("14a70128-56f1-4881-a63d-e09636e812bd", "Home Decor", "image_path1", "logo_path1",  None, "Available", faker.date_time(), faker.date_time()),
        ("9c75b9b7-f047-403b-a715-f99c0ef26283", "paintings", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd","Available", faker.date_time(), faker.date_time()),
        ("ee6bf500-d74b-4510-8a0b-8a610111d619", "blankets", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd","Available", faker.date_time(), faker.date_time()),
        ("59a77ce4-971a-46bd-8988-39080f0d9c25", "pillows", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd","Available", faker.date_time(), faker.date_time()),
        
        # Tech accessories
        ("14a70128-56f1-4881-a63d-10963658123d", "Tech Accessories", "image_path2", "logo_path2", None, "Available", faker.date_time(), faker.date_time()),
        ("79ee3fcf-42c2-4906-badf-8380904792dc", "Phone cases", "image_path2", "logo_path2", "14a70128-56f1-4881-a63d-10963658123d", "Available", faker.date_time(), faker.date_time()),
        ("13a603d6-704d-41e0-8adf-d5ef93582401", "Keychains", "image_path2", "logo_path2", "14a70128-56f1-4881-a63d-10963658123d","Available", faker.date_time(), faker.date_time()),
        
        # Apparel
        ("404bfdf7-b8c4-4d68-ae2b-9e42342b94c6", "Apparel",  "image_path3", "logo_path3", None,"Available", faker.date_time(), faker.date_time()),
        
        ("4c33772d-953d-483f-8111-a112af95d058", "Tops", "image_path1", "logo_path1", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6", "Available",faker.date_time(), faker.date_time()),
        ("bf97280e-cbc3-49ec-ad08-79618a01371b", "Tshirts", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058","Available", faker.date_time(), faker.date_time()),
        ("aa32d550-4e9b-42a0-a6cd-f1062cebb0d0", "Sweatshirts", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058","Available", faker.date_time(), faker.date_time()),
        ("583bea11-39d4-4828-afc3-32b3f151d355", "Sweaters", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058","Available", faker.date_time(), faker.date_time()),
        
        ("e88ba743-e8da-4ef2-91bb-75c164b62144", "Bottoms", "image_path2", "logo_path2", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6","Available", faker.date_time(), faker.date_time()),
        ("5a253d03-f9f5-41ad-9fd5-4189451e1804", "Pants", "image_path2", "logo_path2", "e88ba743-e8da-4ef2-91bb-75c164b62144","Available", faker.date_time(), faker.date_time()),
        ("cb64c665-85f0-4ea6-91f9-4c296945ddd1", "Bras", "image_path2", "logo_path2", "e88ba743-e8da-4ef2-91bb-75c164b62144","Available", faker.date_time(), faker.date_time()),
        
        ("be2d099e-4bab-49b9-aab3-1d63463f384b", "Underwear","image_path3", "logo_path3", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6","Available", faker.date_time(), faker.date_time()),
        ("e2f98d5b-9679-4db5-a7d2-1f71dd1bb441", "Boxers","image_path3", "logo_path3", "be2d099e-4bab-49b9-aab3-1d63463f384b","Available", faker.date_time(), faker.date_time()),
 ]  
    cursor = db.cursor()
    sql_query = "INSERT INTO categories (id, name, image_path, logo_path, parent_category_id, availability_status, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING" 
    
    # Execute the query with the category_data
    cursor.executemany(sql_query, category_data)

    # Commit the changes to the database
    db.commit()

    # THEME TABLE
    # Prepare the data
    theme_data =[
        ("14a70128-56f1-4881-a63d-e09636e812bd", "Nature & environment", faker.paragraph(), "log_path", faker.date_time(), faker.date_time()),
        ("c407faaf-6fd5-4e32-bc32-002e39a8d89e", "Abstract & Geometric", faker.paragraph(), "log_path", faker.date_time(), faker.date_time()),
        ("b4860cc4-f13c-4eb6-bcaa-7df0dce00cc8", "Culture", faker.paragraph(), "log_path",faker.date_time(), faker.date_time()),
        ("ec48f796-78cb-4c80-966f-b778bc85a2cc", "Fantasy", faker.paragraph(), "log_path",faker.date_time(), faker.date_time()),
        ("b1f59f7d-8ad2-4e02-92de-d3f0d879b821", "Science Fiction", faker.paragraph(), "log_path",faker.date_time(), faker.date_time()),
        ("afff6767-ab17-48c7-b0a6-a84f6ded9ff5", "Social & Political", faker.paragraph(), "log_path", faker.date_time(), faker.date_time()),
        ("240a1e1b-72b5-4a95-91e9-e223f6f9faa0", "Food", faker.paragraph(), "log_path",faker.date_time(), faker.date_time()),
        ("74745f05-fb8b-4217-a3c8-d00aa72d415d", "Anime", faker.paragraph(), "log_path", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO themes (id, name, description, logo_path, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    
    # Execute the query with the theme_data
    cursor.executemany(sql_query, theme_data)
    db.commit()

    # Delivery methods
    # Prepare the data : id, name, description, cost, devliery time, created_at, updated_at
    delivery_method_data = [
        ("9b7a49c7-88b6-4767-acf6-c51019ee94b5", "Standard", "Standard delivery method", 0, "3-5 days", faker.date_time(), faker.date_time()),
        ("9382f4f7-97d9-4085-947f-044ec0de6e2e", "Express", "Express delivery method", 5, "1-2 days", faker.date_time(), faker.date_time()),
        ("3373a305-c60c-44c5-be0b-fdada8a41102", "Next day", "Next day delivery method", 10, "1 day", faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO delivery_methods (id, name, description, cost, delivery_time, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"

    # Execute the query with the delivery_method_data
    cursor.executemany(sql_query, delivery_method_data)
    db.commit()


    # Personalizables
    # Prepare the data : id, name, category(must be a leaf category), description, image_path, brand, model, created_at, updated_at 
    personalizable_data = [
        ("cec0b564-ca97-4d1f-9167-44c7d0084471", "Pillow", "59a77ce4-971a-46bd-8988-39080f0d9c25", "sleep pillow", "image path", "generic", "generic", faker.date_time(), faker.date_time()),
        ("700970f2-7d3b-41e4-a625-8e32d7957cc0", "Phone case", "79ee3fcf-42c2-4906-badf-8380904792dc", "phone case", "image path", "generic", "generic", faker.date_time(), faker.date_time()),
        ("33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Tshirt", "bf97280e-cbc3-49ec-ad08-79618a01371b", "blank tshirt", "image path", "generic", "generic", faker.date_time(), faker.date_time()),
        ("0bf45502-8ce8-4a83-b8b0-2071db0b4949", "Pants", "5a253d03-f9f5-41ad-9fd5-4189451e1804", "simple pants", "image path", "generic", "generic", faker.date_time(), faker.date_time()),
        ("6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "Boxers", "e2f98d5b-9679-4db5-a7d2-1f71dd1bb441", "sleep boxers", "image path", "generic", "generic", faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO personalizables (id, name, category_id, description, image_path, brand, model, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"

    # Execute the query with the personalizable_data
    cursor.executemany(sql_query, personalizable_data)
    db.commit()

    # Personalizable zones
    # Prepare the data : id, name, personalizable_id, created_at, updated_at




    # Options
    # Prepare the data : id, name, created_at, updated_at
    option_data = [
        ("345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Color", faker.date_time(), faker.date_time()),
        ("c1622200-8670-45aa-9ae8-a1be7c56d14a", "Size", faker.date_time(), faker.date_time()),
        ("906e811c-2ff6-46fe-ac10-7cdc5020ab1c", "Material", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO options (id, name, created_at, updated_at) VAlUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, option_data)
    db.commit()

    # Option values
    # Prepare the data : id, option_id, value, created_at, updated_at
    option_value_data = [
        # Color
        ("de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Red", faker.date_time(), faker.date_time()),
        ("64bb6750-919d-45ed-a00f-3ea16dc39ea9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Blue", faker.date_time(), faker.date_time()),
        ("6f2a143b-356d-4342-8751-f87d171ecc22", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Green", faker.date_time(), faker.date_time()),
        # Size
        ("e31431a5-0aed-4b3a-94cb-a567fa5e7439", "c1622200-8670-45aa-9ae8-a1be7c56d14a", "Small", faker.date_time(), faker.date_time()),
        ("ecef3173-9c2b-4743-94f4-8a02f7aec69b", "c1622200-8670-45aa-9ae8-a1be7c56d14a", "Medium", faker.date_time(), faker.date_time()),
        ("253886bf-20b3-4b84-9375-d48f779aa026", "c1622200-8670-45aa-9ae8-a1be7c56d14a", "Large", faker.date_time(), faker.date_time()),
        # Material
        ("4ce80fca-af0f-4676-9100-2b748eadb0bf", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", "Cotton", faker.date_time(), faker.date_time()),
        ("0524ad82-10b1-4ce9-9c31-9f94387642c3", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", "Polyester", faker.date_time(), faker.date_time()),
        ("c12018bc-e01b-4a9c-9bb0-2231abf8b2fc", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", "Silk", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO option_values (id, option_id, value, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, option_value_data)
    db.commit()

    # Personalizable options
    # Prepare the data : id, personalizable_id, option_id, option_id, created_at, updated_at
    personalizable_option_data = [
        # Tshirt
        ("0c926a08-d1e7-47c0-adcd-80ec283c5e60", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        ("8c7b726b-74b3-4e77-9fad-14caca27d1d8", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "c1622200-8670-45aa-9ae8-a1be7c56d14a",  faker.date_time(), faker.date_time()),
        ("79adcf21-8147-4df4-8edb-dc2889b2f4c1", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        # Phone case
        ("ee5106fa-b45e-455e-8960-a5a76f7fe1eb", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        ("e2e9b4e5-435c-46bb-a7bc-d2d47784be1e", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        # Pants
        ("3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        ("97bb2b90-8116-44f8-8c61-8faddb971224", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        ("6c20877a-7742-42cb-a789-0e46444628a5", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        # boxer
        ("0c0d9e54-451f-4180-9d88-46cd91382343", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        ("95a9ad8a-01f2-4483-aebd-475d00727c29", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        ("f9a04f3b-fff4-4fef-b2e3-544de2bc75fd", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        # pillows
        ("12acedee-9fe1-4397-a36c-e51235322830", "cec0b564-ca97-4d1f-9167-44c7d0084471", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        ("39e772b7-df9f-44e2-9276-1190ce4530ec", "cec0b564-ca97-4d1f-9167-44c7d0084471", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        ("c7b0798b-6785-4a55-94f6-7b20526df760", "cec0b564-ca97-4d1f-9167-44c7d0084471", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO personalizable_options (id, personalizable_id, option_id, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, personalizable_option_data)
    db.commit()


    # Personalization types
    # Prepare the data : id, name, description, logo_path, image_path, created_at, updated_at
    # personalization types : digital printing, embroidery, screen printing
    personalization_type_data = [
        ("d9f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Digital Printing", "Digital Printing", "logo_path", "image_path", faker.date_time(), faker.date_time()),
        ("e4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Embroidery", "Embroidery", "logo_path", "image_path", faker.date_time(), faker.date_time()),
        ("f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Screen Printing", "Screen Printing", "logo_path", "image_path", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO personalization_types (id, name, description, logo_path, image_path, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, personalization_type_data)
    db.commit()


    # Personalization methods
    # Prepare the data : id, personalization_type_id, name, description,logo_path, image_path, created_at, updated_at
    # personalization methods : sublimation, direct to garment, heat transfer, screen printing, embroidery
    personalization_method_data = [
        ("e4926e08-a551-4d1c-a0ec-9f54c45ca0bf", "d9f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Sublimation", "Sublimation", faker.date_time(), faker.date_time()),
        ("8b9f4bce-ec38-442e-8df9-b7d5f4b0f9ce", "e4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Outline Embroidery", "Outline Embroidery", faker.date_time(), faker.date_time()),
        ("655cfd12-e6e2-47be-a576-d3fa4e85406f", "f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Heat Transfer", "Heat Transfer", faker.date_time(), faker.date_time()),
        ("becf5ca8-40e0-41fd-b21b-06f0f783f5d6", "f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Screen Printing", "Screen Printing", faker.date_time(), faker.date_time()),
        ("e3a525a5-24b0-43e4-973e-4913522380ba", "f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", "Embroidery", "Embroidery", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO personalization_methods (id, personalization_type_id, name, description, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, personalization_method_data)
    db.commit()


    # Organizations
    # Prepare the data : id, name, description, commerce_registry_number, is_verified, created_at, updated_at
    organization_data = [
        ("517292a1-75b6-4688-a052-364d93ecc9b7", faker.company(), faker.paragraph(),faker.phone_number(), True, faker.date_time(), faker.date_time()),
        ("440b3a20-16a3-4e44-bcec-8c3b60c57b47", faker.company(), faker.paragraph(),faker.phone_number(), True, faker.date_time(), faker.date_time()),
        ("f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", faker.company(), faker.paragraph(),faker.phone_number(), True, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO organizations (id, name, description, commerce_registry_number, is_verified, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, organization_data)
    db.commit()

    # Close the cursor and database connection
    cursor.close()
    db.close()







def insert_dynamic_data(db):
    """
    Insert data into dynamic tables that can be modified by the user
    """
    pass
def insert_data(db):
    # Insert static data
    insert_static_data(db)
    # Insert dynamic data
    insert_dynamic_data(db)


def main():
    # Connect to the database
    db = connect_to_database()
    # Insert data into the database
    insert_data(db)
    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()

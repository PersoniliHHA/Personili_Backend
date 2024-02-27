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
    - Accoun
    """
    # CATEGORY TABLE
    # Prepare the data
    category_data = [
        # Home decor
        ("14a70128-56f1-4881-a63d-e09636e812bd", "Home Decor", "image_path1", "logo_path1", None),
        ("9c75b9b7-f047-403b-a715-f99c0ef26283", "paintings", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd"),
        ("ee6bf500-d74b-4510-8a0b-8a610111d619", "blankets", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd"),
        ("59a77ce4-971a-46bd-8988-39080f0d9c25", "pillows", "image_path1", "logo_path1", "14a70128-56f1-4881-a63d-e09636e812bd"),
        
        # Tech accessories
        ("14a70128-56f1-4881-a63d-10963658123d", "Tech Accessories", "image_path2", "logo_path2", None),
        ("79ee3fcf-42c2-4906-badf-8380904792dc", "Phone cases", "image_path2", "logo_path2", "14a70128-56f1-4881-a63d-10963658123d"),
        ("13a603d6-704d-41e0-8adf-d5ef93582401", "Keychains", "image_path2", "logo_path2", "14a70128-56f1-4881-a63d-10963658123d"),
        
        # Apparel
        ("404bfdf7-b8c4-4d68-ae2b-9e42342b94c6", "Apparel",  "image_path3", "logo_path3", None),
        
        ("4c33772d-953d-483f-8111-a112af95d058", "Tops", "image_path1", "logo_path1", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6"),
        ("bf97280e-cbc3-49ec-ad08-79618a01371b", "Tshirts", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058"),
        ("aa32d550-4e9b-42a0-a6cd-f1062cebb0d0", "Sweatshirts", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058"),
        ("583bea11-39d4-4828-afc3-32b3f151d355", "Sweaters", "image_path1", "logo_path1", "4c33772d-953d-483f-8111-a112af95d058"),
        
        ("e88ba743-e8da-4ef2-91bb-75c164b62144", "Bottoms", "image_path2", "logo_path2", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6"),
        ("5a253d03-f9f5-41ad-9fd5-4189451e1804", "Pants", "image_path2", "logo_path2", "e88ba743-e8da-4ef2-91bb-75c164b62144"),
        ("cb64c665-85f0-4ea6-91f9-4c296945ddd1", "Pants", "image_path2", "logo_path2", "e88ba743-e8da-4ef2-91bb-75c164b62144"),
        
        ("be2d099e-4bab-49b9-aab3-1d63463f384b", "Underwear","image_path3", "logo_path3", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6"),
        ("e2f98d5b-9679-4db5-a7d2-1f71dd1bb441", "Boxers","image_path3", "logo_path3", "be2d099e-4bab-49b9-aab3-1d63463f384b"),
 ]
    cursor = db.cursor()
    sql = f"""INSERT INTO category (id, name, image_path, logo_path, parent_category) 
    VALUES ('{category_data[0][0]}', '{category_data[0][1]}', '{category_data[0][2]}', '{category_data[0][3]}', {category_data[0][4]})
    VALUES ('{category_data[1][0]}', '{category_data[1][1]}', '{category_data[1][2]}', '{category_data[1][3]}', {category_data[1][4]})
    VALUES ('{category_data[2][0]}', '{category_data[2][1]}', '{category_data[2][2]}', '{category_data[2][3]}', {category_data[2][4]})
    VALUES ('{category_data[3][0]}', '{category_data[3][1]}', '{category_data[3][2]}', '{category_data[3][3]}', {category_data[3][4]})
    VALUES ('{category_data[4][0]}', '{category_data[4][1]}', '{category_data[4][2]}', '{category_data[4][3]}', {category_data[4][4]})
    VALUES ('{category_data[5][0]}', '{category_data[5][1]}', '{category_data[5][2]}', '{category_data[5][3]}', {category_data[5][4]})
    VALUES ('{category_data[6][0]}', '{category_data[6][1]}', '{category_data[6][2]}', '{category_data[6][3]}', {category_data[6][4]})
    VALUES ('{category_data[7][0]}', '{category_data[7][1]}', '{category_data[7][2]}', '{category_data[7][3]}', {category_data[7][4]})
    VALUES ('{category_data[8][0]}', '{category_data[8][1]}', '{category_data[8][2]}', '{category_data[8][3]}', {category_data[8][4]})"""
    
    # Execute the query with the category_data
    cursor.executemany(sql, category_data)

    # Commit the changes to the database
    db.commit()

    # THEME TABLE
    # Prepare the data
    theme_data =[
        ("14a70128-56f1-4881-a63d-e09636e812bd", "Nature & environment", faker.paragraph(), "log_path"),
        ("c407faaf-6fd5-4e32-bc32-002e39a8d89e", "Abstract & Geometric", faker.paragraph(), "log_path"),
        ("b4860cc4-f13c-4eb6-bcaa-7df0dce00cc8", "Culture", faker.paragraph(), "log_path"),
        ("ec48f796-78cb-4c80-966f-b778bc85a2cc", "Fantasy", faker.paragraph(), "log_path"),
        ("b1f59f7d-8ad2-4e02-92de-d3f0d879b821", "Science Fiction", faker.paragraph(), "log_path"),
        ("afff6767-ab17-48c7-b0a6-a84f6ded9ff5", "Social & Political", faker.paragraph(), "log_path"),
        ("240a1e1b-72b5-4a95-91e9-e223f6f9faa0", "Food", faker.paragraph(), "log_path"),
        ("74745f05-fb8b-4217-a3c8-d00aa72d415d", "Anime", faker.paragraph(), "log_path"),
    ]
    cursor = db.cursor()
    sql = f"""INSERT INTO theme (id, name, description, logo_path)
    VALUES ('{theme_data[0][0]}', '{theme_data[0][1]}', '{theme_data[0][2]}', '{theme_data[0][3]}')
    VALUES ('{theme_data[1][0]}', '{theme_data[1][1]}', '{theme_data[1][2]}', '{theme_data[1][3]}')
    VALUES ('{theme_data[2][0]}', '{theme_data[2][1]}', '{theme_data[2][2]}', '{theme_data[2][3]}')
    VALUES ('{theme_data[3][0]}', '{theme_data[3][1]}', '{theme_data[3][2]}', '{theme_data[3][3]}')
    VALUES ('{theme_data[4][0]}', '{theme_data[4][1]}', '{theme_data[4][2]}', '{theme_data[4][3]}')
    VALUES ('{theme_data[5][0]}', '{theme_data[5][1]}', '{theme_data[5][2]}', '{theme_data[5][3]}')
    VALUES ('{theme_data[6][0]}', '{theme_data[6][1]}', '{theme_data[6][2]}', '{theme_data[6][3]}')
    VALUES ('{theme_data[7][0]}', '{theme_data[7][1]}', '{theme_data[7][2]}', '{theme_data[7][3]}')
    """
    # Execute the query with the theme_data

    # Close the cursor and database connection
    cursor.close()
    db.close()

def insert_dynamic_data(db):
    """
    Insert data into dynamic tables that can be modified by the user
    """
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

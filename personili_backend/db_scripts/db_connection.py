from psycopg2 import connect
import os
from faker import Faker

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
    """
    # CATEGORY TABLE
    # Prepare the data
    data = [
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
        ("e88ba743-e8da-4ef2-91bb-75c164b62144", "Bottoms", "image_path2", "logo_path2", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6"),
        ("be2d099e-4bab-49b9-aab3-1d63463f384b", "Underwear","image_path3", "logo_path3", "404bfdf7-b8c4-4d68-ae2b-9e42342b94c6"),

    
    ]
    cursor = db.cursor()
    sql = """INSERT INTO category (id, name, description, image_path, logo_path, parent_category, availability_status) 
    VALUES ({data[0][1]}, {data[0][2]}, {data[0][3]}, {data[0][4]}, {data[0][5]})
    VALUES ({data[1][1]}, {data[1][2]}, {data[1][3]}, {data[1][4]}, {data[1][5]})
    VALUES ({data[2][1]}, {data[2][2]}, {data[2][3]}, {data[2][4]}, {data[2][5]})
    VALUES ({data[3][1]}, {data[3][2]}, {data[3][3]}, {data[3][4]}, {data[3][5]})
    VALUES ({data[4][1]}, {data[4][2]}, {data[4][3]}, {data[4][4]}, {data[4][5]})
    VALUES ({data[5][1]}, {data[5][2]}, {data[5][3]}, {data[5][4]}, {data[5][5]})
    VALUES ({data[6][1]}, {data[6][2]}, {data[6][3]}, {data[6][4]}, {data[6][5]})
    VALUES ({data[7][1]}, {data[7][2]}, {data[7][3]}, {data[7][4]}, {data[7][5]})
    VALUES ({data[8][1]}, {data[8][2]}, {data[8][3]}, {data[8][4]}, {data[8][5]})"""
    
    # Execute the query with the data
    cursor.executemany(sql, data)

    # Commit the changes to the database
    db.commit()

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

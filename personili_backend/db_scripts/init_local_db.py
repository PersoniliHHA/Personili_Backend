from psycopg2 import connect
import os
from faker import Faker
from django.contrib.auth.hashers import make_password
import random


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
    - Accounts
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
    """

    # ACCOUNTS TABLE
    # Prepare the data: id, email, password(hashed), email_verified, is_active, is_staff, is_admin, is_superuser, created_at, updated_at
    account_data = [
        # passowrd used : soloArena0156..UYUIJNT..4545D5ERG34?
        ("75f55f9a-e913-4082-8444-68d251b937ff", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M0hTWW83UGRrU3dlRTloelB2b3BuRw$8WrcZco7aJP8hg+beel/rmDILtERykBGKM8u4tW8YBI", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("b452214d-332b-4834-a329-7cbd14e53a3e", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M0hTWW83UGRrU3dlRTloelB2b3BuRw$8WrcZco7aJP8hg+beel/rmDILtERykBGKM8u4tW8YBI", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("3ad2dbd7-0299-4719-aeda-6345707971e5", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M0hTWW83UGRrU3dlRTloelB2b3BuRw$8WrcZco7aJP8hg+beel/rmDILtERykBGKM8u4tW8YBI", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("1649f446-a76c-4bfd-8083-534eef38830e", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M0hTWW83UGRrU3dlRTloelB2b3BuRw$8WrcZco7aJP8hg+beel/rmDILtERykBGKM8u4tW8YBI", True, True, False, False, False, faker.date_time(), faker.date_time()),
        
        # password used : soloArena0156..UYUIJNT..DloEth_3123?
        ("e55d3819-8367-4e84-9cc5-4f324648db0a", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("4d1d359e-ad95-4265-a2b8-74846dcb88b6", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("e1731581-ca5a-49ba-b17a-023ac3509f00", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("ec448ce4-5551-4f0f-8911-496ec43d9165", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("9e49a30c-efc5-4315-9923-63bb8a7cec24", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("1e62b388-23fa-46c0-a069-91f1e8e6f603", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$M1RpU09aMFRqNmc3V052VjZmSWo5QQ$fMkYCgt9P4c1G4LOmc/J93sN4BXRejvEp8QsLrxs+SQ", True, True, False, False, False, faker.date_time(), faker.date_time()),
        
        # password used : multiEthiGroup156..UYUIJNT..DloEth_?
        ("8423e696-0ad0-459e-a379-42694f04c813", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$ejM5OTJnWkREdHl4QUw3MVIwMUlaZQ$tkhRiR9iROWA5o5bv6hUbZoNxnbCOkw75goYWftRSC4", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("16338984-449e-4040-9266-dd9a6423286e", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$ejM5OTJnWkREdHl4QUw3MVIwMUlaZQ$tkhRiR9iROWA5o5bv6hUbZoNxnbCOkw75goYWftRSC4", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("0c206a71-9217-4f74-8807-8ebddbe01834", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$ejM5OTJnWkREdHl4QUw3MVIwMUlaZQ$tkhRiR9iROWA5o5bv6hUbZoNxnbCOkw75goYWftRSC4", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("2f19af4f-90af-4a0b-9f75-6b9e8e3c49e3", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$ejM5OTJnWkREdHl4QUw3MVIwMUlaZQ$tkhRiR9iROWA5o5bv6hUbZoNxnbCOkw75goYWftRSC4", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("ad185cf2-4e8b-44ec-af64-f2d638d5bfd2", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$ejM5OTJnWkREdHl4QUw3MVIwMUlaZQ$tkhRiR9iROWA5o5bv6hUbZoNxnbCOkw75goYWftRSC4", True, True, False, False, False, faker.date_time(), faker.date_time()),
        
        # password used : GenkEthiGroup156..UYUIJNT..DloEth_?
        ("7dd4ffa8-5b5d-4470-96cd-de14de61eb23", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$b3FSTmhIVk9Fbm9WTmlVM0lLalkweQ$+YDxhJn4kmFmsZTtKvc/0SPrdZRwgoZon64nJn5/m4s", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("8d8e15a8-575f-4ea7-8fb5-3b9fe4397c98", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$b3FSTmhIVk9Fbm9WTmlVM0lLalkweQ$+YDxhJn4kmFmsZTtKvc/0SPrdZRwgoZon64nJn5/m4s", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("81885568-220c-4957-a316-f64d0eb9565c", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$b3FSTmhIVk9Fbm9WTmlVM0lLalkweQ$+YDxhJn4kmFmsZTtKvc/0SPrdZRwgoZon64nJn5/m4s", True, True, False, False, False, faker.date_time(), faker.date_time()),
        ("0510efef-aa59-47ca-948f-e5fb1715ea63", faker.email(), "argon2$argon2id$v=19$m=102400,t=2,p=8$b3FSTmhIVk9Fbm9WTmlVM0lLalkweQ$+YDxhJn4kmFmsZTtKvc/0SPrdZRwgoZon64nJn5/m4s", True, True, False, False, False, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO accounts (id, email, password, email_verified, is_active, is_staff, is_admin, is_superuser, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, account_data)

    # Commit the changes to the database
    db.commit()

    # Account profiles
    # Prepare the data : id, account_id, first_name, last_name, phone_number, profile_picture_path, age, gender(Male, Female or Not specified), date_of_birth, created_at, updated_at
    account_profile_data = [
        ("0734b5e3-fb69-4b55-a931-6a3f05a331f8", "75f55f9a-e913-4082-8444-68d251b937ff", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not sepcified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("06cbd596-5520-430b-aa3c-2392af714b50", "b452214d-332b-4834-a329-7cbd14e53a3e", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("e8651dce-3327-406a-9740-01cd2f6663ea", "3ad2dbd7-0299-4719-aeda-6345707971e5", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("2df77093-e107-44a0-a172-bc4735563954", "1649f446-a76c-4bfd-8083-534eef38830e", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        
        ("7a9ea5d6-f892-461b-bf4b-004f7ab19e27", "e55d3819-8367-4e84-9cc5-4f324648db0a", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("9184675c-b235-4da2-a63d-b2443f61f9cc", "4d1d359e-ad95-4265-a2b8-74846dcb88b6", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("4d57ec73-e6e9-4d6a-971e-ffcbefdeecbf", "e1731581-ca5a-49ba-b17a-023ac3509f00", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("59dedb05-5dbd-465f-af80-f90b1e9fe22c", "ec448ce4-5551-4f0f-8911-496ec43d9165", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("eeb6e276-11d1-40a5-bc5b-1f429cc53fd0", "9e49a30c-efc5-4315-9923-63bb8a7cec24", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("ce6714db-644b-41c6-ad32-c4404c8befcd", "1e62b388-23fa-46c0-a069-91f1e8e6f603", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        
        ("5794b5c0-eed7-4272-ae95-b55929c45056", "8423e696-0ad0-459e-a379-42694f04c813", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("5c3c5907-c30a-4302-af20-e42705b86046", "16338984-449e-4040-9266-dd9a6423286e", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("c1c32cf6-165a-4910-940d-18f04bb69c2b", "0c206a71-9217-4f74-8807-8ebddbe01834", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("56827a2b-630b-43d4-b8ef-d87ba6af1871", "2f19af4f-90af-4a0b-9f75-6b9e8e3c49e3", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("c6704024-9f1b-4c2a-a720-ce349303138f", "ad185cf2-4e8b-44ec-af64-f2d638d5bfd2", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),

        ("159c083d-61d1-4915-baf1-ffe7ae65df5b", "7dd4ffa8-5b5d-4470-96cd-de14de61eb23", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("9a0970a9-95ef-4a62-9f9c-7e0911f6a486", "8d8e15a8-575f-4ea7-8fb5-3b9fe4397c98", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("b893579d-2ddd-4e2b-9ca7-f6e9514ae603", "81885568-220c-4957-a316-f64d0eb9565c", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
        ("08924234-1df8-4cb4-bf12-a6aa719982ce", "0510efef-aa59-47ca-948f-e5fb1715ea63", faker.first_name(), faker.last_name(), faker.phone_number(), faker.url(), random.randint(13, 110), random.choice(["Male", "Female", "Not specified"]), faker.date(), faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO account_profiles (id, account_id, first_name, last_name, phone_number, profile_picture_path,age, gender, date_of_birth, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, account_profile_data)

    # Commit the changes to the database
    db.commit()

    # Delivery addresses table
    # Prepare the data : id, account_profile_id, street, city, state, country, zip_code, created_at, updated_at
    delivery_address_data = [
        ("e57ce561-adf6-406b-a22a-3de79d52f918", "0734b5e3-fb69-4b55-a931-6a3f05a331f8", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("166bc376-6d9a-4e57-8f9b-baa58e8af888", "06cbd596-5520-430b-aa3c-2392af714b50", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("c0955ddc-daaa-48fe-8800-a566ff5dfbbf", "e8651dce-3327-406a-9740-01cd2f6663ea", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("4e8e482d-9435-4ec8-96e4-4166dd64c801", "2df77093-e107-44a0-a172-bc4735563954", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        
        ("12e1d01d-2826-4f9b-9973-82e0adc03101", "7a9ea5d6-f892-461b-bf4b-004f7ab19e27", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("4b9abe42-5855-4554-84d5-c1a2eb3b6936", "9184675c-b235-4da2-a63d-b2443f61f9cc", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("290ca5e1-60d5-4ba8-9e7b-6bd456bb981a", "4d57ec73-e6e9-4d6a-971e-ffcbefdeecbf", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("f89cfaad-f518-4053-892e-f2c150b54917", "59dedb05-5dbd-465f-af80-f90b1e9fe22c", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("398b8de6-14ae-46d5-8317-dc71831557de", "eeb6e276-11d1-40a5-bc5b-1f429cc53fd0", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
        ("4327ac82-8fb6-4dc6-b270-db70a2452abb", "ce6714db-644b-41c6-ad32-c4404c8befcd", faker.street_address(), faker.city(), faker.state(), faker.country(), faker.zipcode(), faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO delivery_addresses (id, account_profile_id, street, city, state, country, zip_code, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, delivery_address_data)

    # Commit the changes to the database
    db.commit()

    
    #############################################################################################################################################

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
        ("14a70128-56f1-4881-a63d-e09636e812bd", "Nature & environment", faker.paragraph(), faker.image_url(), faker.date_time(), faker.date_time()),
        ("c407faaf-6fd5-4e32-bc32-002e39a8d89e", "Abstract & Geometric", faker.paragraph(), faker.image_url(), faker.date_time(), faker.date_time()),
        ("b4860cc4-f13c-4eb6-bcaa-7df0dce00cc8", "Culture", faker.paragraph(), faker.image_url(),faker.date_time(), faker.date_time()),
        ("ec48f796-78cb-4c80-966f-b778bc85a2cc", "Fantasy", faker.paragraph(), faker.image_url(),faker.date_time(), faker.date_time()),
        ("b1f59f7d-8ad2-4e02-92de-d3f0d879b821", "Science Fiction", faker.paragraph(),faker.image_url(),faker.date_time(), faker.date_time()),
        ("afff6767-ab17-48c7-b0a6-a84f6ded9ff5", "Social & Political", faker.paragraph(),faker.image_url(), faker.date_time(), faker.date_time()),
        ("240a1e1b-72b5-4a95-91e9-e223f6f9faa0", "Food", faker.paragraph(),  faker.image_url(),faker.date_time(), faker.date_time()),
        ("74745f05-fb8b-4217-a3c8-d00aa72d415d", "Anime", faker.paragraph(), faker.image_url(), faker.date_time(), faker.date_time()),
        ("d5623fd9-b017-4ff7-9e15-2f228e22b7e2", "Others", faker.paragraph(),faker.image_url(), faker.date_time(), faker.date_time()),
    
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
        ("cec0b564-ca97-4d1f-9167-44c7d0084471", "Pillow", "59a77ce4-971a-46bd-8988-39080f0d9c25", "sleep pillow",faker.image_url(), "generic", "generic", faker.date_time(), faker.date_time()),
        ("700970f2-7d3b-41e4-a625-8e32d7957cc0", "Phone case", "79ee3fcf-42c2-4906-badf-8380904792dc", "phone case",faker.image_url(), "generic", "generic", faker.date_time(), faker.date_time()),
        ("33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Tshirt", "bf97280e-cbc3-49ec-ad08-79618a01371b", "blank tshirt",faker.image_url(), "generic", "generic", faker.date_time(), faker.date_time()),
        ("0bf45502-8ce8-4a83-b8b0-2071db0b4949", "Pants", "5a253d03-f9f5-41ad-9fd5-4189451e1804", "simple pants", faker.image_url(), "generic", "generic", faker.date_time(), faker.date_time()),
        ("6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "Boxers", "e2f98d5b-9679-4db5-a7d2-1f71dd1bb441", "sleep boxers",faker.image_url(), "generic", "generic", faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO personalizables (id, name, category_id, description, image_path, brand, model, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"

    # Execute the query with the personalizable_data
    cursor.executemany(sql_query, personalizable_data)
    db.commit()

    # Personalizable zones
    # Prepare the data : id, personalizable_id, name, x1, y1, x2, y2, max_nb_designs created_at, updated_at
    personalizable_zone_data = [
        # Tshirt
        ("fa1ce80b-ee75-421b-915a-78c0d3ab60d8", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Front", 0, 0, 100, 100, 4, faker.date_time(), faker.date_time()),
        ("cd663fc5-20f4-4dfd-9898-8a6dfa60d6d4", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Back", 0, 0, 100, 100, 4, faker.date_time(), faker.date_time()),
        ("cba8c97f-2e04-4c49-9d84-153972d6266e", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Left side", 0, 0, 100, 100, 2, faker.date_time(), faker.date_time()),
        ("6ebb4f8d-8590-4334-a8d3-70452c2581a9", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "Right side", 0, 0, 100, 100, 2, faker.date_time(), faker.date_time()),
        
        # Phone case
        ("de5509d8-0022-48b0-8e43-6b5b49bbbff4", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "Front", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
        
        # Pants
        ("71baffce-fe40-4917-8846-f294a019b619", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "Front", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
        ("e7443de3-828f-4430-9f40-c9bf2af1f707", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "Back", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
        
        # Boxers
        ("3fad70ef-11c9-4eb4-95c0-2a01e2850462", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "Front", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
        ("ecb39247-669f-4310-a023-038e1d52bb03", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "Back", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),

        # Pillows
        ("b494e8a4-9ff1-4d32-8e08-55175887b8e7", "cec0b564-ca97-4d1f-9167-44c7d0084471", "Front", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
        ("a92d2f9b-6ca8-4c71-b0dd-d84708da2ffc", "cec0b564-ca97-4d1f-9167-44c7d0084471", "Back", 0, 0, 100, 100, 1, faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO personalizable_zones (id, personalizable_id, name, x1, y1, x2, y2, max_nb_designs, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"

    # Execute the query with the personalizable_zone_data
    cursor.executemany(sql_query, personalizable_zone_data)
    db.commit()

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
        ("de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "White", faker.date_time(), faker.date_time()),
        ("64bb6750-919d-45ed-a00f-3ea16dc39ea9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Black", faker.date_time(), faker.date_time()),
        ("6f2a143b-356d-4342-8751-f87d171ecc22", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", "Grey", faker.date_time(), faker.date_time()),
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
    # Prepare the data : id, personalizable_id, option_id, created_at, updated_at
    personalizable_option_data = [
        # Tshirt
        # Tshirt and color
        ("0c926a08-d1e7-47c0-adcd-80ec283c5e60", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        # Tshirt and size
        ("8c7b726b-74b3-4e77-9fad-14caca27d1d8", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "c1622200-8670-45aa-9ae8-a1be7c56d14a",  faker.date_time(), faker.date_time()),
        # Tshirt and material
        ("79adcf21-8147-4df4-8edb-dc2889b2f4c1", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        
        # Phone case
        # Phone case and color
        ("ee5106fa-b45e-455e-8960-a5a76f7fe1eb", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        # Phone case and material
        ("e2e9b4e5-435c-46bb-a7bc-d2d47784be1e", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        
        # Pants
        # Pants and color
        ("3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        # Pants and size
        ("97bb2b90-8116-44f8-8c61-8faddb971224", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        # Pants and material
        ("6c20877a-7742-42cb-a789-0e46444628a5", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        
        # boxer
        # Boxers and color
        ("0c0d9e54-451f-4180-9d88-46cd91382343", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        # Boxers and size
        ("95a9ad8a-01f2-4483-aebd-475d00727c29", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        # Boxers and material
        ("f9a04f3b-fff4-4fef-b2e3-544de2bc75fd", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "906e811c-2ff6-46fe-ac10-7cdc5020ab1c", faker.date_time(), faker.date_time()),
        
        # pillows
        # pillow and color
        ("12acedee-9fe1-4397-a36c-e51235322830", "cec0b564-ca97-4d1f-9167-44c7d0084471", "345ec45d-a84d-4d0e-8c54-3ac860439fd2", faker.date_time(), faker.date_time()),
        # pillow and size
        ("39e772b7-df9f-44e2-9276-1190ce4530ec", "cec0b564-ca97-4d1f-9167-44c7d0084471", "c1622200-8670-45aa-9ae8-a1be7c56d14a", faker.date_time(), faker.date_time()),
        # pillow and material
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

    # Organization profiles
    # Prepare the data : id, organization_id, logo_path, banner_path, address, facebook_link, x_link, instagram_link, linkedin_link, youtube_link , is_sponsored, created_at, updated_at
    organization_profile_data = [
        ("e16fb7d9-0f6f-46ac-8864-90d017328d3d", "517292a1-75b6-4688-a052-364d93ecc9b7", faker.image_url(), faker.image_url(), faker.address(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), True, faker.date_time(), faker.date_time()),
        ("37eebac5-c9aa-489a-bb93-2728526b7adc", "440b3a20-16a3-4e44-bcec-8c3b60c57b47", faker.image_url(), faker.image_url(), faker.address(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), True, faker.date_time(), faker.date_time()),
        ("7a650f39-aebf-46fd-a6af-1d532f968f7a", "f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", faker.image_url(), faker.image_url(), faker.address(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), faker.uri(), True, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO organization_profiles (id, organization_id, logo_path, banner_path, address, facebook_link, x_link, instagram_link, linkedin_link, youtube_link, is_sponsored, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, organization_profile_data)
    db.commit()

    # Organization memberships
    # Prepare the data : id, account_id, organization_id, role, is_active, created_at, updated_at
    organization_membership_data = [
        ("db3e96c3-2854-4db2-a2fb-80b2cbf8c5f2", "75f55f9a-e913-4082-8444-68d251b937ff", "517292a1-75b6-4688-a052-364d93ecc9b7", "Owner", True, faker.date_time(), faker.date_time()),
        ("640b7a98-652d-454d-a7ec-902fa3db3918", "b452214d-332b-4834-a329-7cbd14e53a3e", "517292a1-75b6-4688-a052-364d93ecc9b7", "Employer", True, faker.date_time(), faker.date_time()),
        ("9844c817-902c-457b-9c70-d9e7bed6e6a4", "3ad2dbd7-0299-4719-aeda-6345707971e5", "517292a1-75b6-4688-a052-364d93ecc9b7", "Employer", True, faker.date_time(), faker.date_time()),
        ("a191590c-e90b-4b45-acd9-eb67f00edf35", "1649f446-a76c-4bfd-8083-534eef38830e", "517292a1-75b6-4688-a052-364d93ecc9b7", "Employer", True, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO organization_memberships (id, account_id, organization_id, role, is_active, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, organization_membership_data)
    db.commit()


    # Workshops
    # Prepare the data : id, organization_id, name, description, address, email, phone, is_active, created_at, updated_at
    workshop_data = [
        ("e1e2cd6a-aaf2-4407-91dd-e87ec880e341", "517292a1-75b6-4688-a052-364d93ecc9b7", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
        ("09cb14c3-0396-48bb-a98c-443922af58b9", "517292a1-75b6-4688-a052-364d93ecc9b7", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
        
        ("2f42a7e6-25a9-4039-8c6c-62dcac1601bc", "f4f3a0f5-2d1e-4f4b-8c7a-4d0c4e4e5f3d", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
        
        ("753c4f48-0e9d-4062-9795-25f43ed40232", "440b3a20-16a3-4e44-bcec-8c3b60c57b47", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
        ("70b870df-7393-4855-a09d-2ae249da7afc", "440b3a20-16a3-4e44-bcec-8c3b60c57b47", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
        ("8bcc8e9f-6087-4b09-8fa2-eaacc9705b9b", "440b3a20-16a3-4e44-bcec-8c3b60c57b47", faker.company(), faker.paragraph(), faker.address(), faker.email(), faker.phone_number(), True, faker.date_time(), faker.date_time()),
    
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO workshops (id, organization_id, name, description, address, email, phone, is_active, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, workshop_data)
    db.commit()

    # Workshop memberships
    # Prepare the data : id, account_id, workshop_id, orgaziation_membership_id, role, is_active, created_at, updated_at
    workshop_membership_data = [
        ("152369af-1b16-4a12-b36e-6da8633ba8db", "75f55f9a-e913-4082-8444-68d251b937ff", "e1e2cd6a-aaf2-4407-91dd-e87ec880e341", "db3e96c3-2854-4db2-a2fb-80b2cbf8c5f2", "Owner", True, faker.date_time(), faker.date_time()),
        ("8877d968-6120-4c69-a9a0-5e9ea9d0283f", "b452214d-332b-4834-a329-7cbd14e53a3e", "e1e2cd6a-aaf2-4407-91dd-e87ec880e341", "640b7a98-652d-454d-a7ec-902fa3db3918", "Employer", True, faker.date_time(), faker.date_time()),
        ("4be45d32-5316-40b3-97f1-df392f9bbdfe", "3ad2dbd7-0299-4719-aeda-6345707971e5", "09cb14c3-0396-48bb-a98c-443922af58b9", "9844c817-902c-457b-9c70-d9e7bed6e6a4", "Employer", True, faker.date_time(), faker.date_time()),
        ("c69c5e5f-f0b8-4b01-9c76-f0fd7ebc8a90", "1649f446-a76c-4bfd-8083-534eef38830e", "09cb14c3-0396-48bb-a98c-443922af58b9", "a191590c-e90b-4b45-acd9-eb67f00edf35", "Employer", True, faker.date_time(), faker.date_time()),    
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO workshop_memberships (id, account_id, workshop_id, organization_membership_id, role, is_active, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, workshop_membership_data)
    db.commit()
  
    # Inventories
    # Prepare the data : id, workshop_id, name, description, address, is_active, created_at, updated_at
    inventory_data = [
        ("c57ffd6f-df49-4a24-ab53-7c543ce6139d", "e1e2cd6a-aaf2-4407-91dd-e87ec880e341", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
        ("49e9567f-9e2a-464a-8ee2-db657ad65c7d", "09cb14c3-0396-48bb-a98c-443922af58b9", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
        ("7b0f0cf7-8d52-46d9-a4e1-1fa83970494e", "09cb14c3-0396-48bb-a98c-443922af58b9", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
        
        ("65208aa6-d0d9-47e0-8917-6a3970361b39", "2f42a7e6-25a9-4039-8c6c-62dcac1601bc", faker.company()+" -Inventory", faker.paragraph(), faker.address(), False, faker.date_time(), faker.date_time()),
        ("b23ebb96-8a97-4d99-ba33-6d0947c85aac", "2f42a7e6-25a9-4039-8c6c-62dcac1601bc", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),

        ("e2262ce4-353d-4956-8cf4-5c4be5a1efc7", "753c4f48-0e9d-4062-9795-25f43ed40232", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
        ("adb053ad-b649-4661-b049-7ec3fbde2797", "70b870df-7393-4855-a09d-2ae249da7afc", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
        ("bcd3b65a-11f8-4c18-b438-b41100a0395f", "8bcc8e9f-6087-4b09-8fa2-eaacc9705b9b", faker.company()+" -Inventory", faker.paragraph(), faker.address(), True, faker.date_time(), faker.date_time()),
    ]

    cursor = db.cursor()
    sql_query = "INSERT INTO inventories (id, workshop_id, name, description, address, is_active, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, inventory_data)
    db.commit()

    # Inventory items
    # prepare the data : id, inventory_id, name, description, base_price, currency, alert_threshold, quantity, created_at, updated_at
    inventory_item_data = [
        ("cc1e2912-8091-4164-8537-9b1c6f7baadb", "c57ffd6f-df49-4a24-ab53-7c543ce6139d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("05823476-792a-4f50-8b48-a666c0dd163b", "c57ffd6f-df49-4a24-ab53-7c543ce6139d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("11c15493-28c7-44aa-ae89-5ec1c8181bf5", "c57ffd6f-df49-4a24-ab53-7c543ce6139d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("abc06b2a-b6d9-4923-a98c-3a8b47fe9fa4", "c57ffd6f-df49-4a24-ab53-7c543ce6139d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("abd65f56-8bb3-4052-af5b-95cb2ae5d35f", "c57ffd6f-df49-4a24-ab53-7c543ce6139d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),

        ("d11ff08e-9750-417d-ba70-b1c09c2a2f15", "49e9567f-9e2a-464a-8ee2-db657ad65c7d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("a9ee8dda-6a35-4499-ac5f-12719886b946", "49e9567f-9e2a-464a-8ee2-db657ad65c7d", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        
        ("16a70411-1a48-401f-914e-6d0c187dbd30", "7b0f0cf7-8d52-46d9-a4e1-1fa83970494e", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),

        ("f132fcd1-ca70-487f-98ff-c6bef38b1840", "65208aa6-d0d9-47e0-8917-6a3970361b39", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("5736602c-0ef6-469a-8ca8-fa1cc3ce6b56", "65208aa6-d0d9-47e0-8917-6a3970361b39", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),

        ("1b667e3b-8893-4ced-a8dc-217f5c3c8433", "adb053ad-b649-4661-b049-7ec3fbde2797", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("b2a994b7-4a84-4360-945d-4b11079a4655", "adb053ad-b649-4661-b049-7ec3fbde2797", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),

        ("9858effe-f4c3-4e5e-80c8-ce6d0fdf0eb2", "bcd3b65a-11f8-4c18-b438-b41100a0395f", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("522a03db-42c7-4833-84da-8c80304ca85e", "bcd3b65a-11f8-4c18-b438-b41100a0395f", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),
        ("27cf0f8c-ac67-4ae1-877e-54b09c70579c", "bcd3b65a-11f8-4c18-b438-b41100a0395f", faker.name()+" -Inventory item", faker.paragraph(), faker.random_int(10, 100),"DA", 10, 100, faker.date_time(), faker.date_time()),

    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO inventory_items (id, inventory_id, name, description, base_price, currency,  alert_threshold, quantity, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, inventory_item_data)
    db.commit()

    # Personalizable variants
    # Prepare the data : id, personalizable_id, sku_id (foreign key to inventory item table), created_at, updated_at
    personalizable_variant_data = [
        # tshirts
        ("79168a62-6e54-4c5b-8fc4-90f92681f15d", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "cc1e2912-8091-4164-8537-9b1c6f7baadb", faker.date_time(), faker.date_time()),
        ("7298f650-420c-473b-b052-ad9c664390bd", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "05823476-792a-4f50-8b48-a666c0dd163b", faker.date_time(), faker.date_time()),
        ("496a1baf-bc28-4c79-aa60-271d7f6a04bc", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "11c15493-28c7-44aa-ae89-5ec1c8181bf5", faker.date_time(), faker.date_time()),
        ("5ca0c4b8-8c5b-4362-b496-e4317c19f722", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "abc06b2a-b6d9-4923-a98c-3a8b47fe9fa4", faker.date_time(), faker.date_time()),
        ("3e7dcf25-aad7-4369-a283-9be0dc0102f9", "33aa029c-8fe1-449f-84a1-4e14faa8ded9", "abd65f56-8bb3-4052-af5b-95cb2ae5d35f", faker.date_time(), faker.date_time()),
        
        # phone case
        ("c91b37ec-278a-4f3c-a40f-dfebb2718745", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "d11ff08e-9750-417d-ba70-b1c09c2a2f15", faker.date_time(), faker.date_time()),
        ("63459aa7-92b2-4e7d-ad6c-01453693172b", "700970f2-7d3b-41e4-a625-8e32d7957cc0", "a9ee8dda-6a35-4499-ac5f-12719886b946", faker.date_time(), faker.date_time()),

        # pants
        ("37b4f2cb-77ab-4d98-9a89-7001e5a8a4e5", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "16a70411-1a48-401f-914e-6d0c187dbd30", faker.date_time(), faker.date_time()),
        ("1eea5af4-359b-4271-ac51-a005c36c5326", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "9858effe-f4c3-4e5e-80c8-ce6d0fdf0eb2", faker.date_time(), faker.date_time()),
        ("3717ae66-5c11-454f-95d7-b07d2c98d1de", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "522a03db-42c7-4833-84da-8c80304ca85e", faker.date_time(), faker.date_time()),
        ("48576d08-a98a-4d73-866c-678b1d7a7f04", "0bf45502-8ce8-4a83-b8b0-2071db0b4949", "27cf0f8c-ac67-4ae1-877e-54b09c70579c", faker.date_time(), faker.date_time()),


        # boxers
        ("e2736073-d5f8-405f-b67c-e8c996f02a08", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "f132fcd1-ca70-487f-98ff-c6bef38b1840", faker.date_time(), faker.date_time()),
        ("14cacb59-3a58-44e0-8ec0-c279aed8bf96", "6709dafa-ba2b-4ddb-9d7e-2367d0b46a2d", "5736602c-0ef6-469a-8ca8-fa1cc3ce6b56", faker.date_time(), faker.date_time()),
        
        # pillows
        ("a128c9ce-ae99-46e7-a766-bd4530b89510", "cec0b564-ca97-4d1f-9167-44c7d0084471", "1b667e3b-8893-4ced-a8dc-217f5c3c8433", faker.date_time(), faker.date_time()),
        ("8add44a1-fa11-42b3-9929-a1335fbcb657", "cec0b564-ca97-4d1f-9167-44c7d0084471", "b2a994b7-4a84-4360-945d-4b11079a4655", faker.date_time(), faker.date_time()),

       
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO personalizable_variants (id, personalizable_id, sku_id, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, personalizable_variant_data)
    db.commit()

    # Personalizable variant values
    # Prepare the data : id, personalizable_variant_id, personalizable_option_id, option_value_id, created_at, updated_at
    personalizable_variant_value_data = [
        # 5 tshirts with different sizes and colors
        # tshirt 1 : white cotton small
        # variant value and material : cotton
        ("e0e5d8d4-3b5c-4f8b-8d6c-1c5e0b4c6c4a", "79168a62-6e54-4c5b-8fc4-90f92681f15d", "79adcf21-8147-4df4-8edb-dc2889b2f4c1", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color : white
        ("a94a79fd-0c67-484e-be68-43bf66e064de", "79168a62-6e54-4c5b-8fc4-90f92681f15d", "0c926a08-d1e7-47c0-adcd-80ec283c5e60", "de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", faker.date_time(), faker.date_time()),
        # variant value and size : small
        ("55020d49-1648-4530-badf-573cae180b09", "79168a62-6e54-4c5b-8fc4-90f92681f15d", "8c7b726b-74b3-4e77-9fad-14caca27d1d8", "e31431a5-0aed-4b3a-94cb-a567fa5e7439", faker.date_time(), faker.date_time()),

        # thisrt 2 : white cotton large
        # variant value and material: cotton
        ("7cfbe10e-d79f-4649-b78e-1eec95302a9c", "7298f650-420c-473b-b052-ad9c664390bd", "79adcf21-8147-4df4-8edb-dc2889b2f4c1", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color white :
        ("d1d3bac8-4899-4df7-8e4e-5361fbf19bae", "7298f650-420c-473b-b052-ad9c664390bd", "0c926a08-d1e7-47c0-adcd-80ec283c5e60", "de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", faker.date_time(), faker.date_time()),
        # variant value and size : large
        ("033389c2-b5ec-4929-8bc6-e1f5e0da573d", "7298f650-420c-473b-b052-ad9c664390bd", "8c7b726b-74b3-4e77-9fad-14caca27d1d8", "253886bf-20b3-4b84-9375-d48f779aa026", faker.date_time(), faker.date_time()),
        
        # tshirt 3 : white cotton medium
        # variant value and material: cotton
        ("79cc6010-e874-477b-8127-deef399a3e7b", "496a1baf-bc28-4c79-aa60-271d7f6a04bc", "79adcf21-8147-4df4-8edb-dc2889b2f4c1", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color white :
        ("ec499165-0aec-414c-a323-e6fdd0f29627", "496a1baf-bc28-4c79-aa60-271d7f6a04bc", "0c926a08-d1e7-47c0-adcd-80ec283c5e60", "de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("ff3d314c-a310-4d90-9b38-34dbd9b97ad6", "496a1baf-bc28-4c79-aa60-271d7f6a04bc", "8c7b726b-74b3-4e77-9fad-14caca27d1d8", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),
        

        # tshirt 4 : black polyster small
        # material: polyster
        ("492f7fea-79f4-4643-b838-42b7ffb32018", "5ca0c4b8-8c5b-4362-b496-e4317c19f722", "79adcf21-8147-4df4-8edb-dc2889b2f4c1", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # color black :
        ("8f6c4fdc-05d8-4401-9b3b-3b6efc772e0f", "5ca0c4b8-8c5b-4362-b496-e4317c19f722", "0c926a08-d1e7-47c0-adcd-80ec283c5e60", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # size : small
        ("298d0afd-3035-4dde-bb6b-9ba7c8a113fe", "5ca0c4b8-8c5b-4362-b496-e4317c19f722", "8c7b726b-74b3-4e77-9fad-14caca27d1d8", "e31431a5-0aed-4b3a-94cb-a567fa5e7439", faker.date_time(), faker.date_time()),
        
        # tshirt 5 : black polyster medium
        # material: polyster
        ("bb22b36d-3eb5-4cac-be9f-31d068c5346b", "3e7dcf25-aad7-4369-a283-9be0dc0102f9", "79adcf21-8147-4df4-8edb-dc2889b2f4c1", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # color black :
        ("581a480d-35e5-45aa-af9a-cbb1b30f5a2a", "3e7dcf25-aad7-4369-a283-9be0dc0102f9", "0c926a08-d1e7-47c0-adcd-80ec283c5e60", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # size : small
        ("c0837303-50f9-4cbe-a50d-f32a18117184", "3e7dcf25-aad7-4369-a283-9be0dc0102f9", "8c7b726b-74b3-4e77-9fad-14caca27d1d8", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),
        
    
        # 2 phones cases
        # phone case 1 : black and polyster
        # variant value and material: polyster
        ("b76abddc-35c9-40d4-89a3-9e6adead5494", "c91b37ec-278a-4f3c-a40f-dfebb2718745", "ee5106fa-b45e-455e-8960-a5a76f7fe1eb", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # variant value and color : black
        ("304b2971-ded2-4684-8b28-4fafda489ae1", "c91b37ec-278a-4f3c-a40f-dfebb2718745", "e2e9b4e5-435c-46bb-a7bc-d2d47784be1e", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),

        # phone case 2 : white and polyster
        # variant value and material: polyster
        ("6385c25e-0389-4865-9e1a-187bb6956abe", "63459aa7-92b2-4e7d-ad6c-01453693172b", "ee5106fa-b45e-455e-8960-a5a76f7fe1eb", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # variant value and color : white
        ("f1dac449-624b-41ae-a1b4-523a0c3b43ae", "63459aa7-92b2-4e7d-ad6c-01453693172b", "e2e9b4e5-435c-46bb-a7bc-d2d47784be1e", "de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", faker.date_time(), faker.date_time()),


        # 4 pants
        # pants 1 : black and cotton and small
        # variant value and material: cotton
        ("d233258d-ef6f-42d8-9c07-ecc29a3e9b20", "37b4f2cb-77ab-4d98-9a89-7001e5a8a4e5", "6c20877a-7742-42cb-a789-0e46444628a5", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color : black
        ("ad01f6fd-2e3a-4cd8-bc16-d6f7efe270a8", "37b4f2cb-77ab-4d98-9a89-7001e5a8a4e5", "3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # variant value and size : small
        ("bb6962e4-ed36-4b4e-9b5f-e88728266b27", "37b4f2cb-77ab-4d98-9a89-7001e5a8a4e5", "97bb2b90-8116-44f8-8c61-8faddb971224", "e31431a5-0aed-4b3a-94cb-a567fa5e7439", faker.date_time(), faker.date_time()),

        # pants 2 : black and cotton and medium
        # variant value and material: cotton
        ("bd68bb6b-4f93-49cb-b8e0-006d8ecbf4a7", "1eea5af4-359b-4271-ac51-a005c36c5326", "6c20877a-7742-42cb-a789-0e46444628a5", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color : black
        ("2e8d3060-eaff-4ca1-850b-4c77ac18de7d", "1eea5af4-359b-4271-ac51-a005c36c5326", "3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("2eb22809-ddb0-4888-b0c4-a873d967e9e3", "1eea5af4-359b-4271-ac51-a005c36c5326", "97bb2b90-8116-44f8-8c61-8faddb971224", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),


        # pants 3 : white and cotton and small
        # variant value and material: cotton
        ("9959df72-2c4f-4c8e-930f-28c85ffd3e23", "3717ae66-5c11-454f-95d7-b07d2c98d1de", "6c20877a-7742-42cb-a789-0e46444628a5", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color : black
        ("538255b1-7905-4a63-8046-5a1d592209b2", "3717ae66-5c11-454f-95d7-b07d2c98d1de", "3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("a30b9b07-62f0-4ded-bcf2-22e673cf6cc2", "3717ae66-5c11-454f-95d7-b07d2c98d1de", "97bb2b90-8116-44f8-8c61-8faddb971224", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),


        # pants 4 : grey and cotton and medium
        # variant value and material: cotton
        ("2542d558-89f9-4c7d-8f55-151f58e55469", "48576d08-a98a-4d73-866c-678b1d7a7f04", "6c20877a-7742-42cb-a789-0e46444628a5", "4ce80fca-af0f-4676-9100-2b748eadb0bf", faker.date_time(), faker.date_time()),
        # variant value and color : grey
        ("35d784f0-626e-484b-9560-538763ebd25c", "48576d08-a98a-4d73-866c-678b1d7a7f04", "3e68b6a9-bdc9-4317-88e3-7bb080b9094c", "6f2a143b-356d-4342-8751-f87d171ecc22", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("0b539205-f924-42cf-a9d6-2c2ee4bb0178", "48576d08-a98a-4d73-866c-678b1d7a7f04", "97bb2b90-8116-44f8-8c61-8faddb971224", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),


        # 2 boxers
        # boxers 1 : grey and polyster and large
        # variant value and material: polyster
        ("0be34e01-9859-477d-9986-badbbdbdfbf4", "e2736073-d5f8-405f-b67c-e8c996f02a08", "f9a04f3b-fff4-4fef-b2e3-544de2bc75fd", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # variant value and color : grey
        ("9574a23c-5343-4d89-8b29-753e57533711", "e2736073-d5f8-405f-b67c-e8c996f02a08", "0c0d9e54-451f-4180-9d88-46cd91382343", "6f2a143b-356d-4342-8751-f87d171ecc22", faker.date_time(), faker.date_time()),
        # variant value and size : large
        ("d2db7dee-509e-40bf-982a-8ce0f2bed376", "e2736073-d5f8-405f-b67c-e8c996f02a08", "95a9ad8a-01f2-4483-aebd-475d00727c29", "253886bf-20b3-4b84-9375-d48f779aa026", faker.date_time(), faker.date_time()),

        # boxers 2 : white and cotton and large
        ("f8a94986-e16f-4379-8ddb-f94f4b2b2245", "14cacb59-3a58-44e0-8ec0-c279aed8bf96", "f9a04f3b-fff4-4fef-b2e3-544de2bc75fd", "0524ad82-10b1-4ce9-9c31-9f94387642c3", faker.date_time(), faker.date_time()),
        # variant value and color : grey
        ("2ab44610-48c4-479f-abf2-ad84c26c3f79", "14cacb59-3a58-44e0-8ec0-c279aed8bf96", "0c0d9e54-451f-4180-9d88-46cd91382343", "6f2a143b-356d-4342-8751-f87d171ecc22", faker.date_time(), faker.date_time()),
        # variant value and size : large
        ("507e98d7-92df-4cc5-a314-37d55c101ccc", "14cacb59-3a58-44e0-8ec0-c279aed8bf96", "95a9ad8a-01f2-4483-aebd-475d00727c29", "253886bf-20b3-4b84-9375-d48f779aa026", faker.date_time(), faker.date_time()),


        # 2 pillows
        # pillow 1 : black and silk and medium
        # variant value and material: silk
        ("ced4c0eb-ab51-4913-898b-031c052ca8fb", "a128c9ce-ae99-46e7-a766-bd4530b89510", "c7b0798b-6785-4a55-94f6-7b20526df760", "c12018bc-e01b-4a9c-9bb0-2231abf8b2fc", faker.date_time(), faker.date_time()),
        # variant value and color : black
        ("683fb8fc-905b-4b51-9d46-18efcc4a9fd5", "a128c9ce-ae99-46e7-a766-bd4530b89510", "12acedee-9fe1-4397-a36c-e51235322830", "64bb6750-919d-45ed-a00f-3ea16dc39ea9", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("1e65e69d-671c-498c-ada3-9547cdf3f13d", "a128c9ce-ae99-46e7-a766-bd4530b89510", "39e772b7-df9f-44e2-9276-1190ce4530ec", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),


        # pillow 2 : white and silk and medium
        # variant value and material: silk
        ("f8b6e4b7-5e0f-4f8f-8c1b-5a3f5a0c6e3a", "8add44a1-fa11-42b3-9929-a1335fbcb657", "c7b0798b-6785-4a55-94f6-7b20526df760", "c12018bc-e01b-4a9c-9bb0-2231abf8b2fc", faker.date_time(), faker.date_time()),
        # variant value and color : white
        ("7e6b8a3c-3d4e-4c4e-8f9d-5e0b4e7e6b8a", "8add44a1-fa11-42b3-9929-a1335fbcb657", "12acedee-9fe1-4397-a36c-e51235322830", "de3ec9d6-0f21-4981-a8a2-cc8e3f626df9", faker.date_time(), faker.date_time()),
        # variant value and size : medium
        ("f8b6e4b7-5e0f-4f8f-8c1b-5a3f5a0c6e3a", "8add44a1-fa11-42b3-9929-a1335fbcb657", "39e772b7-df9f-44e2-9276-1190ce4530ec", "ecef3173-9c2b-4743-94f4-8a02f7aec69b", faker.date_time(), faker.date_time()),

    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO personalizable_variant_values (id, personalizable_variant_id, personalizable_option_id, option_value_id, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, personalizable_variant_value_data)
    db.commit()

    # Stores
    # prepare the data : id, name, account_profile_id, created_at, updated_at
    store_data = [
        ("3a1fe8af-e41a-4d47-9be5-419d52993206", faker.company(), "0734b5e3-fb69-4b55-a931-6a3f05a331f8", faker.date_time(), faker.date_time()),
        ("64a94a5f-0faa-4290-8903-28f1554e612c", faker.company(), "06cbd596-5520-430b-aa3c-2392af714b50", faker.date_time(), faker.date_time()),
        ("8bbafc9e-90e6-4ff6-9462-33d5303dc9ca", faker.company(), "e8651dce-3327-406a-9740-01cd2f6663ea", faker.date_time(), faker.date_time()),
        ("dcd2f5f7-a8dd-4f4c-8614-8cfd0c99dc4a", faker.company(), "2df77093-e107-44a0-a172-bc4735563954", faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO stores (id, name, account_profile_id, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, store_data)
    db.commit()

    # Store profiles
    # prepare the data : id, store_id, type(verified or personal or sponosored), biography, store_logo_path, store_banner_path, is_trending, is_bestseller, is_featured, is_upcoming, created_at, updated_at
    store_profile_data = [
        ("36fde06d-0c99-4cfe-8dcc-18ba8da85a77", "3a1fe8af-e41a-4d47-9be5-419d52993206", "verified", faker.paragraph(), faker.image_url(), faker.image_url(), False, True, False, False, faker.date_time(), faker.date_time()),
        ("436ddae4-2323-403b-bcf9-28a026cb187f", "64a94a5f-0faa-4290-8903-28f1554e612c", "personal", faker.paragraph(), faker.image_url(), faker.image_url(), False, True, False, False, faker.date_time(), faker.date_time()),
        ("fd0e8d11-ebc8-4c24-b96c-2ea290ccbdd2", "8bbafc9e-90e6-4ff6-9462-33d5303dc9ca", "sponsored", faker.paragraph(), faker.image_url(), faker.image_url(), True, False, True, False, faker.date_time(), faker.date_time()),
        ("d43ecf4d-e6ad-4640-a9b9-ac5821cde9a9", "dcd2f5f7-a8dd-4f4c-8614-8cfd0c99dc4a", "verified", faker.paragraph(), faker.image_url(), faker.image_url(), True, True, True, False, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO store_profiles (id, store_id, type, biography, store_logo_path, store_banner_path, is_trending, is_bestseller, is_featured, is_upcoming, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, store_profile_data)
    db.commit()

    # Store collections
    # prepare the data : id, name, store_id, workshop_id, created_at, updated_at (store_id and workshop_id cannot be filled both)
    store_collection_data = [
        ("c41526d6-d0ae-456c-8cf5-0c549e4eac42", faker.last_name(), "3a1fe8af-e41a-4d47-9be5-419d52993206", None, faker.date_time(), faker.date_time()),
        ("5ff408e7-60b7-4ff5-b9a2-cc012f3ae65c", faker.last_name(), "64a94a5f-0faa-4290-8903-28f1554e612c", None, faker.date_time(), faker.date_time()),
        ("ed215c51-ef3f-40a6-ba25-61969efefff2", faker.last_name(), "8bbafc9e-90e6-4ff6-9462-33d5303dc9ca", None, faker.date_time(), faker.date_time()),
        ("456310ce-0414-42cd-aeaa-9d89f024fd00", faker.last_name(), "dcd2f5f7-a8dd-4f4c-8614-8cfd0c99dc4a", None, faker.date_time(), faker.date_time()),
        
        ("2a887af1-e4df-4b43-98d4-57fdd34cc427", faker.last_name(), None, "e1e2cd6a-aaf2-4407-91dd-e87ec880e341", faker.date_time(), faker.date_time()),
        ("2c714c80-4f83-4e7d-beed-6ceed76c8d18", faker.last_name(), None, "09cb14c3-0396-48bb-a98c-443922af58b9", faker.date_time(), faker.date_time()),
        ("f2f21290-55c1-48f9-9dd8-bd68f4ec145a", faker.last_name(), None, "2f42a7e6-25a9-4039-8c6c-62dcac1601bc", faker.date_time(), faker.date_time()),
    
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO collections (id, name, store_id, workshop_id, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, store_collection_data)
    db.commit()

    # Designs
    # prepare the data : id, collection_id, theme_id, title, description, image_path, tags, status(pending, approved, rejected), to_be_published, exclusive_usage, limited_personalizables, created_at, updated_at
    design_data = [
        ("e8be8bc6-4ae8-4264-9907-0fe4ca590018", "c41526d6-d0ae-456c-8cf5-0c549e4eac42", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("e00f0078-fc7e-41fc-a00d-1c8439387b0d", "c41526d6-d0ae-456c-8cf5-0c549e4eac42", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("1030c335-8329-418e-ac7c-5e2eefec01b4", "c41526d6-d0ae-456c-8cf5-0c549e4eac42", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("3ace0690-484e-41d8-a766-1546caab1eed", "c41526d6-d0ae-456c-8cf5-0c549e4eac42", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("24c0323e-82ec-4b58-8979-db2dddeba166", "c41526d6-d0ae-456c-8cf5-0c549e4eac42", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        
        ("0eac82cc-975e-485b-998b-08bc148befed", "5ff408e7-60b7-4ff5-b9a2-cc012f3ae65c", "c407faaf-6fd5-4e32-bc32-002e39a8d89e", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "rejected", True, False, False, faker.date_time(), faker.date_time()),
        ("16cda768-851e-448f-8676-c4f5610e4693", "5ff408e7-60b7-4ff5-b9a2-cc012f3ae65c", "b1f59f7d-8ad2-4e02-92de-d3f0d879b821", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),

        ("2ae3295f-f884-407a-91f1-8c070f1958d4", "ed215c51-ef3f-40a6-ba25-61969efefff2", "afff6767-ab17-48c7-b0a6-a84f6ded9ff5", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("02a727c3-275f-431f-9865-6f984e3ccde1", "ed215c51-ef3f-40a6-ba25-61969efefff2", "240a1e1b-72b5-4a95-91e9-e223f6f9faa0", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),

        ("ba3f4983-98bb-41c6-98f7-ce945ccd1f49", "456310ce-0414-42cd-aeaa-9d89f024fd00", "d5623fd9-b017-4ff7-9e15-2f228e22b7e2", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("9cf24dd9-da10-48c0-9c7f-7925b5eda1cf", "456310ce-0414-42cd-aeaa-9d89f024fd00", "74745f05-fb8b-4217-a3c8-d00aa72d415d", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),

        ("dd568de2-6890-4e6b-8f77-69136edd13e7", "2a887af1-e4df-4b43-98d4-57fdd34cc427", "ec48f796-78cb-4c80-966f-b778bc85a2cc", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("72892788-17cd-4247-8a89-2e2dcbf1e407", "2a887af1-e4df-4b43-98d4-57fdd34cc427", "ec48f796-78cb-4c80-966f-b778bc85a2cc", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),

        ("103c4b2c-1324-4331-ac0b-42efb390de75", "2c714c80-4f83-4e7d-beed-6ceed76c8d18", "14a70128-56f1-4881-a63d-e09636e812bd", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("45324e5d-9a7d-4d24-8e70-781ca05846c6", "2c714c80-4f83-4e7d-beed-6ceed76c8d18", "c407faaf-6fd5-4e32-bc32-002e39a8d89e", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),

        ("8b3fa826-d998-48dc-b581-4f4e68d69fd2", "f2f21290-55c1-48f9-9dd8-bd68f4ec145a", "74745f05-fb8b-4217-a3c8-d00aa72d415d", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
        ("5cd84c45-879a-426a-a912-f595f52fbd06", "f2f21290-55c1-48f9-9dd8-bd68f4ec145a", "74745f05-fb8b-4217-a3c8-d00aa72d415d", faker.last_name(), faker.paragraph(), faker.image_url(), faker.words(), "approved", True, False, False, faker.date_time(), faker.date_time()),
    ]
    cursor = db.cursor()
    sql_query = "INSERT INTO designs (id, collection_id, theme_id, title, description, image_path, tags, status, to_be_published, exclusive_usage, limited_personalizables, created_at, updated_at) VAlUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"
    cursor.executemany(sql_query, design_data)
    db.commit()

    # Design likes
    # prepare data : id, design_id, account_profile_id,


    # Close the cursor and database connection
    cursor.close()
    db.close()

def insert_data(db):
    # Insert static data
    insert_static_data(db)


def main():
    # Connect to the database
    db = connect_to_database()
    # Insert data into the database
    insert_data(db)
    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()

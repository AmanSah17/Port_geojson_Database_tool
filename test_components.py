import asyncio
import os
import sys

# Mock environment
os.environ["SECRET_KEY"] = "test_secret"
os.environ["GOOGLE_CLIENT_ID"] = "test_client_id"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Add path
sys.path.append(os.getcwd())

print("--- Importing modules ---")
try:
    from port_visualization_api import auth, crud, models, database
    print("Modules imported successfully.")
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)

print("\n--- Testing Auth Bypass ---")
try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_info = loop.run_until_complete(auth.verify_google_token("test-token"))
    print(f"Auth result: {user_info}")
except Exception as e:
    print(f"Auth failed: {e}")
    sys.exit(1)

print("\n--- Testing Database User Creation ---")
try:
    # Setup DB
    models.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    
    # Check/Create
    print(f"User info to create: {user_info}")
    
    # crud.create_user expects a dict with email, name, picture
    # Check if user exists
    user = crud.get_user_by_email(db, user_info["email"])
    if user:
         print(f"User already exists: {user.email}")
    else:
         user = crud.create_user(db, user_info)
         print(f"User created: {user.email}")
         
    db.close()
except Exception as e:
    print(f"DB operation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n--- ALL TESTS PASSED ---")

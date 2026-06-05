from pyrogram import Client

api_id = 23760924
api_hash = "1479ed9dfb38ac82f7c3c31c692796ce"

app = Client("my_new_account", api_id=api_id, api_hash=api_hash, test_mode=True)

app.run()
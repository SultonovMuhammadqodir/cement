from fastapi import FastAPI
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel

app = FastAPI()

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = 'cement-tracking-cabc92f3b541.json'  # Ensure this file is in your project directory
SPREADSHEET_NAME = 'Cement Tracking'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SPREADSHEET_NAME).sheet1  # Open the first sheet

class CementData(BaseModel):
    truck_id: str
    quantity: int
    plant: str

@app.post("/log_cement/")
def log_cement(data: CementData):
    sheet.append_row([data.truck_id, data.quantity, data.plant])
    return {"message": "Data logged successfully"}

@app.get("/get_cement_data/")
def get_cement_data():
    records = sheet.get_all_records()
    return {"data": records}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

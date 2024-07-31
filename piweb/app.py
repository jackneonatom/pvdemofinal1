from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import motor.motor_asyncio
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://pv-demo.local"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.PVdemo

@app.get("/stuff")
async def get_latest_from_db():
    try:
        latest_reading = await db["readings"].find_one(sort=[("_id", -1)])
        if latest_reading:
            return {"Battery_Current": latest_reading["Battery_Current"], "Battery_Voltage": latest_reading["Battery_Voltage"], "Battery_Temperature": latest_reading["Battery_Temperature"], "Panel_Current": latest_reading["Panel_Current"], "Panel_Voltage": latest_reading["Panel_Voltage"], "Panel_Temperature": latest_reading["Panel_Temperature"], "Sunlight": latest_reading["Sunlight"],"Load_Current": latest_reading["Load_Current"], "Load_Voltage": latest_reading["Load_Voltage"]}
        else:
            return {"Battery_Current": None, "Battery_Voltage": None, "Battery_Temperature": None, "Panel_Current": None, "Panel_Voltage": None, "Panel_Temperature": None, "Sunlight": None,"Load_Current": None, "Load_Voltage": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch data from database")

@app.get("/history")
async def get_historical_data():
    try:
        readings = await db["readings"].find().sort("_id", -1).to_list(length=100)  # Adjust length as needed
        historical_data = [
            {
                "timestamp": reading["_id"].generation_time.timestamp() * 1000,  # Convert to milliseconds
                "Battery_Current": reading["Battery_Current"],
                "Battery_Voltage": reading["Battery_Voltage"],
                "Battery_Temperature": reading["Battery_Temperature"],
                "Panel_Current": reading["Panel_Current"],
                "Panel_Voltage": reading["Panel_Voltage"],
                "Panel_Temperature": reading["Panel_Temperature"],
                "Sunlight": reading["Sunlight"],
                "Load_Current": reading["Load_Current"],
                "Load_Voltage": reading["Load_Voltage"]
            }
            for reading in readings
        ]
        return historical_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch historical data")

@app.post("/toggle-led")
async def toggle_led():
    try:
        led_status = await db["led_status"].find_one(sort=[("_id", -1)])
        new_status = not led_status["status"] if led_status else True
        await db["led_status"].insert_one({"status": new_status})
        return {"message": "LED toggled", "status": new_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to toggle LED")

@app.get("/led-status")
async def get_led_status():
    try:
        led_status = await db["led_status"].find_one(sort=[("_id", -1)])
        return {"status": led_status["status"] if led_status else False}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch LED status")

async def store_data(bcurrent: float, bvoltage: float, btemp: float, pcurrent: float, pvoltage: float, ptemp: float, plight: float,lcurrent: float, lvoltage: float):
    thing_state = {
        "Battery_Current": bcurrent,
        "Battery_Voltage": bvoltage,
        "Battery_Temperature": btemp,
        "Panel_Current": pcurrent,
        "Panel_Voltage": pvoltage,
        "Panel_Temperature": ptemp,
        "Sunlight": plight,
        "Load_Current": lcurrent,
        "Load_Voltage": lvoltage,
    }

    result = await db["readings"].insert_one(thing_state)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0")
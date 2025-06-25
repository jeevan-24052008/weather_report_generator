import requests
import json
from fpdf import FPDF
from datetime import datetime
def main():
    # Inputs and API request
    city = input('Enter city: ').lower()
    api_key = '118646e17e9de1d15219def2e6e9c44f'
    c1 = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}')
    o = c1.json()[0]
    c2 = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={o['lat']}&lon={o['lon']}&appid={api_key}')

    # Collecting info from API
    p = c2.json()
    type = p['weather'][0]['main']
    temp = f"{round(p['main']['temp'] - 273.15)} °C"
    temo_feels = f"{round(p['main']['feels_like'] - 273.15)} °C"
    max_temp = f"{round(p['main']['temp_max'] - 273.15)} °C"
    min_temp = f"{round(p['main']['temp_min'] - 273.15)} °C"
    hum = f"{p['main']['humidity']} %"
    pres = f"{p['main']['pressure']} mBar"
    wind = f"{round(p['wind']['speed']) * 3.6} KPH"
    if type=='Rain':
        rain = f"{p['rain']['1h']} mm"
    visi = f"{(p['visibility'])/1000} KM"

    # Time
    time = datetime.now().strftime("%Y-%m-%d")

    # Creating PDF
    pdf = FPDF(orientation='landscape',format='A4')
    pdf.add_page()
    if type == 'Clouds' or type =='Clear':
        pdf.image('clear.jpg',1,1,295,210)
    if type == 'Rain':
        pdf.image('rain.jpg',1,1,295,210)

    # Border
    pdf.rect(x=9, y=40, w=277, h=160)

    pdf.set_font('times','B',35)
    pdf.cell(0,15," WEATHER REPORT ",ln=1,align='C')\

    pdf.set_font('helvetica','B',30)
    pdf.cell(0,20,city.upper(),ln=1,align='C')

    pdf.set_font('times','BI',25)
    pdf.cell(120,20,f"-> TYPE: {type}",ln=0,align='L')
    pdf.cell(135,20,f"-> TEMP: {temp}",ln=1,align='R')
    pdf.cell(120,20,f"-> FEELS LIKE: {temo_feels}",ln=0,align='L')
    pdf.cell(135,20,f"-> MAX TEMP: {max_temp}",ln=1,align='R')
    pdf.cell(120,20,f"-> WIND: {wind}",ln=0,align='L')
    pdf.cell(135,20,f"-> MIN TEMP: {min_temp}",ln=1,align='R')
    pdf.cell(120,20,f"-> VISIBILITY: {visi}",ln=0,align='L')
    pdf.cell(135,20,f"-> PRESSURE: {pres}",ln=1,align='R')

    if type=='Rain':
        pdf.cell(120,20,f"-> HUMIDITY: {hum}",ln=0,align='L')
        pdf.cell(135,20,f"-> RAIN: {rain}",ln=1,align='R')
    else:
        pdf.cell(120,20,f"-> HUMIDITY: {hum}",ln=1,align='L')

    # Footer
    pdf.set_font('times','B',20)
    pdf.cell(120,40,f"Data last updated: {time} ",ln=1,align='L')
    pdf.set_font('times','B',15)
    pdf.cell(120,1,f"Powered by OpenWeatherMap",ln=1,align='L')

    filename = f"{city}_weather.pdf"
    pdf.output(filename)

if __name__=="__main__":
    main()

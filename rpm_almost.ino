#include <OneWire.h> 
#include <DallasTemperature.h>
/**********************************************/
#define  A_PHASE 2
#define  B_PHASE 5
#define ONE_WIRE_BUS 8
#define ONE_WIRE_BUS2 10
OneWire oneWire(ONE_WIRE_BUS);
OneWire oneWire2(ONE_WIRE_BUS2);
DallasTemperature sensors(&oneWire);
DallasTemperature sensors2(&oneWire2);

volatile int flag_A = 0;  //Assign a value to the token bit
volatile int flag_B = 0;  //Assign a value to the token bit
float rev = 0;
float oldtime = 0;
float time;
float rpm;
float km;
int kmh = 0;
float Vin=0;
float Vin1=0;
float Vin2=0;
float Vin3=0;
float Vin4=0;
float voltage;
float vout = 0.0;
float R1 = 100000.0;
float R2 = 5000.0;
float left_degree;
float right_degree;

/** *  */
void setup() {
  pinMode(A_PHASE, INPUT);
  pinMode(B_PHASE, INPUT);
  Serial.begin(115200);   //Serial Port Baudrate: 115200
  sensors.begin();
  sensors2.begin();
  attachInterrupt(digitalPinToInterrupt( A_PHASE), interrupt, RISING); //Interrupt trigger mode: RISING
}

void interrupt()// Interrupt function
{
 flag_A++;
 //flag_B++;   //장착 방향에 따라 flag_A or flag_B
}

void loop() {

  
  delay(100);// Direction judgement
  sensors.setWaitForConversion(false);
  sensors2.setWaitForConversion(false);
  sensors.requestTemperatures();
  sensors2.requestTemperatures();
  sensors.setWaitForConversion(true);
  sensors2.setWaitForConversion(true);
  Vin1 = analogRead(A0);
  
  detachInterrupt(digitalPinToInterrupt(A_PHASE));
  time = millis() - oldtime;
  
  //Serial.println(flag_A);           //장착 방향에 따라 flag_A or flag_B
  //Serial.println(flag_B);

  //Serial.println(time);
  rev = (flag_A/360.00)/(time/1000);   // =rps
  //rev = (flag_B/360.00);            //장착 방향에 따라 flag_A or flag_B

  rpm = rev*60;
  //km = ((rpm/3)*60)*1.36*0.001;  //gear_ratio:3 , ME-09 tire D: 433mm
  km = ((rpm/3)*60)*2.3*0.001;  //gear_ratio:3 , ME-10 tire D: 456mm
  kmh = int(km);
  oldtime = millis();

  right_degree = sensors.getTempCByIndex(0);
  left_degree = sensors2.getTempCByIndex(0);

  Vin2 = analogRead(A0); 
  Serial.print(voltage);
  Serial.print("w");
  Serial.print(left_degree);
  Serial.print("w");
  Serial.print(right_degree);
  Serial.print("w");
  Serial.println(kmh);

  flag_A = 0; // Clear variable just before counting again'
  //flag_B = 0; // Clear variable just before counting again   //장착 방향에 따라 flag_A or flag_B
  attachInterrupt(digitalPinToInterrupt( A_PHASE), interrupt, RISING);

  Vin3 = analogRead(A0);
  Vin4 = analogRead(A0);
  Vin = (Vin1 + Vin2 + Vin3 + Vin4)/4;
  
  vout = (Vin * 5.031) / 1023.0; // see text
  voltage = vout / (R2/(R1+R2));
}

#include <FS.h>                   
#include <ESP8266WiFi.h>          
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          
#include <ArduinoJson.h>     
#include <PubSubClient.h>     

// MQTT
char mqtt_server[40];
char mqtt_username[40];
char mqtt_password[40];
char ieeeAddr[40];
char path[100];

WiFiClient espClient;
PubSubClient client(espClient);

//wifi manager
bool shouldSaveConfig = false;   

// INPUT
int SENSOR_1 = 5;            // D1 
int SENSOR_2 = 4;            // D2 
int SENSOR_3 = 0;            // D3 
int SENSOR_4 = 13;           // D7 
int SENSOR_5 = A0;           // A0 

// RESET 
int PIN_RESET_SETTING = 16;  // D0

// LED
int PIN_LED_GREEN = 14;      // D5
int PIN_LED_RED   = 12;      // D6

String sensor_1_state = "ENABLED";     // change to "ENABLED" or "REQUEST_ONLY" to activate
String sensor_2_state = "DISABLED";    // change to "ENABLED" or "REQUEST_ONLY" to activate
String sensor_3_state = "DISABLED";    // change to "ENABLED" or "REQUEST_ONLY" to activate
String sensor_4_state = "DISABLED";    // change to "ENABLED" or "REQUEST_ONLY" to activate
String sensor_5_state = "DISABLED";    // change to "REQUEST_ONLY" to activate

String sensor_1_name = "occupancy";
String sensor_2_name = "sensor_2";
String sensor_3_name = "sensor_3";
String sensor_4_name = "sensor_4";
String sensor_5_name = "sensor_5";

int sensor_1_last_value = 0;
int sensor_2_last_value = 0;
int sensor_3_last_value = 0;
int sensor_4_last_value = 0;
int sensor_5_last_value = 0;


// ############
// split string
// ############

String getValue(String data, char separator, int index) {
  
    int found = 0;
    int strIndex[] = {0, -1};
    int maxIndex = data.length()-1;
  
    for (int i=0; i<=maxIndex && found<=index; i++){
        if(data.charAt(i)==separator || i==maxIndex){
            found++;
            strIndex[0] = strIndex[1]+1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    } 
    return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}


// ############
// wifi manager
// ############

void saveConfigCallback () {
    Serial.println("save new config...");
    shouldSaveConfig = true;
}

void wifi_manager(boolean reset_setting) {

    WiFiManager wifiManager;

    // reset settings ?
    if (reset_setting == true) {
        wifiManager.resetSettings();     // reset wifi settings
        SPIFFS.format();                 // reset config.txt
    }    

    // mounting filesystem
    
    Serial.print("mounting FS...");
  
    if (SPIFFS.begin()) {    
      
        Serial.println("successful");

        // read config file
        
        if (SPIFFS.exists("/config.json")) {
            Serial.print("reading config file...");
            File config_File = SPIFFS.open("/config.json", "r");

            if (config_File) {
              
                size_t size = config_File.size();
                std::unique_ptr<char[]> buf(new char[size]);
                config_File.readBytes(buf.get(), size);
                
                DynamicJsonDocument config_json(128);
                DeserializationError error = deserializeJson(config_json, buf.get());
                
                if (!error) {
                    strcpy(mqtt_server,   config_json["mqtt_server"]);
                    strcpy(mqtt_username, config_json["mqtt_username"]);
                    strcpy(mqtt_password, config_json["mqtt_password"]);                                       
                    Serial.println("successful");
          
                } else {
                    Serial.println("failed");
                }
                config_File.close();
            } 
        }
        
    } else {
        Serial.println("failed");
    }

    WiFiManagerParameter custom_mqtt_server  ("server",   "mqtt server",   mqtt_server, 40);
    WiFiManagerParameter custom_mqtt_username("username", "mqtt username", mqtt_username, 40);
    WiFiManagerParameter custom_mqtt_password("password", "mqtt password", mqtt_password, 40);
        
    wifiManager.setSaveConfigCallback(saveConfigCallback);
    wifiManager.addParameter(&custom_mqtt_server);
    wifiManager.addParameter(&custom_mqtt_username);
    wifiManager.addParameter(&custom_mqtt_password);

    if (!wifiManager.autoConnect("AutoConnectAP", "password")) {
        Serial.println("failed to connect and hit timeout");
        delay(3000);
        ESP.reset();
        delay(5000);
    }
  
    strcpy(mqtt_server,   custom_mqtt_server.getValue());
    strcpy(mqtt_username, custom_mqtt_username.getValue());
    strcpy(mqtt_password, custom_mqtt_password.getValue());
    
    // save new config

    if (shouldSaveConfig) {
        
        DynamicJsonDocument json_data(256);
        json_data["mqtt_server"]   = mqtt_server;
        json_data["mqtt_username"] = mqtt_username;
        json_data["mqtt_password"] = mqtt_password;
    
        File configFile = SPIFFS.open("/config.json", "w");
        
        if (!configFile) {
            Serial.println("failed to open config file for writing");
        }
        
        serializeJson(json_data, Serial);
        Serial.println();
        serializeJson(json_data, configFile);
        configFile.close();
        Serial.println("new config file saved");
    }
}


// ########
// ieeeAddr
// ########

void get_ieeeAddr() {
    Serial.print("mounting FS...");
  
    if (SPIFFS.begin()) {    
      
        Serial.println("successful");

        // read ieeeAddr file
        
        if (SPIFFS.exists("/ieeeAddr.json")) {
            Serial.print("reading ieeeAddr file...");
            File ieeeAddr_File = SPIFFS.open("/ieeeAddr.json", "r");

            if (ieeeAddr_File) {
                size_t size = ieeeAddr_File.size();
                std::unique_ptr<char[]> buf(new char[size]);
                ieeeAddr_File.readBytes(buf.get(), size);
                
                DynamicJsonDocument ieeeAddr_json(128);
                DeserializationError error = deserializeJson(ieeeAddr_json, buf.get());
                
                if (!error) {
                    strcpy(ieeeAddr, ieeeAddr_json["ieeeAddr"]);
                    Serial.println("successful");
          
                } else {
                    Serial.println("failed");
                }
                ieeeAddr_File.close();
            } 

        // ieeeAddr file not exist, generate new ieeeAddr + file
            
        } else {

            Serial.print("generate new ieeeAddr...");

            int randNumber            = random(100000, 999999);
            String ieeeAddr_generated = "0x" + String(randNumber); 
            
            ieeeAddr_generated.toCharArray(ieeeAddr,40); 

            DynamicJsonDocument ieeeAddr_json(128);
            ieeeAddr_json["ieeeAddr"] = ieeeAddr_generated;
        
            File ieeeAddr_File = SPIFFS.open("/ieeeAddr.json", "w");
            
            if (!ieeeAddr_File) {
                Serial.println("failed to open ieeeAddr file for writing");
            }
    
            serializeJson(ieeeAddr_json, Serial);
            Serial.println();
            serializeJson(ieeeAddr_json, ieeeAddr_File);
            ieeeAddr_File.close();
            Serial.println("new ieeeAddr file saved");
        }

    } else {
        Serial.println("failed");
    }
}


// ###########
// MQTT server
// ###########

void reconnect() {
    while (!client.connected()) {

        Serial.print("MQTT: ");       
        Serial.print("Connecting...");

        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);

        digitalWrite(BUILTIN_LED, HIGH);
        digitalWrite(PIN_LED_RED, HIGH);
        digitalWrite(PIN_LED_GREEN, LOW);      

        if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) { 
  
            send_default_mqtt_message();

            client.subscribe("smarthome/mqtt/#");
            Serial.println("MQTT Connected...");

            digitalWrite(BUILTIN_LED, LOW);       
          
        } else {        
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");       
            delay(5000);
        }
    }
}


// #############
// MQTT messages
// #############

void callback (char* topic, byte* payload, unsigned int length) {

    Serial.print("Incoming Message: ");
    Serial.println(topic); 

    String check_ieeeAddr = getValue(topic,'/',2);
    String check_command  = getValue(topic,'/',3);

    if (check_ieeeAddr == "devices"){

        // create path   
        String payload_path = "smarthome/mqtt/log";
        char attributes_path[100];
        payload_path.toCharArray( path, 100 );    

        // create msg as json
        DynamicJsonDocument msg(512);
        
        msg["ieeeAddr"]    = ieeeAddr;
        msg["model"]       = "sensor_module 1.0";
        msg["device_type"] = "sensor_module";
        msg["description"] = "MQTT Sensor_Module";
    
        JsonArray data_inputs   = msg.createNestedArray("inputs");

        if (sensor_1_state != "DISABLED"){
            data_inputs.add(sensor_1_name);        
        }
        if (sensor_2_state != "DISABLED"){  
            data_inputs.add(sensor_2_name);   
        }
        if (sensor_3_state != "DISABLED"){    
            data_inputs.add(sensor_3_name);  
        }
        if (sensor_4_state != "DISABLED"){   
            data_inputs.add(sensor_4_name);
        }
        if (sensor_5_state != "DISABLED"){
            data_inputs.add(sensor_5_name);
        }   

        JsonArray data_commands      = msg.createNestedArray("commands");
        JsonArray data_commands_json = msg.createNestedArray("commands_json");

        // convert msg to char
        char msg_Char[512];
        serializeJson(msg, msg_Char);

        Serial.print("Channel: ");
        Serial.println(path);         
        Serial.print("Publish message: ");
        Serial.println(msg_Char);
        Serial.println();      
          
        client.publish(path, msg_Char);        
    }

    // get 
    if (check_ieeeAddr == ieeeAddr and check_command == "get"){
        send_default_mqtt_message();    
    }      
}


// ####################
// mqtt default message
// ####################

void send_default_mqtt_message() {

    // create channel  
    String payload_path = "smarthome/mqtt/" + String(ieeeAddr);      
    char attributes[100];
    payload_path.toCharArray( path, 100 );    
 
    // create msg as json
    DynamicJsonDocument msg(128);

    if (sensor_1_state == "ENABLED" or sensor_1_state == "REQUEST_ONLY"){
        if (digitalRead(SENSOR_1) == 0){
            msg[sensor_1_name] = "False";
        } else {
            msg[sensor_1_name] = "True";
        }
    }
    if (sensor_2_state == "ENABLED" or sensor_2_state == "REQUEST_ONLY"){
        if (digitalRead(SENSOR_2) == 0){
            msg[sensor_2_name] = "False";
        } else {
            msg[sensor_2_name] = "True";
        }
    }
    if (sensor_3_state == "ENABLED" or sensor_3_state == "REQUEST_ONLY"){
        if (digitalRead(SENSOR_3) == 0){
            msg[sensor_3_name] = "False";
        } else {
            msg[sensor_3_name] = "True";
        }
    }
    if (sensor_4_state == "ENABLED" or sensor_4_state == "REQUEST_ONLY"){  
        if (digitalRead(SENSOR_4) == 0){
            msg[sensor_4_name] = "False";
        } else {
            msg[sensor_4_name] = "True";
        }
    }
    if (sensor_5_state == "REQUEST_ONLY"){    
        msg[sensor_5_name] = analogRead(SENSOR_5);
    }

    // convert msg to char
    char msg_Char[128];
    serializeJson(msg, msg_Char);

    Serial.print("Channel: ");
    Serial.println(path);
    Serial.print("Publish message: ");
    Serial.println(msg_Char);
    Serial.println();
    
    client.publish(path, msg_Char);    
}


// #####
// setup
// #####

void setup() {

    Serial.begin(115200);
    Serial.println();

    pinMode(PIN_LED_RED,OUTPUT);
    pinMode(PIN_LED_GREEN,OUTPUT);
    pinMode(BUILTIN_LED, OUTPUT);   
    pinMode(PIN_RESET_SETTING,INPUT);

    digitalWrite(BUILTIN_LED, HIGH); 
    digitalWrite(PIN_LED_RED, HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);

    pinMode(SENSOR_1, INPUT); 
    pinMode(SENSOR_2, INPUT); 
    pinMode(SENSOR_3, INPUT); 
    pinMode(SENSOR_4, INPUT); 
    pinMode(SENSOR_5, INPUT); 

    Serial.println(digitalRead(PIN_RESET_SETTING));    

    if (digitalRead(PIN_RESET_SETTING) == 1) {
        wifi_manager(true);  // reset settings
    } else {
        wifi_manager(false);
    }
  
    Serial.println(mqtt_server);

    get_ieeeAddr();
    Serial.println(ieeeAddr);
    
    client.setServer(mqtt_server, 1884);
    client.setCallback(callback); 
}


// ####
// loop
// ####

void loop() {

    if (!client.connected()) {
        reconnect();
    }

    if (sensor_1_state == "ENABLED"){
        if (sensor_1_last_value != digitalRead(SENSOR_1)){
            sensor_1_last_value = digitalRead(SENSOR_1);
            send_default_mqtt_message();
        }
    }

    if (sensor_2_state == "ENABLED"){
        if (sensor_2_last_value != digitalRead(SENSOR_2)){
            sensor_2_last_value = digitalRead(SENSOR_2);
            send_default_mqtt_message();
        }
    }

    if (sensor_3_state == "ENABLED"){
        if (sensor_3_last_value != digitalRead(SENSOR_3)){
            sensor_3_last_value = digitalRead(SENSOR_3);
            send_default_mqtt_message();
        }
    }

    if (sensor_4_state == "ENABLED"){
        if (sensor_4_last_value != digitalRead(SENSOR_4)){
            sensor_4_last_value = digitalRead(SENSOR_4);
            send_default_mqtt_message();
        }
    }

    delay(100);
    client.loop();
}

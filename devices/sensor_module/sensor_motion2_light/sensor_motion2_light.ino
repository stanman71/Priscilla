#include <FS.h>                   
#include <ESP8266WiFi.h>          
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          
#include <ArduinoJson.h>     
#include <PubSubClient.h>   
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>

// MQTT
char mqtt_server[40];
char mqtt_username[40];
char mqtt_password[40];
char ieeeAddr[40];
char path[100];

String mqtt_initial_check = "False";

WiFiClient espClient;
PubSubClient client(espClient);

// WIFI MANAGER
bool shouldSaveConfig = false;   

// UPDATE
char message[200];

int update_timer_counter;
int update_timer_value = 3600000;                // 60 minutes (in milliseconds)

bool send_update_report = true;

// RESET 
int PIN_RESET_SETTING = 16;                      // D0

// LED PINS
int PIN_LED_GREEN = 14;                          // D5
int PIN_LED_RED   = 12;                          // D6


// ###############
// CUSTOM SETTINGS
// ###############

int SENSOR_1 = 0;                                // D3 
int SENSOR_2 = A0;                               // A0 

// int SENSOR = 5;                               // D1 
// int SENSOR = 4;                               // D2 
// int SENSOR = 13;                              // D7


char model[40]       = "sensor_motion2_light";
char device_type[40] = "sensor_passiv";
char description[80] = "MQTT Motion Sensor";

String current_Version = "2.0";

int sensor_1_last_value = 0;
int sensor_2_last_value = 0;

int disable_sensor_2_timer = 0;


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
        
        mqtt_initial_check = "True";
    }
}


// ########
// ieeeAddr
// ########

void get_ieeeAddr() {

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
            digitalWrite(PIN_LED_RED, LOW);
            digitalWrite(PIN_LED_GREEN, HIGH);            

        } else {        
          
            Serial.print("failed, rc=");  
            Serial.print(client.state());        
            Serial.println("try again in 5 seconds");           

            // led switch between green, orange and red
            digitalWrite(PIN_LED_RED, LOW);
            digitalWrite(PIN_LED_GREEN, HIGH);                             
            delay(1000);
            digitalWrite(PIN_LED_RED, HIGH);
            digitalWrite(PIN_LED_GREEN, LOW);      
            delay(1000);              
            digitalWrite(PIN_LED_RED, LOW);
            digitalWrite(PIN_LED_GREEN, HIGH);                 
            delay(1000);     
            digitalWrite(PIN_LED_RED, HIGH);
            digitalWrite(PIN_LED_GREEN, LOW);      
            delay(1000);              
            digitalWrite(PIN_LED_RED, LOW);
            digitalWrite(PIN_LED_GREEN, HIGH);                 
            delay(1000);     
            digitalWrite(PIN_LED_RED, HIGH);
            digitalWrite(PIN_LED_GREEN, LOW);          

            // reset setting, if initial check failed
            if (mqtt_initial_check == "True"){
                wifi_manager(true);
            }                                         
        }
    }
}


// #########################
// MQTT send default message
// #########################

void send_default_mqtt_message() {

    // create channel  
    String payload_path = "smarthome/mqtt/" + String(ieeeAddr);      
    char attributes[100];
    payload_path.toCharArray( path, 100 );    
 
    // create msg as json
    DynamicJsonDocument msg(128);

    if (digitalRead(SENSOR_1) == 0){
        msg["occupancy"] = "True";
    } else {
        msg["occupancy"] = "False";
    }

    msg["illuminance"] = sensor_2_last_value;          

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


// ######################
// MQTT control functions
// ######################

void callback (char* topic, byte* payload, unsigned int length) {

    Serial.print("Incoming Message: ");
    Serial.println(topic); 

    String check_ieeeAddr = getValue(topic,'/',2);
    String check_command  = getValue(topic,'/',3);

    // devices 

    if (check_ieeeAddr == "devices"){

        // create path   
        String payload_path = "smarthome/mqtt/log";
        char attributes_path[100];
        payload_path.toCharArray( path, 100 );    

        // create msg as json
        DynamicJsonDocument msg(512);
        
        msg["ieeeAddr"]    = ieeeAddr;
        msg["model"]       = model;
        msg["device_type"] = device_type;
        msg["version"]     = current_Version;        
        msg["description"] = description;
    
        JsonArray data_inputs = msg.createNestedArray("input_values");
        data_inputs.add("occupancy");        
        data_inputs.add("illuminance"); 

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

    // mounting filesystem
    
    if (SPIFFS.begin()) {      
        Serial.println("mounting FS...successful");
    } else {
        Serial.println("mounting FS...failed");
    }

    // check reset settings

    if (digitalRead(PIN_RESET_SETTING) == 1) {
        wifi_manager(true);  // reset settings
    } else {
        wifi_manager(false);
    }

    get_ieeeAddr();
    Serial.print("IEEE_ADDRESS: ");      
    Serial.println(ieeeAddr);

    Serial.print("MQTT_SERVER: ");  
    Serial.println(mqtt_server);
    
    client.setServer(mqtt_server, 1884);
    client.setCallback(callback); 

    // custom settings
    
    pinMode(SENSOR_1, INPUT_PULLUP); 
    pinMode(SENSOR_2, INPUT); 
    
    sensor_2_last_value = analogRead(SENSOR_2);
}


// ####
// loop
// ####

void loop() {

    if (!client.connected()) {
        reconnect();
    }

    // update timer 
    if (update_timer_counter > update_timer_value){
        checkForUpdates();
        update_timer_counter = 0;
    } 

    // send update report
    if (send_update_report == true){
        send_update_report_message();
        send_update_report = false;
    } 
    
    update_timer_counter = update_timer_counter + 10;

    // custom settings

    // if occupancy is true, freeze illuminance value for 30 seconds
    if (digitalRead(SENSOR_1) == 0){
        disable_sensor_2_timer = 30000;
    }   

    // illuminance timer
    if (disable_sensor_2_timer > 0){
        disable_sensor_2_timer = disable_sensor_2_timer - 10; 
    } else {
        disable_sensor_2_timer = 0;
    }

    // read illuminance sensor ?    
    if (disable_sensor_2_timer == 0){
        sensor_2_last_value = analogRead(SENSOR_2);
    }           

    // send message ?     
    if (digitalRead(SENSOR_1) == 0 or sensor_1_last_value != digitalRead(SENSOR_1)){
        sensor_1_last_value = digitalRead(SENSOR_1);
        send_default_mqtt_message();
        delay(1000);
    } 

    delay(10);
    client.loop();
}


// ###############
// update firmware
// ###############

void checkForUpdates() {

    String checkUrl = "/settings/devices/firmware/request";

    String str_mqtt_server(mqtt_server);
    
    checkUrl.concat( "?device_ieeeAddr=" + String(ieeeAddr) );  
    checkUrl.concat( "&current_version=" + String(current_Version) );
  
    Serial.println("Checking for updates at URL: " + str_mqtt_server + String( checkUrl ) );

    save_update_report("success");
  
    t_httpUpdate_return ret = ESPhttpUpdate.update(str_mqtt_server, 80, checkUrl);
  
    switch (ret) {
 
        default:
        case HTTP_UPDATE_FAILED: {
            String error_number      = String(ESPhttpUpdate.getLastError());
            String error_description = ESPhttpUpdate.getLastErrorString().c_str();

            Serial.println("HTTP_UPDATE_FAILED || Error (" + error_number + "): " + error_description);
            save_update_report("HTTP_UPDATE_FAILED || Error (" + error_number + "): " + error_description);
    
            // server connection failed, don't restart
            if (error_number == "-1" or error_number == "-11") {  
                send_update_report = true;           
            } else {
                ESP.reset();
                break;                        
            }
        }
    
        case HTTP_UPDATE_NO_UPDATES: {
            Serial.println("HTTP_UPDATE_NO_UPDATES");
            delete_update_report();
            break;
        }
    
        case HTTP_UPDATE_OK: {
            Serial.println("HTTP_UPDATE_OK");
            break;
        }
    }
}


// ##################
// save update_report
// ##################

void save_update_report(String message) {

    DynamicJsonDocument json_data(512);
    json_data["message"] = message;

    File update_report_File = SPIFFS.open("/update_report.json", "w");
    
    if (!update_report_File) {
        Serial.println("failed to open update_report file for writing");
    }

    serializeJson(json_data, Serial);
    Serial.println();
    serializeJson(json_data, update_report_File);
    update_report_File.close();
    Serial.println("update_report file saved");
}


// ##########################
// send update_report message
// ##########################

void send_update_report_message() {

    // read update_report file   
    
    if (SPIFFS.exists("/update_report.json")) {
        Serial.print("reading update_report file...");
        File update_report_File = SPIFFS.open("/update_report.json", "r");

        if (update_report_File) {
            size_t size = update_report_File.size();
            std::unique_ptr<char[]> buf(new char[size]);
            update_report_File.readBytes(buf.get(), size);
            
            DynamicJsonDocument json_data(512);
            DeserializationError error = deserializeJson(json_data, buf.get());
            
            if (!error) {
                strcpy(message, json_data["message"]);
                Serial.println("successful");

                // create channel  
                String payload_path = "smarthome/mqtt/update";      
                char attributes[100];
                payload_path.toCharArray( path, 100 );   
            
                // create msg as json
                DynamicJsonDocument msg(512);
            
                msg["device_ieeeAddr"] = ieeeAddr; 
                msg["message"]         = message;
                msg["version"]         = current_Version;    
            
                // convert msg to char
                char msg_Char[512];
                serializeJson(msg, msg_Char);
            
                Serial.print("Channel: ");
                Serial.println(path);
                Serial.print("Publish message: ");
                Serial.println(msg_Char);
                Serial.println();
                
                client.publish(path, msg_Char);    

                // delete file
                Serial.println("delete update_report file...");      
                SPIFFS.remove("/update_report.json");   
               
            } else {
                Serial.println("failed");
            }
            
            update_report_File.close();
            
        } 
        
    } else {
        Serial.println("no update report founded");               
    }
}


// ####################
// delete update_report
// ####################

void delete_update_report() {

    // search update_report file   
    if (SPIFFS.exists("/update_report.json")) {

        // delete file
        Serial.println("delete update_report file");      
        SPIFFS.remove("/update_report.json");
    }    
}

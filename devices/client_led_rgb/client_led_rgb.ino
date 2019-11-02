#include <FS.h>                   
#include <ESP8266WiFi.h>          
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>          
#include <ArduinoJson.h>     
#include <PubSubClient.h>   
#include <FastLED.h>  

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

// RESET 
int PIN_RESET_SETTING = 12;  // D6

// FASTLED
#define DATA_PIN 5           // D1
#define TRANSISTOR_PIN 4     // D2
#define NUM_LEDS 300

CRGB leds[NUM_LEDS];

String state   = "OFF";
int brightness = 0;
int red        = 0;
int green      = 0;
int blue       = 0;

boolean state_changed = true;

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

        if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) { 
  
            default_mqtt_message();

            client.subscribe("miranda/mqtt/#");
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


// ####################
// mqtt default message
// ####################

void default_mqtt_message() {

    // create channel  
    String payload_path = "miranda/mqtt/" + String(ieeeAddr);      
    char attributes[100];
    payload_path.toCharArray( path, 100 );    
 
    // create msg as json
    DynamicJsonDocument msg(128);

    msg["state"]      = state;
    msg["brightness"] = brightness;
    msg["color"]["r"] = red;
    msg["color"]["g"] = green;
    msg["color"]["b"] = blue;
 
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
        String payload_path = "miranda/mqtt/log";
        char attributes_path[100];
        payload_path.toCharArray( path, 100 );    

        // create msg as json
        DynamicJsonDocument msg(512);
        
        msg["ieeeAddr"]    = ieeeAddr;
        msg["model"]       = "client led_rgb";
        msg["device_type"] = "led_rgb";
        msg["description"] = "MQTT Client LED RGB";
    
        JsonArray data_inputs = msg.createNestedArray("inputs");
        data_inputs.add("");   

        JsonArray data_commands = msg.createNestedArray("commands");
        data_commands.add("");     

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
        default_mqtt_message();    
    }    


    // set 
    if (check_ieeeAddr == ieeeAddr and check_command == "set"){

        char msg[length+1];
  
        for (int i = 0; i < length; i++) {
            msg[i] = (char)payload[i];
        }
        msg[length] = '\0';
        
        Serial.print("msg: ");
        Serial.println(msg);

        // convert msg to json
        DynamicJsonDocument msg_json(128);
        deserializeJson(msg_json, msg);

        String temp_state = msg_json["state"];
        
        state      = temp_state;    
        brightness = msg_json["brightness"];
        red        = msg_json["color"]["r"];
        green      = msg_json["color"]["g"];
        blue       = msg_json["color"]["b"];

        state_changed = true;

        if (state == "ON"){   

            Serial.print("State: ");
            Serial.print(state); 
            Serial.print(" / Brightmess: ");
            Serial.print(brightness);            
            Serial.print(" / Red: ");
            Serial.print(red);            
            Serial.print(" / Green: ");
            Serial.print(green);            
            Serial.print(" / Blue: "); 
            Serial.println(blue);             

        } else {
                   
            brightness = 0;
            red        = 0;
            green      = 0;
            blue       = 0;

            Serial.print("State: ");
            Serial.print(state); 
            Serial.print(" / Brightmess: ");
            Serial.print(brightness);            
            Serial.print(" / Red: ");
            Serial.print(red);            
            Serial.print(" / Green: ");
            Serial.print(green);            
            Serial.print(" / Blue: "); 
            Serial.println(blue);       
         
        }       

        while (!client.connected()) {
            reconnect();
        }
        
        default_mqtt_message();                          
    }     
}

// #####
// setup
// #####

void setup() {

    Serial.begin(115200);
    Serial.println();
        
    pinMode(BUILTIN_LED, OUTPUT); 
    pinMode(TRANSISTOR_PIN, OUTPUT);     
    pinMode(PIN_RESET_SETTING,INPUT);

    digitalWrite(BUILTIN_LED, HIGH); 
    digitalWrite(TRANSISTOR_PIN, LOW);     

    Serial.println(digitalRead(PIN_RESET_SETTING));    

    if (digitalRead(PIN_RESET_SETTING) == 1) {
        wifi_manager(true);  // reset settings
    } else {
        wifi_manager(false);
    }
  
    Serial.println(mqtt_server);

    get_ieeeAddr();
    Serial.println(ieeeAddr);
    
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback); 

    FastLED.addLeds<WS2813, DATA_PIN, RGB>(leds, NUM_LEDS);
}


// ####
// loop
// ####

void loop() {

    if (!client.connected()) {
        reconnect();
    }

    if (state_changed == true){   

        if (brightness != 0){   
            digitalWrite(TRANSISTOR_PIN, LOW); 

            delay(250);
          
            FastLED.clear();
            fill_solid( leds, NUM_LEDS, CRGB(green, red, blue));
            FastLED.setBrightness(brightness);
            FastLED.show();

        } else {
            digitalWrite(TRANSISTOR_PIN, HIGH);  
        }
    }

    delay(100);
    client.loop();
}

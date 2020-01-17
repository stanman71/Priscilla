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

// OUTPUT
int CHANNEL_1 = 5;           // D1 
int CHANNEL_2 = 4;           // D2 
int CHANNEL_3 = 0;           // D3 
int CHANNEL_4 = 13;          // D7 

// RESET 
int PIN_RESET_SETTING = 16;  // D0

// LED
int PIN_LED_GREEN = 14;      // D5
int PIN_LED_RED   = 12;      // D6

String channel_1_state = "DISABLED";    // change to "OFF" to activate
String channel_2_state = "DISABLED";    // change to "OFF" to activate
String channel_3_state = "DISABLED";    // change to "OFF" to activate
String channel_4_state = "DISABLED";    // change to "OFF" to activate


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
        JsonArray data_commands = msg.createNestedArray("commands");
       
        if (channel_1_state != "DISABLED"){
            data_commands.add("Channal_1_ON");
            data_commands.add("Channal_1_OFF");       
        }
        if (channel_2_state != "DISABLED"){         
            data_commands.add("Channal_2_ON");
            data_commands.add("Channal_2_OFF");     
        }
        if (channel_3_state != "DISABLED"){            
            data_commands.add("Channal_3_ON");
            data_commands.add("Channal_3_OFF");     
        }
        if (channel_4_state != "DISABLED"){        
            data_commands.add("Channal_4_ON");
            data_commands.add("Channal_4_OFF");     
        }

        JsonArray data_commands_json = msg.createNestedArray("commands_json");

        if (channel_1_state != "DISABLED"){
            data_commands.add("{'channel_1:'ON'}");     
            data_commands.add("{'channel_1:'OFF'}");    
        }
        if (channel_2_state != "DISABLED"){    
            data_commands.add("{'channel_2:'ON'}");     
            data_commands.add("{'channel_2:'OFF'}");    
        }
        if (channel_3_state != "DISABLED"){    
            data_commands.add("{'channel_3:'ON'}");     
            data_commands.add("{'channel_3:'OFF'}");    
        }
        if (channel_4_state != "DISABLED"){                
            data_commands.add("{'channel_4:'ON'}");     
            data_commands.add("{'CHANNEL_4:'OFF'}");    
        }        

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
    
        // control channel 1

        if (channel_1_state != "DISABLED"){        
            String channel_1_setting = msg_json["channel_1"];

            if (channel_1_setting == "ON") {

                digitalWrite(CHANNEL_1, HIGH);
                channel_1_state = "ON";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_1_ON");
            }

            if (channel_1_setting == "OFF") {

                digitalWrite(CHANNEL_1, LOW);
                channel_1_state = "OFF";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_1_OFF");
            }
        }

        // control channel 2

        if (channel_2_state != "DISABLED"){        
            String channel_2_setting = msg_json["channel_2"];

            if (channel_2_setting == "ON") {

                digitalWrite(CHANNEL_2, HIGH);
                channel_2_state = "ON";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_2_ON");
            }

            if (channel_2_setting == "OFF") {

                digitalWrite(CHANNEL_2, LOW);
                channel_2_state = "OFF";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_1_OFF");
            }
        }

        // control channel 3

        if (channel_3_state != "DISABLED"){        
            String channel_3_setting = msg_json["channel_3"];

            if (channel_3_setting == "ON") {

                digitalWrite(CHANNEL_3, HIGH);
                channel_3_state = "ON";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_3_ON");
            }

            if (channel_3_setting == "OFF") {

                digitalWrite(CHANNEL_3, LOW);
                channel_3_state = "OFF";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_3_OFF");
            }
        }

        // control channel 4

        if (channel_4_state != "DISABLED"){        
            String channel_4_setting = msg_json["channel_4"];

            if (channel_4_setting == "ON") {

                digitalWrite(CHANNEL_4, HIGH);
                channel_4_state = "ON";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_4_ON");
            }

            if (channel_4_setting == "OFF") {

                digitalWrite(CHANNEL_4, LOW);
                channel_4_state = "OFF";

                send_default_mqtt_message(); 
                Serial.println("CHANNEL_4_OFF");
            }
        }
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
    DynamicJsonDocument msg(256);

    if (channel_1_state != "DISABLED"){      
        msg["channel_1"] = channel_1_state;
    }
    if (channel_2_state != "DISABLED"){          
        msg["channel_2"] = channel_2_state;
    }
    if (channel_3_state != "DISABLED"){          
        msg["channel_3"] = channel_3_state;
    }
    if (channel_4_state != "DISABLED"){        
        msg["channel_4"] = channel_4_state;
    }

    // convert msg to char
    char msg_Char[256];
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

    pinMode(CHANNEL_1, OUTPUT); 
    pinMode(CHANNEL_2, OUTPUT); 
    pinMode(CHANNEL_3, OUTPUT); 
    pinMode(CHANNEL_4, OUTPUT); 

    digitalWrite(CHANNEL_1, LOW);
    digitalWrite(CHANNEL_2, LOW);
    digitalWrite(CHANNEL_3, LOW);
    digitalWrite(CHANNEL_4, LOW);    

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
    
    delay(100);
    client.loop();
}

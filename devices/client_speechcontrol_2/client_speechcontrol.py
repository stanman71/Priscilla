from snipskit.hermes.apps import HermesSnipsApp
from snipskit.hermes.decorators import intent

import paho.mqtt.client as mqtt


def MQTT_PUBLISH(channel, msg):

    def on_publish(client, userdata, mid):
        print ('Message Published...')

    client = mqtt.Client()
    client.username_pw_set(username="miranda",password="qwer1234")
    client.on_publish = on_publish
    client.connect("192.168.1.111", 1883)
    client.publish(channel,msg)
    client.disconnect()



class SimpleSnipsApp(HermesSnipsApp):

    @intent('domi:currentTime')
    def example_intent(self, hermes, intent_message):
        print("OK")
        MQTT_PUBLISH("miranda/mqtt/test", '{"snowboy_pause":"test"}')


if __name__ == "__main__":
    print("START")
    SimpleSnipsApp()

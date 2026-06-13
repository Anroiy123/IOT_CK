#include <Arduino.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include "config.h"

enum class Mode { CAR, ARM };

struct State {
  Mode mode = Mode::CAR;
  uint32_t lastSeq = 0;
  unsigned long lastCommandMs = 0;
  const char* lastAction = "boot";
  int speed = 0;
  int selectedJoint = 0;
  int servoAngles[4] = {90, 90, 90, 60};
};

State state;
WebServer server(HTTP_PORT);
WebSocketsServer webSocket(WEBSOCKET_PORT);
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);
const char* jointNames[4] = {"base", "lower", "upper", "gripper"};
const int servoMinAngles[4] = {0, 20, 20, 15};
const int servoMaxAngles[4] = {180, 160, 160, 100};

void stopMotors() {
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  digitalWrite(PIN_IN3, LOW);
  digitalWrite(PIN_IN4, LOW);
  ledcWrite(PWM_LEFT_CHANNEL, 0);
  ledcWrite(PWM_RIGHT_CHANNEL, 0);
  state.speed = 0;
}

void setMotorGroup(int inA, int inB, bool forward) {
  digitalWrite(inA, forward ? HIGH : LOW);
  digitalWrite(inB, forward ? LOW : HIGH);
}

void drive(const char* action, int speed) {
  speed = constrain(speed, 0, 255);
  if (strcmp(action, "forward") == 0) {
    setMotorGroup(PIN_IN1, PIN_IN2, true);
    setMotorGroup(PIN_IN3, PIN_IN4, true);
  } else if (strcmp(action, "backward") == 0) {
    setMotorGroup(PIN_IN1, PIN_IN2, false);
    setMotorGroup(PIN_IN3, PIN_IN4, false);
  } else if (strcmp(action, "left") == 0) {
    setMotorGroup(PIN_IN1, PIN_IN2, false);
    setMotorGroup(PIN_IN3, PIN_IN4, true);
  } else if (strcmp(action, "right") == 0) {
    setMotorGroup(PIN_IN1, PIN_IN2, true);
    setMotorGroup(PIN_IN3, PIN_IN4, false);
  } else {
    stopMotors();
    return;
  }
  ledcWrite(PWM_LEFT_CHANNEL, speed);
  ledcWrite(PWM_RIGHT_CHANNEL, speed);
  state.speed = speed;
}

int pulseForAngle(int angle) {
  return map(constrain(angle, 0, 180), 0, 180, 102, 512);
}

void writeServo(int index) {
  pwm.setPWM(index, 0, pulseForAngle(state.servoAngles[index]));
}

int jointIndex(const char* joint) {
  for (int i = 0; i < 4; i++) {
    if (strcmp(joint, jointNames[i]) == 0) return i;
  }
  return state.selectedJoint;
}

bool applyCommand(JsonDocument& doc, String& error) {
  const char* token = doc["token"] | "";
  if (strcmp(token, COMMAND_TOKEN) != 0) {
    error = "bad_token";
    stopMotors();
    return false;
  }
  uint32_t seq = doc["seq"] | 0;
  if (seq <= state.lastSeq) {
    error = "stale_seq";
    return false;
  }
  int ttlMs = doc["ttl_ms"] | COMMAND_TIMEOUT_MS;
  if (ttlMs <= 0 || ttlMs > 5000) {
    error = "bad_ttl";
    stopMotors();
    return false;
  }

  const char* mode = doc["mode"] | "car";
  const char* action = doc["action"] | "stop";
  state.mode = strcmp(mode, "arm") == 0 ? Mode::ARM : Mode::CAR;
  state.lastSeq = seq;
  state.lastCommandMs = millis();
  state.lastAction = action;

  if (strcmp(action, "stop") == 0 || strcmp(action, "set_mode") == 0) {
    stopMotors();
    return true;
  }
  if (state.mode == Mode::CAR) {
    drive(action, doc["speed"] | 160);
    return true;
  }
  if (strcmp(action, "select_joint") == 0) {
    state.selectedJoint = jointIndex(doc["joint"] | jointNames[state.selectedJoint]);
    return true;
  }
  if (strcmp(action, "arm_delta") == 0) {
    int idx = jointIndex(doc["joint"] | jointNames[state.selectedJoint]);
    state.selectedJoint = idx;
    state.servoAngles[idx] = constrain(
      state.servoAngles[idx] + (doc["delta"] | 0),
      servoMinAngles[idx],
      servoMaxAngles[idx]
    );
    writeServo(idx);
    return true;
  }
  error = "unknown_action";
  stopMotors();
  return false;
}

String stateJson() {
  StaticJsonDocument<512> doc;
  doc["mode"] = state.mode == Mode::ARM ? "arm" : "car";
  doc["last_seq"] = state.lastSeq;
  doc["last_action"] = state.lastAction;
  doc["speed"] = state.speed;
  doc["selected_joint"] = jointNames[state.selectedJoint];
  JsonArray servos = doc["servos"].to<JsonArray>();
  for (int i = 0; i < 4; i++) servos.add(state.servoAngles[i]);
  String out;
  serializeJson(doc, out);
  return out;
}

void onWebSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type != WStype_TEXT) return;
  StaticJsonDocument<512> doc;
  StaticJsonDocument<256> response;
  DeserializationError jsonError = deserializeJson(doc, payload, length);
  if (jsonError) {
    response["ok"] = false;
    response["error"] = "bad_json";
  } else {
    String error;
    bool ok = applyCommand(doc, error);
    response["ok"] = ok;
    response["seq"] = state.lastSeq;
    if (!ok) response["error"] = error;
  }
  String out;
  serializeJson(response, out);
  webSocket.sendTXT(num, out);
}

void setupPins() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  ledcSetup(PWM_LEFT_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_RIGHT_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(PIN_ENA, PWM_LEFT_CHANNEL);
  ledcAttachPin(PIN_ENB, PWM_RIGHT_CHANNEL);
  stopMotors();
}

void setupWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  for (int i = 0; i < 30 && WiFi.status() != WL_CONNECTED; i++) delay(500);
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi failed; update firmware/include/config.h");
  }
}

void setup() {
  Serial.begin(115200);
  setupPins();
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  pwm.begin();
  pwm.setPWMFreq(50);
  for (int i = 0; i < 4; i++) writeServo(i);
  setupWiFi();
  server.on("/health", HTTP_GET, []() { server.send(200, "application/json", "{\"status\":\"ok\"}"); });
  server.on("/state", HTTP_GET, []() { server.send(200, "application/json", stateJson()); });
  server.begin();
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
  state.lastCommandMs = millis();
}

void loop() {
  server.handleClient();
  webSocket.loop();
  if (millis() - state.lastCommandMs > COMMAND_TIMEOUT_MS) stopMotors();
}

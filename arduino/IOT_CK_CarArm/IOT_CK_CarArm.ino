#include <Arduino.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include "config.h"

enum class Mode { CAR, ARM };

struct DeviceState {
  Mode mode = Mode::CAR;
  uint32_t lastSeq = 0;
  unsigned long lastCommandMs = 0;
  String lastAction = "boot";
  int speed = 0;
  int selectedJoint = 0;
  int servoAngles[4] = {90, 90, 90, 60};
};

DeviceState state;
WebServer httpServer(HTTP_PORT);
WebSocketsServer webSocket(WEBSOCKET_PORT);
Adafruit_PWMServoDriver servoDriver(0x40);

const char* JOINT_NAMES[4] = {"base", "lower", "upper", "gripper"};
const int SERVO_MIN_ANGLES[4] = {0, 20, 20, 15};
const int SERVO_MAX_ANGLES[4] = {180, 160, 160, 100};

void stopMotors() {
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  digitalWrite(PIN_IN3, LOW);
  digitalWrite(PIN_IN4, LOW);
  ledcWrite(PIN_ENA, 0);
  ledcWrite(PIN_ENB, 0);
  state.speed = 0;
}

void setMotorGroup(int inputA, int inputB, bool forward) {
  digitalWrite(inputA, forward ? HIGH : LOW);
  digitalWrite(inputB, forward ? LOW : HIGH);
}

void drive(const String& action, int speed) {
  speed = constrain(speed, 0, 255);

  if (action == "forward") {
    setMotorGroup(PIN_IN1, PIN_IN2, true);
    setMotorGroup(PIN_IN3, PIN_IN4, true);
  } else if (action == "backward") {
    setMotorGroup(PIN_IN1, PIN_IN2, false);
    setMotorGroup(PIN_IN3, PIN_IN4, false);
  } else if (action == "left") {
    setMotorGroup(PIN_IN1, PIN_IN2, false);
    setMotorGroup(PIN_IN3, PIN_IN4, true);
  } else if (action == "right") {
    setMotorGroup(PIN_IN1, PIN_IN2, true);
    setMotorGroup(PIN_IN3, PIN_IN4, false);
  } else {
    stopMotors();
    return;
  }

  ledcWrite(PIN_ENA, speed);
  ledcWrite(PIN_ENB, speed);
  state.speed = speed;
}

int pulseForAngle(int angle) {
  return map(constrain(angle, 0, 180), 0, 180, 102, 512);
}

void writeServo(int index) {
  servoDriver.setPWM(index, 0, pulseForAngle(state.servoAngles[index]));
}

int jointIndex(const String& joint) {
  for (int index = 0; index < 4; index++) {
    if (joint == JOINT_NAMES[index]) {
      return index;
    }
  }
  return state.selectedJoint;
}

bool applyCommand(JsonDocument& document, String& error) {
  const String token = document["token"] | "";
  if (token != COMMAND_TOKEN) {
    error = "bad_token";
    stopMotors();
    return false;
  }

  const uint32_t sequence = document["seq"] | 0;
  if (sequence <= state.lastSeq) {
    error = "stale_seq";
    return false;
  }

  const int ttlMs = document["ttl_ms"] | COMMAND_TIMEOUT_MS;
  if (ttlMs <= 0 || ttlMs > 5000) {
    error = "bad_ttl";
    stopMotors();
    return false;
  }

  const String mode = document["mode"] | "car";
  const String action = document["action"] | "stop";
  state.mode = mode == "arm" ? Mode::ARM : Mode::CAR;
  state.lastSeq = sequence;
  state.lastCommandMs = millis();
  state.lastAction = action;

  if (action == "stop" || action == "set_mode") {
    stopMotors();
    return true;
  }

  if (state.mode == Mode::CAR) {
    drive(action, document["speed"] | 160);
    return true;
  }

  if (action == "select_joint") {
    state.selectedJoint = jointIndex(document["joint"] | JOINT_NAMES[state.selectedJoint]);
    return true;
  }

  if (action == "arm_delta") {
    const int index = jointIndex(document["joint"] | JOINT_NAMES[state.selectedJoint]);
    const int delta = document["delta"] | 0;
    state.selectedJoint = index;
    state.servoAngles[index] = constrain(
      state.servoAngles[index] + delta,
      SERVO_MIN_ANGLES[index],
      SERVO_MAX_ANGLES[index]
    );
    writeServo(index);
    return true;
  }

  error = "unknown_action";
  stopMotors();
  return false;
}

String buildStateJson() {
  JsonDocument document;
  document["mode"] = state.mode == Mode::ARM ? "arm" : "car";
  document["last_seq"] = state.lastSeq;
  document["last_action"] = state.lastAction;
  document["speed"] = state.speed;
  document["selected_joint"] = JOINT_NAMES[state.selectedJoint];
  document["wifi_connected"] = WiFi.status() == WL_CONNECTED;
  document["ip"] = WiFi.localIP().toString();

  JsonArray servos = document["servos"].to<JsonArray>();
  for (int index = 0; index < 4; index++) {
    servos.add(state.servoAngles[index]);
  }

  String response;
  serializeJson(document, response);
  return response;
}

void onWebSocketEvent(uint8_t clientNumber, WStype_t type, uint8_t* payload, size_t length) {
  if (type != WStype_TEXT) {
    return;
  }

  JsonDocument command;
  JsonDocument response;
  DeserializationError jsonError = deserializeJson(command, payload, length);

  if (jsonError) {
    response["ok"] = false;
    response["error"] = "bad_json";
  } else {
    String commandError;
    const bool ok = applyCommand(command, commandError);
    response["ok"] = ok;
    response["seq"] = state.lastSeq;
    response["request_id"] = command["request_id"] | "";
    response["session_id"] = command["session_id"] | "";
    if (!ok) {
      response["error"] = commandError;
    }
  }

  String responseText;
  serializeJson(response, responseText);
  webSocket.sendTXT(clientNumber, responseText);
}

void setupPins() {
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);

  if (!ledcAttach(PIN_ENA, PWM_FREQ, PWM_RESOLUTION)) {
    Serial.println("ERROR: cannot attach ENA PWM");
  }
  if (!ledcAttach(PIN_ENB, PWM_FREQ, PWM_RESOLUTION)) {
    Serial.println("ERROR: cannot attach ENB PWM");
  }
  stopMotors();
}

void setupWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting WiFi");

  for (int attempt = 0; attempt < 30 && WiFi.status() != WL_CONNECTED; attempt++) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("WiFi connected. IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi failed. Check SSID/password and use a 2.4 GHz network.");
  }
}

void handleSerialTest() {
  if (!Serial.available()) {
    return;
  }

  const char input = tolower(Serial.read());
  state.lastCommandMs = millis();
  state.lastSeq++;

  switch (input) {
    case 'f':
      state.lastAction = "serial_forward";
      drive("forward", 160);
      break;
    case 'b':
      state.lastAction = "serial_backward";
      drive("backward", 160);
      break;
    case 'l':
      state.lastAction = "serial_left";
      drive("left", 160);
      break;
    case 'r':
      state.lastAction = "serial_right";
      drive("right", 160);
      break;
    case 's':
      state.lastAction = "serial_stop";
      stopMotors();
      break;
    case '0':
    case '1':
    case '2':
    case '3':
      state.selectedJoint = input - '0';
      Serial.printf("Selected joint: %s\n", JOINT_NAMES[state.selectedJoint]);
      break;
    case '+':
      state.servoAngles[state.selectedJoint] = constrain(
        state.servoAngles[state.selectedJoint] + 5,
        SERVO_MIN_ANGLES[state.selectedJoint],
        SERVO_MAX_ANGLES[state.selectedJoint]
      );
      writeServo(state.selectedJoint);
      break;
    case '-':
      state.servoAngles[state.selectedJoint] = constrain(
        state.servoAngles[state.selectedJoint] - 5,
        SERVO_MIN_ANGLES[state.selectedJoint],
        SERVO_MAX_ANGLES[state.selectedJoint]
      );
      writeServo(state.selectedJoint);
      break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("\nIOT_CK CarArm starting");

  setupPins();
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  servoDriver.begin();
  servoDriver.setPWMFreq(50);
  setupWiFi();

  httpServer.on("/health", HTTP_GET, []() {
    httpServer.send(200, "application/json", "{\"status\":\"ok\"}");
  });
  httpServer.on("/state", HTTP_GET, []() {
    httpServer.send(200, "application/json", buildStateJson());
  });
  httpServer.begin();

  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);

  state.lastCommandMs = millis();
  Serial.println("HTTP debug: port 80 (/health, /state)");
  Serial.println("WebSocket command: port 81");
  Serial.println("Serial test: f/b/l/r/s, joint 0-3, +/-");
}

void loop() {
  httpServer.handleClient();
  webSocket.loop();
  handleSerialTest();

  if (millis() - state.lastCommandMs > COMMAND_TIMEOUT_MS && state.speed > 0) {
    stopMotors();
    state.lastAction = "watchdog_stop";
  }
}

#include "pin.h"

void src_print(String content, uint8_t col, uint8_t row) {
  screen.setCursor(col, row);
  screen.print(content);
}
void lcd_begin() {
  src_print("PUT YOUR FINGER!", 0, 0);
  delay(500);
}
void pin_mode() {
  pinMode(btn_1, INPUT_PULLUP);
  pinMode(btn_2, INPUT_PULLUP);
  // digitalWrite(btn_1, 0);
  // digitalWrite(btn_2, 0);
  pinMode(relay, OUTPUT);
  pinMode(buzzer, OUTPUT);
  digitalWrite(relay, 1);
}

uint8_t getFingerID() {
  // Lấy ID vân tay
  while (finger.getImage() != FINGERPRINT_OK) finger.getImage();
  if (finger.image2Tz() == FINGERPRINT_OK)
    if (finger.fingerSearch() == FINGERPRINT_OK) return finger.fingerID;
  return -1;
}
bool add_finger() {
  //Hiển thị
  screen.clear();
  src_print("NEW FINGER,", 2, 0);
  src_print("PUT YOUR FINGER!", 0, 1);
  // Lấy ID hiện tại
  finger.getTemplateCount();
  uint8_t current_id = finger.templateCount + 2;

  // Chờ cho đến khi có ngón tay đặt vào
  while (finger.getImage() != FINGERPRINT_OK) finger.getImage();

  //Thêm vân tay
  if (finger.image2Tz(1) == FINGERPRINT_OK) {
    delay(2000);
    while (finger.getImage() != FINGERPRINT_NOFINGER) finger.getImage();
    while (finger.getImage() != FINGERPRINT_OK) finger.getImage();
    if (finger.image2Tz(2) == FINGERPRINT_OK)
      if (finger.createModel() == FINGERPRINT_OK)
        if (finger.storeModel(current_id) == FINGERPRINT_OK) {
          screen.clear();
          src_print("FINGER ADDED!", 2, 0);
          delay(2000);
          screen.clear();
          lcd_begin();
          return true;
        }
  }
  screen.clear();
  src_print("CAN'T ADD", 3, 0);
  src_print("YOUR FINGER", 2, 1);
  delay(3000);
  screen.clear();
  lcd_begin();
  return false;
}
bool delete_finger() {
  finger.getTemplateCount();
  if (finger.templateCount == 1) return true;
  //Hiển thị
  screen.clear();
  src_print("DELETE FINGER!", 1, 0);
  // Xóa vân tay theo ID
  uint8_t id_delete = getFingerID();
  if (id_delete != -1 && id_delete != 255)
    if (finger.deleteModel(id_delete) == FINGERPRINT_OK) {
      screen.clear();
      src_print("DELETED", 4, 0);
      delay(1000);
      lcd_begin();
      return true;
    }
  return false;
}

void setup() {
  // Cổng nối tiếp
  Serial.begin(9600);
  // Khởi động cảm biến vân tay
  finger.begin(57600);
  // Khởi động màn hình
  screen.init();
  screen.backlight();
  src_print("HELLO :))", 3, 0);
  delay(1000);

  // Cấu hình
  pin_mode();

  // Kiểm tra cảm biến có lỗi hay không?
  if (!finger.verifyPassword()) while (1) delay(1);
  // Nếu chưa có vân tay nào, thêm vân tay
  finger.getTemplateCount();
  if (finger.templateCount == 0) while(!add_finger()) {}
  else {
    // Hiển thị chữ
    lcd_begin();
  }
}
void loop() {
  if (!digitalRead(btn_1)) bool add = add_finger();
  if (!digitalRead(btn_2)) bool del = delete_finger();
  if (finger.getImage() == FINGERPRINT_OK) {
    uint8_t id = getFingerID();
    if (id != -1 && id != 255) {
      Serial.println(id);
      digitalWrite(relay, 0);
      screen.clear();
      src_print("WELCOME ID #", 1, 0);
      src_print(String(id), 12, 0);
      delay(1000);
      screen.clear();
      lcd_begin();
      digitalWrite(relay, 1);
    } else {
      src_print("INVALID FINGER!", 0, 0);
      delay(1000);
      lcd_begin();
    }
  }
  // Serial.println(digitalRead(btn_1));
  // Serial.println(digitalRead(btn_2));
}
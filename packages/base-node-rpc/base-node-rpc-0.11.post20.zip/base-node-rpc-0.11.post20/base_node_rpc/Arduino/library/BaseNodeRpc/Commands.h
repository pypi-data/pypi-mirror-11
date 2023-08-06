#ifndef ___BASE_NODE_RPC__COMMANDS___
#define ___BASE_NODE_RPC__COMMANDS___

#include "CArrayDefs.h"



namespace base_node_rpc {


struct BaseNodeSoftwareVersionRequest {
};

struct BaseNodeSoftwareVersionResponse {
  UInt8Array result;
};

struct NameRequest {
};

struct NameResponse {
  UInt8Array result;
};

struct ManufacturerRequest {
};

struct ManufacturerResponse {
  UInt8Array result;
};

struct SoftwareVersionRequest {
};

struct SoftwareVersionResponse {
  UInt8Array result;
};

struct UrlRequest {
};

struct UrlResponse {
  UInt8Array result;
};

struct MicrosecondsRequest {
};

struct MicrosecondsResponse {
  uint32_t result;
};

struct MillisecondsRequest {
};

struct MillisecondsResponse {
  uint32_t result;
};

struct DelayUsRequest {
  uint16_t us;
};

struct DelayUsResponse {
};

struct DelayMsRequest {
  uint16_t ms;
};

struct DelayMsResponse {
};

struct RamFreeRequest {
};

struct RamFreeResponse {
  uint32_t result;
};

struct PinModeRequest {
  uint8_t pin;
  uint8_t mode;
};

struct PinModeResponse {
};

struct DigitalReadRequest {
  uint8_t pin;
};

struct DigitalReadResponse {
  uint8_t result;
};

struct DigitalWriteRequest {
  uint8_t pin;
  uint8_t value;
};

struct DigitalWriteResponse {
};

struct AnalogReadRequest {
  uint8_t pin;
};

struct AnalogReadResponse {
  uint16_t result;
};

struct AnalogWriteRequest {
  uint8_t pin;
  uint8_t value;
};

struct AnalogWriteResponse {
};

struct ArrayLengthRequest {
  UInt8Array array;
};

struct ArrayLengthResponse {
  uint16_t result;
};

struct EchoArrayRequest {
  UInt32Array array;
};

struct EchoArrayResponse {
  UInt32Array result;
};

struct StrEchoRequest {
  UInt8Array msg;
};

struct StrEchoResponse {
  UInt8Array result;
};

struct MaxSerialPayloadSizeRequest {
};

struct MaxSerialPayloadSizeResponse {
  int32_t result;
};

struct UpdateEepromBlockRequest {
  uint16_t address;
  UInt8Array data;
};

struct UpdateEepromBlockResponse {
};

struct ReadEepromBlockRequest {
  uint16_t address;
  uint16_t n;
};

struct ReadEepromBlockResponse {
  UInt8Array result;
};

struct EepromE2endRequest {
};

struct EepromE2endResponse {
  uint32_t result;
};

struct SetI2cAddressRequest {
  uint8_t address;
};

struct SetI2cAddressResponse {
};

struct I2cAddressRequest {
};

struct I2cAddressResponse {
  uint8_t result;
};

struct I2cBufferSizeRequest {
};

struct I2cBufferSizeResponse {
  uint16_t result;
};

struct I2cScanRequest {
};

struct I2cScanResponse {
  UInt8Array result;
};

struct I2cAvailableRequest {
};

struct I2cAvailableResponse {
  int16_t result;
};

struct I2cReadByteRequest {
};

struct I2cReadByteResponse {
  int8_t result;
};

struct I2cRequestFromRequest {
  uint8_t address;
  uint8_t n_bytes_to_read;
};

struct I2cRequestFromResponse {
  int8_t result;
};

struct I2cReadRequest {
  uint8_t address;
  uint8_t n_bytes_to_read;
};

struct I2cReadResponse {
  UInt8Array result;
};

struct I2cWriteRequest {
  uint8_t address;
  UInt8Array data;
};

struct I2cWriteResponse {
};

struct I2cEnableBroadcastRequest {
};

struct I2cEnableBroadcastResponse {
};

struct I2cDisableBroadcastRequest {
};

struct I2cDisableBroadcastResponse {
};

struct MaxI2cPayloadSizeRequest {
};

struct MaxI2cPayloadSizeResponse {
  uint32_t result;
};

struct I2cRequestRequest {
  uint8_t address;
  UInt8Array data;
};

struct I2cRequestResponse {
  UInt8Array result;
};

struct I2cPacketResetRequest {
};

struct I2cPacketResetResponse {
};

struct GetBufferRequest {
};

struct GetBufferResponse {
  UInt8Array result;
};

struct BeginRequest {
};

struct BeginResponse {
};



static const int CMD_BASE_NODE_SOFTWARE_VERSION = 0x00;
static const int CMD_NAME = 0x01;
static const int CMD_MANUFACTURER = 0x02;
static const int CMD_SOFTWARE_VERSION = 0x03;
static const int CMD_URL = 0x04;
static const int CMD_MICROSECONDS = 0x05;
static const int CMD_MILLISECONDS = 0x06;
static const int CMD_DELAY_US = 0x07;
static const int CMD_DELAY_MS = 0x08;
static const int CMD_RAM_FREE = 0x09;
static const int CMD_PIN_MODE = 0x0a;
static const int CMD_DIGITAL_READ = 0x0b;
static const int CMD_DIGITAL_WRITE = 0x0c;
static const int CMD_ANALOG_READ = 0x0d;
static const int CMD_ANALOG_WRITE = 0x0e;
static const int CMD_ARRAY_LENGTH = 0x0f;
static const int CMD_ECHO_ARRAY = 0x10;
static const int CMD_STR_ECHO = 0x11;
static const int CMD_MAX_SERIAL_PAYLOAD_SIZE = 0x20;
static const int CMD_UPDATE_EEPROM_BLOCK = 0x40;
static const int CMD_READ_EEPROM_BLOCK = 0x41;
static const int CMD_EEPROM_E2END = 0x42;
static const int CMD_SET_I2C_ADDRESS = 0x60;
static const int CMD_I2C_ADDRESS = 0x61;
static const int CMD_I2C_BUFFER_SIZE = 0x62;
static const int CMD_I2C_SCAN = 0x63;
static const int CMD_I2C_AVAILABLE = 0x64;
static const int CMD_I2C_READ_BYTE = 0x65;
static const int CMD_I2C_REQUEST_FROM = 0x66;
static const int CMD_I2C_READ = 0x67;
static const int CMD_I2C_WRITE = 0x68;
static const int CMD_I2C_ENABLE_BROADCAST = 0x69;
static const int CMD_I2C_DISABLE_BROADCAST = 0x6a;
static const int CMD_MAX_I2C_PAYLOAD_SIZE = 0x80;
static const int CMD_I2C_REQUEST = 0x81;
static const int CMD_I2C_PACKET_RESET = 0x82;
static const int CMD_GET_BUFFER = 0xa0;
static const int CMD_BEGIN = 0xa1;

}  // namespace base_node_rpc



#endif  // ifndef ___BASE_NODE_RPC__COMMANDS___

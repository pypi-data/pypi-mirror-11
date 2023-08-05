#ifndef ___MOTOR_CONTROL___
#define ___MOTOR_CONTROL___

#include "Array.h"


#define BASE_NODE__NAME  ("motor_control")
#define BASE_NODE__MANUFACTURER  ("Wheeler Lab")
#define BASE_NODE__SOFTWARE_VERSION  ("0.2.post2")
#define BASE_NODE__URL  ("http://github.com/wheeler-microfluidics/motor-control.git")


namespace motor_control {


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

struct LoadConfigRequest {
};

struct LoadConfigResponse {
};

struct SaveConfigRequest {
};

struct SaveConfigResponse {
};

struct ResetConfigRequest {
};

struct ResetConfigResponse {
};

struct SerializeConfigRequest {
};

struct SerializeConfigResponse {
  UInt8Array result;
};

struct UpdateConfigRequest {
  UInt8Array serialized;
};

struct UpdateConfigResponse {
  uint8_t result;
};

struct OnConfigSerialNumberChangedRequest {
  uint32_t new_value;
};

struct OnConfigSerialNumberChangedResponse {
  bool result;
};

struct OnConfigBaudRateChangedRequest {
  uint32_t new_value;
};

struct OnConfigBaudRateChangedResponse {
  bool result;
};

struct OnConfigI2cAddressChangedRequest {
  uint32_t new_value;
};

struct OnConfigI2cAddressChangedResponse {
  bool result;
};

struct ResetStateRequest {
};

struct ResetStateResponse {
};

struct SerializeStateRequest {
};

struct SerializeStateResponse {
  UInt8Array result;
};

struct UpdateStateRequest {
  UInt8Array serialized;
};

struct UpdateStateResponse {
  uint8_t result;
};

struct SetMsRequest {
  uint8_t ms1;
  uint8_t ms2;
  uint8_t ms3;
};

struct SetMsResponse {
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

struct SetI2cAddressRequest {
  uint8_t value;
};

struct SetI2cAddressResponse {
};

struct TargetPositionRequest {
};

struct TargetPositionResponse {
  int32_t result;
};

struct SetTargetPositionRequest {
  int32_t absolute;
};

struct SetTargetPositionResponse {
};

struct OnTickRequest {
};

struct OnTickResponse {
};

struct TickCountRequest {
};

struct TickCountResponse {
  uint32_t result;
};

struct ResetTickCountRequest {
};

struct ResetTickCountResponse {
};

struct SetPeriodRequest {
  uint32_t period;
};

struct SetPeriodResponse {
};

struct EnableTimerRequest {
  uint32_t period;
};

struct EnableTimerResponse {
};

struct DisableTimerRequest {
};

struct DisableTimerResponse {
};

struct PositionRequest {
};

struct PositionResponse {
  int32_t result;
};

struct MoveRequest {
  int32_t relative;
};

struct MoveResponse {
};

struct PulseUsRequest {
};

struct PulseUsResponse {
  uint32_t result;
};

struct DelayUsRequest {
};

struct DelayUsResponse {
  uint32_t result;
};

struct MotorSetSpeedRequest {
  int32_t steps_per_second;
};

struct MotorSetSpeedResponse {
};

struct MotorStartRequest {
  int32_t steps_per_second;
};

struct MotorStartResponse {
};

struct MotorStopRequest {
};

struct MotorStopResponse {
};

struct MotorSetHomeRequest {
};

struct MotorSetHomeResponse {
};

struct OnStateMotorDelayUsChangedRequest {
  uint32_t new_value;
};

struct OnStateMotorDelayUsChangedResponse {
  bool result;
};

struct OnStateMotorContinuousChangedRequest {
  bool new_value;
};

struct OnStateMotorContinuousChangedResponse {
  bool result;
};

struct OnStateMotorEnabledChangedRequest {
  bool new_value;
};

struct OnStateMotorEnabledChangedResponse {
  bool result;
};

struct OnStateMotorDirectionChangedRequest {
  bool new_value;
};

struct OnStateMotorDirectionChangedResponse {
  bool result;
};


template <typename Obj>
class CommandProcessor {
  /* # `CommandProcessor` #
   *
   * Each call to this functor processes a single command.
   *
   * All arguments are passed by reference, such that they may be used to form
   * a response.  If the integer return value of the call is zero, the call is
   * assumed to have no response required.  Otherwise, the arguments contain
   * must contain response values. */
protected:
  Obj &obj_;
public:
  CommandProcessor(Obj &obj) : obj_(obj) {}


    static const int CMD_BASE_NODE_SOFTWARE_VERSION = 0x00;
    static const int CMD_NAME = 0x01;
    static const int CMD_MANUFACTURER = 0x02;
    static const int CMD_SOFTWARE_VERSION = 0x03;
    static const int CMD_URL = 0x04;
    static const int CMD_MICROSECONDS = 0x05;
    static const int CMD_MILLISECONDS = 0x06;
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
    static const int CMD_LOAD_CONFIG = 0xa0;
    static const int CMD_SAVE_CONFIG = 0xa1;
    static const int CMD_RESET_CONFIG = 0xa2;
    static const int CMD_SERIALIZE_CONFIG = 0xa3;
    static const int CMD_UPDATE_CONFIG = 0xa4;
    static const int CMD_ON_CONFIG_SERIAL_NUMBER_CHANGED = 0xa5;
    static const int CMD_ON_CONFIG_BAUD_RATE_CHANGED = 0xa6;
    static const int CMD_ON_CONFIG_I2C_ADDRESS_CHANGED = 0xa7;
    static const int CMD_RESET_STATE = 0xc0;
    static const int CMD_SERIALIZE_STATE = 0xc1;
    static const int CMD_UPDATE_STATE = 0xc2;
    static const int CMD_SET_MS = 0xe0;
    static const int CMD_GET_BUFFER = 0xe1;
    static const int CMD_BEGIN = 0xe2;
    static const int CMD_SET_I2C_ADDRESS = 0xe3;
    static const int CMD_TARGET_POSITION = 0xe4;
    static const int CMD_SET_TARGET_POSITION = 0xe5;
    static const int CMD_ON_TICK = 0xe6;
    static const int CMD_TICK_COUNT = 0xe7;
    static const int CMD_RESET_TICK_COUNT = 0xe8;
    static const int CMD_SET_PERIOD = 0xe9;
    static const int CMD_ENABLE_TIMER = 0xea;
    static const int CMD_DISABLE_TIMER = 0xeb;
    static const int CMD_POSITION = 0xec;
    static const int CMD_MOVE = 0xed;
    static const int CMD_PULSE_US = 0xee;
    static const int CMD_DELAY_US = 0xef;
    static const int CMD_MOTOR_SET_SPEED = 0xf0;
    static const int CMD_MOTOR_START = 0xf1;
    static const int CMD_MOTOR_STOP = 0xf2;
    static const int CMD_MOTOR_SET_HOME = 0xf3;
    static const int CMD_ON_STATE_MOTOR_DELAY_US_CHANGED = 0xf4;
    static const int CMD_ON_STATE_MOTOR_CONTINUOUS_CHANGED = 0xf5;
    static const int CMD_ON_STATE_MOTOR_ENABLED_CHANGED = 0xf6;
    static const int CMD_ON_STATE_MOTOR_DIRECTION_CHANGED = 0xf7;

  UInt8Array process_command(UInt8Array request_arr, UInt8Array buffer) {
    /* ## Call operator ##
     *
     * Arguments:
     *
     *  - `request_arr`: Serialized command request structure array,
     *  - `buffer`: Buffer array (available for writing output). */

    UInt8Array result;

    // Interpret first byte of request as command code.
    switch (request_arr.data[0]) {

        case CMD_BASE_NODE_SOFTWARE_VERSION:
          {
            /* Cast buffer as request. */
    
    
            BaseNodeSoftwareVersionResponse response;

            response.result =
            obj_.base_node_software_version();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_NAME:
          {
            /* Cast buffer as request. */
    
    
            NameResponse response;

            response.result =
            obj_.name();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_MANUFACTURER:
          {
            /* Cast buffer as request. */
    
    
            ManufacturerResponse response;

            response.result =
            obj_.manufacturer();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_SOFTWARE_VERSION:
          {
            /* Cast buffer as request. */
    
    
            SoftwareVersionResponse response;

            response.result =
            obj_.software_version();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_URL:
          {
            /* Cast buffer as request. */
    
    
            UrlResponse response;

            response.result =
            obj_.url();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_MICROSECONDS:
          {
            /* Cast buffer as request. */
    
    
            MicrosecondsResponse response;

            response.result =
            obj_.microseconds();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            MicrosecondsResponse &output = *(reinterpret_cast
                                                 <MicrosecondsResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_MILLISECONDS:
          {
            /* Cast buffer as request. */
    
    
            MillisecondsResponse response;

            response.result =
            obj_.milliseconds();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            MillisecondsResponse &output = *(reinterpret_cast
                                                 <MillisecondsResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_DELAY_MS:
          {
            /* Cast buffer as request. */
    
            DelayMsRequest &request = *(reinterpret_cast
                                          <DelayMsRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.delay_ms(request.ms);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_RAM_FREE:
          {
            /* Cast buffer as request. */
    
    
            RamFreeResponse response;

            response.result =
            obj_.ram_free();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            RamFreeResponse &output = *(reinterpret_cast
                                                 <RamFreeResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_PIN_MODE:
          {
            /* Cast buffer as request. */
    
            PinModeRequest &request = *(reinterpret_cast
                                          <PinModeRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.pin_mode(request.pin, request.mode);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_DIGITAL_READ:
          {
            /* Cast buffer as request. */
    
            DigitalReadRequest &request = *(reinterpret_cast
                                          <DigitalReadRequest *>
                                          (&request_arr.data[1]));
    
    
            DigitalReadResponse response;

            response.result =
            obj_.digital_read(request.pin);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            DigitalReadResponse &output = *(reinterpret_cast
                                                 <DigitalReadResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_DIGITAL_WRITE:
          {
            /* Cast buffer as request. */
    
            DigitalWriteRequest &request = *(reinterpret_cast
                                          <DigitalWriteRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.digital_write(request.pin, request.value);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_ANALOG_READ:
          {
            /* Cast buffer as request. */
    
            AnalogReadRequest &request = *(reinterpret_cast
                                          <AnalogReadRequest *>
                                          (&request_arr.data[1]));
    
    
            AnalogReadResponse response;

            response.result =
            obj_.analog_read(request.pin);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            AnalogReadResponse &output = *(reinterpret_cast
                                                 <AnalogReadResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ANALOG_WRITE:
          {
            /* Cast buffer as request. */
    
            AnalogWriteRequest &request = *(reinterpret_cast
                                          <AnalogWriteRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.analog_write(request.pin, request.value);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_ARRAY_LENGTH:
          {
            /* Cast buffer as request. */
    
            ArrayLengthRequest &request = *(reinterpret_cast
                                          <ArrayLengthRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.array.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.array.data);
            ArrayLengthResponse response;

            response.result =
            obj_.array_length(request.array);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            ArrayLengthResponse &output = *(reinterpret_cast
                                                 <ArrayLengthResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ECHO_ARRAY:
          {
            /* Cast buffer as request. */
    
            EchoArrayRequest &request = *(reinterpret_cast
                                          <EchoArrayRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.array.data = (uint32_t *)((uint8_t *)&request + (uint16_t)request.array.data);
            EchoArrayResponse response;

            response.result =
            obj_.echo_array(request.array);
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_STR_ECHO:
          {
            /* Cast buffer as request. */
    
            StrEchoRequest &request = *(reinterpret_cast
                                          <StrEchoRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.msg.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.msg.data);
            StrEchoResponse response;

            response.result =
            obj_.str_echo(request.msg);
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_MAX_SERIAL_PAYLOAD_SIZE:
          {
            /* Cast buffer as request. */
    
    
            MaxSerialPayloadSizeResponse response;

            response.result =
            obj_.max_serial_payload_size();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            MaxSerialPayloadSizeResponse &output = *(reinterpret_cast
                                                 <MaxSerialPayloadSizeResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_UPDATE_EEPROM_BLOCK:
          {
            /* Cast buffer as request. */
    
            UpdateEepromBlockRequest &request = *(reinterpret_cast
                                          <UpdateEepromBlockRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.data.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.data.data);
            obj_.update_eeprom_block(request.address, request.data);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_READ_EEPROM_BLOCK:
          {
            /* Cast buffer as request. */
    
            ReadEepromBlockRequest &request = *(reinterpret_cast
                                          <ReadEepromBlockRequest *>
                                          (&request_arr.data[1]));
    
    
            ReadEepromBlockResponse response;

            response.result =
            obj_.read_eeprom_block(request.address, request.n);
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_I2C_ADDRESS:
          {
            /* Cast buffer as request. */
    
    
            I2cAddressResponse response;

            response.result =
            obj_.i2c_address();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            I2cAddressResponse &output = *(reinterpret_cast
                                                 <I2cAddressResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_BUFFER_SIZE:
          {
            /* Cast buffer as request. */
    
    
            I2cBufferSizeResponse response;

            response.result =
            obj_.i2c_buffer_size();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            I2cBufferSizeResponse &output = *(reinterpret_cast
                                                 <I2cBufferSizeResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_SCAN:
          {
            /* Cast buffer as request. */
    
    
            I2cScanResponse response;

            response.result =
            obj_.i2c_scan();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_I2C_AVAILABLE:
          {
            /* Cast buffer as request. */
    
    
            I2cAvailableResponse response;

            response.result =
            obj_.i2c_available();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            I2cAvailableResponse &output = *(reinterpret_cast
                                                 <I2cAvailableResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_READ_BYTE:
          {
            /* Cast buffer as request. */
    
    
            I2cReadByteResponse response;

            response.result =
            obj_.i2c_read_byte();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            I2cReadByteResponse &output = *(reinterpret_cast
                                                 <I2cReadByteResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_REQUEST_FROM:
          {
            /* Cast buffer as request. */
    
            I2cRequestFromRequest &request = *(reinterpret_cast
                                          <I2cRequestFromRequest *>
                                          (&request_arr.data[1]));
    
    
            I2cRequestFromResponse response;

            response.result =
            obj_.i2c_request_from(request.address, request.n_bytes_to_read);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            I2cRequestFromResponse &output = *(reinterpret_cast
                                                 <I2cRequestFromResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_READ:
          {
            /* Cast buffer as request. */
    
            I2cReadRequest &request = *(reinterpret_cast
                                          <I2cReadRequest *>
                                          (&request_arr.data[1]));
    
    
            I2cReadResponse response;

            response.result =
            obj_.i2c_read(request.address, request.n_bytes_to_read);
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_I2C_WRITE:
          {
            /* Cast buffer as request. */
    
            I2cWriteRequest &request = *(reinterpret_cast
                                          <I2cWriteRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.data.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.data.data);
            obj_.i2c_write(request.address, request.data);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_I2C_ENABLE_BROADCAST:
          {
            /* Cast buffer as request. */
    
    
            obj_.i2c_enable_broadcast();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_I2C_DISABLE_BROADCAST:
          {
            /* Cast buffer as request. */
    
    
            obj_.i2c_disable_broadcast();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_MAX_I2C_PAYLOAD_SIZE:
          {
            /* Cast buffer as request. */
    
    
            MaxI2cPayloadSizeResponse response;

            response.result =
            obj_.max_i2c_payload_size();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            MaxI2cPayloadSizeResponse &output = *(reinterpret_cast
                                                 <MaxI2cPayloadSizeResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_I2C_REQUEST:
          {
            /* Cast buffer as request. */
    
            I2cRequestRequest &request = *(reinterpret_cast
                                          <I2cRequestRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.data.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.data.data);
            I2cRequestResponse response;

            response.result =
            obj_.i2c_request(request.address, request.data);
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_LOAD_CONFIG:
          {
            /* Cast buffer as request. */
    
    
            obj_.load_config();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_SAVE_CONFIG:
          {
            /* Cast buffer as request. */
    
    
            obj_.save_config();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_RESET_CONFIG:
          {
            /* Cast buffer as request. */
    
    
            obj_.reset_config();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_SERIALIZE_CONFIG:
          {
            /* Cast buffer as request. */
    
    
            SerializeConfigResponse response;

            response.result =
            obj_.serialize_config();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_UPDATE_CONFIG:
          {
            /* Cast buffer as request. */
    
            UpdateConfigRequest &request = *(reinterpret_cast
                                          <UpdateConfigRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.serialized.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.serialized.data);
            UpdateConfigResponse response;

            response.result =
            obj_.update_config(request.serialized);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            UpdateConfigResponse &output = *(reinterpret_cast
                                                 <UpdateConfigResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_CONFIG_SERIAL_NUMBER_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnConfigSerialNumberChangedRequest &request = *(reinterpret_cast
                                          <OnConfigSerialNumberChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnConfigSerialNumberChangedResponse response;

            response.result =
            obj_.on_config_serial_number_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnConfigSerialNumberChangedResponse &output = *(reinterpret_cast
                                                 <OnConfigSerialNumberChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_CONFIG_BAUD_RATE_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnConfigBaudRateChangedRequest &request = *(reinterpret_cast
                                          <OnConfigBaudRateChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnConfigBaudRateChangedResponse response;

            response.result =
            obj_.on_config_baud_rate_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnConfigBaudRateChangedResponse &output = *(reinterpret_cast
                                                 <OnConfigBaudRateChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_CONFIG_I2C_ADDRESS_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnConfigI2cAddressChangedRequest &request = *(reinterpret_cast
                                          <OnConfigI2cAddressChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnConfigI2cAddressChangedResponse response;

            response.result =
            obj_.on_config_i2c_address_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnConfigI2cAddressChangedResponse &output = *(reinterpret_cast
                                                 <OnConfigI2cAddressChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_RESET_STATE:
          {
            /* Cast buffer as request. */
    
    
            obj_.reset_state();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_SERIALIZE_STATE:
          {
            /* Cast buffer as request. */
    
    
            SerializeStateResponse response;

            response.result =
            obj_.serialize_state();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_UPDATE_STATE:
          {
            /* Cast buffer as request. */
    
            UpdateStateRequest &request = *(reinterpret_cast
                                          <UpdateStateRequest *>
                                          (&request_arr.data[1]));
    
    
            /* Add relative array data offsets to start payload structure. */
    
            request.serialized.data = (uint8_t *)((uint8_t *)&request + (uint16_t)request.serialized.data);
            UpdateStateResponse response;

            response.result =
            obj_.update_state(request.serialized);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            UpdateStateResponse &output = *(reinterpret_cast
                                                 <UpdateStateResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_SET_MS:
          {
            /* Cast buffer as request. */
    
            SetMsRequest &request = *(reinterpret_cast
                                          <SetMsRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.set_MS(request.ms1, request.ms2, request.ms3);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_GET_BUFFER:
          {
            /* Cast buffer as request. */
    
    
            GetBufferResponse response;

            response.result =
            obj_.get_buffer();
    
            /* Copy result to output buffer. */
            /* Result type is an array, so need to do `memcpy` for array data. */
            uint16_t length = (response.result.length *
                               sizeof(response.result.data[0]));

            result.data = (uint8_t *)response.result.data;
            result.length = length;
          }
          break;

        case CMD_BEGIN:
          {
            /* Cast buffer as request. */
    
    
            obj_.begin();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_SET_I2C_ADDRESS:
          {
            /* Cast buffer as request. */
    
            SetI2cAddressRequest &request = *(reinterpret_cast
                                          <SetI2cAddressRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.set_i2c_address(request.value);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_TARGET_POSITION:
          {
            /* Cast buffer as request. */
    
    
            TargetPositionResponse response;

            response.result =
            obj_.target_position();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            TargetPositionResponse &output = *(reinterpret_cast
                                                 <TargetPositionResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_SET_TARGET_POSITION:
          {
            /* Cast buffer as request. */
    
            SetTargetPositionRequest &request = *(reinterpret_cast
                                          <SetTargetPositionRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.set_target_position(request.absolute);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_ON_TICK:
          {
            /* Cast buffer as request. */
    
    
            obj_.on_tick();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_TICK_COUNT:
          {
            /* Cast buffer as request. */
    
    
            TickCountResponse response;

            response.result =
            obj_.tick_count();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            TickCountResponse &output = *(reinterpret_cast
                                                 <TickCountResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_RESET_TICK_COUNT:
          {
            /* Cast buffer as request. */
    
    
            obj_.reset_tick_count();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_SET_PERIOD:
          {
            /* Cast buffer as request. */
    
            SetPeriodRequest &request = *(reinterpret_cast
                                          <SetPeriodRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.set_period(request.period);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_ENABLE_TIMER:
          {
            /* Cast buffer as request. */
    
            EnableTimerRequest &request = *(reinterpret_cast
                                          <EnableTimerRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.enable_timer(request.period);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_DISABLE_TIMER:
          {
            /* Cast buffer as request. */
    
    
            obj_.disable_timer();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_POSITION:
          {
            /* Cast buffer as request. */
    
    
            PositionResponse response;

            response.result =
            obj_.position();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            PositionResponse &output = *(reinterpret_cast
                                                 <PositionResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_MOVE:
          {
            /* Cast buffer as request. */
    
            MoveRequest &request = *(reinterpret_cast
                                          <MoveRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.move(request.relative);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_PULSE_US:
          {
            /* Cast buffer as request. */
    
    
            PulseUsResponse response;

            response.result =
            obj_.pulse_us();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            PulseUsResponse &output = *(reinterpret_cast
                                                 <PulseUsResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_DELAY_US:
          {
            /* Cast buffer as request. */
    
    
            DelayUsResponse response;

            response.result =
            obj_.delay_us();
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            DelayUsResponse &output = *(reinterpret_cast
                                                 <DelayUsResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_MOTOR_SET_SPEED:
          {
            /* Cast buffer as request. */
    
            MotorSetSpeedRequest &request = *(reinterpret_cast
                                          <MotorSetSpeedRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.motor_set_speed(request.steps_per_second);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_MOTOR_START:
          {
            /* Cast buffer as request. */
    
            MotorStartRequest &request = *(reinterpret_cast
                                          <MotorStartRequest *>
                                          (&request_arr.data[1]));
    
    
            obj_.motor_start(request.steps_per_second);
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_MOTOR_STOP:
          {
            /* Cast buffer as request. */
    
    
            obj_.motor_stop();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_MOTOR_SET_HOME:
          {
            /* Cast buffer as request. */
    
    
            obj_.motor_set_home();
    
        result.data = buffer.data;
        result.length = 0;
          }
          break;

        case CMD_ON_STATE_MOTOR_DELAY_US_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnStateMotorDelayUsChangedRequest &request = *(reinterpret_cast
                                          <OnStateMotorDelayUsChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnStateMotorDelayUsChangedResponse response;

            response.result =
            obj_.on_state_motor_delay_us_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnStateMotorDelayUsChangedResponse &output = *(reinterpret_cast
                                                 <OnStateMotorDelayUsChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_STATE_MOTOR_CONTINUOUS_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnStateMotorContinuousChangedRequest &request = *(reinterpret_cast
                                          <OnStateMotorContinuousChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnStateMotorContinuousChangedResponse response;

            response.result =
            obj_.on_state_motor_continuous_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnStateMotorContinuousChangedResponse &output = *(reinterpret_cast
                                                 <OnStateMotorContinuousChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_STATE_MOTOR_ENABLED_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnStateMotorEnabledChangedRequest &request = *(reinterpret_cast
                                          <OnStateMotorEnabledChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnStateMotorEnabledChangedResponse response;

            response.result =
            obj_.on_state_motor_enabled_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnStateMotorEnabledChangedResponse &output = *(reinterpret_cast
                                                 <OnStateMotorEnabledChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

        case CMD_ON_STATE_MOTOR_DIRECTION_CHANGED:
          {
            /* Cast buffer as request. */
    
            OnStateMotorDirectionChangedRequest &request = *(reinterpret_cast
                                          <OnStateMotorDirectionChangedRequest *>
                                          (&request_arr.data[1]));
    
    
            OnStateMotorDirectionChangedResponse response;

            response.result =
            obj_.on_state_motor_direction_changed(request.new_value);
    
            /* Copy result to output buffer. */
            /* Cast start of buffer as reference of result type and assign result. */
            OnStateMotorDirectionChangedResponse &output = *(reinterpret_cast
                                                 <OnStateMotorDirectionChangedResponse *>
                                                 (&buffer.data[0]));
            output = response;
            result.data = buffer.data;
            result.length = sizeof(output);
          }
          break;

      default:
        result.length = 0xFFFF;
        result.data = NULL;
    }
    return result;
  }
};

}  // namespace motor_control



#endif  // ifndef ___MOTOR_CONTROL___

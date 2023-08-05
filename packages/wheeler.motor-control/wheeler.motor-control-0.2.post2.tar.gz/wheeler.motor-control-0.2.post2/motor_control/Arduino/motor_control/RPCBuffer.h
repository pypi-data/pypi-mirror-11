#ifndef ___RPC_BUFFER__H___
#define ___RPC_BUFFER__H___

#include <stdint.h>




#ifdef __AVR_ATmega328P__


/* ## uno settings ## */

#ifndef PACKET_SIZE
#define PACKET_SIZE  80
#endif  // #ifndef PACKET_SIZE

#ifndef I2C_PACKET_SIZE
#define I2C_PACKET_SIZE  PACKET_SIZE
#endif  // #ifndef I2C_PACKET_SIZE



#elif __AVR_ATmega2560__

/* ## mega2560 settings ## */

#ifndef PACKET_SIZE
#define PACKET_SIZE  256
#endif  // #ifndef PACKET_SIZE

#ifndef I2C_PACKET_SIZE
#define I2C_PACKET_SIZE  PACKET_SIZE
#endif  // #ifndef I2C_PACKET_SIZE



#else


/* ## default settings ## */

#ifndef PACKET_SIZE
#define PACKET_SIZE  80
#endif  // #ifndef PACKET_SIZE

#ifndef I2C_PACKET_SIZE
#define I2C_PACKET_SIZE  PACKET_SIZE
#endif  // #ifndef I2C_PACKET_SIZE



#endif


/* To save RAM, the serial-port interface may be disabled by defining
 * `DISABLE_SERIAL`. */
#ifndef DISABLE_SERIAL
extern uint8_t packet_buffer[PACKET_SIZE];
#endif  // #ifndef DISABLE_SERIAL

#endif  // #ifndef ___RPC_BUFFER__H___
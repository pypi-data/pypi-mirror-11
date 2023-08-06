
#line 1 "packet_socket_fsm_actions.rl"

#line 31 "packet_socket_fsm_actions.rl"


#include <stdio.h>
#include <string.h>
#include "PacketSocket.h"


#line 13 "packet_socket_fsm_actions.cpp"
static const int packet_socket_fsm_start = 10;
static const int packet_socket_fsm_first_final = 10;
static const int packet_socket_fsm_error = 0;

static const int packet_socket_fsm_en_main = 10;


#line 38 "packet_socket_fsm_actions.rl"

void PacketSocket::reset() {
  
#line 25 "packet_socket_fsm_actions.cpp"
	{
	cs = packet_socket_fsm_start;
	}

#line 41 "packet_socket_fsm_actions.rl"
}


void PacketSocket::parse_byte(uint8_t *byte) {
  uint8_t dummy_byte;

  if (byte == NULL) {
    /* If no byte is available _(i.e., `NULL` byte pointer was provided)_, set
     * Ragel parser pointers to trigger end-of-file actions. */
    p = &dummy_byte;
    pe = p;
    eof = p;
  } else {
    p = byte;
    pe = p + 1;
  }

  
#line 49 "packet_socket_fsm_actions.cpp"
	{
	if ( p == pe )
		goto _test_eof;
	switch ( cs )
	{
tr2:
#line 5 "packet_socket_fsm_actions.rl"
	{}
	goto st10;
st10:
	if ( ++p == pe )
		goto _test_eof10;
case 10:
#line 63 "packet_socket_fsm_actions.cpp"
	if ( (*p) == 105 )
		goto tr23;
	goto st0;
st0:
cs = 0;
	goto _out;
tr9:
#line 18 "packet_socket_fsm_actions.rl"
	{}
	goto st1;
tr10:
#line 19 "packet_socket_fsm_actions.rl"
	{}
	goto st1;
tr11:
#line 20 "packet_socket_fsm_actions.rl"
	{ queue_nack_queue_full(); }
	goto st1;
tr15:
#line 15 "packet_socket_fsm_actions.rl"
	{ pop_packet(); }
	goto st1;
tr18:
#line 27 "packet_socket_fsm_actions.rl"
	{ update_rx_queue(); }
	goto st1;
tr19:
#line 26 "packet_socket_fsm_actions.rl"
	{}
	goto st1;
tr20:
#line 23 "packet_socket_fsm_actions.rl"
	{ resend_packet(); }
	goto st1;
tr21:
#line 16 "packet_socket_fsm_actions.rl"
	{ queue_ack(); }
#line 7 "packet_socket_fsm_actions.rl"
	{}
	goto st1;
tr22:
#line 25 "packet_socket_fsm_actions.rl"
	{}
	goto st1;
tr23:
#line 12 "packet_socket_fsm_actions.rl"
	{ idle_state_ = cs; }
	goto st1;
st1:
	if ( ++p == pe )
		goto _test_eof1;
case 1:
#line 116 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 65: goto tr0;
		case 68: goto tr2;
		case 73: goto tr3;
		case 79: goto tr4;
	}
	goto st0;
tr0:
#line 21 "packet_socket_fsm_actions.rl"
	{ read_stream(); }
	goto st2;
st2:
	if ( ++p == pe )
		goto _test_eof2;
case 2:
#line 132 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 76: goto tr5;
		case 99: goto st1;
		case 101: goto tr7;
		case 114: goto tr8;
	}
	goto st0;
tr5:
#line 6 "packet_socket_fsm_actions.rl"
	{}
	goto st3;
tr7:
#line 14 "packet_socket_fsm_actions.rl"
	{}
	goto st3;
tr16:
#line 13 "packet_socket_fsm_actions.rl"
	{ handle_no_free_packets(); }
	goto st3;
tr17:
#line 17 "packet_socket_fsm_actions.rl"
	{ handle_queue_full(); }
	goto st3;
st3:
	if ( ++p == pe )
		goto _test_eof3;
case 3:
#line 160 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 76: goto tr9;
		case 101: goto tr10;
		case 102: goto tr11;
	}
	goto st0;
tr8:
#line 11 "packet_socket_fsm_actions.rl"
	{ handle_packet(); }
	goto st4;
st4:
	if ( ++p == pe )
		goto _test_eof4;
case 4:
#line 175 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 78: goto st1;
		case 97: goto tr12;
		case 100: goto tr13;
		case 110: goto tr14;
	}
	goto st0;
tr12:
#line 8 "packet_socket_fsm_actions.rl"
	{ handle_ack_packet(); }
	goto st5;
st5:
	if ( ++p == pe )
		goto _test_eof5;
case 5:
#line 191 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 78: goto st1;
		case 89: goto tr15;
	}
	goto st0;
tr13:
#line 9 "packet_socket_fsm_actions.rl"
	{ handle_data_packet(); }
	goto st6;
st6:
	if ( ++p == pe )
		goto _test_eof6;
case 6:
#line 205 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 70: goto tr16;
		case 102: goto tr17;
		case 114: goto tr18;
	}
	goto st0;
tr14:
#line 10 "packet_socket_fsm_actions.rl"
	{ handle_nack_packet(); }
	goto st7;
st7:
	if ( ++p == pe )
		goto _test_eof7;
case 7:
#line 220 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 76: goto tr19;
		case 78: goto st1;
	}
	if ( 101 <= (*p) && (*p) <= 102 )
		goto tr20;
	goto st0;
tr3:
#line 22 "packet_socket_fsm_actions.rl"
	{ process_rx_packet(); }
	goto st8;
st8:
	if ( ++p == pe )
		goto _test_eof8;
case 8:
#line 236 "packet_socket_fsm_actions.cpp"
	if ( (*p) == 113 )
		goto tr21;
	goto st0;
tr4:
#line 24 "packet_socket_fsm_actions.rl"
	{ process_tx_packet(); }
	goto st9;
st9:
	if ( ++p == pe )
		goto _test_eof9;
case 9:
#line 248 "packet_socket_fsm_actions.cpp"
	switch( (*p) ) {
		case 78: goto st1;
		case 115: goto tr22;
	}
	goto st0;
	}
	_test_eof10: cs = 10; goto _test_eof; 
	_test_eof1: cs = 1; goto _test_eof; 
	_test_eof2: cs = 2; goto _test_eof; 
	_test_eof3: cs = 3; goto _test_eof; 
	_test_eof4: cs = 4; goto _test_eof; 
	_test_eof5: cs = 5; goto _test_eof; 
	_test_eof6: cs = 6; goto _test_eof; 
	_test_eof7: cs = 7; goto _test_eof; 
	_test_eof8: cs = 8; goto _test_eof; 
	_test_eof9: cs = 9; goto _test_eof; 

	_test_eof: {}
	_out: {}
	}

#line 59 "packet_socket_fsm_actions.rl"
}

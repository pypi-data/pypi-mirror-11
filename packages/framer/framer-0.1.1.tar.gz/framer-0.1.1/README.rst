======================
Network Framer Library
======================

The TCP network protocol provides a bidirectional stream of data
between two network applications, but it turns out that most protocols
do not use the communication link as a stream.  In most network
protocols, the stream is chopped up into individual units.  The name
given to these units varies by protocol: some call it a *packet*; in
others, it's a *record*; and many protocols actually use plain text,
separating the units with carriage return/newline pairs.  Regardless
of the name, however, the vast majority of protocols impose some sort
of separation onto the stream of data and only deal in whole units.

The Framer library is a network communications library, built on top
of ``asyncio``, for managing these units, which it calls *frames*.
The Framer library is built as an ``asyncio`` protocol which also
happens to implement the behavior of an ``asyncio`` transport.  The
protocol object can have *framers* set on both directions of the
communication; these framers translate between the stream interface
provided by TCP and the sequence of frames desired by the application.

A *framer* is simply an object implementing a couple of methods which
implement the transformation from a stream to a frame and from a frame
to a sequence of bytes to transmit on the stream.  These framers can
range from rather trivial--as in a text-oriented protocol like
SMTP--all the way to a complex binary data transmission protocol such
as some forms of RPC.

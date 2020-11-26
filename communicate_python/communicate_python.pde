/**
 * oscP5sendreceive by andreas schlegel
 * example shows how to send and receive osc messages.
 * oscP5 website at http://www.sojamo.de/oscP5
 */

import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

int x = 0;
int y = 0;
int w = 10;
int h = 10;

void setup() {
  size(400, 400);
  frameRate(25);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 12000);

  /* myRemoteLocation is a NetAddress. a NetAddress takes 2 parameters,
   * an ip address and a port number. myRemoteLocation is used as parameter in
   * oscP5.send() when sending osc packets to another computer, device, 
   * application. usage see below. for testing purposes the listening port
   * and the port of the remote location address are the same, hence you will
   * send messages back to this sketch.
   */
  myRemoteLocation = new NetAddress("127.0.0.1", 12001);
}


void draw() {
  background(0);
  rect(x, y, w, h);
}

void mousePressed() {
  String address = "/test";
  String message= "123";
  sendMessage(address, message);
}

void sendMessage(String address, String message) {
  /* in the following different ways of creating osc messages are shown by example */
  OscMessage myMessage = new OscMessage(address);

  myMessage.add(message); /* add an int to the osc message */

  /* send the message */
  oscP5.send(myMessage, myRemoteLocation);
}


/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.");
  print(" addrpattern: "+theOscMessage.addrPattern());
  println(" typetag: "+theOscMessage.typetag()); 
  if (theOscMessage.checkTypetag("f")) {
    float OSCvalue = theOscMessage.get(0).floatValue();
    println(" message: "+ OSCvalue);
  }
  if (theOscMessage.checkTypetag("i")) {
    int OSCvalue = theOscMessage.get(0).intValue();
  }

  if (theOscMessage.checkAddrPattern("x")) {
    println("x");
    int OSCvalue = theOscMessage.get(0).intValue();
    x = OSCvalue;
  }

  if (theOscMessage.checkAddrPattern("y")) {
    int OSCvalue = theOscMessage.get(0).intValue();
    y = OSCvalue;
  }


  if (theOscMessage.checkAddrPattern("w")) {
    int OSCvalue = theOscMessage.get(0).intValue();
    w = OSCvalue;
  }

  if (theOscMessage.checkAddrPattern("h")) {
    int OSCvalue = theOscMessage.get(0).intValue();
    h = OSCvalue;
  }
}

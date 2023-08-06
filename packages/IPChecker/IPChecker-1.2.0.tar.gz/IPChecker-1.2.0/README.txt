##################################
 __Program__: IPChecker
 __version__: 1.2.0
 __Author__ : Boumediene Kaddour
 __Country__: Algeria
##################################

IPChecker is a tiny Python library that is used to check if an IP version address is Private, Public or Invalid,
The library returns Booleans and contains a couple of methods summurized as follows:

  isValid(): This method returns True, if a valid IPv4's given, otherwise, it returns False.
  isPrivate(): This little method returns True if the given IP 
is private, otherwise, False is returned.
  isMCast(): This little method returns True, if a Valid IPv4 is given and it's among the multicast ip range, otherwise, it returns a False. 
  isPublic(): This little method returns True if the given IP is a Valid IPv4, not private and not multicast address, otherwise, False is returned.

Usage:
 >>> from IPChecker import IPChecker
 >>> obj = IPChecker("172.16.122.254")
 >>> obj.isValid()
 >>> True
 >>> obj.isPrivate()
 >>> True
 >>> obj.isPublic()
 >>> False
 
 Here is a sample grabbed from the IPchecker source code given as an example of how you can checkout for a valid IPv4 address using regular expressions.

 in this example, the built-in python re module is used.
 
 >>> def isValid(self):
 >>> ____if findall( "(?i)^(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5]).(\d|\d\d|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$" ,self.IP):
 >>> ________ return True
 >>> ____else:
 >>> ________ return False
 
 
 
 
 

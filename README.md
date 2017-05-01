# red-rover-ui
Simple web-based ui for the YURT cargo rover

This is a web-based interface for the Red Rover. Before installing on a new OBC, you should prepare the server environment:

Install the server software from a repository:
sudo apt-get install lighttpd --> this is the server software
sudo apt-get install python-flup --> this utility parses http requests for us

Create new user and group:

sudo groupadd lighttpd
sudo useradd -g lighttpd -d /var/www/html -s /sbin/nologin lighttpd --> this user will run the server for security purposes

Edit permissions for the following files:

sudo chown -R lighttpd:lighttpd /var/log/lighttpd
sudo chown -R lighttpd:lighttpd /var/run/lighttpd.pid
sudo chown -R lighttpd:lighttpd /var/www/html

Edit the config files:
sudo nano /etc/lighttpd/lighttpd.conf
  Add "mod_cgi" and "mod_fastcgi" to the list of mods
  Change server and groupname to lighttpd
  Change the port to 8080
  Append the following lines:
fastcgi.server = (
   ".py" => (
     "python-fcgi" => (
       "socket" => "/tmp/fastcgi.python.socket",
       "bin-path" => "/var/www/html/test.py",
       "check-local" => "disable",
       "max-procs" => 1)
    )
 )
 
Start the server:
/etc/init.d/lighttpd start

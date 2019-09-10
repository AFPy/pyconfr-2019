# PyConFr 2019

You've seen a mistake? Please go to the `templates` folder above an fix it ;).

---

To serve the dynamic website on localhost:

    make serve

To build and deploy the static website in production:

    make deploy

with something like this in your `~/.ssh/config`:

    Host rainette
      HostName rainette.afpy.org
      Port 2222
      User changeme

    Host pyconfr
      ProxyJump rainette
      HostName 192.168.42.110
      Port 4242
      User pyconfr

That's all you need! Other rules are available in `Makefile`, mostly for debugging purpose.

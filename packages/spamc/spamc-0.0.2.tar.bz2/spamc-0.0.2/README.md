# spamc


## Python spamassassin spamc client library

spamc is a python module that provides all the client side functionality of the
[spamassassin](https://spamassassin.apache.org)
[spamd protocol](https://github.com/apache/spamassassin/blob/trunk/spamd/PROTOCOL)

It is built using [restkit](http://restkit.readthedocs.org) so can be used
with [gevent](http://www.gevent.org) and [eventlet](http://www.eventlet.net),
is thread safe, reuses connections and supports streaming.


## Installation

Install from PyPi

    pip install spamc

Install from Githib

    git clone https://github.com/akissa/spamc.git
    cd spamc
    python setup.py install

## Usage

Examples are in the examples directory

## Contributing

1. Fork it (https://github.com/akissa/spamc/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request


## License

All code is licensed under the
[AGPLv3+ License](https://github.com/akissa/spamc/blob/master/LICENSE).

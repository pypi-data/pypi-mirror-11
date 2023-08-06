rpcviaredis
==========
*Using redis server to build RPC environment - by Oscar LASM*

----------
rpcviaredis intended to provide a simple tool for establishing a pattern RPC over an installation Redis.
Implement python, it is composed of:

 - **Server** which serve remote commands
 - **Client** Use to connect and call commands hosted on server
 - **Transport protocol** Use to pack and unpack request and response during communication process

**Examples**:

Server implementation:

    from rpcviaredis import *

	class DummyServer(ServerRPC):

		def sum(self, x, y):
	        return Response(response=x+y, exception=None, reason=None, return_code=200)

	    def naive_div(self, x, y):
	        return Response(response=x/y, exception=None, reason=None, return_code=200)

	    def multiplication(self, x, y):
	        return Response(response=x*y, exception=None, reason=None, return_code=200)

	if __name__ == "__main__":
	    import redis

	    r = redis.StrictRedis(db=2)
	    s = DummyServer(r, 'test-rpc', transport_klass=JSONTransport)
	    try:
	        s.start()
	    except KeyboardInterrupt:
	        pass
	    finally:
	        s.stop()

Client Implementation

    import redis
    from rpcviaredis import Client

    r = redis.StrictRedis(db=2)
    c = Client(r, 'test-rpc', transport_klass=JsonTransport)
    retval = c.sum(1,2)
    print(retval.response) # print 3

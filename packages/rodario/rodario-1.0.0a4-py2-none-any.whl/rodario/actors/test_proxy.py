""" ActorProxy unit tests for rodario framework """

# stdlib
import unittest
import multiprocessing.queues

# local
from rodario.actors import Actor, ActorProxy

# pylint: disable=I0011,R0201


class TestActor(Actor):

    """ Stubbed Actor class for testing """

    def test(self):
        """ Simple method call. """

        return 1


# pylint: disable=I0011,C0103,R0904
class ProxyTests(unittest.TestCase):

    """ ActorProxy unit tests """

    @classmethod
    def setUpClass(cls):
        """ Create an Actor and an ActorProxy for it. """

        cls.actor = TestActor(uuid='noexist_proxy')
        cls.actor.start()
        cls.proxy = cls.actor.proxy()

    @classmethod
    def tearDownClass(cls):
        """ Kill the Actor. """

        cls.actor.stop()

    def testNoParametersInConstructor(self):
        """ Raise Exception when no constructor parameters are passed. """

        self.assertRaises(Exception, ActorProxy)

    def testUUIDConstructor(self):
        """ Create a proxy for a given UUID. """

        proxy = ActorProxy(uuid='noexist_proxy')
        self.assertEqual('noexist_proxy', proxy.uuid)

    def testMethodExists(self):
        """ Ensure that the 'test' method of MyActor has been proxied. """

        self.assertTrue(getattr(self.proxy, 'test') is not None)

    def testActorUUID(self):
        """ Validate the UUID of the underlying Actor. """

        self.assertEqual('noexist_proxy', self.proxy.uuid)

    def testProxyResponseIsQueue(self):
        """ Validate that the object returned from a proxy call is a Queue. """

        response = self.proxy.test()  # pylint: disable=I0011,E1101
        self.assertTrue(isinstance(response, multiprocessing.queues.Queue))
        response.get(timeout=1)

    def testProxyCallAndResponse(self):
        """ Validate the return value of MyActor.test. """

        # pylint: disable=I0011,E1101
        response = self.proxy.test().get(timeout=1)
        self.assertEqual(1, response)

    def testInvalidProxy(self):
        """ Raise Exception when proxying to an invalid actor. """

        newactor = Actor()
        falseproxy = newactor.proxy()
        del newactor
        # pylint: disable=I0011,W0212
        self.assertRaises(Exception, falseproxy._proxy, None)

if __name__ == '__main__':
    unittest.main()

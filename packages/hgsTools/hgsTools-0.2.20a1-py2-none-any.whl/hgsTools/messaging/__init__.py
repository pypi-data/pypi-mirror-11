'''
Created on May 25, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty
from hgsTools import auxiliary

supported_apps = ['grok_hgs', 'enkf']

mgs_types_dic = {
                         'create': 'create_app',
                         'delete': 'delete_app',
                         'retrieve': 'retrieve_cli_output',
                         'output': 'update_output',
                         'accepted': 'app_accepted',
                         'info': 'update_info',
                         'status': 'update_app_status',
                         'spawning': 'update_vm_spawning_time',
                         'preprocessing': 'preprocessing',
                         'preprocessed': 'preprocessed',
}

kwargs_dic = {
                         'create_app': ['tmp_id', 'app_type', 'input', 'output'],
                         'delete_app': ['app_id'],
                         'retrieve_cli_output': ['app_id'],
                         'update_output': ['app_id', 'output'],
                         'app_accepted': ['tmp_id', 'app_id'],
                         'update_info': ['app_id', 'info_type', 'info'],
                         'update_app_status': ['app_id', 'status'],
                         'update_vm_spawning_time': ['app_id', 'time'],
                         'preprocessing': ['input'],
                         'preprocessed': ['input'],
}

#TODO: add warnings about extra parameters

def createMessage(m_type, return_queue='', interface='eth0', **kwargs):
    if m_type in mgs_types_dic:
        msg_type = mgs_types_dic[m_type]
    else:
        print "Unexpected type: %s. List of available types: %s" % (m_type, mgs_types_dic.keys())
        raise BaseException
    
    if msg_type not in mgs_types_dic.values() or msg_type not in kwargs_dic:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = kwargs_dic[msg_type]
    
    for element in args:
        if element not in kwargs.keys():
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    return_address = auxiliary.getIPAdreess(interface)
    
    message = {
               'msg_type': msg_type,
               'return_params': {
                                 'return_address': return_address, 
                                 'return_queue': return_queue
                                 },
               'kwargs': kwargs,
    }
    
    return message

def messageCheck(message):
    msg_type = message['msg_type']
    kwargs = message['kwargs']
    
    if msg_type not in mgs_types_dic.values() or msg_type not in kwargs_dic:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = kwargs_dic[msg_type]
    
    for element in args:
        if element not in kwargs:
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    return True

class MessageConsumer(object):
    def __init__(self, connectionLink, queueName, callback, logger=None):
        self.queueName = queueName
        self.connectionLink = connectionLink
        self.callback = callback
        self.logger = logger
        
    def consumeOneMsg(self):
        ret = True
        
        with Connection(self.connectionLink) as conn:
            with conn.SimpleQueue(self.queueName) as queue:
                try:
                    message = queue.get_nowait()
                    self.logger.info('Message received')
                    self.callback(message, self.logger)
                    message.ack()
                except Empty:
                    ret = False
                    
        return ret
    
    def constantConsuming(self):
        self.logger.info('Starting constant consuming')
        
        while True:
            if not self.consumeOneMsg():
                time.sleep(1)


#TODO: add logging information
class MessageProducer(object):
    def __init__(self, connectionLink, queueName, logger=None):
        self.queueName = queueName
        self.connectionLink = connectionLink
        self.logger = logger
        
    def publish(self, message):
        with Connection(self.connectionLink) as conn:
            with conn.SimpleQueue(self.queueName) as queue:
                queue.put(message)
                
                
def constantConsumerWrapper(config_file_path, queue, log_file, log_lvl, callback):
    import ConfigParser
    from hgsTools.auxiliary import read_option, buildRabbitMQConnectionLink, getIPAdreess, initLogger, readConfig
    import logging
    
    config = readConfig(config_file_path)
    #reading the global config file
    #path = config_file_path
    #config = ConfigParser.RawConfigParser()
    #config.read(path)
    
    QUEUE = read_option(config, 'general', queue)
    
    protocol = read_option(config, 'rabbit_mq', 'protocol')
    user = read_option(config, 'rabbit_mq', 'user')
    password = read_option(config, 'rabbit_mq', 'password')
    address = getIPAdreess()
    port = read_option(config, 'rabbit_mq', 'port')
    CONNECTION_LINK = buildRabbitMQConnectionLink(address, protocol=protocol, user=user, password=password, port=port)
    
    logger = initLogger(log_file, log_lvl)
    logger.info('Connection link: ' + CONNECTION_LINK)
    
    consumer = MessageConsumer(CONNECTION_LINK, QUEUE, callback, logger)
    consumer.constantConsuming()

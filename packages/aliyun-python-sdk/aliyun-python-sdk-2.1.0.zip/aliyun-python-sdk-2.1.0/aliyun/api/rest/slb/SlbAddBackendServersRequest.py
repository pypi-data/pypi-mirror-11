'''
Created by auto_sdk on 2015.06.23
'''
from aliyun.api.base import RestApi
class SlbAddBackendServersRequest(RestApi):
	def __init__(self,domain='slb.aliyuncs.com',port=80):
		RestApi.__init__(self,domain, port)
		self.backendServers = None
		self.loadBalancerId = None

	def getapiname(self):
		return 'slb.aliyuncs.com.AddBackendServers.2013-02-21'

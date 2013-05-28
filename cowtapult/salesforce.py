from simple_salesforce import Salesforce
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('salesforce.cfg')

username = config.get('salesforce','username')
password = config.get('salesforce','password')
security_token = config.get('salesforce','security_token')
sandbox = config.get('salesforce','sandbox')

sf = Salesforce(
    username=username,
    password=password,
    security_token=security_token,
    sandbox=sandbox
)

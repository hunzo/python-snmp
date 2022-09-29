from fastapi import FastAPI
from pysnmp import hlapi
from snmp import SNMP
app = FastAPI()

snmp = SNMP()

@app.get("/")
def main():

    # communityV3 = hlapi.UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey',
    #                            authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)

    communityV2 = hlapi.CommunityData('YOUR_COMUNITY_STRING')

    # server_list = [
    #     "10.10.31.188",
    #     "10.100.100.30"
    # ]

    # for srv in server_list:
    #     print(snmp.get(
    #         srv,
    #         # ['1.3.6.1.2.1.1.5.0'],
    #         [
    #             '.1.3.6.1.4.1.2021.9.1.2.1',
    #         ],
    #         communityV2,
    #     ))

    # Get Bulk
    its = snmp.get_bulk_auto(
        '10.10.39.161',
        ['1.3.6.1.2.1.2.2.1.2 ', '1.3.6.1.2.1.31.1.1.1.18'],
        communityV2,
        '1.3.6.1.2.1.2.1.0'
    )

    for it in its:
        for k, v in it.items():
            print("{0}={1}".format(k, v))
        print('')

    return {
        "success": True,
        "its": its
    }
